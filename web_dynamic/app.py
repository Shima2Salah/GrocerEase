#!/usr/bin/python3
"""Start web application with a route to display categories."""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from models import storage
from models.admin import Admin
from models.admin_role import AdminRole
from models.base_model import BaseModel, Base
from models.category import Category
from models.coupon import Coupon
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

"""@app.route('/page3.html', methods=['GET'])
@app.route('/page3', methods=['GET'])
def page3():
    """'''Displays specific category without all categories'''"""
    # Get all categories
    categories = storage.all(Category)
    sorted_categories = sorted(categories.values(), key=lambda category: category.category_name)

    # Get selected category ID from query parameters
    selected_category_id = request.args.get('category', None)
    if selected_category_id:
        selected_category_id = int(selected_category_id)

    # Filter products based on selected category
    if selected_category_id:
        products = storage.filter_by_category(Product, selected_category_id)
    else:
        products = storage.all(Product)
    
    # Filter out any strings if they are not supposed to be there
    products = [product for product in products if isinstance(product, Product)]

    # Now sort the remaining products by their name
    sorted_products = sorted(products, key=lambda product: product.product_name)

    # Pagination logic
    page = int(request.args.get('page', 1))
    per_page = 10
    total_products = len(sorted_products)
    total_pages = (total_products + per_page - 1) // per_page
    paged_products = sorted_products[(page - 1) * per_page: page * per_page]

    # Ensure all variables are defined before rendering
    return render_template('page3.html', 
                           sorted_categories=sorted_categories,
                           paged_products=paged_products,
                           page=page,
                           total_pages=total_pages,
                           selected_category_id=selected_category_id,
                           int=int)"""
@app.route('/page3.html', methods=['GET'])
@app.route('/page3', methods=['GET'])
def page3():
    """Displays categories and paginated products based on selected category."""
    # Get all categories
    categories = storage.all(Category)
    sorted_categories = sorted(categories.values(), key=lambda category: category.category_name)

    # Get selected category ID from query parameters
    selected_category_id = request.args.get('category', None)

    # Convert selected_category_id to an integer if it is not None and is numeric
    if selected_category_id and selected_category_id.isnumeric():
        selected_category_id = int(selected_category_id)
    else:
        selected_category_id = None

    # Get the selected category object if a valid ID is provided
    selected_category = None
    if selected_category_id:
        selected_category = storage.get(Category, selected_category_id)

    # Filter products based on selected category
    if selected_category:
        products = storage.filter_by_category(Product, selected_category_id)
    else:
        # If "All Categories" is selected, fetch all products
        products = storage.all(Product)

    # Convert products dict to a list
    if isinstance(products, dict):
        products = list(products.values())
    
    # Filter out any strings if they are not supposed to be there
    products = [product for product in products if isinstance(product, Product)]

    # Now sort the remaining products by their name
    sorted_products = sorted(products, key=lambda product: product.product_name)

    # Pagination logic
    page = int(request.args.get('page', 1))
    per_page = 10
    total_products = len(sorted_products)
    total_pages = (total_products + per_page - 1) // per_page
    paged_products = sorted_products[(page - 1) * per_page: page * per_page]

    # Ensure all variables are defined before rendering
    return render_template('page3.html', 
                           sorted_categories=sorted_categories,
                           paged_products=paged_products,
                           page=page,
                           total_pages=total_pages,
                           selected_category_id=selected_category_id,
                           selected_category=selected_category)

