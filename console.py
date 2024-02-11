#!/usr/bin/python3
"""
The command interpreter for the AirBnB clone project.
"""
import cmd

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
