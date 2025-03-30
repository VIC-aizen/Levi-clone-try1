from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Payments, db, Admin, Products, Orders, Users, Suppliers
from hashpass import verify_password

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        admin = Admin.query.filter_by(email=email).first()  # Find admin by email

        if admin and verify_password(admin.password, password):
            session["admin_id"] = admin.admin_id  # Store admin ID in session
            flash("Login successful!", "success")
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("❌ Invalid email or password", "danger")  # Show error message

    return render_template("admin_login.html")

# Removed duplicate admin_dashboard route to avoid conflict

@admin_bp.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    flash("✅ Logged out successfully", "success")
    return redirect(url_for("admin.admin_login"))


# Admin Dashboard
@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        flash("⚠️ Please log in as admin first", "warning")
        return redirect(url_for("admin.admin_login"))

    total_products = Products.query.count()
    total_orders = Orders.query.count()
    total_users = Users.query.count()

    return render_template("admin_dashboard.html", total_products=total_products, total_orders=total_orders, total_users=total_users)

# View All Products
@admin_bp.route("/admin/products")
def view_products():
    if "admin_id" not in session:
        flash("⚠️ Please log in as admin first", "warning")
        return redirect(url_for("admin.admin_login"))

    products = Products.query.all()
    return render_template("admin_products.html", products=products)

# View Orders (Fetching Order Status from Orders & Payment Status from Payments)
@admin_bp.route("/admin/orders")
def view_orders():
    if "admin_id" not in session:
        flash("⚠️ Please log in as admin first", "warning")
        return redirect(url_for("admin.admin_login"))

    # Fetch orders and payment status from payments table
    orders = db.session.query(
        Orders.order_id,
        Orders.user_id,
        Orders.status.label("order_status"),  # ✅ Fetching from Orders table
        db.case(
            (Payments.status == "Success", "Success"),  # ✅ Passed as a positional element
            else_="Not Paid"
        ).label("payment_status")  # ✅ Fetching from Payments table
    ).outerjoin(Payments, Orders.order_id == Payments.order_id).all()

    return render_template("admin_orders.html", orders=orders)


# View Users
@admin_bp.route("/admin/users")
def view_users():
    if "admin_id" not in session:
        flash("⚠️ Please log in as admin first", "warning")
        return redirect(url_for("admin.admin_login"))

    users = Users.query.all()
    return render_template("admin_users.html", users=users)

# 🟢 Add Product
@admin_bp.route("/admin/products/add", methods=["GET", "POST"])
def add_product():
    if "admin_id" not in session:
        flash("⚠️ Please log in as admin first", "warning")
        return redirect(url_for("admin.admin_login"))

    suppliers = Suppliers.query.all()  # Get all suppliers

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]
        supplier_id = request.form["supplier_id"]

        new_product = Products(name=name, price=price, stock=stock, supplier_id=supplier_id)
        db.session.add(new_product)
        db.session.commit()
        flash("✅ Product added successfully!", "success")
        return redirect(url_for("admin.view_products"))

    return render_template("admin_add_product.html", suppliers=suppliers)

# 🟢 Edit Product
@admin_bp.route("/admin/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if "admin_id" not in session:
        flash("⚠️ Please log in as admin first", "warning")
        return redirect(url_for("admin.admin_login"))

    product = Products.query.get_or_404(product_id)
    suppliers = Suppliers.query.all()  # Get all suppliers

    if request.method == "POST":
        product.name = request.form["name"]
        product.price = request.form["price"]
        product.stock = request.form["stock"]
        product.supplier_id = request.form["supplier_id"]
        db.session.commit()
        flash("✅ Product updated successfully!", "success")
        return redirect(url_for("admin.view_products"))

    return render_template("admin_edit_product.html", product=product, suppliers=suppliers)
# 🟢 Delete Product
@admin_bp.route("/admin/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    if "admin_id" not in session:
        flash("⚠️ Please log in as admin first", "warning")
        return redirect(url_for("admin.admin_login"))

    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("❌ Product deleted successfully!", "danger")
    return redirect(url_for("admin.view_products"))