@app.route('/single.html/<int:product_id>', methods=['GET', 'POST'])
@app.route('/single/<int:product_id>', methods=['GET', 'POST'])
def single(product_id):
    """Display a single product page and handle adding to cart."""
    product = storage.get(Product, product_id)

    if not product:
        return 'Product not found', 404

    discount = product.discount  # Fetch the discount if available
    price_after_discount = round(
        product.unit_price * (1 - discount.discount_percentage / 100), 2
    ) if discount else product.unit_price

    if request.method == 'POST':
        amount = Decimal(request.form.get('amount'))

        if amount > 0 and amount <= product.stock_weight:
            price = round(price_after_discount * amount, 2)
            order_item = {'product_id': product_id, 'amount': amount, 'price': price}

            if 'order' not in session:
                session['order'] = []

            # Append the new order item to the existing list in the session
            session['order'].append(order_item)
            session.modified = True

            # Debug prints
            print(session.keys())  # Print all keys in the session
            print(session.get('order'))  # Print the 'order' key in the session
            print(session)

            return redirect(url_for('cart'))
        else:
            return 'Invalid amount or insufficient stock'

    return render_template(
        'single.html',
        product=product,
        discount=discount,
        price_after_discount=price_after_discount
    )

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    """Display the shopping cart and handle updates."""
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        amount = float(request.form.get('amount'))

        return redirect(url_for('cart'))
    else:
        if 'order' in session: 
            order_items = session['order']
            total_price = round(sum(float(item['price']) for item in order_items), 2)

            final_price = session.get('final_price', total_price)


            for item in order_items:
                product = storage.get(Product, item['product_id'])
                if product:
                    item['product_name'] = product.product_name
                    item['image_url'] = product.image_url
                    item['price_after_discount'] = product.price_after_discount

            print(session.keys())  # Print all keys in the session
            print(session.get('order'))  # Print the 'order' key in the session
            print(session)

            return render_template('cart.html', order_items=order_items, total_price=total_price, final_price=final_price)
        else:
            return render_template('cart.html', order_items=[], total_price=0)


@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    """Apply a coupon code and update the total price."""
    coupon_code = request.form.get('coupon_code')
    
    # Fetch the coupon details from the database
    coupon = storage.query(Coupon).filter_by(coupon_code=coupon_code, is_deleted=False).first()
    
    # Debugging: Print the coupon object
    print("Coupon Retrieved:", coupon)

    if coupon and coupon.start_date <= datetime.utcnow() <= coupon.end_date:
        if 'order' in session:
            order_items = session['order']
            total_price = round(sum(float(item['price']) for item in order_items), 2)
            
            # Calculate the final price after applying the coupon
            coupon_amount = float(coupon.coupon_amount)
            final_price = round(total_price - coupon_amount, 2)
            final_price = max(final_price, 0)  # Ensure price doesn't go negative
            
            # Store final price and coupon details in session
            session['total_price'] = total_price
            session['final_price'] = final_price
            session['coupon_amount'] = coupon_amount
            session['coupon_code'] = coupon_code  # Store coupon code for display

            return render_template('cart.html', 
                                   order_items=order_items, 
                                   total_price=total_price, 
                                   final_price=final_price, 
                                   coupon_amount=coupon_amount)
    else:
        flash("Invalid or expired coupon code.")
        return redirect(url_for('cart'))



@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    """Clear the shopping cart."""
    if 'order' in session:
        session.pop('order', None)  # Remove the 'order' key from the session
        session.pop('coupon_id', None)
        session.pop('coupon_code', None)
        session.pop('final_price', None)  # Clear final_price after processing
        session.pop('coupon_amount', None)
        session.modified = True  # Mark the session as modified

        print(session.keys())  # Print all keys in the session
        print(session.get('order'))  # Print the 'order' key in the session
        print(session)

    flash('Cart has been cleared successfully.', 'success')
    return redirect(url_for('cart'))



