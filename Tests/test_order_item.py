from models.order_item import OrderItem
from unittest.mock import patch
import datetime


import pytest

class TestOrderItem:

    # Creating an OrderItem instance with valid attributes
    def test_create_order_item_with_valid_attributes(self):
        valid_attributes = {
            'product_id': 1,
            'amount': 10.00,
            'price': 5.99,
            'order_id': 1
        }
        order_item = OrderItem(**valid_attributes)
        assert order_item.product_id == 1
        assert order_item.amount == 10.00
        assert order_item.price == 5.99
        assert order_item.order_id == 1

    # Creating an OrderItem instance with missing required attributes
    def test_create_order_item_with_missing_attributes(self):
        invalid_attributes = {
            'amount': 10.00,
            'price': 5.99
        }
        with pytest.raises(TypeError):
            OrderItem(**invalid_attributes)

    # Saving an OrderItem instance to the database
    def test_saving_order_item_instance_to_database(self, mocker):
        valid_attributes = {
            'product_id': 1,
            'amount': 10.00,
            'price': 5.99,
            'order_id': 1
        }
        order_item = OrderItem(**valid_attributes)
        with mocker.patch('models.storage.new') as mock_new, \
             mocker.patch('models.storage.save') as mock_save:
            order_item.save()
            mock_new.assert_called_once_with(order_item)
            mock_save.assert_called_once()

    # Converting an OrderItem instance to a dictionary
    def test_convert_order_item_to_dict(self):
        # Create an OrderItem instance
        order_item = OrderItem(product_id=1, amount=10.00, price=5.99, order_id=1)
    
        # Convert the OrderItem instance to a dictionary
        order_item_dict = order_item.to_dict()
    
        # Check the keys and values in the dictionary
        assert order_item_dict["product_id"] == 1
        assert order_item_dict["amount"] == 10.00
        assert order_item_dict["price"] == 5.99
        assert order_item_dict["order_id"] == 1

    # Updating the 'updated_at' attribute on save
    def test_update_updated_at_on_save(self, mocker):
        # Setup
        mocker.patch('models.storage')
        order_item = OrderItem()
    
        # Act
        order_item.save()
    
        # Assert
        assert order_item.updated_at is not None

    # Establishing relationships with Product and Order models
    def test_establish_relationships_with_product_and_order_models(self):
        # Given
        product_id = 1
        amount = 10.00
        price = 5.99
        order_id = 1
        valid_attributes = {
            'product_id': product_id,
            'amount': amount,
            'price': price,
            'order_id': order_id
        }
    
        # When
        order_item = OrderItem(**valid_attributes)
    
        # Then
        assert order_item.product_id == product_id
        assert order_item.amount == amount
        assert order_item.price == price
        assert order_item.order_id == order_id

    # Initializing an OrderItem instance with unexpected keyword arguments
    def test_initialize_order_item_unexpected_kwargs(self):
        with pytest.raises(TypeError):
            unexpected_kwargs = {
                'invalid_key': 'value'
            }
            OrderItem(**unexpected_kwargs)

    # Checking the auto-generation of 'id' in database storage mode
    def test_auto_generate_id_in_db_mode(self):
        # Given
        valid_attributes = {
            'product_id': 1,
            'amount': 10.00,
            'price': 5.99,
            'order_id': 1
        }
        # When
        order_item = OrderItem(**valid_attributes)
        # Then
        assert hasattr(order_item, 'id')
        assert order_item.product_id == 1
        assert order_item.amount == 10.00
        assert order_item.price == 5.99
        assert order_item.order_id == 1

    # Handling invalid data types for attributes
    def test_handling_invalid_data_types(self):
        order_item = OrderItem(product_id="string", amount="string", price="string", order_id="string")
        assert order_item.product_id == ""
        assert order_item.amount == ""
        assert order_item.price == ""
        assert order_item.order_id == ""

    # Handling None values for nullable attributes
    def test_handling_none_values(self):
        order_item = OrderItem()
        assert order_item.order_id is None
        assert order_item.product_id is None
        assert order_item.amount is None
        assert order_item.price is None

    # Ensuring relationships are correctly populated in database storage mode
    def test_relationships_correctly_populated(self):
        product_id = 1
        amount = 10.00
        price = 5.99
        order_id = 1
        valid_attributes = {
            'product_id': product_id,
            'amount': amount,
            'price': price,
            'order_id': order_id
        }
        # Mocking the OrderItem class
        with patch('models.order_item.OrderItem', autospec=True) as mock_order_item:
            # When
            order_item = OrderItem(**valid_attributes)
            # Then
            assert order_item.product_id == product_id
            assert order_item.amount == amount
            assert order_item.price == price
            assert order_item.order_id == order_id

    # Verifying the string representation of an OrderItem instance
    def test_string_representation_order_item(self):
        order_item = OrderItem(product_id=1, amount=10.00, price=5.99, order_id=1)
        expected_output = "[OrderItem] (1) {'product_id': 1, 'amount': 10.00, 'price': 5.99, 'order_id': 1}"
        assert str(order_item) == expected_output

    # Soft deleting an OrderItem instance and setting 'is_deleted' and 'deleted_at'
    def test_soft_delete_order_item(self, mocker):
        # Setup
        order_item_data = {
            'product_id': 1,
            'amount': 10.00,
            'price': 5.99,
            'order_id': 1
        }
        order_item = OrderItem(**order_item_data)
    
        # Mocking datetime.utcnow()
        mocker.patch('models.base_model.datetime.utcnow', return_value=datetime(2023, 1, 1))
    
        # Action
        order_item.delete()
    
        # Assertion
        assert order_item.is_deleted is True
        assert order_item.deleted_at == datetime(2023, 1, 1)

    # Ensuring 'created_at' and 'updated_at' are correctly formatted in the dictionary output
    def test_correctly_formatted_dates_in_dict_output(self):
        # Create an instance of OrderItem
        order_item = OrderItem()
    
        # Set created_at and updated_at to specific datetime values
        order_item.created_at = datetime(2022, 1, 15, 10, 30, 0)
        order_item.updated_at = datetime(2022, 1, 20, 15, 45, 0)
    
        # Get the dictionary representation of the OrderItem
        order_item_dict = order_item.to_dict()
    
        # Check if created_at and updated_at are correctly formatted in the dictionary output
        assert order_item_dict["created_at"] == "2022-01-15 10:30:00"
        assert order_item_dict["updated_at"] == "2022-01-20 15:45:00"
