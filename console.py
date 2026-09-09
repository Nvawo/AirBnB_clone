#!/usr/bin/python3
"""Command interpreter for the AirBnB clone project."""

import cmd
import shlex

from models import storage
from models.base_model import BaseModel
from models.user import User


class HBNBCommand(cmd.Cmd):
    """AirBnB command interpreter."""

    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Exit the program on EOF."""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_create(self, arg):
        """Create a new instance."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show an instance."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        print(objects[key])

    def do_destroy(self, arg):
        """Delete an instance."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        del objects[key]
        storage.save()

    def do_all(self, arg):
        """Print all instances or all instances of a class."""
        args = shlex.split(arg)
        objects = storage.all()

        if args:
            class_name = args[0]

            if class_name not in self.classes:
                print("** class doesn't exist **")
                return

            result = []

            for key, obj in objects.items():
                if key.split(".")[0] == class_name:
                    result.append(str(obj))

            print(result)
            return

        print([str(obj) for obj in objects.values()])

    def do_update(self, arg):
        """Update an instance."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        attribute_name = args[2]

        if len(args) < 4:
            print("** value missing **")
            return

        attribute_value = args[3]
        instance = objects[key]

        if hasattr(instance, attribute_name):
            current_value = getattr(instance, attribute_name)

            if isinstance(current_value, int):
                attribute_value = int(attribute_value)
            elif isinstance(current_value, float):
                attribute_value = float(attribute_value)

        setattr(instance, attribute_name, attribute_value)
        instance.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
