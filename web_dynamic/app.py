#!/usr/bin/python3
"""Start web application with two routings
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import storage
from models.category import Category
from models.color import Color
from models.order import Order
from models.orderItem import OrderItem
from models.product import Product
from models.size import Size
from models.user import User
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
    colors = storage.all(Color)
    sorted_colors = sorted(colors.values(), key=lambda color: color.color_name)
    categories = storage.all(Category)
    sorted_categories = sorted(categories.values(), key=lambda category: category.name)
    sizes = storage.all(Size)
    sorted_sizes = sorted(sizes.values(), key=lambda size: size.size_name, reverse=True)
    return render_template('page3.html', sorted_products=sorted_products,
                           sorted_colors=sorted_colors, sorted_categories=sorted_categories,
                           sorted_sizes=sorted_sizes)


@app.route('/single.html/<int:product_id>', methods=['GET', 'POST'])
@app.route('/single/<int:product_id>', methods=['GET', 'POST'])
def single(product_id):
    """ display a HTML page only if n is an integer """
    if request.method == 'POST':
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))

        product = storage.get(Product, product_id)

        if product and quantity > 0:
            price = round(product.price * quantity, 2)
            order_item = {'product_id': product_id, 'quantity': quantity, 'price': price}

            if 'order' not in session:
                session['order'] = []

            # Append the new order item to the existing list in the session
            session['order'].append(order_item)
            session.modified = True
            print(session.keys()) # Debug: Print all keys in the session
            print(session.get('order')) # Debug: Print the 'order' key in the session
            print(session)
            return redirect(url_for('cart'))
        else:
            return 'Product not found or invalid quantity'
    else:
        # Get the product details from the database based on the product_id
        product = storage.get(Product, product_id)
        # Pass the product details to the template
        return render_template('single.html', product=product)

@app.route('/cart.html', methods=['GET', 'POST'])
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    """ Prints a Message when /c is called """
    if request.method == 'POST':
        # Handle the POST request here
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')

        # Your logic to add the product to the order and calculate total price

        # Redirect to the GET request to display all order items
        return redirect(url_for('cart'))
    else:
        # Handle the GET request here
        if 'order' in session: 
            order_items = session['order']
            total_price = round(sum(item['price'] for item in order_items), 2)
            # Fetch product details from the database based on product_id
            for item in order_items:
                product = storage.get(Product, item['product_id'])
                if product:
                    item['product_name'] = product.product_name
                    item['image_url'] = product.image_url
                    item['unit_price'] = product.price
                    # You can fetch other product details here and add them to the order item
            return render_template('cart.html', order_items=order_items, total_price=total_price)
        else:
            return render_template('cart.html', order_items=[], total_price=0)


@app.route('/proced.html', methods=['GET', 'POST'])
@app.route('/proced', methods=['GET', 'POST'])
def proced():
    """ display a HTML page only if n is an integer """
    if request.method == 'POST':
        # Process the form data
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

        # Create a new User instance
        new_user = User(**user_data)
        storage.new(new_user)
        storage.save()

        # Process the order stored in the session
        if 'order' in session:
            total_price = sum(item['price'] for item in session['order'])
            new_order = Order(user_id=new_user.id, total_price=Decimal(total_price))
            storage.new(new_order)
            storage.save()

            for item in session['order']:
                new_order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'], quantity=item['quantity'], price=item['price'])
                storage.new(new_order_item)
                storage.save()

            # Clear the order from the session
            session.pop('order', None)

        return redirect(url_for('thankyou'))
    return render_template('proced.html')

@app.route('/thankyou.html')
@app.route('/thankyou')
def thankyou():
    """ display a HTML page only if n is an integer """
    return render_template('thankyou.html')


@app.teardown_appcontext
def app_teardown(arg=None):
    storage.close()

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