@app.route('/proced.html', methods=['GET', 'POST'])
@app.route('/proced', methods=['GET', 'POST'])
def proced():
    '''Handle the checkout process.'''
    if request.method == 'POST':
        user_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'contact_number': request.form.get('contact_number'),
            'email': request.form.get('email'),
            'country': request.form.get('country'),
            'company_name': request.form.get('company_name'),
            'address': request.form.get('address'),
            'state_or_country': request.form.get('state_or_country'),
            'postal_or_zip': request.form.get('postal_or_zip'),
            'order_notes': request.form.get('order_notes'),
            'payment_method': request.form.get('payment_method')  # Capture payment method
        }

        new_user = User(**user_data)
        storage.new(new_user)
        storage.save()

        if 'order' in session:
            total_price = sum(float(item['price']) for item in session['order'])
            final_price = session.get('final_price', total_price)  # Use final_price from session or fallback to total_price
            
            # Create payment first
            new_payment = Payment(payment_method=user_data['payment_method'])
            storage.new(new_payment)
            storage.save()

            print(f"Total Price from session: {total_price}")
            print(f"Final Price from session: {final_price}")

            # Create order with payment_id and final_price
            new_order = Order(
                user_id=new_user.id,
                total_price=Decimal(total_price),
                final_price=Decimal(final_price),  # Use final_price here
                payment_id=new_payment.id  # Set payment_id
            )
            storage.new(new_order)
            storage.save()

            print(f"Total Price from session: {total_price}")
            print(f"Final Price from session: {final_price}")


            for item in session['order']:
                new_order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item['product_id'],
                    amount=item['amount'],
                    price=item['price']
                )
                storage.new(new_order_item)
                storage.save()

            print(f"Total Price from session: {total_price}")
            print(f"Final Price from session: {final_price}")


            session.pop('order', None)
            session.pop('coupon_id', None)
            session.pop('coupon_code', None)
            session.pop('total_price', None)
            session.pop('final_price', None)  # Clear final_price after processing
            session.pop('coupon_amount', None)  # Clear coupon_amount after processing

            print(session.keys())  # Print all keys in the session
            print(session.get('order'))  # Print the 'order' key in the session
            print(session)

        return redirect(url_for('thankyou'))
    return render_template('proced.html')



@app.route('/thankyou.html')
@app.route('/thankyou')
def thankyou():
    """ display a HTML page only if n is an integer """
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
def admin_dashboard():
    # Ensure admin is logged in
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Fetch products to display on the dashboard
        products = storage.session.query(Product).all()

        return render_template('admin.html', admin=admin, products=products)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/categories')
def admin_categories():
    # Check if admin is logged in
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Retrieve only non-deleted categories
        categories = [cat for cat in storage.all(Category).values() if not cat.is_deleted]
        return render_template('categories.html', admin=admin, categories=categories)
    else:
        return redirect(url_for('admin_login'))



'''@app.route('/admin/categories')
def admin_categories():
    # Check if admin is logged in
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        categories = storage.all(Category).values()  # Retrieve all categories
        return render_template('categories.html', admin=admin, categories=categories)
    else:
        return redirect(url_for('admin_login'))'''


