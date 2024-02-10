import unittest
import sys
from io import StringIO
from console import HBNBConsole

class TestConsole(unittest.TestCase):
    def setUp(self):
        self.console = HBNBConsole()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def test_help_command(self):
        self.console.onecmd("help")
        output = sys.stdout.getvalue().strip()
        self.assertIn("Documented commands", output)

    def test_quit_command(self):
        result = self.console.onecmd("quit")
        self.assertTrue(result)

    def test_EOF_command(self):
        result = self.console.onecmd("EOF")
        self.assertTrue(result)

    def test_nonexistent_command(self):
        self.console.onecmd("nonexistent")
        output = sys.stderr.getvalue().strip()
        self.assertIn("No help for nonexistent", output)

    def test_create_command(self):
        self.console.onecmd("create User")
        output = sys.stdout.getvalue().strip()
        self.assertTrue(output)

    # Add more test cases as needed for your specific commands and functionalities

if __name__ == '__main__':
    unittest.main()

