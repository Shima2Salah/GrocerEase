from models.delivery import Delivery
import models
from models.order import Order
from unittest.mock import patch


import pytest

class TestDelivery:

    # Delivery instance is created with all required attributes
    def test_delivery_creation_with_all_attributes(self):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        assert delivery.delivery_name == "Test Delivery"
        assert delivery.contact_number == "1234567890"
        assert delivery.address == "123 Test St"
        assert delivery.is_active == 1

    # Delivery instance is initialized with missing required attributes
    def test_delivery_creation_with_missing_attributes(self):
        with pytest.raises(TypeError):
            Delivery()

    # Delivery instance is correctly initialized with default values when no arguments are provided
    def test_delivery_default_initialization(self):
        delivery = Delivery()
        assert delivery.delivery_name == ""
        assert delivery.contact_number == ""
        assert delivery.address == ""
        assert delivery.is_active == 1

    # Delivery instance is correctly initialized with provided keyword arguments
    def test_delivery_instance_initialized_correctly(self):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        assert delivery.delivery_name == "Test Delivery"
        assert delivery.contact_number == "1234567890"
        assert delivery.address == "123 Test St"
        assert delivery.is_active == 1

    # Delivery instance can be converted to a dictionary representation
    def test_delivery_to_dict(self):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        delivery_dict = delivery.to_dict()
        assert delivery_dict["delivery_name"] == "Test Delivery"
        assert delivery_dict["contact_number"] == "1234567890"
        assert delivery_dict["address"] == "123 Test St"
        assert delivery_dict["is_active"] == 1

    # Delivery instance can be saved to the database
    def test_delivery_instance_saved_to_database(self, mocker):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        mocker.patch('models.storage.new')
        mocker.patch('models.storage.save')
    
        delivery.save()
    
        assert models.storage.new.called
        assert models.storage.save.called

    # Delivery instance can be soft deleted
    def test_soft_delete_delivery_instance(self):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        delivery.delete()
        assert delivery.is_deleted is True
        assert delivery.deleted_at is not None

    # Delivery instance is initialized with invalid data types for attributes
    def test_invalid_data_types_initialization(self):
        with pytest.raises(Exception):
            Delivery(delivery_name=123, contact_number=456, address=789, is_active="active")

    # Delivery instance is initialized with null values for non-nullable fields
    def test_delivery_instance_initialized_with_null_values(self):
        delivery = Delivery()
        assert delivery.delivery_name is None
        assert delivery.contact_number is None
        assert delivery.address is None
        assert delivery.is_active is None

    # Delivery instance is initialized with empty strings for required string fields
    def test_delivery_instance_initialized_with_empty_strings(self):
        delivery = Delivery()
        assert delivery.delivery_name == ""
        assert delivery.contact_number == ""
        assert delivery.address == ""

    # Delivery instance is initialized with extra attributes not defined in the model
    def test_delivery_extra_attributes_initialization(self):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1, extra_attr="Extra")
        assert hasattr(delivery, 'extra_attr')

    # Delivery instance string representation is correctly formatted
    def test_delivery_instance_string_representation(self):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        expected_output = "[Delivery] (None) {'delivery_name': 'Test Delivery', 'contact_number': '1234567890', 'address': '123 Test St', 'is_active': 1}"
        assert str(delivery) == expected_output

    # Delivery instance updates the 'updated_at' field on save
    def test_delivery_updates_updated_at_on_save(self, mocker):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        updated_at_before = delivery.updated_at
        with mocker.patch('models.base_model.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = '2023-09-15 14:30:00'
            delivery.save()
            assert delivery.updated_at == '2023-09-15 14:30:00'
            assert delivery.updated_at != updated_at_before

    # Delivery instance maintains relationships with Order instances
    def test_delivery_relationship_with_orders(self):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        order = Order(order_number="12345")
        delivery.orders.append(order)
        assert order in delivery.orders

    # Delivery instance handles database-specific and non-database-specific storage modes
    def test_delivery_storage_modes(self):
        # Test database-specific storage mode
        with patch('models.storage_t', 'db'):
            delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
            assert delivery.delivery_name == "Test Delivery"
            assert delivery.contact_number == "1234567890"
            assert delivery.address == "123 Test St"
            assert delivery.is_active == 1

        # Test non-database-specific storage mode
        with patch('models.storage_t', 'fs'):
            delivery = Delivery()
            assert delivery.delivery_name == ""
            assert delivery.contact_number == ""
            assert delivery.address == ""
            assert delivery.is_active == 1

    # Delivery instance handles soft delete correctly by setting 'is_deleted' and 'deleted_at'
    def test_soft_delete_handling(self):
        delivery = Delivery(delivery_name="Test Delivery", contact_number="1234567890", address="123 Test St", is_active=1)
        delivery.delete()
        assert delivery.is_deleted == True
        assert delivery.deleted_at is not None
