#!/usr/bin/python3
"""Start web application with a route to display categories."""

from flask import Flask, render_template, request
from flask import redirect, url_for, session, jsonify, flash
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
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
app.secret_key = "5NrvVndJurj7iZLj0Kgg2A1T1h5XGKOgbv2LmWzX1B8Vxo"
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Folder to store uploaded images
app.config['UPLOAD_FOLDER'] = 'web_dynamic/static/images'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

notifications = []


@app.route('/index.html')
@app.route('/home')
@app.route('/')
def home():
    """Displays the home page with the first three categories,
    first four products with category_id=6,
    first six products with discount_id=4,
    and first six products with category_id=4."""
    categories = storage.all(Category)
    sorted_categories = sorted(categories.values(),
                               key=lambda
                               category: category.category_name)[:3]

    # Get the first four products where category_id = 6
    products_by_category = storage.filter_by_category(
        Product, category_id=6)[:4]

    # Get the first six products where discount_id = 4
    products_by_discount = storage.filter_by_discount(
        Product, discount_id=4)[:6]

    # Get the first six products where category_id = 2
    products_by_category_2 = storage.filter_by_category(
        Product, category_id=2)[:6]

    return render_template(
        'index.html',
        sorted_categories=sorted_categories,
        sorted_products_by_category=products_by_category,
        sorted_products_by_discount=products_by_discount,
        sorted_products_by_category_2=products_by_category_2
    )


@app.route('/about.html')
@app.route('/about')
def about():
    """ Prints a Message when /hbnb is called """
    return render_template('about.html')


