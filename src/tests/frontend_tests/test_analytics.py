import unittest
import pandas as pd
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.frontend.python.analytics.kpi_analytics import KPIAnalytics
from src.frontend.python.analytics.medical_analytics import MedicalAnalytics
import medisys_bindings

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.db = medisys_bindings.DBManager("dbname=medisys_test user=postgres password=secret host=localhost")
        self.db.initialize_schema()
        self.kpi_analytics = KPIAnalytics(self.db)
        self.medical_analytics = MedicalAnalytics(self.db)

    def test_doctor_kpi_empty(self):
        df = self.kpi_analytics.get_doctor_kpi(1, "2025-01-01", "2025-12-31")
        self.assertTrue(df.empty)

    def test_medical_metrics_empty(self):
        df = self.medical_analytics.get_patient_metrics(1, "2025-01-01", "2025-12-31")
        self.assertTrue(df.empty)

    def test_trend_summary_empty(self):
        trends = self.medical_analytics.get_trend_summary(1, "2025-01-01", "2025-12-31")
        self.assertEqual(trends, {})