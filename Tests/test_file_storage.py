import sys
import os

# Append the parent directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.engine.db_storage import DBStorage
# Dependencies:
# pip install pytest-mock
import pytest

class TestFileStorage:

    # Serialize objects to JSON file correctly
    def test_serialize_objects_to_json_file(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel
        import json

        # Mock the open function and json.dump
        mock_open = mocker.patch("builtins.open", mocker.mock_open())
        mock_json_dump = mocker.patch("json.dump")

        # Create a FileStorage instance and add a BaseModel object
        storage = FileStorage()
        obj = BaseModel()
        obj.id = "1234"
        storage.new(obj)

        # Call the save method
        storage.save()

        # Check that open was called with the correct file path and mode
        mock_open.assert_called_once_with("file.json", 'w')

        # Check that json.dump was called with the correct data
        expected_dict = {f"BaseModel.{obj.id}": obj.to_dict(save_fs=1)}
        mock_json_dump.assert_called_once_with(expected_dict, mock_open())

    # Handle non-existent JSON file gracefully during reload
    def test_handle_non_existent_json_file_during_reload(self, mocker):
        from models.engine.file_storage import FileStorage

        # Mock the open function to raise a FileNotFoundError
        mocker.patch("builtins.open", side_effect=FileNotFoundError)

        # Create a FileStorage instance and call the reload method
        storage = FileStorage()
        storage.reload()

        # Check that __objects is still an empty dictionary
        assert storage.all() == {}

    # Return all objects when no class is specified
    def test_return_all_objects_no_class_specified(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel

        # Create a FileStorage instance and add a BaseModel object
        storage = FileStorage()
        obj = BaseModel()
        obj.id = "1234"
        storage.new(obj)

        # Call the all method without specifying a class
        result = storage.all()

        # Check that the result contains the added object
        assert f"BaseModel.{obj.id}" in result

    # Return objects of a specific class when class is specified
    def test_return_objects_of_specific_class(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel

        # Create a FileStorage instance and add a BaseModel object
        storage = FileStorage()
        obj = BaseModel()
        obj.id = "1234"
        storage.new(obj)

        # Call the get method with the BaseModel class and object id
        returned_obj = storage.get(BaseModel, "1234")

        # Check that the returned object is the same as the added object
        assert returned_obj == obj

    # Deserialize objects from JSON file correctly
    def test_deserialize_objects_from_json_file(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel
        import json

        # Mock the open function and json.load
        mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data='{"BaseModel.1234": {"__class__": "BaseModel", "id": "1234"}}'))
        mock_json_load = mocker.patch("json.load")

        # Create a FileStorage instance
        storage = FileStorage()

        # Call the reload method
        storage.reload()

        # Check that open was called with the correct file path and mode
        mock_open.assert_called_once_with("file.json", 'r')

        # Check that json.load was called
        mock_json_load.assert_called_once()

        # Check that the object was deserialized correctly
        assert "BaseModel.1234" in storage._FileStorage__objects

    # Add new objects to the storage
    def test_add_new_objects_to_storage(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel
    
        # Mock the open function and json.dump
        mock_open = mocker.patch("builtins.open", mocker.mock_open())
        mock_json_dump = mocker.patch("json.dump")
    
        # Create a FileStorage instance and add a BaseModel object
        storage = FileStorage()
        obj = BaseModel()
        obj.id = "1234"
        storage.new(obj)
    
        # Call the save method
        storage.save()
    
        # Check that open was called with the correct file path and mode
        mock_open.assert_called_once_with("file.json", 'w')
    
        # Check that json.dump was called with the correct data
        expected_dict = {f"BaseModel.{obj.id}": obj.to_dict(save_fs=1)}
        mock_json_dump.assert_called_once_with(expected_dict, mock_open())

    # Delete specified objects from the storage
    def test_delete_specified_objects(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel

        # Create a FileStorage instance and add a BaseModel object
        storage = FileStorage()
        obj = BaseModel()
        obj.id = "1234"
        storage.new(obj)

        # Call the delete method
        storage.delete(obj)

        # Check that the object was deleted from __objects
        assert f"BaseModel.{obj.id}" not in storage._FileStorage__objects.keys()

    # Return the correct object based on class and ID
    def test_return_correct_object(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel

        # Create a FileStorage instance and add a BaseModel object
        storage = FileStorage()
        obj = BaseModel()
        obj.id = "1234"
        storage.new(obj)

        # Call the get method with the class and ID of the added object
        result = storage.get(BaseModel, "1234")

        # Check that the returned object is the same as the added object
        assert result == obj

    # Close method calls reload method successfully
    def test_close_calls_reload_successfully(self, mocker):
        from models.engine.file_storage import FileStorage
        import json

        # Mock the reload method
        mocker.patch.object(FileStorage, 'reload')

        # Create a FileStorage instance
        storage = FileStorage()

        # Call the close method
        storage.close()

        # Check that reload was called
        storage.reload.assert_called_once()

    # Count all objects in storage
    def test_count_all_objects_in_storage(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel
        import models

        # Create a FileStorage instance and add some objects
        storage = FileStorage()
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj3 = BaseModel()
        storage.new(obj1)
        storage.new(obj2)
        storage.new(obj3)

        # Mock the models.storage.all method
        mocker.patch.object(models.storage, 'all', return_value=storage.__objects)

        # Test counting all objects
        assert storage.count() == 3

    # Count objects of a specific class in storage
    def test_count_objects_of_specific_class(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel
        import models

        # Create a FileStorage instance and add multiple BaseModel objects
        storage = FileStorage()
        obj1 = BaseModel()
        obj1.id = "1234"
        storage.new(obj1)
        obj2 = BaseModel()
        obj2.id = "5678"
        storage.new(obj2)

        # Mock the models.storage.all method to return the objects
        mocker.patch.object(models.storage, 'all', return_value={f"BaseModel.{obj1.id}": obj1, f"BaseModel.{obj2.id}": obj2})

        # Test counting all objects
        assert storage.count() == 2

        # Test counting objects of a specific class
        assert storage.count(BaseModel) == 2

    # Handle get method with non-existent ID
    def test_handle_get_method_with_non_existent_id(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel
        import json

        # Mock the models.storage.all method
        mocker.patch('models.storage.all', return_value={})

        # Create a FileStorage instance and add a BaseModel object
        storage = FileStorage()
        obj = BaseModel()
        obj.id = "1234"
        storage.new(obj)

        # Call the get method with a non-existent ID
        result = storage.get(BaseModel, "5678")

        # Check that the result is None
        assert result is None

    # Handle empty JSON file during reload
    def test_handle_empty_json_file_during_reload(self, mocker):
        from models.engine.file_storage import FileStorage
        import json

        # Mock the open function and json.load
        mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="{}"))
        mock_json_load = mocker.patch("json.load", return_value={})

        # Create a FileStorage instance
        storage = FileStorage()

        # Call the reload method
        storage.reload()

        # Check that open was called with the correct file path and mode
        mock_open.assert_called_once_with("file.json", 'r')

        # Check that json.load was called
        mock_json_load.assert_called_once_with(mock_open())

    # Handle invalid JSON content during reload
    def test_handle_invalid_json_content_during_reload(self, mocker):
        from models.engine.file_storage import FileStorage
        import json

        # Mock the open function and json.load
        mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data='invalid_json_data'))
        mock_json_load = mocker.patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0))

        # Create a FileStorage instance
        storage = FileStorage()

        # Call the reload method
        storage.reload()

        # Check that open was called with the correct file path and mode
        mock_open.assert_called_once_with("file.json", 'r')

        # Check that json.load was called
        mock_json_load.assert_called_once()

    # Handle get method with invalid class
    def test_handle_get_method_with_invalid_class(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel
        import json

        # Mock the classes dictionary
        classes = {
            "BaseModel": BaseModel
        }

        # Mock the storage and add a BaseModel object
        storage = FileStorage()
        obj = BaseModel()
        obj.id = "1234"
        storage.new(obj)

        # Mock the all method to return an empty dictionary
        mocker.patch.object(storage, 'all', return_value={})

        # Call the get method with an invalid class
        result = storage.get("InvalidClass", "1234")

        # Check that the result is None
        assert result is None

    # Handle deletion of non-existent objects
    def test_delete_non_existent_object(self, mocker):
        from models.engine.file_storage import FileStorage
        from models.base_model import BaseModel

        # Create a FileStorage instance
        storage = FileStorage()

        # Create a BaseModel object with an ID
        obj = BaseModel()
        obj.id = "1234"

        # Add the object to the storage
        storage.new(obj)

        # Call delete with a different object
        obj_to_delete = BaseModel()
        obj_to_delete.id = "5678"
        storage.delete(obj_to_delete)

        # Check that the original object is still in storage
        assert f"BaseModel.{obj.id}" in storage._FileStorage__objects

        # Call delete with the original object
        storage.delete(obj)

        # Check that the original object is removed from storage
        assert f"BaseModel.{obj.id}" not in storage._FileStorage__objects
