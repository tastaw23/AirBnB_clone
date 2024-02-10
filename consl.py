#!/usr/bin/python3
"""Interactive console for your project."""

import cmd
import sys


class HBNBConsole(cmd.Cmd):
    """Command-line interpreter class."""

    prompt = '(hbnb) '

    def do_help(self, arg):
        """Display help messages."""
        if arg:
            print(self.help_text.get(arg, f'No help for {arg}'))
        else:
            print("Documented commands (type help <topic>):")
            print("========================================")
            print("EOF  help  quit")

    def do_quit(self, arg):
        """Exit the console."""
        return True

    def do_EOF(self, arg):
        """Exit the console on EOF (Ctrl+D)."""
        print("")
        return True

    help_text = {
        'quit': 'Exit the console.',
        'EOF': 'Exit the console on EOF (Ctrl+D).',
        'help': 'Display help messages.'
    }
