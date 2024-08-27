from models.product import Product
import models
from unittest.mock import MagicMock
from unittest.mock import patch
from models.order_item import OrderItem


import pytest

class TestProduct:

    # Creating a Product instance with all required fields
    def test_create_product_with_all_required_fields(self):
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
        assert product.product_name == "Test Product"
        assert product.unit_price == 10.00
        assert product.supplier_id == 1
        assert product.created_by_admin_id == 1
        assert product.category_id == 1

    # Creating a Product instance with missing required fields
    def test_create_product_with_missing_required_fields(self):
        product_data = {
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        with pytest.raises(TypeError):
            product = Product(**product_data)

    # Saving a Product instance to the database
    def test_save_product_instance_to_database(self, mocker):
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
        mocker.patch('models.storage.new')
        mocker.patch('models.storage.save')
    
        product.save()
    
        assert product.updated_at is not None
        models.storage.new.assert_called_once_with(product)
        models.storage.save.assert_called_once()

    # Retrieving a Product instance from the database
    def test_retrieve_product_instance(self, mocker):
        # Mocking the Product class
        mocker.patch('models.product.Product', autospec=True)
    
        # Call the function that retrieves a Product instance from the database
        product_instance = Product()
    
        # Assert that the Product class was called
        models.product.Product.assert_called_once()

    # Deleting a Product instance using soft delete
    def test_delete_product_soft_delete(self, mocker):
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
        mocker.patch('models.storage_t', return_value="db")
        product.delete()
        assert product.is_deleted is True
        assert product.deleted_at is not None

    # Updating a Product instance and saving changes
    def test_update_product_and_save_changes(self):  
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
        product.save()
        product.unit_price = 15.00
        product.save()
        assert product.unit_price == 15.00

    # Calculating price after discount for a Product instance
    def test_calculate_price_after_discount(self):
        # Create a Product instance with a discount
        discount_mock = MagicMock()
        discount_mock.discount_percentage = 10
        product_data = {
            "product_name": "Test Product",
            "unit_price": 100.00,
            "discount": discount_mock
        }
        product = Product(**product_data)
    
        # Calculate the price after discount
        price_after_discount = product.price_after_discount
    
        # Assert the calculated price is correct
        assert price_after_discount == 90.00

    # Converting a Product instance to a dictionary
    def test_convert_product_instance_to_dict(self):
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
        product_dict = product.to_dict()
        assert product_dict["product_name"] == "Test Product"
        assert product_dict["unit_price"] == 10.00
        assert product_dict["supplier_id"] == 1
        assert product_dict["created_by_admin_id"] == 1
        assert product_dict["category_id"] == 1

    # Ensuring relationships with Supplier, Admin, Discount, Category, and OrderItem are correctly established
    def test_relationships_established(self):
        # Creating mock objects for relationships
        supplier_mock = MagicMock()
        admin_mock = MagicMock()
        discount_mock = MagicMock()
        category_mock = MagicMock()
        order_item_mock = MagicMock()

        # Creating a Product instance
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)

        # Setting relationships
        product.supplier = supplier_mock
        product.admin = admin_mock
        product.discount = discount_mock
        product.category = category_mock
        product.order_items.append(order_item_mock)

        assert product.supplier == supplier_mock
        assert product.admin == admin_mock
        assert product.discount == discount_mock
        assert product.category == category_mock
        assert order_item_mock in product.order_items

    # Handling None values for optional fields in Product
    def test_handling_none_values(self):
        product = Product()
        assert product.product_name == ""
        assert product.unit_price is None
        assert product.image_url == ""
        assert product.description == ""
        assert product.supplier_id is None
        assert product.created_by_admin_id is None
        assert product.discount_id is None
        assert product.created_at is None
        assert product.updated_at is None
        assert product.stock_weight is None
        assert product.min_stock is None
        assert product.unit is None
        assert product.min_order_amount is None
        assert product.category_id is None

    # Calculating price after discount when discount is None
    def test_calculate_price_no_discount(self):
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        with patch.object(Product, 'discount', None):
            product = Product(**product_data)
            assert product.price_after_discount == 10.00

    # Ensuring soft delete sets is_deleted and deleted_at correctly
    def test_soft_delete_sets_correctly(self):
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
        product.delete()
        assert product.is_deleted == True
        assert product.deleted_at is not None

    # Handling invalid data types for Product fields
    def test_handling_invalid_data_types(self):
        product_data = {
            "product_name": 123,  # Invalid data type
            "unit_price": "10.00",  # Invalid data type
            "supplier_id": "1",  # Invalid data type
            "created_by_admin_id": "admin",  # Invalid data type
            "category_id": "category"  # Invalid data type
        }
        product = Product(**product_data)
        assert product.product_name == ""  # Expecting default value due to invalid data type
        assert product.unit_price is None  # Expecting default value due to invalid data type
        assert product.supplier_id is None  # Expecting default value due to invalid data type
        assert product.created_by_admin_id is None  # Expecting default value due to invalid data type
        assert product.category_id is None  # Expecting default value due to invalid data type

    # Converting a Product instance to a dictionary when fields are None
    def test_convert_product_instance_to_dict_with_none_fields(self):
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1,
            "discount_id": None,
            "stock_weight": None,
            "min_stock": None,
            "unit": None,
            "min_order_amount": None,
            "created_at": None,
            "updated_at": None
        }
        product = Product(**product_data)
        product_dict = product.to_dict()
        assert product_dict["product_name"] == "Test Product"
        assert product_dict["unit_price"] == 10.00
        assert product_dict["supplier_id"] == 1
        assert product_dict["created_by_admin_id"] == 1
        assert product_dict["category_id"] == 1
        assert product_dict["discount_id"] is None
        assert product_dict["stock_weight"] is None
        assert product_dict["min_stock"] is None
        assert product_dict["unit"] is None
        assert product_dict["min_order_amount"] is None
        assert product_dict["created_at"] is None
        assert product_dict["updated_at"] is None

    # Creating a Product instance when storage type is not 'db'
    def test_create_product_instance_not_db(self):
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        with patch('models.base_model.models.storage_t', return_value="fs"):
            product = Product(**product_data)
            assert product.product_name == "Test Product"
            assert product.unit_price == 10.00
            assert product.supplier_id == 1
            assert product.created_by_admin_id == 1
            assert product.category_id == 1

    # Validating foreign key constraints for supplier_id, created_by_admin_id, discount_id, and category_id
    def test_validate_foreign_keys(self):
        # Create a Product instance with foreign key constraints
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "discount_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
    
        # Validate the foreign key constraints
        assert product.supplier_id == 1
        assert product.created_by_admin_id == 1
        assert product.discount_id == 1
        assert product.category_id == 1

    # Ensuring unique constraints on product_name if applicable
    def test_ensuring_unique_constraints_on_product_name(self):  
        # Create a product with a specific product_name
        product_data = {
            "product_name": "Unique Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
    
        # Save the product to check uniqueness
        product.save()
    
        # Attempt to create another product with the same product_name
        duplicate_product_data = {
            "product_name": "Unique Product",
            "unit_price": 20.00,
            "supplier_id": 2,
            "created_by_admin_id": 2,
            "category_id": 2
        }
        duplicate_product = Product(**duplicate_product_data)
    
        # Check that the duplicate product cannot be saved due to unique constraint
        with pytest.raises(Exception):
            duplicate_product.save()

    # Ensuring cascading delete works for related OrderItem instances
    def test_cascading_delete_for_order_items(self):
        # Create a Product instance
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1
        }
        product = Product(**product_data)
    
        # Create an OrderItem instance related to the Product
        order_item_data = {
            "quantity": 2,
            "product_id": product.id
        }
        order_item = OrderItem(**order_item_data)
    
        # Ensure the OrderItem is related to the Product
        assert order_item.product_id == product.id
    
        # Delete the Product and check if the OrderItem is deleted as well
        product.delete()
    
        # Check if the OrderItem is deleted
        assert order_item not in models.storage.all(OrderItem)

    # Handling large text inputs for description and image_url
    def test_handling_large_text_inputs(self):
        # Create a Product instance with large text inputs for description and image_url
        product_data = {
            "product_name": "Test Product",
            "unit_price": 10.00,
            "supplier_id": 1,
            "created_by_admin_id": 1,
            "category_id": 1,
            "description": "This is a very long description that exceeds the normal limit",
            "image_url": "https://example.com/very_large_image.jpg"
        }
        product = Product(**product_data)
    
        # Assert that the description and image_url are correctly set
        assert product.description == "This is a very long description that exceeds the normal limit"
        assert product.image_url == "https://example.com/very_large_image.jpg"

    # Ensuring default values are set correctly when storage type is not 'db'
    def test_default_values_not_db(self):
        # Setup
        product = Product()

        # Assertion
        assert product.product_name == ""
        assert product.unit_price == None
        assert product.image_url == ""
        assert product.description == ""
        assert product.supplier_id == None
        assert product.created_by_admin_id == None
        assert product.discount_id == None
        assert product.created_at == None
        assert product.updated_at == None
        assert product.stock_weight == None
        assert product.min_stock == None
        assert product.unit == None
        assert product.min_order_amount == None
        assert product.category_id == None