@app.route('/shop.html', methods=['GET'])
@app.route('/shop', methods=['GET'])
def shop():
    """Displays categories and paginated products"""
    # Get all categories
    categories = storage.all(Category)
    sorted_categories = sorted(categories.values(),
                               key=lambda category: category.category_name)

    # Get selected category ID from query parameters
    selected_category_id = request.args.get('category', None)

    # Convert selected_category_id to an integer
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
    products = [product for product in products
                if isinstance(product, Product)]

    # Now sort the remaining products by their name
    sorted_products = sorted(
        products, key=lambda product: product.product_name)

    # Pagination logic
    page = int(request.args.get('page', 1))
    per_page = 12
    total_products = len(sorted_products)
    total_pages = (total_products + per_page - 1) // per_page
    paged_products = sorted_products[(page - 1) * per_page: page * per_page]

    # Ensure all variables are defined before rendering
    return render_template('shop.html',
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
            order_item = {'product_id': product_id,
                          'amount': amount, 'price': price}

            if 'order' not in session:
                session['order'] = []

            # Append the new order item to the existing list in the session
            session['order'].append(order_item)
            session.modified = True

            # Debug prints
            print(session.keys())  # Print all keys in the session
            print(session.get('order'))
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


@app.route('/cart.html', methods=['GET', 'POST'])
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    """Display the shopping cart and handle updates."""
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        delete = request.form.get('delete')

        # If delete is present, remove the item
        if delete:
            product_id_to_delete = delete
            if 'order' in session:
                session['order'] = [item for item in
                                    session['order']
                                    if item['product_id'] !=
                                    product_id_to_delete]
                session.modified = True
            return redirect(url_for('cart'))

        # Handle amount update
        amount = request.form.get('amount')
        # Debug prints
        if not product_id or not amount:
            return 'Product ID or amount is missing', 400

        try:
            amount = Decimal(amount)  # Convert amount to Decimal
        except (ValueError, InvalidOperation):
            return 'Invalid amount', 400

        if not product_id.isdigit():
            return 'Invalid product ID', 400

        product = storage.get(Product, int(product_id))
        if not product:
            return 'Product not found', 404

# Calculate price after discount
        discount = product.discount
        price_after_discount = round(
            product.unit_price * (1 - discount.discount_percentage / 100), 2
        ) if discount else product.unit_price

        price = round(price_after_discount * amount, 2)

        cart_item = {
            'product_id': product_id,
            'amount': amount,
            'price': price,
            'product_name': product.product_name,
            'image_url': product.image_url,
            'price_after_discount': price_after_discount
        }

        if 'order' not in session:
            session['order'] = []

        item_updated = False
        for item in session['order']:
            if item['product_id'] == product_id:
                # Update the existing item's amount and price
                item['amount'] = amount
                item['price'] = price
                item['price_after_discount'] = price_after_discount
                item_updated = True
                break

        if not item_updated:
            # Add new item if it does not exist in the cart
            cart_item = {
                'product_id': product_id,
                'amount': amount,
                'price': price,
                'product_name': product.product_name,
                'image_url': product.image_url,
                'price_after_discount': price_after_discount
            }
            session['order'].append(cart_item)

        session.modified = True

        print("Session order data after updating item:", session.get('order'))
        return redirect(url_for('cart'))
    else:
        if 'order' in session:
            order_items = session['order']
            total_price = round(sum(
                float(item['price']) for item in order_items), 2)

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

            return render_template('cart.html', order_items=order_items,
                                   total_price=total_price,
                                   final_price=final_price)
        else:
            return render_template('cart.html', order_items=[], total_price=0)


@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    """Apply a coupon code and update the total price."""
    coupon_code = request.form.get('coupon_code')
    source_page = request.form.get('source_page')
    # Debugging: Print source_page to verify
    print("Source Page:", source_page)
    # Handle case where source_page is None
    if not source_page:
        flash("An error occurred. Please try again.")
        return redirect(url_for('cart'))

    # Check if coupon code is provided
    if not coupon_code:
        flash("Coupon code is required.")
        return redirect(url_for(source_page))

    # Fetch the coupon details from the database
    coupon = storage.query(Coupon).filter_by(
        coupon_code=coupon_code, is_deleted=False).first()

    # Debugging: Print the coupon object
    print("Coupon Retrieved:", coupon)

    if coupon and coupon.start_date <= datetime.utcnow() <= coupon.end_date:
        if 'order' in session:
            order_items = session['order']
            total_price = round(sum(
                float(item['price']) for item in order_items), 2)

            # Calculate the final price after applying the coupon
            coupon_amount = float(coupon.coupon_amount)
            final_price = round(total_price - coupon_amount, 2)
            final_price = max(final_price, 0)

            # Store final price and coupon details in session
            session['total_price'] = total_price
            session['final_price'] = final_price
            session['coupon_amount'] = coupon_amount
            session['coupon_code'] = coupon_code

            flash("Coupon code applied successfully!")
            return redirect(url_for(source_page))
    else:
        flash("Invalid or expired coupon code.")
        return redirect(url_for(source_page))


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    """Clear the shopping cart."""
    if 'order' in session:
        session.pop('order', None)
        session.pop('coupon_id', None)
        session.pop('coupon_code', None)
        session.pop('final_price', None)
        session.pop('coupon_amount', None)
        session.modified = True

        print(session.keys())
        print(session.get('order'))
        print(session)

    flash('Cart has been cleared successfully.', 'success')
    return redirect(url_for('cart'))


@app.route('/checkout.html', methods=['GET', 'POST'])
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
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
            'payment_method': request.form.get('payment_method')
        }

        new_user = User(**user_data)
        storage.new(new_user)
        storage.save()

        if 'order' in session:
            total_price = sum(
                float(item['price']) for item in session['order'])
            final_price = session.get('final_price', total_price)
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
                final_price=Decimal(final_price),
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
            session.pop('final_price', None)
            session.pop('coupon_amount', None)

            print(session.keys())  # Print all keys in the session
            print(session.get('order'))  # Print the 'order' key in the session
            print(session)

        return redirect(url_for('thankyou'))
    return render_template('checkout.html')


@app.route('/thankyou.html')
@app.route('/thankyou')
def thankyou():
    """ display a HTML page only if n is an integer """
    return render_template('thankyou.html')


