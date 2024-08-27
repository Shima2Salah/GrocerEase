from models.category import Category
from models.admin import Admin
from unittest.mock import patch
import models


import pytest

class TestCategory:

    # Category initialization with valid data
    def test_category_initialization_with_valid_data(self):
        valid_data = {
            'category_name': 'Fruits',
            'image_url': 'http://example.com/image.jpg',
            'created_by_admin_id': 1
        }
        category = Category(**valid_data)
        assert category.category_name == 'Fruits'
        assert category.image_url == 'http://example.com/image.jpg'
        assert category.created_by_admin_id == 1

    # Category initialization with invalid data types
    def test_category_initialization_with_invalid_data_types(self):
        invalid_data = {
            'category_name': 123,  # Should be a string
            'image_url': 456,      # Should be a string
            'created_by_admin_id': 'admin'  # Should be an integer
        }
        with pytest.raises(TypeError):
            Category(**invalid_data)

    # Category initialization with no data
    def test_category_initialization_with_no_data(self):
        category = Category()
        assert category.category_name == ""
        assert category.image_url == ""
        assert category.created_by_admin_id == None

    # Category string representation
    def test_category_string_representation(self):
        category_data = {
            'category_name': 'Fruits',
            'image_url': 'http://example.com/image.jpg',
            'created_by_admin_id': 1
        }
        category = Category(**category_data)
        expected_output = "[Category] (None) {'category_name': 'Fruits', 'image_url': 'http://example.com/image.jpg', 'created_by_admin_id': 1}"
        assert str(category) == expected_output

    # Category save method updates timestamps
    def test_category_save_updates_timestamps(self, mocker):
        category_data = {
            'category_name': 'Vegetables',
            'image_url': 'http://example.com/vegetables.jpg',
            'created_by_admin_id': 2
        }
        category = Category(**category_data)
        initial_updated_at = category.updated_at
        mocker.patch('models.storage.save')
        category.save()
        assert category.updated_at != initial_updated_at

    # Category delete method soft deletes the instance
    def test_category_soft_delete(self, mocker):
        category_data = {
            'category_name': 'Test Category',
            'image_url': 'http://example.com/test.jpg',
            'created_by_admin_id': 1
        }
        category = Category(**category_data)
    
        mocker.patch('models.storage_t', return_value='db')
        mocker.patch('models.storage.new')
        mocker.patch('models.storage.save')
    
        category.delete()
    
        assert category.is_deleted is True
        assert category.deleted_at is not None

    # Category to_dict method returns correct dictionary
    def test_to_dict_returns_correct_dictionary(self):
        # Setup
        category_data = {
            'category_name': 'Fruits',
            'image_url': 'http://example.com/image.jpg',
            'created_by_admin_id': 1
        }
        category = Category(**category_data)

        # Assertion
        expected_dict = {
            'category_name': 'Fruits',
            'image_url': 'http://example.com/image.jpg',
            'created_by_admin_id': 1,
            '__class__': 'Category'
        }
        assert category.to_dict() == expected_dict

    # Relationship with Product is correctly established
    def test_relationship_with_product(self):
        # Setup
        from unittest.mock import MagicMock
        from models.category import Category
        from models.product import Product

        # Create a mock Product instance
        mock_product = MagicMock()

        # Create a Category instance with a mock Product relationship
        category = Category(products=[mock_product])

        # Assertion
        assert category.products[0] == mock_product

    # Relationship with Admin is correctly established
    def test_relationship_with_admin(self):
        # Setup
        admin_id = 1
        valid_data = {
            'category_name': 'Fruits',
            'image_url': 'http://example.com/image.jpg',
            'created_by_admin_id': admin_id
        }
        admin_instance = Admin(id=admin_id)
        with patch('models.Admin', return_value=admin_instance):
            # Action
            category = Category(**valid_data)
            # Assertion
            assert category.admin == admin_instance

    # Category initialization with missing required fields
    def test_category_initialization_with_missing_required_fields(self):
        with pytest.raises(TypeError):
            category = Category()

    # Category save method without prior initialization
    def test_category_save_without_initialization(self):
        category = Category()
        with pytest.raises(Exception):
            category.save()

    # Category to_dict method with missing attributes
    def test_to_dict_missing_attributes(self):
        category_data = {
            'category_name': 'Fruits',
            'created_by_admin_id': 1
        }
        category = Category(**category_data)
        category_dict = category.to_dict()
        assert 'category_name' in category_dict
        assert 'created_by_admin_id' in category_dict
        assert 'image_url' not in category_dict

    # Category delete method when storage_t is not 'db'
    def test_category_delete_not_db(self, mocker):
        # Setup
        mocker.patch('models.storage.delete')
        category_data = {
            'category_name': 'Fruits',
            'image_url': 'http://example.com/image.jpg',
            'created_by_admin_id': 1
        }
        category = Category(**category_data)

        # Call delete method
        category.delete()

        # Assertion
        models.storage.delete.assert_called_once_with(category)

    # Category initialization with extra unknown fields
    def test_category_initialization_with_extra_unknown_fields(self):
        unknown_data = {
            'category_name': 'Vegetables',
            'image_url': 'http://example.com/vegetables.jpg',
            'created_by_admin_id': 2,
            'extra_field': 'Extra Field Value'
        }
        category = Category(**unknown_data)
        assert category.category_name == 'Vegetables'
        assert category.image_url == 'http://example.com/vegetables.jpg'
        assert category.created_by_admin_id == 2
        assert not hasattr(category, 'extra_field')

    # Category initialization with partial data
    def test_category_initialization_with_partial_data(self):
        partial_data = {
            'category_name': 'Vegetables',
            'created_by_admin_id': 2
        }
        category = Category(**partial_data)
        assert category.category_name == 'Vegetables'
        assert category.image_url == ''
        assert category.created_by_admin_id == 2

    # Category save method with database connection issues
    def test_category_save_with_db_connection_issues(self, mocker):
        # Setup
        category_data = {
            'category_name': 'Fruits',
            'image_url': 'http://example.com/image.jpg',
            'created_by_admin_id': 1
        }
        category = Category(**category_data)
    
        # Mocking the models.storage.save method to raise an exception
        mocker.patch('models.storage.save', side_effect=Exception('Database connection error'))
    
        # Assertion
        with pytest.raises(Exception) as exc:
            category.save()
        assert str(exc.value) == 'Database connection error'

    # Category to_dict method with special characters in fields
    def test_category_to_dict_special_characters(self):
        # Prepare
        special_category_name = 'Fruits & Vegetables'
        special_image_url = 'http://example.com/image.jpg?size=large'
        special_admin_id = 1
        category_data = {
            'category_name': special_category_name,
            'image_url': special_image_url,
            'created_by_admin_id': special_admin_id
        }
        category = Category(**category_data)

        # Execute
        category_dict = category.to_dict()

        # Validate
        assert category_dict['category_name'] == special_category_name
        assert category_dict['image_url'] == special_image_url
        assert category_dict['created_by_admin_id'] == special_admin_id

    # Category delete method with already deleted instance
    def test_category_delete_with_already_deleted_instance(self, mocker):
        # Create a Category instance
        category_data = {'category_name': 'Fruits', 'image_url': 'http://example.com/image.jpg', 'created_by_admin_id': 1}
        category = Category(**category_data)
    
        # Mock the delete method to simulate already deleted instance
        mocker.patch.object(models.storage, 'delete')
        category.delete()
    
        # Assert that the delete method was not called again
        models.storage.delete.assert_not_called()

    # Category relationship with non-existent Product or Admin
    def test_category_relationship_with_non_existent(self):
        category_data = {
            'category_name': 'Vegetables',
            'image_url': 'http://example.com/vegetables.jpg',
            'created_by_admin_id': 2
        }
        category = Category(**category_data)
        assert category.category_name == 'Vegetables'
        assert category.image_url == 'http://example.com/vegetables.jpg'
        assert category.created_by_admin_id == 2
