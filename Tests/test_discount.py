import time
from unittest.mock import patch
import datetime


import pytest

class TestDiscount:

    # Initialize Discount with valid discount_percentage, start_date, and end_date
    def test_initialize_discount_with_valid_data(self):
        from models.discount import Discount
        from datetime import datetime

        discount_data = {
            'discount_percentage': 15.00,
            'start_date': datetime(2023, 1, 1),
            'end_date': datetime(2023, 12, 31)
        }
        discount = Discount(**discount_data)

        assert discount.discount_percentage == 15.00
        assert discount.start_date == datetime(2023, 1, 1)
        assert discount.end_date == datetime(2023, 12, 31)

    # Initialize Discount with missing discount_percentage
    def test_initialize_discount_with_missing_discount_percentage(self):
        from models.discount import Discount
        from datetime import datetime

        discount_data = {
            'start_date': datetime(2023, 1, 1),
            'end_date': datetime(2023, 12, 31)
        }
        discount = Discount(**discount_data)

        assert discount.discount_percentage == 0.00
        assert discount.start_date == datetime(2023, 1, 1)
        assert discount.end_date == datetime(2023, 12, 31)

    # Save a Discount instance to the database
    def test_save_discount_instance_to_database(self, mocker):
        from models.discount import Discount
        from datetime import datetime

        discount_data = {
            'discount_percentage': 10.00,
            'start_date': datetime(2023, 1, 1),
            'end_date': datetime(2023, 12, 31)
        }
        discount = Discount(**discount_data)
    
        # Mock the storage and save methods
        mocker.patch('models.base_model.models.storage.new')
        mocker.patch('models.base_model.models.storage.save')

        discount.save()

        assert discount.discount_percentage == 10.00
        assert discount.start_date == datetime(2023, 1, 1)
        assert discount.end_date == datetime(2023, 12, 31)

    # Convert a Discount instance to a dictionary
    def test_convert_discount_instance_to_dict(self):
        from models.discount import Discount
        from datetime import datetime

        discount_data = {
            'discount_percentage': 15.00,
            'start_date': datetime(2023, 1, 1),
            'end_date': datetime(2023, 12, 31)
        }
        discount = Discount(**discount_data)

        discount_dict = discount.to_dict()

        assert discount_dict['discount_percentage'] == 15.00
        assert discount_dict['start_date'] == datetime(2023, 1, 1).strftime(time)
        assert discount_dict['end_date'] == datetime(2023, 12, 31).strftime(time)
        assert '__class__' in discount_dict

    # Soft delete a Discount instance
    def test_soft_delete_discount_instance(self, mocker):
        from models.discount import Discount
        from datetime import datetime

        discount_data = {
            'discount_percentage': 20.00,
            'start_date': datetime(2023, 1, 1),
            'end_date': datetime(2023, 12, 31)
        }
        discount = Discount(**discount_data)
        discount.delete()

        assert discount.is_deleted is True
        assert discount.deleted_at is not None

    # Establish relationship between Discount and Product
    def test_establish_relationship_with_product(self):  
        from models.discount import Discount
        from unittest.mock import MagicMock

        # Create a Discount instance
        discount = Discount()

        # Mock the relationship method of Product
        with patch('models.discount.relationship') as mock_relationship:
            discount.products = MagicMock()

            # Assert that the relationship method was called with the correct parameters
            mock_relationship.assert_called_once_with(
                "Product",
                backref="discounts",
                cascade="all, delete, delete-orphan"
            )

    # Check relationship cascade delete for associated Product instances
    def test_relationship_cascade_delete(self):
        from models.discount import Discount
        from unittest.mock import MagicMock

        # Create a Discount instance
        discount = Discount()

        # Create a mock Product instance
        product_mock = MagicMock()
        discount.products.append(product_mock)

        # Check if the product is in the products list
        assert product_mock in discount.products

        # Delete the Discount instance
        discount.delete()

        # Check if the product was deleted along with the Discount instance
        assert product_mock not in discount.products

    # Ensure Discount instance does not have created_at and updated_at fields
    def test_discount_instance_without_timestamp_fields(self):
        from models.discount import Discount

        discount = Discount()

        assert not hasattr(discount, 'created_at')
        assert not hasattr(discount, 'updated_at')

    # Save a Discount instance with missing required fields
    def test_save_discount_missing_fields(self):
        from models.discount import Discount

        discount = Discount()
        with pytest.raises(Exception):
            discount.save()

    # Verify soft delete sets is_deleted and deleted_at fields
    def test_soft_delete_sets_fields(self, mocker):
        from models.discount import Discount
        from datetime import datetime

        discount_data = {
            'discount_percentage': 15.00,
            'start_date': datetime(2023, 1, 1),
            'end_date': datetime(2023, 12, 31)
        }
        discount = Discount(**discount_data)
    
        discount.delete()
    
        assert discount.is_deleted == True
        assert isinstance(discount.deleted_at, datetime)

    # Test Discount initialization without any arguments
    def test_initialize_discount_without_arguments(self):
        from models.discount import Discount
        discount = Discount()
    
        assert discount.discount_percentage == 0.00
        assert discount.start_date == None
        assert discount.end_date == None

    # Validate Discount instance string representation
    def test_validate_discount_instance_string_representation(self):
        from models.discount import Discount

        discount_data = {
            'discount_percentage': 15.00,
            'start_date': datetime(2023, 1, 1),
            'end_date': datetime(2023, 12, 31)
        }
        discount = Discount(**discount_data)

        expected_string = "[Discount] (None) {'discount_percentage': 15.00, 'start_date': datetime.datetime(2023, 1, 1), 'end_date': datetime.datetime(2023, 12, 31), 'products': []}"
        assert str(discount) == expected_string

    # Initialize Discount with invalid date formats
    def test_initialize_discount_with_invalid_date_formats(self):  
        from models.discount import Discount
        from datetime import datetime
        from pytest import raises

        invalid_discount_data = {
            'discount_percentage': 15.00,
            'start_date': 'invalid_date_format',
            'end_date': 'another_invalid_format'
        }

        with raises(Exception):
            discount = Discount(**invalid_discount_data)

    # Initialize Discount with negative discount_percentage
    def test_initialize_discount_with_negative_discount_percentage(self):
        from models.discount import Discount

        discount_data = {
            'discount_percentage': -10.00,
            'start_date': None,
            'end_date': None
        }
        discount = Discount(**discount_data)

        assert discount.discount_percentage == -10.00
        assert discount.start_date == None
        assert discount.end_date == None

    # Initialize Discount with future start_date and past end_date
    def test_initialize_discount_with_future_start_and_past_end(self):
        from models.discount import Discount
        from datetime import datetime

        discount_data = {
            'discount_percentage': 10.00,
            'start_date': datetime(2023, 1, 1),
            'end_date': datetime(2022, 12, 31)
        }
        discount = Discount(**discount_data)

        assert discount.discount_percentage == 10.00
        assert discount.start_date == datetime(2023, 1, 1)
        assert discount.end_date == datetime(2022, 12, 31)
