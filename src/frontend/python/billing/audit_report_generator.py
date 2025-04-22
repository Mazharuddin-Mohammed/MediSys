from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import pandas as pd
import medisys_bindings

class AuditReportGenerator:
    def __init__(self, db, logo_path="src/frontend/python/resources/images/logo.jpg",
                 banner_path="src/frontend/python/resources/images/banner.jpg"):
        """
        Initialize the audit report generator.

        Args:
            db: medisys_bindings.DBManager instance for database access.
            logo_path (str): Path to MediSys logo image.
            banner_path (str): Path to MediSys banner image.
        """
        self.db = db
        self.logo_path = logo_path
        self.banner_path = banner_path
        self.styles = getSampleStyleSheet()

    def fetch_audit_data(self, start_date, end_date, user_id=None, entity_type=None):
        """
        Fetch audit log data from the database with optional filters.

        Args:
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.
            user_id (int, optional): Filter by user ID.
            entity_type (str, optional): Filter by entity type (e.g., 'patient', 'transaction').

        Returns:
            pandas.DataFrame: Audit log data.
        """
        query = """
        SELECT u.username, al.action, al.entity_type, al.entity_id,
               al.details, al.ip_address, al.session_id, al.created_at
        FROM audit_log al
        LEFT JOIN users u ON al.user_id = u.id
        WHERE al.created_at BETWEEN %s AND %s
        """
        params = [start_date, end_date]

        if user_id:
            query += " AND al.user_id = %s"
            params.append(user_id)
        if entity_type:
            query += " AND al.entity_type = %s"
            params.append(entity_type)

        query += " ORDER BY al.created_at DESC"

        conn = self.db.get_connection()
        df = pd.read_sql_query(query, conn, params=params)
        return df

    def generate_report(self, output_path, start_date, end_date, user_id=None,
                       entity_type=None, admin_user_id=0, ip_address="unknown", session_id="unknown"):
        """
        Generate a PDF audit report with logo and banner.

        Args:
            output_path (str): Path to save the PDF.
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.
            user_id (int, optional): Filter by user ID.
            entity_type (str, optional): Filter by entity type.
            admin_user_id (int): ID of the admin generating the report (for audit logging).
            ip_address (str): IP address of the admin (for audit logging).
            session_id (str): Session ID of the admin (for audit logging).
        """
        # Log report generation action
        self.db.set_audit_context(admin_user_id, ip_address, session_id)
        conn = self.db.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT log_audit_action(%s, %s, %s, %s, %s, %s, %s)
            """, (
                admin_user_id,
                "generate_audit_report",
                "audit_report",
                0,
                {"start_date": start_date, "end_date": end_date,
                 "user_id": user_id, "entity_type": entity_type},
                ip_address,
                session_id
            ))
            conn.commit()

        # Fetch audit data
        df = self.fetch_audit_data(start_date, end_date, user_id, entity_type)
        if df.empty:
            raise ValueError("No audit data found for the specified criteria")

        # Setup PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                               leftMargin=0.5*inch, rightMargin=0.5*inch,
                               topMargin=1.5*inch, bottomMargin=0.5*inch)
        elements = []

        # Header with logo and banner
        c = canvas.Canvas("temp.pdf")  # Temporary canvas for header
        c.drawImage(self.banner_path, 0.5*inch, letter[1] - 1.5*inch,
                    width=7.5*inch, height=1*inch)
        c.drawImage(self.logo_path, 0.5*inch, letter[1] - 2*inch,
                    width=0.5*inch, height=0.5*inch)
        c.showPage()
        c.save()

        # Title
        title = Paragraph("MediSys Audit Report", self.styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))

        # Report details
        details = Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
            f"Period: {start_date} to {end_date}<br/>"
            f"Filters: User ID = {user_id or 'All'}, Entity Type = {entity_type or 'All'}",
            self.styles['Normal']
        )
        elements.append(details)
        elements.append(Spacer(1, 0.2*inch))

        # Table data
        data = [["Username", "Action", "Entity Type", "Entity ID", "Details",
                 "IP Address", "Session ID", "Timestamp"]]
        for _, row in df.iterrows():
            details_str = str(row['details'])[:50] + "..." if len(str(row['details'])) > 50 else str(row['details'])
            data.append([
                row['username'] or "Unknown",
                row['action'],
                row['entity_type'],
                str(row['entity_id']),
                details_str,
                row['ip_address'] or "N/A",
                row['session_id'] or "N/A",
                row['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            ])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(table)

        # Build PDF
        doc.build(elements, onFirstPage=self._add_header_footer,
                  onLaterPages=self._add_header_footer)

    def _add_header_footer(self, canvas, doc):
        """
        Add header (logo and banner) and footer (page number) to each page.

        Args:
            canvas: ReportLab canvas object.
            doc: ReportLab document object.
        """
        # Header
        canvas.drawImage(self.banner_path, 0.5*inch, letter[1] - 1.5*inch,
                         width=7.5*inch, height=1*inch)
        canvas.drawImage(self.logo_path, 0.5*inch, letter[1] - 2*inch,
                         width=0.5*inch, height=0.5*inch)

        # Footer
        canvas.saveState()
        canvas.setFont('Helvetica', 10)
        page_number = f"Page {doc.page}"
        canvas.drawString(0.5*inch, 0.3*inch, page_number)
        canvas.drawRightString(letter[0] - 0.5*inch, 0.3*inch,
                              f"Generated by MediSys on {datetime.now().strftime('%Y-%m-%d')}")
        canvas.restoreState()