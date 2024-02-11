#!/usr/bin/python3
"""
The command interpreter for the AirBnB clone project.
"""
import cmd
from models import storage
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """The HBNBCommand class."""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Handles the EOF signal to exit the program."""
        print("")  # New line for clarity
        return True

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it, and prints the id."""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                cls_name = args[0]
                obj_id = args[1]
                key = "{}.{}".format(cls_name, obj_id)
                obj = storage.all().get(key)
                if obj:
                    print(obj)
                else:
                    print("** no instance found **")
            except IndexError:
                print("** instance id missing **")
            except NameError:
                print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                cls_name = args[0]
                obj_id = args[1]
                key = "{}.{}".format(cls_name, obj_id)
                obj = storage.all().get(key)
                if obj:
                    del storage.all()[key]
                    storage.save()
                else:
                    print("** no instance found **")
            except IndexError:
                print("** instance id missing **")
            except NameError:
                print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        args = arg.split()
        objs = storage.all()
        if not args:
            print([str(obj) for obj in objs.values()])
        else:
            try:
                cls_name = args[0]
                if cls_name in storage.classes():
                    print([str(obj) for key, obj in objs.items() if cls_name in key])
                else:
                    print("** class doesn't exist **")
            except NameError:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                cls_name = args[0]
                obj_id = args[1]
                key = "{}.{}".format(cls_name, obj_id)
                obj = storage.all().get(key)
                if obj:
                    if len(args) < 3:
                        print("** attribute name missing **")
                        return
                    if len(args) < 4:
                        print("** value missing **")
                        return
                    attr_name = args[2]
                    attr_val = args[3]
                    setattr(obj, attr_name, eval(attr_val))
                    storage.save()
                else:
                    print("** no instance found **")
            except IndexError:
                print("** instance id missing **")
            except NameError:
                print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()

