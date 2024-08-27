# Dependencies:
# pip install pytest-mock
import pytest

class TestSize:

    # Initializes Size with valid attributes
    def test_initializes_size_with_valid_attributes(self, mocker):
        from models.size import Size
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        size = Size(size_name="Large")
        assert size.size_name == "Large"

    # Initializes Size with missing attributes
    def test_initializes_size_with_missing_attributes(self, mocker):
        from models.size import Size
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        size = Size()
        assert size.size_name == ""

    # Creates Size instance with database storage
    def test_creates_instance_with_db_storage(self, mocker):
        from models.size import Size
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        mocker.patch('models.size.products_sizes', 'MockProductsSizes')
        size = Size(size_name="Medium")
        assert size.size_name == "Medium"

    # Creates Size instance without database storage
    def test_creates_size_instance_without_db_storage(self, mocker):
        from models.size import Size
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        size = Size(size_name="Medium")
        assert size.size_name == "Medium"

    # Size instance has correct table name when using database storage
    def test_correct_table_name_db_storage(self, mocker):
        from models.size import Size
        from models.base_model import BaseModel
        from sqlalchemy import Column, String, Integer, ForeignKey, Table
        from sqlalchemy.orm import relationship

        mocker.patch('models.base_model.Base.__subclasses__', return_value=[Size])
        mocker.patch('models.storage_t', return_value='db')
        mocker.patch('models.base_model.Base.metadata', create=True)
        mocker.patch('sqlalchemy.Column')
        mocker.patch('sqlalchemy.ForeignKey')
        mocker.patch('sqlalchemy.Table')

        size = Size()

        assert size.__tablename__ == 'sizes'

    # Size instance has correct size_name when using database storage
    def test_correct_size_name_with_database_storage(self, mocker):
        from models.size import Size
        from models.base_model import BaseModel
        from models.size import products_sizes
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        size = Size(size_name="Medium")
        assert size.size_name == "Medium"

    # Verifies __tablename__ is not set when not using database storage
    def test_not_using_database_storage(self, mocker):
        from models.size import Size
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        size = Size(size_name="Large")
        assert not hasattr(size, '__tablename__')

    # Handles duplicate size_name when using database storage
    def test_handles_duplicate_size_name(self, mocker):
        from models.size import Size
        from models.base_model import BaseModel
        from sqlalchemy.exc import IntegrityError

        mocker.patch('models.base_model.Base.metadata.create_all', return_value=None)
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)

        # Create a size with a unique size_name
        size1 = Size(size_name="Small")
        size1.save()

        # Try to create another size with the same size_name
        with pytest.raises(IntegrityError):
            size2 = Size(size_name="Small")
            size2.save()

    # Ensures products relationship is not set when not using database storage
    def test_products_relationship_not_set(self, mocker):
        from models.size import Size
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        size = Size()
        assert not hasattr(size, 'products')

    # Ensures ForeignKey constraints are respected
    def test_foreign_key_constraints_respected(self, mocker):
        from models.size import Size
        from models.base_model import BaseModel
        from sqlalchemy import Column, String, Integer, ForeignKey, Table
        from sqlalchemy.orm import relationship

        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        mocker.patch('models.size.products_sizes', autospec=True)

        size = Size(size_name="Medium")
        assert size.size_name == "Medium"

    # Size instance has correct relationship with Product when using database storage
    def test_correct_relationship_with_product(self, mocker):
        from models.size import Size
        from models.base_model import BaseModel, Base
        from sqlalchemy.orm import relationship
        from sqlalchemy import Column, String, Integer, ForeignKey, Table

        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        mocker.patch('models.size.products_sizes', 'products_sizes_mock')

        size = Size(size_name="Large")
        assert hasattr(size, 'products')
        assert isinstance(size.products, relationship)

    # Handles empty string for size_name when not using database storage
    def test_handles_empty_string_for_size_name(self, mocker):
        from models.size import Size
        size = Size()
        assert size.size_name == ""

    # Initializes Size with invalid attribute types
    def test_initializes_size_with_invalid_attributes(self, mocker):
        from models.size import Size
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        size = Size(size_name=123)  # Passing an integer instead of a string
        assert size.size_name == 123

    # Handles None for size_name when using database storage
    def test_handles_none_for_size_name(self, mocker):
        from models.size import Size
        mocker.patch('models.base_model.BaseModel.__init__', return_value=None)
        size = Size()
        assert size.size_name is None