@app.route('/admin_login.html', methods=['GET', 'POST'])
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """function for admin login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Assuming storage.all() returns a dictionary of all objects
        admins = storage.all(Admin).values()
        admin = next((
            admin for admin in admins if admin.admin_name == username),
                     None)

        if admin and admin.verify_password(password):
            # Successful login
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        else:
            # Failed login
            return render_template('admin_login.html',
                                   error="Invalid username or password")

    return render_template('admin_login.html')


@app.route('/admin')
def admin_dashboard():
    """Ensure admin is logged in"""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Fetch relevant data based on admin role
        if admin.admin_role.admin_role_name == 'Super Admin':
            products = storage.session.query(Product).all()
        elif admin.admin_role.admin_role_name == 'Supplier Manager':
            products = storage.session.query(Product).all()
        elif admin.admin_role.admin_role_name == 'Product Manager':
            products = storage.session.query(Product).all()
        elif admin.admin_role.admin_role_name == 'Order Manager':
            orders = storage.session.query(Order).all()

        return render_template('admin.html', admin=admin)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/categories')
def admin_categories():
    """function to manage categories"""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)
        categories = [cat for cat in storage.all(
            Category).values() if not cat.is_deleted]
        return render_template('categories.html',
                               admin=admin, categories=categories)
    else:
        return redirect(url_for('admin_login'))


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    """function to add new category"""
    if 'admin_id' in session:
        if request.method == 'POST':
            admin_id = session.get('admin_id')
            category_name = request.form.get('category_name')
            image = request.files.get('image_url')

            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = f'images/{filename}'
            else:
                image_url = None

            new_category = Category(
                category_name=category_name,
                image_url=image_url,
                created_by_admin_id=admin_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            storage.new(new_category)
            storage.save()

            return redirect(url_for('admin_categories'))
        return render_template('add_category.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """function to edit categories"""
    if 'admin_id' in session:
        category = storage.get(Category, category_id)

        if request.method == 'POST':
            category_name = request.form.get('category_name')
            image = request.files.get('image_url')

            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                category.image_url = f'images/{filename}'  # Save relative path

            category.category_name = category_name
            category.updated_at = datetime.utcnow()
            storage.save()

            return redirect(url_for('admin_categories'))

        return render_template('edit_category.html',
                               category=category)
    else:
        return redirect(url_for('admin_login'))


@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    """function to delete category"""
    if 'admin_id' in session:
        category = storage.get(Category, category_id)
        if category:
            category.is_deleted = True
            category.deleted_at = datetime.utcnow()
            storage.save()
        return redirect(url_for('admin_categories'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/admins')
def admin_admins():
    """function to manage admins"""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)
        admins = [adm for adm in storage.all(
            Admin).values() if not adm.is_deleted]
        return render_template('admins.html', admin=admin, admins=admins)
    else:
        return redirect(url_for('admin_login'))


@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    """function to add new admin"""
    if 'admin_id' in session:
        admin_roles = storage.all(AdminRole).values()
        if request.method == 'POST':
            admin_name = request.form.get('admin_name')
            email = request.form.get('email')
            password = request.form.get('password')
            admin_role_id = request.form.get('admin_role_id')
            image = request.files.get('image_url')

            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = f'images/{filename}'
            else:
                image_url = None

            new_admin = Admin(
                admin_name=admin_name,
                email=email,
                password=password,
                admin_role_id=admin_role_id,
                image_url=image_url,
                status=1,  # Default active status
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            storage.new(new_admin)
            storage.save()

            return redirect(url_for('admin_admins'))

        return render_template('add_admin.html', admin_roles=admin_roles)
    else:
        return redirect(url_for('admin_login'))


@app.route('/edit_admin/<int:admin_id>', methods=['GET', 'POST'])
def edit_admin(admin_id):
    """function to edit admin"""
    if 'admin_id' in session:
        admin = storage.get(Admin, admin_id)
        admin_roles = storage.all(AdminRole).values()

        if request.method == 'POST':
            admin.admin_name = request.form.get('admin_name')
            email = request.form.get('email')
            admin_role_id = request.form.get('admin_role_id')
            image = request.files.get('image_url')

            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                admin.image_url = f'images/{filename}'

            admin.email = email
            admin.admin_role_id = admin_role_id
            admin.updated_at = datetime.utcnow()
            storage.save()

            return redirect(url_for('admin_admins'))

        return render_template('edit_admin.html',
                               admin=admin, admin_roles=admin_roles)
    else:
        return redirect(url_for('admin_login'))


@app.route('/delete_admin/<int:admin_id>')
def delete_admin(admin_id):
    """function to delete admin"""
    if 'admin_id' in session:
        admin = storage.get(Admin, admin_id)
        if admin:
            admin.is_deleted = True
            admin.deleted_at = datetime.utcnow()
            storage.save()
        return redirect(url_for('admin_admins'))
    else:
        return redirect(url_for('admin_login'))


# Admin coupons route
@app.route('/admin/coupons')
def admin_coupons():
    """function to manage coupons"""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Retrieve only non-deleted coupons
        coupons = [coupon for coupon in storage.all(
            Coupon).values() if not coupon.is_deleted]
        return render_template('coupons.html',
                               admin=admin, coupons=coupons)
    else:
        return redirect(url_for('admin_login'))


# Add coupon route
@app.route('/add_coupon', methods=['GET', 'POST'])
def add_coupon():
    """function to add new coupon"""
    if 'admin_id' in session:
        if request.method == 'POST':
            admin_id = session.get('admin_id')
            coupon_code = request.form.get('coupon_code')
            coupon_amount = request.form.get('coupon_amount')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            new_coupon = Coupon(
                coupon_code=coupon_code,
                coupon_amount=coupon_amount,
                start_date=start_date,
                end_date=end_date,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            storage.new(new_coupon)
            storage.save()

            return redirect(url_for('admin_coupons'))
        else:
            return render_template('add_coupon.html')
    else:
        return redirect(url_for('admin_login'))


# Edit coupon route
@app.route('/edit_coupon/<int:coupon_id>', methods=['GET', 'POST'])
def edit_coupon(coupon_id):
    """function to edit coupon"""
    if 'admin_id' in session:
        coupon = storage.get(Coupon, coupon_id)

        if request.method == 'POST':
            coupon.coupon_code = request.form.get('coupon_code')
            coupon.coupon_amount = request.form.get('coupon_amount')
            coupon.start_date = request.form.get('start_date')
            coupon.end_date = request.form.get('end_date')
            coupon.updated_at = datetime.utcnow()
            storage.save()
            return redirect(url_for('admin_coupons'))

        return render_template('edit_coupon.html', coupon=coupon)
    else:
        return redirect(url_for('admin_login'))


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%dT%H:%M'):
    """function to return date"""
    return value.strftime(format)


# Delete coupon route
@app.route('/delete_coupon/<int:coupon_id>')
def delete_coupon(coupon_id):
    """function to delete coupon"""
    if 'admin_id' in session:
        coupon = storage.get(Coupon, coupon_id)
        if coupon:
            coupon.is_deleted = True
            coupon.deleted_at = datetime.utcnow()
            storage.save()
        return redirect(url_for('admin_coupons'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/deliveries')
def admin_deliveries():
    """function to manage deliveries"""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)

        # Retrieve only non-deleted deliveries
        deliveries = [delivery for delivery in storage.all(
            Delivery).values() if not delivery.is_deleted]
        return render_template('deliveries.html',
                               admin=admin, deliveries=deliveries)
    else:
        return redirect(url_for('admin_login'))


@app.route('/add_delivery', methods=['GET', 'POST'])
def add_delivery():
    """function to view deliveries"""
    if 'admin_id' in session:
        if request.method == 'POST':
            delivery_name = request.form.get('delivery_name')
            contact_number = request.form.get('contact_number')
            address = request.form.get('address')
            is_active = int(request.form.get('is_active'))

            new_delivery = Delivery(
                delivery_name=delivery_name,
                contact_number=contact_number,
                address=address,
                is_active=is_active,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            storage.new(new_delivery)
            storage.save()

            return redirect(url_for('admin_deliveries'))
        else:
            return render_template('add_delivery.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/edit_delivery/<int:delivery_id>', methods=['GET', 'POST'])
def edit_delivery(delivery_id):
    """function to edit delivery"""
    if 'admin_id' in session:
        delivery = storage.get(Delivery, delivery_id)

        if request.method == 'POST':
            delivery.delivery_name = request.form.get('delivery_name')
            delivery.contact_number = request.form.get('contact_number')
            delivery.address = request.form.get('address')
            delivery.is_active = int(request.form.get('is_active'))
            delivery.updated_at = datetime.utcnow()

            storage.save()
            return redirect(url_for('admin_deliveries'))

        return render_template('edit_delivery.html', delivery=delivery)
    else:
        return redirect(url_for('admin_login'))


@app.route('/delete_delivery/<int:delivery_id>')
def delete_delivery(delivery_id):
    """function to delete delivery"""
    if 'admin_id' in session:
        delivery = storage.get(Delivery, delivery_id)
        if delivery:
            delivery.is_deleted = True
            delivery.deleted_at = datetime.utcnow()
            storage.save()
        return redirect(url_for('admin_deliveries'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/discounts')
def admin_discounts():
    """function to manage admins"""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)
        discounts = [disc for disc in storage.all(
            Discount).values() if not disc.is_deleted]
        return render_template('discounts.html',
                               admin=admin, discounts=discounts)
    else:
        return redirect(url_for('admin_login'))


@app.route('/add_discount', methods=['GET', 'POST'])
def add_discount():
    """function to add new discount"""
    if 'admin_id' in session:
        if request.method == 'POST':
            discount_percentage = request.form.get('discount_percentage')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            new_discount = Discount(
                discount_percentage=discount_percentage,
                start_date=start_date,
                end_date=end_date,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            storage.new(new_discount)
            storage.save()

            return redirect(url_for('admin_discounts'))
        return render_template('add_discount.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/edit_discount/<int:discount_id>', methods=['GET', 'POST'])
def edit_discount(discount_id):
    """function to edit discount"""
    if 'admin_id' in session:
        discount = storage.get(Discount, discount_id)

        if request.method == 'POST':
            discount_percentage = request.form.get('discount_percentage')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            discount.discount_percentage = discount_percentage
            discount.start_date = start_date
            discount.end_date = end_date
            discount.updated_at = datetime.utcnow()
            storage.save()

            return redirect(url_for('admin_discounts'))

        return render_template('edit_discount.html', discount=discount)
    else:
        return redirect(url_for('admin_login'))


@app.route('/delete_discount/<int:discount_id>')
def delete_discount(discount_id):
    """function to delete discount"""
    if 'admin_id' in session:
        discount = storage.get(Discount, discount_id)
        if discount:
            discount.is_deleted = True
            discount.deleted_at = datetime.utcnow()
            storage.save()
        return redirect(url_for('admin_discounts'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/suppliers')
def admin_suppliers():
    """function to manage suppliers"""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)
        suppliers = [sup for sup in storage.all(
            Supplier).values() if not sup.is_deleted]
        return render_template('suppliers.html',
                               admin=admin, suppliers=suppliers)
    else:
        return redirect(url_for('admin_login'))


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    """function to add supplier"""
    if 'admin_id' in session:
        if request.method == 'POST':
            supplier_name = request.form.get('supplier_name')
            contact_number = request.form.get('contact_number')
            address = request.form.get('address')
            company_name = request.form.get('company_name')
            email = request.form.get('email')
            notes = request.form.get('notes')

            admin_id = session.get('admin_id')

            new_supplier = Supplier(
                supplier_name=supplier_name,
                contact_number=contact_number,
                address=address,
                company_name=company_name,
                email=email,
                notes=notes,
                created_by_admin_id=admin_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            storage.new(new_supplier)
            storage.save()

            return redirect(url_for('admin_suppliers'))
        return render_template('add_supplier.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    """function to edit supplier"""
    if 'admin_id' in session:
        supplier = storage.get(Supplier, supplier_id)

        if request.method == 'POST':
            supplier.supplier_name = request.form.get('supplier_name')
            supplier.contact_number = request.form.get('contact_number')
            supplier.address = request.form.get('address')
            supplier.company_name = request.form.get('company_name')
            supplier.email = request.form.get('email')
            supplier.notes = request.form.get('notes')

            supplier.updated_at = datetime.utcnow()
            storage.save()

            return redirect(url_for('admin_suppliers'))

        return render_template('edit_supplier.html', supplier=supplier)
    else:
        return redirect(url_for('admin_login'))


@app.route('/delete_supplier/<int:supplier_id>')
def delete_supplier(supplier_id):
    """function to delete supplier"""
    if 'admin_id' in session:
        supplier = storage.get(Supplier, supplier_id)
        if supplier:
            supplier.is_deleted = True
            supplier.deleted_at = datetime.utcnow()
            storage.save()
        return redirect(url_for('admin_suppliers'))
    else:
        return redirect(url_for('admin_login'))


'''@app.route('/admin/products')
def admin_products():
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)
        products = [prod for prod in storage.all(
            Product).values() if not prod.is_deleted]
        return render_template('products.html', admin=admin, products=products)
    else:
        return redirect(url_for('admin_login'))'''


@app.route('/admin/products')
def admin_products():
    """function that view and manage pproducts"""
    if 'admin_id' in session:
        admin_id = session.get('admin_id')
        admin = storage.get(Admin, admin_id)
        products = [prod for prod in storage.all(
            Product).values() if not prod.is_deleted]

        # Check for stock level issues
        notifications = []
        for product in products:
            if product.stock_weight <= product.min_stock:
                notifications.append(
                    f"Warning: {product.product_name} stock weight \
                        is less than or equal to min stock levels.")
        session['notifications'] = notifications
        return render_template('products.html', admin=admin,
                               products=products,
                               notifications=len(notifications),
                               notifications_list=notifications)
    else:
        return redirect(url_for('admin_login'))


@app.route('/mark_notifications_read', methods=['POST'])
def mark_notifications_read():
    """Clear the notifications from the session"""
    session['notifications'] = []
    return redirect(url_for('admin_products'))


@app.route('/notification')
def notification():
    """functn for notifications"""
    global notifications
    notifications = []  # Clear notifications when viewed
    return redirect(url_for('admin_products'))


@app.route('/products')
def products():
    """function that view products"""
    products = get_products()
    notifications = len(session.get('notifications', []))
    notifications_list = session.get('notifications', [])
    return render_template('products.html', products=products,
                           notifications=notifications,
                           notifications_list=notifications_list)


def get_products():
    """Replace this function with your actual logic to fetch products"""
    return [
        {'product_name': 'Product 1', 'stock_weight': 5,
         'min_stock': 10, 'unit': 'kg'},
        {'product_name': 'Product 2', 'stock_weight': 15,
         'min_stock': 10, 'unit': 'kg'},
    ]


@app.before_request
def check_notifications():
    """function to check notifications"""
    products = get_products()
    notifications = []
    for product in products:
        if product['min_stock'] >= product['stock_weight']:
            notifications.append(
                f"Warning: {product['product_name']} stock \
                    weight is less than or equal to min stock levels.")

    session['notifications'] = notifications


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """function to add a product"""
    if 'admin_id' in session:
        if request.method == 'POST':
            product_name = request.form.get('product_name')
            unit_price = request.form.get('unit_price')
            description = request.form.get('description')
            stock_weight = request.form.get('stock_weight')
            min_stock = request.form.get('min_stock')
            unit = request.form.get('unit')
            min_order_amount = request.form.get('min_order_amount')
            supplier_id = request.form.get('supplier_id')
            category_id = request.form.get('category_id')
            discount_id = request.form.get('discount_id')
            image = request.files.get('image_url')

            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = f'images/{filename}'
            else:
                image_url = None

            admin_id = session.get('admin_id')

            new_product = Product(
                product_name=product_name,
                unit_price=unit_price,
                description=description,
                stock_weight=stock_weight,
                min_stock=min_stock,
                unit=unit,
                min_order_amount=min_order_amount,
                supplier_id=supplier_id,
                category_id=category_id,
                discount_id=discount_id,
                image_url=image_url,
                created_by_admin_id=admin_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Calculate price after discount if applicable
            if discount_id:
                discount = storage.get(Discount, discount_id)
                if discount:
                    new_product.price_after_discount = float(unit_price) * (
                        1 - discount.discount_percentage / 100)

            storage.new(new_product)
            storage.save()

            return redirect(url_for('admin_products'))

        suppliers = storage.all(Supplier).values()
        categories = storage.all(Category).values()
        discounts = storage.all(Discount).values()

        return render_template('add_product.html', suppliers=suppliers,
                               categories=categories, discounts=discounts)
    else:
        return redirect(url_for('admin_login'))


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """function to edit products"""
    if 'admin_id' in session:
        product = storage.get(Product, product_id)

        if request.method == 'POST':
            product.product_name = request.form.get('product_name')
            product.unit_price = request.form.get('unit_price')
            product.description = request.form.get('description')
            product.stock_weight = request.form.get('stock_weight')
            product.min_stock = request.form.get('min_stock')
            product.unit = request.form.get('unit')
            product.min_order_amount = request.form.get('min_order_amount')
            product.supplier_id = request.form.get('supplier_id')
            product.category_id = request.form.get('category_id')
            product.discount_id = request.form.get('discount_id')
            image = request.files.get('image_url')

            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                product.image_url = f'images/{filename}'  # Save relative path

            # Recalculate price after discount if applicable
            if product.discount_id:
                discount = storage.get(Discount, product.discount_id)
                if discount:
                    product.price_after_discount = float(
                        product.unit_price) * (
                        1 - discount.discount_percentage / 100)

            product.updated_at = datetime.utcnow()
            storage.save()

            return redirect(url_for('admin_products'))

        suppliers = storage.all(Supplier).values()
        categories = storage.all(Category).values()
        discounts = storage.all(Discount).values()

        return render_template('edit_product.html', product=product,
                               suppliers=suppliers, categories=categories,
                               discounts=discounts)
    else:
        return redirect(url_for('admin_login'))


@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    """function to delete a product"""
    if 'admin_id' in session:
        product = storage.get(Product, product_id)
        if product:
            product.is_deleted = True
            product.deleted_at = datetime.utcnow()
            storage.save()
        return redirect(url_for('admin_products'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/orders')
def admin_orders():
    """function to view orders"""
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


# Edit Order Route
@app.route('/admin/orders/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    """function to edit an order"""
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
    """to close session"""
    storage.close()


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
