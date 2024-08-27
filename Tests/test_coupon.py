import datetime
from models.coupon import Coupon
from unittest.mock import patch
from models.order import Order
import time
from MySQLdb import IntegrityError
import models


import pytest

class TestCoupon:

    # Coupon instance creation with valid data
    def test_coupon_creation_with_valid_data(self):
        valid_data = {
            "coupon_code": "SAVE20",
            "coupon_amount": 20.00,
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31)
        }
        coupon = Coupon(**valid_data)
        assert coupon.coupon_code == "SAVE20"
        assert coupon.coupon_amount == 20.00
        assert coupon.start_date == datetime(2023, 1, 1)
        assert coupon.end_date == datetime(2023, 12, 31)

    # Coupon instance creation with missing required fields
    def test_coupon_creation_with_missing_fields(self):
        invalid_data = {
            "coupon_code": "SAVE20",
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31)
        }
        with pytest.raises(TypeError):
            Coupon(**invalid_data)

    # Coupon instance string representation
    def test_coupon_instance_string_representation(self):
        coupon_data = {
            "coupon_code": "SAVE20",
            "coupon_amount": 20.00,
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31)
        }
        coupon = Coupon(**coupon_data)
        expected_str = "[Coupon] (None) {'coupon_code': 'SAVE20', 'coupon_amount': Decimal('20.00'), 'start_date': datetime.datetime(2023, 1, 1, 0, 0), 'end_date': datetime.datetime(2023, 12, 31, 0, 0), 'orders': [], 'created_at': None, 'updated_at': None}"
        assert str(coupon) == expected_str

    # Coupon instance save operation
    def test_coupon_instance_save_operation(self):
        coupon_data = {
            "coupon_code": "SAVEMORE",
            "coupon_amount": 15.50,
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31)
        }
        coupon = Coupon(**coupon_data)
        with patch('models.storage') as mock_storage:
            coupon.save()
            mock_storage.new.assert_called_once_with(coupon)
            mock_storage.save.assert_called_once()

    # Coupon instance creation with default values
    def test_coupon_instance_creation_with_default_values(self):
        coupon = Coupon()
        assert coupon.coupon_code == ""
        assert coupon.coupon_amount == 0.00
        assert coupon.start_date == None
        assert coupon.end_date == None

    # Coupon instance relationship with Order
    def test_coupon_instance_relationship_with_order(self):
        # Given
        order = Order()
        coupon = Coupon()
    
        # When
        coupon.orders.append(order)
    
        # Then
        assert order in coupon.orders

    # Coupon instance dictionary conversion
    def test_coupon_instance_dictionary_conversion(self):
        coupon_data = {
            "coupon_code": "SALE50",
            "coupon_amount": 50.00,
            "start_date": datetime(2023, 6, 1),
            "end_date": datetime(2023, 6, 30)
        }
        coupon = Coupon(**coupon_data)
        coupon_dict = coupon.to_dict()
        assert coupon_dict["coupon_code"] == "SALE50"
        assert coupon_dict["coupon_amount"] == 50.00
        assert coupon_dict["start_date"] == datetime(2023, 6, 1).strftime(time)
        assert coupon_dict["end_date"] == datetime(2023, 6, 30).strftime(time)

    # Coupon instance soft delete operation
    def test_soft_delete_coupon_instance(self, mocker):
        coupon_data = {
            "coupon_code": "SALE50",
            "coupon_amount": 50.00,
            "start_date": datetime(2023, 6, 1),
            "end_date": datetime(2023, 6, 30)
        }
        coupon = Coupon(**coupon_data)
        coupon.delete()
        assert coupon.is_deleted is True
        assert coupon.deleted_at is not None

    # Coupon instance creation with invalid data types
    def test_coupon_creation_with_invalid_data_types(self):
        invalid_data = {
            "coupon_code": 123,  # Invalid data type for coupon_code
            "coupon_amount": "50.00",  # Invalid data type for coupon_amount
            "start_date": "2023-01-01",  # Invalid data type for start_date
            "end_date": "2023-12-31"  # Invalid data type for end_date
        }
        with pytest.raises(Exception):  # Assuming an Exception is raised for invalid data types
            coupon = Coupon(**invalid_data)

    # Coupon instance creation with duplicate coupon_code
    def test_coupon_creation_with_duplicate_coupon_code(self):  
        # Create a coupon with a specific coupon_code
        coupon_data = {
            "coupon_code": "SALE50",
            "coupon_amount": 50.00,
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31)
        }
        coupon1 = Coupon(**coupon_data)
    
        # Attempt to create another coupon with the same coupon_code
        with pytest.raises(IntegrityError):
            coupon2 = Coupon(**coupon_data)

    # Coupon instance save operation when storage type is not 'db'
    def test_coupon_save_operation_not_db(self, mocker):
        # Setup
        coupon_data = {
            "coupon_code": "SALE50",
            "coupon_amount": 50.00,
            "start_date": datetime(2023, 6, 1),
            "end_date": datetime(2023, 6, 30)
        }
        coupon = Coupon(**coupon_data)
    
        # Mocking
        mocker.patch('models.storage.save')
        mocker.patch('models.storage.new')
    
        # Call
        coupon.save()
    
        # Assertion
        models.storage.new.assert_called_once_with(coupon)
        models.storage.save.assert_called_once()

    # Coupon instance soft delete operation when storage type is not 'db'
    def test_soft_delete_operation_when_storage_not_db(self, mocker):
        # Setup
        coupon_data = {
            "coupon_code": "SALE50",
            "coupon_amount": 50.00,
            "start_date": datetime(2023, 6, 1),
            "end_date": datetime(2023, 6, 30)
        }
        coupon = Coupon(**coupon_data)
    
        # Mocking
        mocker.patch('models.storage.delete')
    
        # Call
        coupon.delete()
    
        # Assertion
        models.storage.delete.assert_called_once_with(coupon)

    # Coupon instance initialization with extra kwargs
    def test_coupon_initialization_with_extra_kwargs(self):
        extra_kwargs = {
            "coupon_code": "SUMMER25",
            "coupon_amount": 25.00,
            "start_date": datetime(2023, 6, 1),
            "end_date": datetime(2023, 8, 31)
        }
        coupon = Coupon(**extra_kwargs)
        assert coupon.coupon_code == "SUMMER25"
        assert coupon.coupon_amount == 25.00
        assert coupon.start_date == datetime(2023, 6, 1)
        assert coupon.end_date == datetime(2023, 8, 31)

    # Coupon instance dictionary conversion excluding password
    def test_coupon_instance_dict_conversion_excluding_password(self):
        coupon_data = {
            "coupon_code": "SAVE10",
            "coupon_amount": 10.00,
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31)
        }
        coupon = Coupon(**coupon_data)
        coupon_dict = coupon.to_dict()
        assert "password" not in coupon_dict

    # Coupon instance save operation updates updated_at field
    def test_coupon_instance_save_updates_updated_at(self, mocker):
        coupon_data = {
            "coupon_code": "SALE50",
            "coupon_amount": 50.00,
            "start_date": datetime(2023, 6, 1),
            "end_date": datetime(2023, 6, 30)
        }
        coupon = Coupon(**coupon_data)
        initial_updated_at = coupon.updated_at
        with mocker.patch('models.storage.save') as mock_save:
            coupon.save()
            assert coupon.updated_at != initial_updated_at
            mock_save.assert_called_once()

    # Coupon instance soft delete sets is_deleted and deleted_at
    def test_soft_delete_sets_is_deleted_and_deleted_at(self):  
        # Create a Coupon instance
        coupon = Coupon()
    
        # Mock the models.storage_t value
        with patch('models.storage_t', 'db'):
            # Call the delete method to soft delete the instance
            coupon.delete()
        
            # Check if is_deleted is set to True
            assert coupon.is_deleted == True
        
            # Check if deleted_at is set to a datetime value
            assert isinstance(coupon.deleted_at, datetime)

    # Coupon instance relationship cascade delete
    def test_coupon_instance_relationship_cascade_delete(self):
        with patch('models.storage') as mock_storage:
            coupon_data = {
                "coupon_code": "SALE50",
                "coupon_amount": 50.00,
                "start_date": datetime(2023, 6, 1),
                "end_date": datetime(2023, 6, 30)
            }
            coupon = Coupon(**coupon_data)
            order_data = {
                # Define order data
            }
            order = Order(**order_data)
            coupon.orders.append(order)
            coupon.delete()
            assert coupon.is_deleted is True
            assert coupon.deleted_at is not None
            mock_storage.save.assert_called_once()
