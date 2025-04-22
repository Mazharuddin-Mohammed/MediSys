import pandas as pd
import matplotlib.pyplot as plt
import medisys_bindings
from datetime import datetime

class KPIAnalytics:
    def __init__(self, db):
        self.db = db

    def get_doctor_kpi(self, doctor_id, start_date, end_date):
        query = """
        SELECT metric_name, metric_value, metric_date
        FROM doctor_kpi
        WHERE doctor_id = %s AND metric_date BETWEEN %s AND %s
        ORDER BY metric_date
        """
        conn = self.db.getConnection()
        df = pd.read_sql_query(query, conn, params=(doctor_id, start_date, end_date))
        return df

    def plot_doctor_kpi(self, doctor_id, start_date, end_date, output_path):
        df = self.get_doctor_kpi(doctor_id, start_date, end_date)
        if df.empty:
            return

        plt.figure(figsize=(10, 6))
        for metric in df['metric_name'].unique():
            metric_data = df[df['metric_name'] == metric]
            plt.plot(metric_data['metric_date'], metric_data['metric_value'], label=metric)

        plt.title(f"Doctor KPI Metrics (ID: {doctor_id})")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()

    def get_department_kpi(self, department_id, start_date, end_date):
        query = """
        SELECT metric_name, metric_value, metric_date
        FROM department_kpi
        WHERE department_id = %s AND metric_date BETWEEN %s AND %s
        ORDER BY metric_date
        """
        conn = self.db.getConnection()
        df = pd.read_sql_query(query, conn, params=(department_id, start_date, end_date))
        return df

    def plot_department_kpi(self, department_id, start_date, end_date, output_path):
        df = self.get_department_kpi(department_id, start_date, end_date)
        if df.empty:
            return

        plt.figure(figsize=(10, 6))
        for metric in df['metric_name'].unique():
            metric_data = df[df['metric_name'] == metric]
            plt.plot(metric_data['metric_date'], metric_data['metric_value'], label=metric)

        plt.title(f"Department KPI Metrics (ID: {department_id})")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()