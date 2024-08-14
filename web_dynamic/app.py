#!/usr/bin/python3
"""Start web application with a route to display categories."""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import storage
from models.admin import Admin
from models.admin_role import AdminRole
from models.base_model import BaseModel, Base
from models.category import Category
from models.delivery import Delivery
from models.discount import Discount
from models.order import Order
from models.order_item import OrderItem
from models.order_status import OrderStatus
from models.payment import Payment
from models.product import Product
from models.user import User
from models.supplier import Supplier
from decimal import Decimal

app = Flask(__name__)
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
app.secret_key = "5NrvVndJurj7iZLj0Kgg2A1T1h5XGKOgbv2LmWzX1B8Vxo"
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route('/index.html')
@app.route('/home')
@app.route('/')
def home():
    """ Prints a Message when / is called """
    return render_template('index.html')

@app.route('/about.html')
@app.route('/about')
def about():
    """ Prints a Message when /hbnb is called """
    return render_template('about.html')

@app.route('/page3.html', methods=['GET'])
@app.route('/page3', methods=['GET'])
def page3():
    """ Prints a Message when /python is called """
    products = storage.all(Product)
    sorted_products = sorted(products.values(), key=lambda product: product.product_name)
    categories = storage.all(Category)
    sorted_categories = sorted(categories.values(), key=lambda category: category.category_name)
    return render_template('page3.html', sorted_products=sorted_products,
                           sorted_categories=sorted_categories)
@app.route('/single/<int:product_id>', methods=['GET', 'POST'])
def single(product_id):
    """Display a single product page and handle adding to cart."""
    if request.method == 'POST':
        product_id = int(request.form.get('product_id'))
        weight = int(request.form.get('weight'))

        product = storage.get(Product, product_id)

        if product and weight > 0:
            price = round(product.unit_price * weight, 2)
            order_item = {'product_id': product_id, 'weight': weight, 'price': price}

            if 'order' not in session:
                session['order'] = []

            # Append the new order item to the existing list in the session
            session['order'].append(order_item)
            session.modified = True
            return redirect(url_for('cart'))
        else:
            return 'Product not found or invalid weight'
    else:
        product = storage.get(Product, product_id)
        return render_template('single.html', product=product)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    """Display the shopping cart and handle updates."""
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        weight = request.form.get('weight')

        return redirect(url_for('cart'))
    else:
        if 'order' in session: 
            order_items = session['order']
            total_price = round(sum(float(item['price']) for item in order_items), 2)

            for item in order_items:
                product = storage.get(Product, item['product_id'])
                if product:
                    item['product_name'] = product.product_name
                    item['image_url'] = product.image_url
                    item['unit_price'] = product.unit_price

            return render_template('cart.html', order_items=order_items, total_price=total_price)
        else:
            return render_template('cart.html', order_items=[], total_price=0)

@app.route('/proced', methods=['GET', 'POST'])
def proced():
    """Handle the checkout process."""
    if request.method == 'POST':
        user_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'contact_number': request.form.get('contact_number'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'country': request.form.get('country'),
            'company_name': request.form.get('company_name'),
            'address': request.form.get('address'),
            'state_or_country': request.form.get('state_or_country'),
            'postal_or_zip': request.form.get('postal_or_zip'),
            'order_notes': request.form.get('order_notes')
        }

        new_user = User(**user_data)
        storage.new(new_user)
        storage.save()

        if 'order' in session:
            total_price = sum(item['price'] for item in session['order'])
            new_order = Order(user_id=new_user.id, total_price=Decimal(total_price))
            storage.new(new_order)
            storage.save()

            for item in session['order']:
                new_order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'], quantity=item['weight'], price=item['price'])
                storage.new(new_order_item)
                storage.save()

            session.pop('order', None)

        return redirect(url_for('thankyou'))
    return render_template('proced.html')

@app.route('/thankyou')
def thankyou():
    """Display a thank you page after a successful order."""
    return render_template('thankyou.html')

@app.teardown_appcontext
def app_teardown(arg=None):
    storage.close()

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
