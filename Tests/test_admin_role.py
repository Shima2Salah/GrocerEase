from models.admin_role import AdminRole
from models.base_model import BaseModel
from lib2to3.pytree import Base
from pytest_mock import mocker
import models


import pytest

class TestAdminRole:

    # Initialization of AdminRole with valid attributes
    def test_initialization_with_valid_attributes(self):
        valid_attributes = {
            'admin_role_name': 'Super Admin',
            'admin_role_description': 'Has all access rights'
        }
        admin_role = AdminRole(**valid_attributes)
        assert admin_role.admin_role_name == 'Super Admin'
        assert admin_role.admin_role_description == 'Has all access rights'

    # Initialization of AdminRole with missing attributes
    def test_initialization_with_missing_attributes(self):
        admin_role = AdminRole()
        assert admin_role.admin_role_name == ""
        assert admin_role.admin_role_description == ""

    # Correct setting of admin_role_name and admin_role_description
    def test_correct_setting_of_admin_role_name_and_description(self):
        # Create an instance of AdminRole
        admin_role = AdminRole(admin_role_name='Super Admin', admin_role_description='Has all access rights')
    
        # Check if admin_role_name and admin_role_description are set correctly
        assert admin_role.admin_role_name == 'Super Admin'
        assert admin_role.admin_role_description == 'Has all access rights'

    # Behavior when updating admin_role_name and admin_role_description
    def test_update_admin_role_name_and_description(self):
        # Setup
        admin_role_data = {
            'admin_role_name': 'New Admin Role',
            'admin_role_description': 'Description of the new role'
        }
        admin_role = AdminRole(**admin_role_data)

        # Exercise
        updated_name = 'Updated Admin Role'
        updated_description = 'Updated description of the role'
        admin_role.admin_role_name = updated_name
        admin_role.admin_role_description = updated_description

        # Verify
        assert admin_role.admin_role_name == updated_name
        assert admin_role.admin_role_description == updated_description

    # Proper inheritance from BaseModel and Base
    def test_proper_inheritance(self):
        admin_role = AdminRole()
        assert isinstance(admin_role, BaseModel)
        assert isinstance(admin_role, Base)

    # Handling of special characters in admin_role_name and admin_role_description
    def test_handling_special_characters(self):
        # Create an AdminRole instance with special characters in name and description
        special_name = "Admin_Role#1"
        special_description = "Description with $pecial characters!"
        admin_role = AdminRole(admin_role_name=special_name, admin_role_description=special_description)
    
        # Check if the special characters are correctly stored
        assert admin_role.admin_role_name == special_name
        assert admin_role.admin_role_description == special_description

    # Proper relationship setup with Admin model
    def test_proper_relationship_setup_with_admin_model(self):
        # Create necessary mocks and stubs
        mocker.patch('models.storage_t', return_value='db')
        mocker.patch('models.storage.new')
        mocker.patch('models.storage.save')

        # Create an instance of AdminRole
        admin_role = AdminRole()

        # Check the relationship setup with Admin model
        assert hasattr(admin_role, 'admins')
        assert admin_role.admins.property.backref == 'admin_roles'
        assert admin_role.admins.property.cascade == 'all, delete, delete-orphan'

    # Behavior when models.storage_t is not 'db'
    def test_initialization_with_empty_attributes(self):
        admin_role = AdminRole()
        assert admin_role.admin_role_name == ""
        assert admin_role.admin_role_description == ""

    # Behavior when deleting an AdminRole instance
    def test_delete_admin_role_instance(self, mocker):
        # Setup
        admin_role_data = {
            'admin_role_name': 'Super Admin',
            'admin_role_description': 'Has all access rights'
        }
        admin_role = AdminRole(**admin_role_data)
    
        # Mocking
        mocker.patch('models.storage_t', return_value='db')
        mocker.patch.object(models.storage, 'save')
    
        # Action
        admin_role.delete()
    
        # Assertion
        assert admin_role.is_deleted is True
        assert admin_role.deleted_at is not None
        models.storage.save.assert_called_once()

    # Validation of relationship cascade options
    def test_validation_of_relationship_cascade_options(self):
        # Create an instance of AdminRole
        admin_role = AdminRole()

        # Check if the cascade options are correctly set
        assert admin_role.admins.cascade == "all, delete, delete-orphan"

    # Handling of duplicate admin_role_name values
    def test_handling_duplicate_admin_role_name(self):
        # Create two AdminRole instances with the same admin_role_name
        admin_role1 = AdminRole(admin_role_name='Admin', admin_role_description='Description 1')
        admin_role2 = AdminRole(admin_role_name='Admin', admin_role_description='Description 2')
    
        # Check that the admin_role_name is the same for both instances
        assert admin_role1.admin_role_name == 'Admin'
        assert admin_role2.admin_role_name == 'Admin'

    # Handling of large strings for admin_role_name and admin_role_description
    def test_handling_large_strings(self):
        long_name = 'a' * 100
        long_description = 'b' * 255
        admin_role = AdminRole(admin_role_name=long_name, admin_role_description=long_description)
        assert admin_role.admin_role_name == long_name
        assert admin_role.admin_role_description == long_description
