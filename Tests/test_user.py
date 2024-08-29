from models.user import User
import datetime
from datetime import timedelta
import models
from models.order import Order


# Dependencies:
# pip install pytest-mock
import pytest

class TestUser:

    # User instance creation with all attributes in'db' mode
    def test_user_creation_with_all_attributes_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            contact_number="1234567890",
            country="USA",
            company_name="Example Inc.",
            address="123 Main St",
            state_or_country="CA",
            postal_or_zip="90210",
            order_notes="Please deliver between 9 AM and 5 PM",
            password_hash="hashed_password",
            is_create_account=1
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.contact_number == "1234567890"
        assert user.country == "USA"
        assert user.company_name == "Example Inc."
        assert user.address == "123 Main St"
        assert user.state_or_country == "CA"
        assert user.postal_or_zip == "90210"
        assert user.order_notes == "Please deliver between 9 AM and 5 PM"
        assert user.password_hash == "hashed_password"
        assert user.is_create_account == 1

    # User instance creation with missing required attributes in 'db' mode
    def test_user_creation_missing_required_attributes_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'db')
        with pytest.raises(TypeError):
            User(
                last_name="Doe",
                email="john.doe@example.com",
                contact_number="1234567890",
                country="USA",
                company_name="Example Inc.",
                address="123 Main St",
                state_or_country="CA",
                postal_or_zip="90210"
            )

    # User instance creation with default attributes in non-'db' mode
    def test_user_creation_with_default_attributes_non_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'non_db')
        user = User()
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.email == ""
        assert user.contact_number == ""
        assert user.country == ""
        assert user.company_name == ""
        assert user.address == ""
        assert user.state_or_country == ""
        assert user.postal_or_zip == ""
        assert user.order_notes == ""
        assert user.password_hash == ""
        assert user.is_create_account is None

    # User instance relationship with Order in 'db' mode
    def test_user_instance_relationship_with_order_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            contact_number="1234567890",
            country="USA",
            company_name="Example Inc.",
            address="123 Main St",
            state_or_country="CA",
            postal_or_zip="90210",
            order_notes="Please deliver between 9 AM and 5 PM",
            password_hash="hashed_password",
            is_create_account=1
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.contact_number == "1234567890"
        assert user.country == "USA"
        assert user.company_name == "Example Inc."
        assert user.address == "123 Main St"
        assert user.state_or_country == "CA"
        assert user.postal_or_zip == "90210"
        assert user.order_notes == "Please deliver between 9 AM and 5 PM"
        assert user.password_hash == "hashed_password"
        assert user.is_create_account == 1

    # User instance soft delete setting 'is_deleted' and 'deleted_at'
    def test_user_soft_delete_setting(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User()
        user.delete()
        assert user.is_deleted == True
        assert user.deleted_at is not None

    # User instance string representation
    def test_user_instance_string_representation(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            contact_number="1234567890",
            country="USA",
            company_name="Example Inc.",
            address="123 Main St",
            state_or_country="CA",
            postal_or_zip="90210",
            order_notes="Please deliver between 9 AM and 5 PM",
            password_hash="hashed_password",
            is_create_account=1
        )
        expected_output = "[User] (None) {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'contact_number': '1234567890', 'country': 'USA', 'company_name': 'Example Inc.', 'address': '123 Main St', 'state_or_country': 'CA', 'postal_or_zip': '90210', 'order_notes': 'Please deliver between 9 AM and 5 PM', 'password_hash': 'hashed_password', 'is_create_account': 1}"
        assert str(user) == expected_output

    # User instance save method updating 'updated_at'
    def test_user_instance_save_method_updates_updated_at(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User()
        original_updated_at = user.updated_at
        user.save()
        assert user.updated_at != original_updated_at

    # User instance creation with invalid attribute types
    def test_user_creation_with_invalid_attributes_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'db')
        with pytest.raises(Exception):
            user = User(
                first_name=123,  # Invalid type
                last_name="Doe",
                email="john.doe@example.com",
                contact_number="1234567890",
                country="USA",
                company_name="Example Inc.",
                address="123 Main St",
                state_or_country="CA",
                postal_or_zip="90210",
                order_notes="Please deliver between 9 AM and 5 PM",
                password_hash="hashed_password",
                is_create_account=1
            )

    # User instance dictionary conversion
    def test_user_instance_dictionary_conversion(self, mocker):
        user_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com",
            "contact_number": "9876543210",
            "country": "Canada",
            "company_name": "ABC Company",
            "address": "456 Elm St",
            "state_or_country": "Ontario",
            "postal_or_zip": "M1M 1M1",
            "order_notes": "Urgent delivery needed",
            "password_hash": "hashed_password",
            "is_create_account": 0
        }
        mocker.patch('models.storage_t', 'db')
        user = User(**user_data)
        user_dict = user.to_dict()
        assert user_dict["first_name"] == "Alice"
        assert user_dict["last_name"] == "Smith"
        assert user_dict["email"] == "alice.smith@example.com"
        assert user_dict["contact_number"] == "9876543210"
        assert user_dict["country"] == "Canada"
        assert user_dict["company_name"] == "ABC Company"
        assert user_dict["address"] == "456 Elm St"
        assert user_dict["state_or_country"] == "Ontario"
        assert user_dict["postal_or_zip"] == "M1M 1M1"
        assert user_dict["order_notes"] == "Urgent delivery needed"
        assert user_dict["password_hash"] == "hashed_password"
        assert user_dict["is_create_account"] == 0

    # User instance soft delete in non-'db' mode
    def test_user_instance_soft_delete_non_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'fs')
        user = User()
        user.delete()
        assert user.is_deleted == True
        assert user.deleted_at is not None

    # User instance save method without prior initialization
    def test_user_instance_save_without_initialization(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User()
        with pytest.raises(Exception):
            user.save()

    # User instance creation with empty strings for non-nullable fields in 'db' mode
    def test_user_creation_with_empty_strings_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User()
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.email == ""
        assert user.contact_number == ""
        assert user.country == ""
        assert user.company_name == ""
        assert user.address == ""
        assert user.state_or_country == ""
        assert user.postal_or_zip == ""
        assert user.order_notes == ""
        assert user.password_hash == ""
        assert user.is_create_account is None

    # User instance creation with future dates for 'created_at' or 'updated_at'
    def test_user_creation_with_future_dates_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'db')
        future_date = datetime.utcnow() + timedelta(days=1)
        user = User(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            contact_number="9876543210",
            country="UK",
            company_name="ABC Ltd.",
            address="456 Park Ave",
            state_or_country="London",
            postal_or_zip="W1A 1AA",
            order_notes="Urgent delivery required",
            password_hash="hashed_password",
            is_create_account=1,
            created_at=future_date,
            updated_at=future_date
        )
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"
        assert user.email == "alice.smith@example.com"
        assert user.contact_number == "9876543210"
        assert user.country == "UK"
        assert user.company_name == "ABC Ltd."
        assert user.address == "456 Park Ave"
        assert user.state_or_country == "London"
        assert user.postal_or_zip == "W1A 1AA"
        assert user.order_notes == "Urgent delivery required"
        assert user.password_hash == "hashed_password"
        assert user.is_create_account == 1
        assert user.created_at < datetime.utcnow()
        assert user.updated_at < datetime.utcnow()

    # User instance dictionary conversion with missing 'created_at' or 'updated_at'
    def test_user_instance_dict_conversion_missing_created_or_updated_at(self, mocker):
        user_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'contact_number': '9876543210',
            'country': 'Canada',
            'company_name': 'ABC Corp',
            'address': '456 Elm St',
            'state_or_country': 'ON',
            'postal_or_zip': 'M1S 2E8',
            'order_notes': 'Urgent delivery needed',
            'password_hash': 'hashed_password',
            'is_create_account': 1
        }
        mocker.patch('models.storage_t', '')
        user = User(**user_data)
        user_dict = user.to_dict()
        assert user_dict['created_at'] is None
        assert user_dict['updated_at'] is None

    # User instance save method with database connection issues
    def test_user_instance_save_db_connection_issues(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User()
        mocker.patch.object(models.storage, 'new', side_effect=Exception('Database connection error'))
        with pytest.raises(Exception):
            user.save()

    # User instance deletion with existing related Order instances
    def test_user_deletion_with_related_orders(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            contact_number="1234567890",
            country="USA",
            company_name="Example Inc.",
            address="123 Main St",
            state_or_country="CA",
            postal_or_zip="90210",
            order_notes="Please deliver between 9 AM and 5 PM",
            password_hash="hashed_password",
            is_create_account=1
        )
        order = Order(user=user)  # Creating a related Order instance
        user.delete()  # Deleting the user instance
        assert user.is_deleted is True
        assert user.deleted_at is not None

    # User instance creation with special characters in string fields
    def test_user_creation_with_special_characters_db_mode(self, mocker):
        mocker.patch('models.storage_t', 'db')
        user = User(
            first_name="J*hn",
            last_name="Doe",
            email="john.doe@example.com",
            contact_number="1234567890",
            country="USA",
            company_name="Example Inc.",
            address="123 Main St",
            state_or_country="CA",
            postal_or_zip="90210",
            order_notes="Please deliver between 9 AM and 5 PM",
            password_hash="hashed_password",
            is_create_account=1
        )
        assert user.first_name == "J*hn"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.contact_number == "1234567890"
        assert user.country == "USA"
        assert user.company_name == "Example Inc."
        assert user.address == "123 Main St"
        assert user.state_or_country == "CA"
        assert user.postal_or_zip == "90210"
        assert user.order_notes == "Please deliver between 9 AM and 5 PM"
        assert user.password_hash == "hashed_password"
        assert user.is_create_account == 1
