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
from datetime import datetime

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
    """ Prints a Message when /page3 is called """
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

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Assuming storage.all() returns a dictionary of all objects
        admins = storage.all(Admin).values()
        admin = next((admin for admin in admins if admin.admin_name == username), None)

        if admin and admin.verify_password(password):
            # Successful login
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        else:
            # Failed login
            return render_template('admin_login.html', error="Invalid username or password")

    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard2():
    return render_template('admin.html')

@app.route('/admin/products')
def admin_products():
    # Add your logic here to retrieve and display products
    """Admin products page."""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Fetch products to display on the products
        products = storage.session.query(Product).all()

        return render_template('products.html', admin=admin, products=products)
    else:
        return redirect(url_for('admin_login'))
    
@app.route('/add_category', methods=['POST'])
def add_category():
    # Assume admin_id is fetched from the session or request context
    admin_id = session.get('admin_id')  # or however you retrieve the current admin ID
    
    if admin_id is None:
        return "Admin must be logged in", 400  # Handle the error as needed
    
    category_name = request.form.get('category_name')
    new_category = Category(
        category_name=category_name,
        created_by_admin_id=admin_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Add the new category to the database session
    storage.new(new_category)  # Use the 'new' method to add the object
    storage.save()  # Commit the transaction
    return "Category added successfully", 201

@app.route('/admin/suppliers')
def admin_suppliers():
    suppliers = storage.all(Supplier)  # Assuming storage is your DBStorage instance
    return render_template('suppliers.html', suppliers=suppliers)


@app.route('/admin/categories')
def admin_categories():
    # Add your logic here to retrieve and display categories
    return render_template('categories.html')



@app.route('/admin/admins')
def admin_admins():
    # Add your logic here to retrieve and display admins
    return render_template('admins.html')

@app.route('/admin/discounts')
def admin_discounts():
    # Add your logic here to retrieve and display discounts
    return render_template('discounts.html')

@app.route('/admin/coupons')
def admin_coupons():
    # Add your logic here to retrieve and display coupons
    return render_template('coupons.html')

@app.route('/admin/deliveries')
def admin_deliveries():
    # Add your logic here to retrieve and display deliveries
    return render_template('deliveries.html')

@app.route('/admin/orders')
def admin_orders():
    # Add your logic here to retrieve and display orders
    return render_template('orders.html')

# Route to render the admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page."""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Fetch products to display on the dashboard
        products = storage.session.query(Product).all()

        return render_template('admin_dashboard.html', admin=admin, products=products)
    else:
        return redirect(url_for('admin_login'))

# Route to add new category







# Route to add new product
@app.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    category_id = request.form['category_id']
    unit_price = request.form['unit_price']
    weight = request.form['weight']
    new_product = Product(name=product_name, category_id=category_id, unit_price=unit_price, weight=weight)
    storage.new(new_product)
    storage.save()
    return redirect(url_for('admin_dashboard'))

# Route to add new supplier
@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    supplier_name = request.form['supplier_name']
    new_supplier = Supplier(name=supplier_name)
    storage.new(new_supplier)
    storage.save()
    return redirect(url_for('admin_dashboard'))

# Route to add new coupon
@app.route('/add_coupon', methods=['POST'])
def add_coupon():
    coupon_code = request.form['coupon_code']
    discount_id = request.form['discount_id']
    new_coupon = Coupon(code=coupon_code, discount_id=discount_id)
    storage.new(new_coupon)
    storage.save()
    return redirect(url_for('admin_dashboard'))

# Route to add new discount
@app.route('/add_discount', methods=['POST'])
def add_discount():
    discount_value = request.form['discount_value']
    new_discount = Discount(value=discount_value)
    storage.new(new_discount)
    storage.save()
    return redirect(url_for('admin_dashboard'))

# Route to add new admin
@app.route('/add_admin', methods=['POST'])
def add_admin():
    admin_name = request.form['admin_name']
    admin_role = request.form['admin_role']
    new_admin = Admin(name=admin_name, role=admin_role)
    storage.new(new_admin)
    storage.save()
    return redirect(url_for('admin_dashboard'))





@app.route('/admin/some_protected_route')
def some_protected_route():
    """Protected admin route."""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    # Continue with the rest of the view logic

@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.pop('admin_id', None)
    return redirect(url_for('admin_login'))


@app.teardown_appcontext
def app_teardown(arg=None):
    storage.close()

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
