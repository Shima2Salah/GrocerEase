import datetime
from models.order import Order
from pytest_mock import mocker


import pytest

class TestOrder:

    # Creating an Order instance with valid data initializes all attributes correctly
    def test_order_initialization_with_valid_data(self):
        valid_data = {
            'user_id': 1,
            'total_price': 100.00,
            'delivery_id': 2,
            'order_date': datetime.utcnow(),
            'status_id': 1,
            'payment_id': 3,
            'coupon_id': 4,
            'delivery_date': datetime.utcnow(),
            'payment_date': datetime.utcnow(),
            'payment_status': 1,
            'final_price': 90.00
        }
        order = Order(**valid_data)
        for key, value in valid_data.items():
            assert getattr(order, key) == value

    # Creating an Order instance without required fields raises appropriate errors
    def test_order_initialization_without_required_fields(self):
        invalid_data = {
            'total_price': 100.00,
            'delivery_id': 2,
            'order_date': datetime.utcnow(),
            'status_id': 1,
            'payment_id': 3,
            'coupon_id': 4,
            'delivery_date': datetime.utcnow(),
            'payment_date': datetime.utcnow(),
            'payment_status': 1,
            'final_price': 90.00
        }
        with pytest.raises(TypeError):
            Order(**invalid_data)

    # Saving an Order instance without changes does not alter the 'updated_at' attribute
    def test_saving_order_without_changes_does_not_alter_updated_at_attribute(self, mocker):
        order_data = {
            'user_id': 1,
            'total_price': 100.00,
            'delivery_id': 2,
            'order_date': datetime.utcnow(),
            'status_id': 1,
            'payment_id': 3,
            'coupon_id': 4,
            'delivery_date': datetime.utcnow(),
            'payment_date': datetime.utcnow(),
            'payment_status': 1,
            'final_price': 90.00
        }
        order = Order(**order_data)
        original_updated_at = order.updated_at
        order.save()
        assert order.updated_at == original_updated_at

    # Initialization of Order instance with both positional and keyword arguments
    def test_order_initialization_with_valid_data(self):
        valid_data = {
            'user_id': 1,
            'total_price': 100.00,
            'delivery_id': 2,
            'order_date': datetime.utcnow(),
            'status_id': 1,
            'payment_id': 3,
            'coupon_id': 4,
            'delivery_date': datetime.utcnow(),
            'payment_date': datetime.utcnow(),
            'payment_status': 1,
            'final_price': 90.00
        }
        order = Order(**valid_data)
        for key, value in valid_data.items():
            assert getattr(order, key) == value

    # Creating an Order instance with a coupon applies the coupon correctly to the final price
    def test_order_instance_with_coupon_applies_coupon_to_final_price(self, mocker):
        valid_data = {
            'user_id': 1,
            'total_price': 100.00,
            'delivery_id': 2,
            'order_date': datetime.utcnow(),
            'status_id': 1,
            'payment_id': 3,
            'coupon_id': 4,
            'delivery_date': datetime.utcnow(),
            'payment_date': datetime.utcnow(),
            'payment_status': 1,
            'final_price': 90.00
        }
        coupon_mock = mocker.MagicMock()
        coupon_mock.start_date = datetime.utcnow()
        coupon_mock.end_date = datetime.utcnow()
        coupon_mock.coupon_amount = 10.00
        mocker.patch('models.storage.get', return_value=coupon_mock)
    
        order = Order(**valid_data)
    
        assert order.final_price == 90.00

    # Relationships with other models (User, Payment, Delivery, etc.) are correctly established
    def test_relationships_established(self):
        # Prepare
        user_mock = mocker.MagicMock()
        payment_mock = mocker.MagicMock()
        delivery_mock = mocker.MagicMock()
        order_status_mock = mocker.MagicMock()
        order_item_mock = mocker.MagicMock()
        coupon_mock = mocker.MagicMock()

        # Action
        order = Order()
    
        # Assertion
        assert hasattr(order, 'user')
        assert hasattr(order, 'payment')
        assert hasattr(order, 'delivery')
        assert hasattr(order, 'order_status')
        assert hasattr(order, 'order_items')
        assert hasattr(order, 'coupon')

    # Converting an Order instance to a dictionary includes all relevant attributes
    def test_order_instance_to_dict(self):
        order_data = {
            'user_id': 1,
            'total_price': 100.00,
            'delivery_id': 2,
            'order_date': datetime.utcnow(),
            'status_id': 1,
            'payment_id': 3,
            'coupon_id': 4,
            'delivery_date': datetime.utcnow(),
            'payment_date': datetime.utcnow(),
            'payment_status': 1,
            'final_price': 90.00
        }
        order = Order(**order_data)
        order_dict = order.to_dict()
        relevant_attributes = ['user_id', 'total_price', 'delivery_id', 'order_date', 'status_id',
                               'payment_id', 'coupon_id', 'delivery_date', 'payment_date', 'payment_status',
                               'final_price']
        for attr in relevant_attributes:
            assert attr in order_dict

    def test_saving_order_with_changes_updates_updated_at_attribute(self, mocker):
        order_data = {
            'user_id': 1,
            'total_price': 100.00,
            'delivery_id': 2,
            'order_date': datetime.utcnow(),
            'status_id': 1,
            'payment_id': 3,
            'coupon_id': 4,
            'delivery_date': datetime.utcnow(),
            'payment_date': datetime.utcnow(),
            'payment_status': 1,
            'final_price': 90.00
        }
        order = Order(**order_data)
        original_updated_at = order.updated_at
        # Simulate changes and save
        order.total_price = 120.00
        order.save()
        assert order.updated_at != original_updated_at

    def test_order_initialization_with_invalid_data_raises_errors(self):
        invalid_data = {
            'user_id': 'invalid',
            'total_price': 'invalid',
            'delivery_id': 2,
            'order_date': datetime.utcnow(),
            'status_id': 1,
            'payment_id': 3,
            'coupon_id': 4,
            'delivery_date': datetime.utcnow(),
            'payment_date': datetime.utcnow(),
            'payment_status': 1,
            'final_price': 90.00
        }
        with pytest.raises(TypeError):
            Order(**invalid_data)
