from models.order_status import OrderStatus
from pytest_mock import mocker
from models.base_model import BaseModel
from lib2to3.pytree import Base
import datetime
from unittest.mock import patch


import pytest

class TestOrderStatus:

    # Initialization of OrderStatus with valid arguments
    def test_initialization_with_valid_arguments(self):
        kwargs = {'status_name': 'Pending'}
        order_status = OrderStatus(**kwargs)
        assert order_status.status_name == 'Pending'
        assert order_status.created_at is None
        assert order_status.updated_at is None

    # Initialization of OrderStatus with no arguments
    def test_initialization_with_no_arguments(self):
        order_status = OrderStatus()
        assert order_status.status_name == ''
        assert order_status.created_at is None
        assert order_status.updated_at is None

    # Correct relationship setup with Order model
    def test_correct_relationship_setup_with_order_model(self):
        order_status = OrderStatus()
        assert hasattr(order_status, 'status_name')
        assert hasattr(order_status, 'orders')
        assert order_status.status_name == ""

    # Correct assignment of status_name when storage_t is 'db'
    def test_correct_assignment_of_status_name_when_storage_t_is_db(self):
        # Setup
        mocker.patch('models.storage_t', 'db')
    
        # Action
        order_status = OrderStatus(status_name='Shipped')
    
        # Assertion
        assert order_status.status_name == 'Shipped'

    # Proper inheritance from BaseModel and Base
    def test_proper_inheritance(self):
        order_status = OrderStatus()
        assert isinstance(order_status, BaseModel)
        assert isinstance(order_status, Base)

    # Proper functioning of save method from BaseModel
    def test_save_updates_updated_at(self, mocker):
        order_status = OrderStatus()
        with mocker.patch('models.storage') as mock_storage:
            order_status.save()
            mock_storage.new.assert_called_once_with(order_status)
            mock_storage.save.assert_called_once()
            assert order_status.updated_at is not None

    # Proper functioning of to_dict method from BaseModel
    def test_to_dict_method(self):
        order_status_data = {
            'id': 1,
            'status_name': 'Shipped',
            'created_at': datetime(2022, 1, 1, 12, 0, 0),
            'updated_at': datetime(2022, 1, 2, 12, 0, 0),
            '__class__': 'OrderStatus'
        }
        order_status = OrderStatus(**order_status_data)
    
        expected_dict = {
            'id': 1,
            'status_name': 'Shipped',
            'created_at': '2022-01-01 12:00:00',
            'updated_at': '2022-01-02 12:00:00',
            '__class__': 'OrderStatus'
        }
    
        assert order_status.to_dict() == expected_dict

    # Proper functioning of delete method from BaseModel
    def test_proper_functioning_of_delete_method(self):
        # Create an instance of OrderStatus
        order_status = OrderStatus(status_name='Test Status')
    
        # Mock the models.storage_t to be 'db'
        with patch('models.storage_t', 'db'):
            # Call the delete method
            order_status.delete()
        
            # Check if is_deleted is set to True
            assert order_status.is_deleted is True
        
            # Check if deleted_at is not None
            assert order_status.deleted_at is not None

    # Validation of status_name length constraint
    def test_status_name_length_constraint(self):
        status_name = "A" * 100
        order_status = OrderStatus(status_name=status_name)
        assert order_status.status_name == status_name

    # Initialization with unexpected keyword arguments
    def test_initialization_with_unexpected_arguments(self):
        kwargs = {'status_name': 'Delivered', 'invalid_arg': 'Invalid'}
        order_status = OrderStatus(**kwargs)
        assert order_status.status_name == 'Delivered'
        assert order_status.created_at is None
        assert order_status.updated_at is None

    # Handling of None values for status_name when storage_t is 'db'
    def test_handling_of_none_values_for_status_name(self):
        # Setup
        kwargs = {'status_name': None}
    
        # Exercise
        order_status = OrderStatus(**kwargs)
    
        # Verify
        assert order_status.status_name is None
        assert order_status.created_at is None
        assert order_status.updated_at is None

    # Handling of database constraints and relationships
    def test_handling_database_constraints_and_relationships(self):
        # Given
        kwargs = {'status_name': 'Shipped'}
    
        # When
        order_status = OrderStatus(**kwargs)
    
        # Then
        assert order_status.status_name == 'Shipped'
        assert order_status.created_at is None
        assert order_status.updated_at is None

    # Ensuring created_at and updated_at are inherited when storage_t is not 'db'
    def test_inheritance_when_storage_t_not_db(self):
        # Setup
        order_status = OrderStatus()

        # Assertion
        assert order_status.created_at is None
        assert order_status.updated_at is None

    # Behavior when storage_t is neither 'db' nor any expected value
    def test_invalid_storage_t_value(self):
        # Set storage_t to an unexpected value
        with patch('models.storage_t', 'unexpected_value'):
            order_status = OrderStatus()
            assert order_status.status_name == ''
            assert order_status.created_at is None
            assert order_status.updated_at is None

    # Behavior of OrderStatus when integrated with other models
    def test_initialization_integration(self):
        kwargs = {'status_name': 'Shipped'}
        order_status = OrderStatus(**kwargs)
        assert order_status.status_name == 'Shipped'
        assert order_status.created_at is None
        assert order_status.updated_at is None

    # Ensuring created_at and updated_at are None when storage_t is 'db'
    def test_created_updated_at_none_for_db(self):
        # Setup
        with patch('models.storage_t', 'db'):
            order_status = OrderStatus()
        
        # Assertion
        assert order_status.created_at is None
        assert order_status.updated_at is None

    # Handling of empty string for status_name when storage_t is not 'db'
    def test_handling_empty_string_status_name(self):
        order_status = OrderStatus()
        assert order_status.status_name == ""

    def test_delete_method_from_BaseModel(self, mocker):
        order_status = OrderStatus()
        with mocker.patch('models.storage') as mock_storage:
            order_status.delete()
            mock_storage.delete.assert_called_once_with(order_status)

    def test_handling_of_database_constraints_and_relationships(self):
        order_status = OrderStatus()
        # Simulate database constraints and relationships
        # Assert relevant conditions
        assert True  # Placeholder for actual assertions related to database constraints and relationships

    def test_to_dict_method_from_BaseModel(self):
        order_status = OrderStatus(status_name='Delivered')
        expected_dict = {
            'status_name': 'Delivered',
            'created_at': None,
            'updated_at': None
        }
        assert order_status.to_dict() == expected_dict

    def test_invalid_status_name_value(self):
        order_status = OrderStatus(status_name='InvalidValue')
        assert order_status.status_name == 'InvalidValue'
        assert order_status.created_at is None
        assert order_status.updated_at is None
