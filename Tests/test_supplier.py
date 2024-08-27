from models.supplier import Supplier
import models
from unittest.mock import patch
import datetime


import pytest

class TestSupplier:

    # Supplier instance is created with valid attributes
    def test_supplier_creation_with_valid_attributes(self):
        valid_attributes = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            'address': '123 Test St',
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        supplier = Supplier(**valid_attributes)
        for key, value in valid_attributes.items():
            assert getattr(supplier, key) == value

    # Supplier instance is created with missing mandatory attributes
    def test_supplier_creation_with_missing_mandatory_attributes(self):
        invalid_attributes = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            # Missing address
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        with pytest.raises(TypeError):
            supplier = Supplier(**invalid_attributes)

    # Supplier instance is saved to the database correctly
    def test_supplier_instance_saved_to_database_correctly(self, mocker):
        valid_attributes = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            'address': '123 Test St',
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        supplier = Supplier(**valid_attributes)
        with mocker.patch('models.storage.new') as mock_new, \
             mocker.patch('models.storage.save') as mock_save:
            supplier.save()
            mock_new.assert_called_once_with(supplier)
            mock_save.assert_called_once()

    # Supplier instance is converted to dictionary correctly
    def test_supplier_instance_to_dict(self):
        supplier_data = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            'address': '123 Test St',
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        supplier = Supplier(**supplier_data)
        supplier_dict = supplier.to_dict()
        assert supplier_dict['supplier_name'] == supplier_data['supplier_name']
        assert supplier_dict['contact_number'] == supplier_data['contact_number']
        assert supplier_dict['address'] == supplier_data['address']
        assert supplier_dict['created_by_admin_id'] == supplier_data['created_by_admin_id']
        assert supplier_dict['company_name'] == supplier_data['company_name']
        assert supplier_dict['email'] == supplier_data['email']
        assert supplier_dict['notes'] == supplier_data['notes']

    # Supplier instance is soft deleted correctly
    def test_soft_delete_supplier_instance(self, mocker):
        # Setup
        supplier_data = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            'address': '123 Test St',
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        supplier = Supplier(**supplier_data)
    
        # Mocking
        mocker.patch('models.storage_t', return_value='db')
        mocker.patch('models.storage.new')
        mocker.patch('models.storage.save')
    
        # Action
        supplier.delete()
    
        # Assertion
        assert supplier.is_deleted is True
        assert supplier.deleted_at is not None
        models.storage.new.assert_called_once_with(supplier)
        models.storage.save.assert_called_once()

    # Supplier instance relationships with Product and Admin are correctly established
    def test_supplier_instance_relationships(self):
        # Create a mock Product class
        class Product:
            pass

        # Create a mock Admin class
        class Admin:
            pass

        # Mock the models.storage_t value
        models.storage_t = 'db'

        # Mock the models.storage.new and models.storage.save methods
        models.storage.new = lambda x: None
        models.storage.save = lambda: None

        # Create a Supplier instance
        supplier = Supplier()

        # Check if the relationships are correctly established
        assert hasattr(supplier, 'products')
        assert hasattr(supplier, 'admin')

    # Supplier instance string representation is correct
    def test_supplier_instance_string_representation(self):
        supplier = Supplier(supplier_name='Test Supplier', contact_number='1234567890', address='123 Test St',
                            created_by_admin_id=1, company_name='Test Company', email='test@supplier.com',
                            notes='Test notes')
        expected_output = "[Supplier] (None) {'supplier_name': 'Test Supplier', 'contact_number': '1234567890', 'address': '123 Test St', 'created_by_admin_id': 1, 'company_name': 'Test Company', 'email': 'test@supplier.com', 'notes': 'Test notes'}"
        assert str(supplier) == expected_output

    # Supplier instance is created with invalid attribute types
    def test_supplier_creation_with_invalid_attributes(self):
        invalid_attributes = {
            'supplier_name': 123,  # Invalid type
            'contact_number': 1234567890,
            'address': '123 Test St',
            'created_by_admin_id': '1',  # Invalid type
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': ['Test notes']  # Invalid type
        }
        with pytest.raises(Exception):  # Adjust the exception type accordingly
            supplier = Supplier(**invalid_attributes)

    # Supplier instance is created with duplicate email
    def test_supplier_creation_with_duplicate_email(self):
        # Create a Supplier instance with a duplicate email
        valid_attributes = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            'address': '123 Test St',
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        supplier1 = Supplier(**valid_attributes)
        # Create another Supplier instance with the same email
        supplier2 = Supplier(**valid_attributes)
        # Check that the second instance was not created
        assert supplier2 is None

    # Supplier instance is created with special characters in string fields
    def test_supplier_creation_with_special_characters(self):
        special_attributes = {
            'supplier_name': 'Test$Supplier',
            'contact_number': '123-456-7890',
            'address': '123 Test St!',
            'created_by_admin_id': 1,
            'company_name': 'Test#Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes with special characters: !@#$%^&*()_+'
        }
        supplier = Supplier(**special_attributes)
        for key, value in special_attributes.items():
            assert getattr(supplier, key) == value

    # Supplier instance is created with extremely long string values
    def test_supplier_creation_with_extremely_long_strings(self):
        extremely_long_attributes = {
            'supplier_name': 'A' * 300,
            'contact_number': '1' * 100,
            'address': 'A' * 200,
            'company_name': 'B' * 300,
            'email': 'C' * 150,
            'notes': 'D' * 300
        }
        supplier = Supplier(**extremely_long_attributes)
        for key, value in extremely_long_attributes.items():
            assert getattr(supplier, key) == value

    # Supplier instance is created with null values for non-nullable fields
    def test_supplier_instance_created_with_null_values(self):
        supplier = Supplier()
        assert supplier.supplier_name is None
        assert supplier.contact_number is None
        assert supplier.address is None
        assert supplier.created_by_admin_id is None
        assert supplier.company_name is None
        assert supplier.email is None
        assert supplier.notes is None

    # Supplier instance is deleted from the database
    def test_supplier_instance_deleted_from_database(self, mocker):
        supplier_data = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            'address': '123 Test St',
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        supplier = Supplier(**supplier_data)
        with mocker.patch('models.storage_t', return_value='db'):
            supplier.delete()
            assert supplier.is_deleted is True

    # Supplier instance is created without any attributes
    def test_supplier_creation_without_attributes(self):
        supplier = Supplier()
        assert supplier.supplier_name == ""
        assert supplier.contact_number == ""
        assert supplier.address == ""
        assert supplier.created_by_admin_id == None
        assert supplier.company_name == ""
        assert supplier.email == ""
        assert supplier.notes == ""

    # Supplier instance is created in non-database storage mode
    def test_supplier_instance_creation_non_db_mode(self):
        supplier = Supplier()
        assert supplier.supplier_name == ""
        assert supplier.contact_number == ""
        assert supplier.address == ""
        assert supplier.created_by_admin_id is None
        assert supplier.company_name == ""
        assert supplier.email == ""
        assert supplier.notes == ""

    # Supplier instance is updated after creation
    def test_supplier_instance_updated_after_creation(self):
        supplier_data = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            'address': '123 Test St',
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        with patch('models.base_model.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2023, 1, 1)  # Mock datetime.utcnow to a fixed value
            supplier = Supplier(**supplier_data)
            assert supplier.updated_at == datetime(2023, 1, 1)

    # Supplier instance is created with additional unexpected attributes
    def test_supplier_instance_unexpected_attributes(self):
        valid_attributes = {
            'supplier_name': 'Test Supplier',
            'contact_number': '1234567890',
            'address': '123 Test St',
            'created_by_admin_id': 1,
            'company_name': 'Test Company',
            'email': 'test@supplier.com',
            'notes': 'Test notes'
        }
        supplier = Supplier(**valid_attributes)
        expected_keys = ['supplier_name', 'contact_number', 'address', 'created_by_admin_id', 'company_name', 'email', 'notes']
        unexpected_attributes = [attr for attr in supplier.__dict__ if attr not in expected_keys]
        assert not unexpected_attributes, f"Unexpected attributes found: {unexpected_attributes}"
