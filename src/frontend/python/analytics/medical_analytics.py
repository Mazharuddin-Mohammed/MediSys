import pandas as pd
import matplotlib.pyplot as plt
import medisys_bindings
from datetime import datetime

class MedicalAnalytics:
    def __init__(self, db):
        self.db = db

    def get_patient_metrics(self, patient_id, start_date, end_date):
        query = """
        SELECT metric_name, metric_value, metric_date, trend
        FROM medical_analytics
        WHERE patient_id = %s AND metric_date BETWEEN %s AND %s
        ORDER BY metric_date
        """
        conn = self.db.getConnection()
        df = pd.read_sql_query(query, conn, params=(patient_id, start_date, end_date))
        return df

    def plot_patient_metrics(self, patient_id, start_date, end_date, output_path):
        df = self.get_patient_metrics(patient_id, start_date, end_date)
        if df.empty:
            return

        plt.figure(figsize=(10, 6))
        for metric in df['metric_name'].unique():
            metric_data = df[df['metric_name'] == metric]
            plt.plot(metric_data['metric_date'], metric_data['metric_value'], label=metric)

        plt.title(f"Patient Medical Metrics (ID: {patient_id})")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()

    def get_trend_summary(self, patient_id, start_date, end_date):
        df = self.get_patient_metrics(patient_id, start_date, end_date)
        if df.empty:
            return {}

        trends = df.groupby('metric_name')['trend'].last().to_dict()
        return trends