@app.route('/add_category', methods=['POST'])
def add_category():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        category_name = request.form.get('category_name')

        new_category = Category(
            category_name=category_name,
            created_by_admin_id=admin_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        storage.new(new_category)
        storage.save()

        return redirect(url_for('admin_categories'))  # Redirect to categories page after adding
    else:
        return redirect(url_for('admin_login'))

# Implement similar routes for editing and deleting categories, products, etc.

@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if 'admin_id' in session:
        category = storage.get(Category, category_id)

        if request.method == 'POST':
            category.category_name = request.form.get('category_name')
            category.updated_at = datetime.utcnow()
            storage.save()
            return redirect(url_for('admin_categories'))

        return render_template('edit_category.html', category=category)
    else:
        return redirect(url_for('admin_login'))

@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    if 'admin_id' in session:
        category = storage.get(Category, category_id)
        if category:
            category.delete()  # Call the soft delete method from BaseModel
        return redirect(url_for('admin_categories'))
    else:
        return redirect(url_for('admin_login'))

'''@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    if 'admin_id' in session:
        category = storage.get(Category, category_id)
        storage.delete(category)
        storage.save()
        return redirect(url_for('admin_categories'))
    else:
        return redirect(url_for('admin_login'))'''


'''@app.route('/admin/products')
def admin_products():
    # Check if admin is logged in
    if 'admin_id' in session:
        products = storage.all(Product).values()  # Retrieve all products
        return render_template('products.html', products=products)
    else:
        return redirect(url_for('admin_login'))'''

@app.route('/admin/products')
def admin_products():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Retrieve only products with non-deleted categories
        products = [prod for prod in storage.session.query(Product).all() if not prod.category.is_deleted]
        return render_template('products.html', admin=admin, products=products)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/suppliers')
def admin_suppliers():
    suppliers = storage.all(Supplier)  # Assuming storage is your DBStorage instance
    return render_template('suppliers.html', suppliers=suppliers)



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
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Fetch all orders along with related information
        orders = storage.session.query(Order).all()
        order_items = storage.session.query(OrderItem).all()
        products = storage.session.query(Product).all()
        categories = storage.session.query(Category).all()
        deliveries = storage.session.query(Delivery).all()
        users = storage.session.query(User).all()
        order_statuses = storage.session.query(OrderStatus).all()

        return render_template('orders.html', 
                               admin=admin, 
                               orders=orders, 
                               order_items=order_items, 
                               products=products, 
                               categories=categories,
                               deliveries=deliveries,
                               users=users,
                               order_statuses=order_statuses)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/orders/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        order = storage.get(Order, order_id)

        if request.method == 'POST':
            # Update the order with the new details from the form
            order.delivery_id = request.form.get('delivery_id')
            order.status_id = request.form.get('status_id')
            order.user_id = request.form.get('user_id')
            order.user_address = request.form.get('user_address')

            storage.save()
            return redirect(url_for('admin_orders'))

        # Fetch necessary data to populate the edit form
        deliveries = storage.session.query(Delivery).all()
        users = storage.session.query(User).all()
        order_statuses = storage.session.query(OrderStatus).all()

        return render_template('edit_order.html', 
                               admin=admin, 
                               order=order, 
                               deliveries=deliveries, 
                               users=users,
                               order_statuses=order_statuses)
    else:
        return redirect(url_for('admin_login'))








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

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout."""
    session.pop('admin_id', None)  # Clear session
    return redirect(url_for('admin_login'))


@app.teardown_appcontext
def app_teardown(arg=None):
    storage.close()

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)


# Route to render the admin dashboard
'''@app.route('/admin/dashboard')
def admin_dashboard2():
    """Admin dashboard page."""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Fetch products to display on the dashboard
        products = storage.session.query(Product).all()

        return render_template('admin_dashboard.html', admin=admin, products=products)
    else:
        return redirect(url_for('admin_login'))'''

"""@app.route('/proced.html', methods=['GET', 'POST'])
@app.route('/proced', methods=['GET', 'POST'])
def proced():
    '''Handle the checkout process.'''
    if request.method == 'POST':
        user_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'contact_number': request.form.get('contact_number'),
            'email': request.form.get('email'),
            'country': request.form.get('country'),
            'company_name': request.form.get('company_name'),
            'address': request.form.get('address'),
            'state_or_country': request.form.get('state_or_country'),
            'postal_or_zip': request.form.get('postal_or_zip'),
            'order_notes': request.form.get('order_notes'),
            'payment_method': request.form.get('payment_method')  # Capture payment method
        }

        new_user = User(**user_data)
        storage.new(new_user)
        storage.save()

        if 'order' in session:
            total_price = sum(float(item['price']) for item in session['order'])
            # Create payment first
            new_payment = Payment(payment_method=user_data['payment_method'])
            storage.new(new_payment)
            storage.save()

            # Create order with payment_id
            new_order = Order(
                user_id=new_user.id,
                total_price=Decimal(total_price),
                payment_id=new_payment.id  # Set payment_id
            )
            storage.new(new_order)
            storage.save()

            for item in session['order']:
                new_order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item['product_id'],
                    amount=item['amount'],
                    price=item['price']
                )
                storage.new(new_order_item)
                storage.save()

            session.pop('order', None)

        return redirect(url_for('thankyou'))
    return render_template('proced.html')"""
