from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.product import Product
from models.user import User
from models.order import Order
from models.order_item import OrderItem
from models.category import Category
from models.coupon import Coupon
from models.supplier import Supplier
from models.admin import Admin
from models.admin_role import AdminRole
from models.discount import Discount
from models.delivery import Delivery
from models.order_status import OrderStatus
from models.payment import Payment
import models
import sys
import os

# Append the parent directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.engine.db_storage import DBStorage


# Dependencies:
# pip install pytest-mock
import pytest

class TestDBStorage:

    # Initialize DBStorage and verify engine creation
    def test_initialize_db_storage_engine_creation(self, mocker):
        mocker.patch('models.engine.db_storage.getenv', side_effect=lambda k: {
            'GROCER_MYSQL_USER': 'user',
            'GROCER_MYSQL_PWD': 'pwd',
            'GROCER_MYSQL_HOST': 'localhost',
            'GROCER_MYSQL_DB': 'test_db',
            'GROCER_ENV': 'development'
        }.get(k))
        mock_create_engine = mocker.patch('models.engine.db_storage.create_engine')
    
        storage = DBStorage()
    
        mock_create_engine.assert_called_once_with('mysql+mysqldb://user:pwd@localhost/test_db')

    # Initialize DBStorage with missing environment variables
    def test_initialize_db_storage_missing_env_vars(self, mocker):
        mocker.patch('models.engine.db_storage.getenv', return_value=None)
        mock_create_engine = mocker.patch('models.engine.db_storage.create_engine')
    
        with pytest.raises(TypeError):
            storage = DBStorage()
    
        mock_create_engine.assert_not_called()

    # Query all objects without class filter
    def test_query_all_objects_without_class_filter(self, mocker):
        # Setup
        mock_classes = {
            "BaseModel": BaseModel,
            "Product": Product,
            "User": User,
            "Order": Order,
            "OrderItem": OrderItem,
            "Category": Category,
            "Coupon": Coupon,
            "Supplier": Supplier,
            "Admin": Admin,
            "AdminRole": AdminRole,
            "Discount": Discount,
            "Delivery": Delivery,
            "OrderStatus": OrderStatus,
            "Payment": Payment
        }
        mocker.patch.object(DBStorage, '_DBStorage__session')
        mocker.patch.object(DBStorage, 'all', return_value=mock_classes)
        db_storage = DBStorage()

        # Exercise
        result = db_storage.all()

        # Verify
        assert isinstance(result, dict)
        assert len(result) == 0  # No objects returned without class filter

    # Add a new object to the session
    def test_add_new_object_to_session(self, mocker):
        # Prepare
        mock_create_engine = mocker.patch('models.engine.db_storage.create_engine')
        storage = DBStorage()
        obj = BaseModel()
    
        # Execute
        storage.new(obj)
    
        # Assert
        assert obj in storage._DBStorage__session.new

    # Reload data from the database
    def test_reload_data_from_database(self, mocker):
        mock_create_engine = mocker.patch('models.engine.db_storage.create_engine')
        mock_sessionmaker = mocker.patch('models.engine.db_storage.sessionmaker')
        mock_scoped_session = mocker.patch('models.engine.db_storage.scoped_session')
        mock_Base_metadata = mocker.patch('models.engine.db_storage.Base.metadata')

        storage = DBStorage()
        storage.reload()

        mock_Base_metadata.create_all.assert_called_once_with(storage._DBStorage__engine)
        mock_sessionmaker.assert_called_once_with(bind=storage._DBStorage__engine, expire_on_commit=False)
        mock_scoped_session.assert_called_once_with(mock_sessionmaker.return_value)
        assert storage._DBStorage__session == mock_scoped_session.return_value

    # Commit changes to the session
    def test_commit_changes_to_session(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.commit = mocker.MagicMock()
        mocker.patch('models.engine.db_storage.sessionmaker', return_value=mock_session)
    
        storage = DBStorage()
        storage.save()
    
        mock_session.commit.assert_called_once()

    # Close the session properly
    def test_close_session_properly(self, mocker):
        mock_remove = mocker.patch.object(DBStorage, '_DBStorage__session')
    
        storage = DBStorage()
        storage.close()
    
        mock_remove.assert_called_once()

    # Retrieve object by class and ID
    def test_retrieve_object_by_class_and_id(self, mocker):
        # Setup
        mock_classes = {
            "Product": Product,
            "User": User,
            "Order": Order,
            "OrderItem": OrderItem,
            "Category": Category,
            "Coupon": Coupon,
            "Supplier": Supplier,
            "Admin": Admin,
            "AdminRole": AdminRole,
            "Discount": Discount,
            "Delivery": Delivery,
            "OrderStatus": OrderStatus,
            "Payment": Payment
        }
        mocker.patch.object(DBStorage, '_DBStorage__session')
        db_storage = DBStorage()
        db_storage.__session.query = mocker.MagicMock()
        db_storage.__session.query.return_value.all.return_value = [mock_classes["Product"](id=1), mock_classes["Product"](id=2)]
    
        # Call
        result = db_storage.get(Product, 2)
    
        # Assertion
        assert result.id == 2

    # Query objects by class
    def test_query_objects_by_class(self, mocker):
        # Setup
        mock_classes = {
            "BaseModel": BaseModel,
            "Product": Product,
            "User": User,
            "Order": Order,
            "OrderItem": OrderItem,
            "Category": Category,
            "Coupon": Coupon,
            "Supplier": Supplier,
            "Admin": Admin,
            "AdminRole": AdminRole,
            "Discount": Discount,
            "Delivery": Delivery,
            "OrderStatus": OrderStatus,
            "Payment": Payment
        }
        mocker.patch.object(DBStorage, '_DBStorage__session')
        mocker.patch.object(DBStorage, 'all', return_value={})
        mocker.patch.object(DBStorage, 'query')

        # Call the function to test
        storage = DBStorage()
        storage.query(BaseModel)

        # Assertion
        storage.query.assert_called_once_with(BaseModel)

    # Query all objects with invalid class filter
    def test_query_invalid_class_filter(self, mocker):
        # Setup
        mock_classes = {
            "BaseModel": BaseModel,
            "Product": Product,
            "User": User,
            "Order": Order,
            "OrderItem": OrderItem,
            "Category": Category,
            "Coupon": Coupon,
            "Supplier": Supplier,
            "Admin": Admin,
            "AdminRole": AdminRole,
            "Discount": Discount,
            "Delivery": Delivery,
            "OrderStatus": OrderStatus,
            "Payment": Payment
        }
        mocker.patch.object(DBStorage, '_DBStorage__session')
        db_storage = DBStorage()

        # Exercise
        result = db_storage.query("InvalidClass")

        # Verify
        assert result is None

    # Count objects in storage
    def test_count_objects_in_storage(self, mocker):
        classes = {
            "BaseModel": BaseModel,
            "Product": Product,
            "User": User,
            "Order": Order,
            "OrderItem": OrderItem,
            "Category": Category,
            "Coupon": Coupon,
            "Supplier": Supplier,
            "Admin": Admin,
            "AdminRole": AdminRole,
            "Discount": Discount,
            "Delivery": Delivery,
            "OrderStatus": OrderStatus,
            "Payment": Payment
        }
        with mocker.patch('models.engine.db_storage.classes', classes):
            storage = DBStorage()
            storage.reload()
            count = storage.count()
        
            assert count == 0  # Assuming no objects are initially in storage

    # Retrieve Admin object by username
    def test_retrieve_admin_by_username(self, mocker):
        # Prepare
        mock_admin = Admin()
        mock_session = mocker.Mock()
        mocker.patch('models.engine.db_storage.create_engine')
        mocker.patch('models.engine.db_storage.session', mock_session)
        mocker.patch('models.engine.db_storage.classes', {"Admin": Admin})
        db_storage = DBStorage()

        # Define
        username = "test_admin"
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_admin

        # Execute
        result = db_storage.get_by_username(Admin, username)

        # Assert
        assert result == mock_admin
        mock_session.query.assert_called_once_with(Admin)
        mock_session.query.return_value.filter_by.assert_called_once_with(admin_name=username)
        mock_session.query.return_value.filter_by.return_value.first.assert_called_once()

    # Delete an object that does not exist
    def test_delete_non_existing_object(self, mocker):
        # Setup
        obj = BaseModel()
        db_storage = DBStorage()
        mocker.patch.object(db_storage, '_DBStorage__session')
    
        # Assertion
        with pytest.raises(Exception):
            db_storage.delete(obj)

    # Count objects with invalid class filter
    def test_count_objects_invalid_class_filter(self, mocker):
        # Setup
        mock_classes = {
            "BaseModel": BaseModel,
            "Product": Product,
            "User": User,
            "Order": Order,
            "OrderItem": OrderItem,
            "Category": Category,
            "Coupon": Coupon,
            "Supplier": Supplier,
            "Admin": Admin,
            "AdminRole": AdminRole,
            "Discount": Discount,
            "Delivery": Delivery,
            "OrderStatus": OrderStatus,
            "Payment": Payment
        }
        mocker.patch.object(DBStorage, '_DBStorage__session')
        mocker.patch.object(models.storage, 'all', return_value={})

        # Exercise
        with pytest.raises(AttributeError):
            DBStorage().count("InvalidClass")

        # Verify
        models.storage.all.assert_not_called()

    # Retrieve Admin object with non-existent username
    def test_retrieve_admin_non_existent_username(self, mocker):
        # Prepare
        mock_admin_query = mocker.patch('models.engine.db_storage.DBStorage.session.query')
        mock_admin_query.return_value.filter_by.return_value.first.return_value = None
    
        # Execute
        db_storage = DBStorage()
        result = db_storage.get_by_username(Admin, 'non_existent_username')
    
        # Assert
        assert result is None
        mock_admin_query.assert_called_once_with(Admin)
        mock_admin_query.return_value.filter_by.assert_called_once_with(admin_name='non_existent_username')
        mock_admin_query.return_value.filter_by.return_value.first.assert_called_once()

    # Query objects with invalid class
    def test_query_invalid_class(self, mocker):
        # Setup
        mock_classes = {
            "BaseModel": BaseModel,
            "Product": Product,
            "User": User,
            "Order": Order,
            "OrderItem": OrderItem,
            "Category": Category,
            "Coupon": Coupon,
            "Supplier": Supplier,
            "Admin": Admin,
            "AdminRole": AdminRole,
            "Discount": Discount,
            "Delivery": Delivery,
            "OrderStatus": OrderStatus,
            "Payment": Payment
        }
        mocker.patch.object(DBStorage, '_DBStorage__session')
        db_storage = DBStorage()

        # Assertion
        assert db_storage.query("InvalidClass") is None

    # Retrieve object with invalid class and ID
    def test_retrieve_invalid_class_and_id(self, mocker):
        # Setup
        mock_classes = {
            "Product": Product,
            "User": User,
            "Order": Order,
            "OrderItem": OrderItem,
            "Category": Category,
            "Coupon": Coupon,
            "Supplier": Supplier,
            "Admin": Admin,
            "AdminRole": AdminRole,
            "Discount": Discount,
            "Delivery": Delivery,
            "OrderStatus": OrderStatus,
            "Payment": Payment
        }
        mocker.patch.object(DBStorage, '_DBStorage__session')
        mocker.patch.object(models.storage, 'all', return_value={})

        # Execute
        db_storage = DBStorage()
        result = db_storage.get("InvalidClass", 123)

        # Verify
        assert result is None

    # Filter by discount with invalid discount_id
    def test_filter_by_discount_invalid_discount_id(self, mocker):
        # Setup
        mock_session = mocker.MagicMock()
        mock_query = mocker.MagicMock()
        mock_session.query.return_value = mock_query
        mocker.patch.object(DBStorage, '_DBStorage__session', mock_session)
    
        # Define test data
        invalid_discount_id = 999  # Assuming this is an invalid discount_id
    
        # Call the function
        DBStorage().filter_by_discount(Discount, invalid_discount_id)
    
        # Assertion
        mock_session.query.assert_called_once_with(Discount)
        mock_query.filter.assert_called_once_with(Discount.discount_id == invalid_discount_id)

    # Filter by category with invalid category_id
    def test_filter_by_category_invalid_category_id(self, mocker):
        # Setup
        mock_session = mocker.MagicMock()
        mock_query = mocker.MagicMock()
        mock_session.query.return_value = mock_query
        mocker.patch.object(DBStorage, '_DBStorage__session', mock_session)
    
        # Define inputs
        model_class = Category  # Assuming Category is the model class
        invalid_category_id = 999  # Assuming 999 is an invalid category_id
    
        # Call the function
        result = DBStorage().filter_by_category(model_class, invalid_category_id)
    
        # Assertions
        assert result == mock_query.filter_by.return_value.all.return_value
        mock_session.query.assert_called_once_with(model_class)
        mock_query.filter_by.assert_called_once_with(category_id=invalid_category_id)

    # Ensure session is reloaded if not initialized
    def test_reload_session_if_not_initialized(self, mocker):
        mock_create_engine = mocker.patch('models.engine.db_storage.create_engine')
        mock_sessionmaker = mocker.patch('sqlalchemy.orm.sessionmaker')
        mock_scoped_session = mocker.patch('sqlalchemy.orm.scoped_session')
    
        storage = DBStorage()
        storage.reload()
    
        mock_create_engine.assert_called_once()
        mock_sessionmaker.assert_called_once_with(bind=storage._DBStorage__engine, expire_on_commit=False)
        mock_scoped_session.assert_called_once_with(mock_sessionmaker.return_value)
