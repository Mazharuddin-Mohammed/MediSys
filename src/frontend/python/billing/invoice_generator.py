from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime

def generate_invoice(patient_name, transaction_id, amount, description, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Add banner
    c.drawImage("src/frontend/python/resources/images/banner.jpg", 0.5 * inch, height - 1.5 * inch, width=7 * inch, height=1 * inch)

    # Invoice details
    c.setFont("Helvetica", 12)
    c.drawString(0.5 * inch, height - 2.5 * inch, f"Invoice #{transaction_id}")
    c.drawString(0.5 * inch, height - 2.75 * inch, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(0.5 * inch, height - 3 * inch, f"Patient: {patient_name}")
    c.drawString(0.5 * inch, height - 3.25 * inch, f"Amount: ${amount:.2f}")
    c.drawString(0.5 * inch, height - 3.5 * inch, f"Description: {description}")

    c.showPage()
    c.save()