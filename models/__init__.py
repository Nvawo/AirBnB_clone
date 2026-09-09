#!/usr/bin/python3
"""Create the storage instance."""

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
