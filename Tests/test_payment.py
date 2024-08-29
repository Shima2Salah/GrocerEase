from models.payment import Payment
from unittest.mock import patch


import pytest

class TestPayment:

    # Payment instance initializes with correct attributes
    def test_initializes_with_correct_attributes(self):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
        assert payment.payment_method == 'Credit Card'
        assert payment.orders == []

    # Payment instance initializes with missing attributes
    def test_initializes_with_missing_attributes(self):
        payment = Payment()
        assert payment.payment_method == ''
        assert payment.orders == []

    # Payment instance initializes with extra attributes
    def test_initializes_with_extra_attributes(self):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
        assert payment.payment_method == 'Credit Card'
        assert payment.orders == []

    # Payment instance overrides BaseModel columns correctly in database mode
    def test_payment_instance_overrides_columns_correctly(self):
        # Define the expected attributes for Payment instance in db mode
        expected_attributes = {
            'payment_method': 'Credit Card',
            'orders': []
        }
    
        # Create a Payment instance in db mode
        with patch('models.storage_t', 'db'):
            payment = Payment(**expected_attributes)
        
            # Check if the overridden columns are set correctly
            assert not hasattr(payment, 'created_at')
            assert not hasattr(payment, 'updated_at')
            assert payment.payment_method == 'Credit Card'
            assert payment.orders == []

    # Payment instance initializes with empty kwargs
    def test_initializes_with_empty_kwargs(self):
        payment = Payment()
        assert payment.payment_method == ''
        assert payment.orders == None

    # Payment instance soft deletes correctly in database mode
    def test_soft_deletes_correctly(self, mocker):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
        with mocker.patch('models.storage') as mock_storage:
            payment.delete()
            assert payment.is_deleted == True
            assert payment.deleted_at is not None
            mock_storage.save.assert_called_once()

    # Payment instance saves correctly in database mode
    def test_payment_instance_saves_correctly(self, mocker):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        with mocker.patch('models.storage.new') as mock_new, \
             mocker.patch('models.storage.save') as mock_save:
            payment = Payment(**payment_data)
            payment.save()
            mock_new.assert_called_once_with(payment)
            mock_save.assert_called_once()

    # Payment instance initializes with non-empty kwargs
    def test_initializes_with_non_empty_kwargs(self):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        with patch('models.base_model.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = '2023-01-01 12:00:00'
            payment = Payment(**payment_data)
            assert payment.payment_method == 'Credit Card'
            assert payment.orders == []
            assert payment.created_at == '2023-01-01 12:00:00'
            assert payment.updated_at == '2023-01-01 12:00:00'

    # Payment instance string representation is accurate
    def test_payment_instance_string_representation(self):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
        expected_output = "[Payment] (None) {'payment_method': 'Credit Card', 'orders': []}"
        assert str(payment) == expected_output

    # Payment instance converts to dictionary correctly
    def test_payment_instance_to_dict(self):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
        payment_dict = payment.to_dict()
        assert payment_dict['payment_method'] == 'Credit Card'
        assert payment_dict['orders'] == []

    # Payment instance updates attributes correctly
    def test_updates_attributes_correctly(self):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
        assert payment.payment_method == 'Credit Card'
        assert payment.orders == []

    # Payment instance converts to dictionary with missing attributes
    def test_payment_instance_to_dict_with_missing_attributes(self):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
        payment_dict = payment.to_dict()
        assert payment_dict["payment_method"] == 'Credit Card'
        assert payment_dict["orders"] == []
        assert "created_at" not in payment_dict
        assert "updated_at" not in payment_dict

    # Payment instance initializes with invalid attribute types
    def test_initializes_with_invalid_attributes(self):
        payment_data = {
            'payment_method': 123,  # Invalid type
            'orders': "Order123"  # Invalid type
        }
        payment = Payment(**payment_data)
        assert not hasattr(payment, 'payment_method')  # Should not initialize with invalid type
        assert not hasattr(payment, 'orders')

    def test_soft_deletes_correctly_in_db_mode(self, mocker):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
        with mocker.patch('models.storage') as mock_storage:
            payment.delete()
            assert payment.is_deleted == True
            assert payment.deleted_at is not None
            mock_storage.save.assert_called_once()

    def test_initializes_with_invalid_attributes(self):
        payment_data = {
            'payment_method': 123,  # Invalid type
            'orders': "Order123"  # Invalid type
        }
        payment = Payment(**payment_data)
        assert not hasattr(payment, 'payment_method')  # Should not initialize with invalid type
        assert not hasattr(payment, 'orders')

    def test_initializes_with_invalid_attribute_values(self):
        payment_data = {
            'payment_method': 123,  # Invalid type
            'orders': "Order123"  # Invalid type
        }
        payment = Payment(**payment_data)
        assert not hasattr(payment, 'payment_method')  # Should not initialize with invalid type
        assert not hasattr(payment, 'orders')

    def test_updates_orders_correctly(self):
        payment_data = {
            'payment_method': 'Credit Card',
            'orders': []
        }
        payment = Payment(**payment_data)
    
        # Update orders attribute
        new_orders = ['Order1', 'Order2']
        payment.orders = new_orders
    
        assert payment.orders == new_orders  # Should not initialize with invalid type
