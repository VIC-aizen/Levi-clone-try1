from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from models import db, Cart, Products, Orders, OrderItems

cart_bp = Blueprint("cart", __name__)

# 🟢 View Cart
@cart_bp.route("/cart")
def view_cart():
    user_id = session.get('user_id')
    if not user_id:
        return "Please log in to view your cart.", 403

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    products_in_cart = [
    {
        'cart_id': cart_item.cart_id,
        'product_name': product.name,  # Ensure this key is correct
        'product_price': product.price,
        'quantity': cart_item.quantity
    }
    for cart_item in cart_items
    for product in Products.query.filter_by(product_id=cart_item.product_id)
]
    return render_template('cart.html', cart_items=products_in_cart)

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    user_id = session.get('user_id')
    if not user_id:
        return "Please log in to add items to the cart.", 403

    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))

    # Check if product is already in the cart
    existing_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)

    db.session.commit()
    return redirect(url_for('cart.view_cart'))

# 🟢 Update Cart Quantity
@cart_bp.route("/cart/update/<int:cart_id>", methods=["POST"])
def update_cart(cart_id):
    if "user_id" not in session:
        flash("⚠️ Please log in first", "warning")
        return redirect(url_for("auth.login"))

    new_quantity = int(request.form["quantity"])
    cart_item = Cart.query.get_or_404(cart_id)
    cart_item.quantity = new_quantity
    db.session.commit()
    flash("✅ Cart updated!", "success")
    return redirect(url_for("cart.view_cart"))

# 🟢 Remove from Cart
@cart_bp.route("/cart/remove/<int:cart_id>", methods=["POST"])
def remove_from_cart(cart_id):
    if "user_id" not in session:
        flash("⚠️ Please log in first", "warning")
        return redirect(url_for("auth.login"))

    cart_item = Cart.query.get_or_404(cart_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash("🗑️ Item removed from cart!", "success")
    return redirect(url_for("cart.view_cart"))

@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))  # Redirect to login page

    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        flash("Your cart is empty!", "error")
        return redirect(url_for('cart.view_cart'))

    # Calculate total amount
    total_amount = sum(Products.query.get(item.product_id).price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Create a new order with total_amount
        new_order = Orders(user_id=user_id, total_amount=total_amount, status="Pending")
        db.session.add(new_order)
        db.session.commit()

        # Add items to order
        for item in cart_items:
            product = Products.query.get(item.product_id)  # Retrieve the product here
            if product:
                order_item = OrderItems(
                    order_id=new_order.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price * item.quantity  # Now product is defined
                )
                db.session.add(order_item)

                # Reduce stock
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                else:
                    flash(f"Not enough stock for {product.name}!", "error")
                    return redirect(url_for('cart.view_cart'))

        # Clear cart after successful order placement
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        flash("Checkout successful! Your order has been placed.", "success")
        return redirect(url_for('user.view_order', order_id=new_order.order_id))  # Redirect to order history page

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)
