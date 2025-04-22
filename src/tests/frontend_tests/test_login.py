import unittest
from PySide6.QtWidgets import QApplication
from src.frontend.python.gui.login_window import LoginWindow
import medisys_bindings

class TestLoginWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.db = medisys_bindings.DBManager("dbname=medisys_test user=postgres password=secret host=localhost")
        self.db.initialize_schema()
        self.window = LoginWindow(self.db)

    def test_empty_inputs(self):
        self.window.username_input.setText("")
        self.window.password_input.setText("")
        self.window.handle_login()
        self.assertEqual(self.window.error_label.text(), "Username and password are required")

    def test_invalid_length(self):
        self.window.username_input.setText("a" * 51)
        self.window.password_input.setText("test")
        self.window.handle_login()
        self.assertEqual(self.window.error_label.text(), "Input too long")

    def tearDown(self):
        self.window.close()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()