"""
Login Window Tests for MediSys Hospital Management System

This module contains unit tests for the login window functionality, including
input validation and error handling. It tests the login form with various
input scenarios to ensure proper validation and error messages.

Author: Mazharuddin Mohammed
"""

import unittest
from PySide6.QtWidgets import QApplication
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

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