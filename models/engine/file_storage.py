#!/usr/bin/python3
"""Defines the FileStorage class."""

import json

from models.base_model import BaseModel


class FileStorage:
    """Serializes instances to a JSON file and deserializes them."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary of all objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to storage."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize objects to the JSON file."""
        objects_dict = {}

        for key, obj in FileStorage.__objects.items():
            objects_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w") as file:
            json.dump(objects_dict, file)

    def reload(self):
        """Deserialize the JSON file."""
        try:
            with open(FileStorage.__file_path, "r") as file:
                objects_dict = json.load(file)

            for key, obj_dict in objects_dict.items():
                if obj_dict.get("__class__") == "BaseModel":
                    FileStorage.__objects[key] = BaseModel(**obj_dict)
        except FileNotFoundError:
            pass
