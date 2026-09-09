#!/usr/bin/python3
"""Tests for the command interpreter."""

import unittest
from unittest.mock import patch
from io import StringIO

from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    """Test cases for the console."""

    def setUp(self):
        """Clear storage before each test."""
        storage.all().clear()

    def tearDown(self):
        """Clear storage after each test."""
        storage.all().clear()

    def test_create_missing_class(self):
        """Test create without a class."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create")

        self.assertEqual(
            output.getvalue(),
            "** class name missing **\n"
        )

    def test_create_invalid_class(self):
        """Test create with an invalid class."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Invalid")

        self.assertEqual(
            output.getvalue(),
            "** class doesn't exist **\n"
        )

    def test_create_user(self):
        """Test creating a User."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")

        user_id = output.getvalue().strip()

        self.assertTrue(user_id)
        self.assertIn("User.{}".format(user_id), storage.all())

    def test_show_missing_class(self):
        """Test show without a class."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("show")

        self.assertEqual(
            output.getvalue(),
            "** class name missing **\n"
        )

    def test_show_missing_id(self):
        """Test show without an id."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("show User")

        self.assertEqual(
            output.getvalue(),
            "** instance id missing **\n"
        )

    def test_show_invalid_id(self):
        """Test show with an invalid id."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("show User invalid-id")

        self.assertEqual(
            output.getvalue(),
            "** no instance found **\n"
        )

    def test_all(self):
        """Test all command."""
        with patch("sys.stdout", new=StringIO()):
            HBNBCommand().onecmd("create User")

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("all User")

        self.assertIn("User", output.getvalue())

    def test_destroy(self):
        """Test destroy command."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")

        user_id = output.getvalue().strip()

        with patch("sys.stdout", new=StringIO()):
            HBNBCommand().onecmd(
                "destroy User {}".format(user_id)
            )

        self.assertNotIn(
            "User.{}".format(user_id),
            storage.all()
        )

    def test_update(self):
        """Test update command."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")

        user_id = output.getvalue().strip()

        HBNBCommand().onecmd(
            'update User {} first_name "Nvawo"'.format(user_id)
        )

        key = "User.{}".format(user_id)

        self.assertEqual(
            storage.all()[key].first_name,
            "Nvawo"
        )


if __name__ == "__main__":
    unittest.main()
quit
