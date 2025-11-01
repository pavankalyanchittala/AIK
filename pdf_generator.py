"""
PDF Generator for Complaints and FIR
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os


class ComplaintPDFGenerator:
    """Generate PDF for complaints and FIR"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles()
    
    def custom_styles(self):
        """Create custom styles for the PDF"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
    
    def generate_complaint_pdf(self, complaint_data, filename="complaint.pdf"):
        """Generate a complaint PDF"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("COMPLAINT FORM", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Date and time
        date_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
        date_para = Paragraph(f"<b>Date:</b> {date_str}", self.styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 0.2*inch))
        
        # Police Station - Clean format
        if complaint_data.get('police_station'):
            # Clean the police station name
            ps_name = str(complaint_data['police_station'])
            # Remove markdown and extra text
            ps_name = ps_name.replace('**', '').replace('*', '').split('\n')[0].strip()
            # If it's too long, truncate
            if len(ps_name) > 200:
                ps_name = ps_name[:200] + "..."
            
            ps_para = Paragraph(f"<b>To:</b> {ps_name}", self.styles['Normal'])
            story.append(ps_para)
            story.append(Spacer(1, 0.3*inch))
        
        # Personal Details Section
        story.append(Paragraph("<b>COMPLAINANT DETAILS</b>", self.heading_style))
        
        personal_data = [
            ["Name:", complaint_data.get('name', 'N/A')],
            ["Father's/Husband's Name:", complaint_data.get('father_name', 'N/A')],
            ["Age:", complaint_data.get('age', 'N/A')],
            ["Phone:", complaint_data.get('phone', 'N/A')],
            ["Email:", complaint_data.get('email', 'N/A')],
            ["Address:", complaint_data.get('address', 'N/A')],
        ]
        
        personal_table = Table(personal_data, colWidths=[2*inch, 4*inch])
        personal_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(personal_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Complaint Details Section
        story.append(Paragraph("<b>COMPLAINT DETAILS</b>", self.heading_style))
        
        if complaint_data.get('complaint_type'):
            type_para = Paragraph(f"<b>Type of Complaint:</b> {complaint_data['complaint_type']}", self.styles['Normal'])
            story.append(type_para)
            story.append(Spacer(1, 0.1*inch))
        
        if complaint_data.get('incident_date'):
            date_para = Paragraph(f"<b>Date of Incident:</b> {complaint_data['incident_date']}", self.styles['Normal'])
            story.append(date_para)
            story.append(Spacer(1, 0.1*inch))
        
        if complaint_data.get('incident_location'):
            loc_para = Paragraph(f"<b>Place of Incident:</b> {complaint_data['incident_location']}", self.styles['Normal'])
            story.append(loc_para)
            story.append(Spacer(1, 0.1*inch))
        
        if complaint_data.get('description'):
            story.append(Spacer(1, 0.1*inch))
            desc_para = Paragraph(f"<b>Detailed Description:</b><br/>{complaint_data['description']}", self.styles['Normal'])
            story.append(desc_para)
            story.append(Spacer(1, 0.2*inch))
        
        # Applicable Laws Section
        if complaint_data.get('applicable_laws'):
            story.append(Paragraph("<b>APPLICABLE LAWS/SECTIONS</b>", self.heading_style))
            laws_para = Paragraph(complaint_data['applicable_laws'], self.styles['Normal'])
            story.append(laws_para)
            story.append(Spacer(1, 0.3*inch))
        
        # Police Station Full Details Section (if available)
        if complaint_data.get('police_details'):
            story.append(Paragraph("<b>POLICE STATION DETAILS</b>", self.heading_style))
            
            # Clean police details for PDF
            police_details = str(complaint_data['police_details'])
            # Remove markdown formatting
            police_details = police_details.replace('**', '').replace('###', '').replace('##', '').replace('*', '')
            # Replace emojis with text
            police_details = police_details.replace('📍', 'Address:').replace('📞', 'Phone:').replace('✅', 'Jurisdiction:').replace('⚠️', 'Note:')
            
            police_para = Paragraph(police_details, self.styles['Normal'])
            story.append(police_para)
            story.append(Spacer(1, 0.3*inch))
        
        # Signature Section
        story.append(Spacer(1, 0.5*inch))
        signature_data = [
            ["", ""],
            ["", ""],
            ["Place: Kakinada", "Signature of Complainant"],
            [f"Date: {datetime.now().strftime('%d-%m-%Y')}", f"Name: {complaint_data.get('name', '')}"]
        ]
        
        sig_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(sig_table)
        
        # Footer note
        story.append(Spacer(1, 0.3*inch))
        footer_text = """<i>Note: This is a computer-generated complaint form. Please review all details carefully before submission. 
        It is advisable to consult with a legal professional before filing. Attach any supporting documents and evidence.</i>"""
        footer_para = Paragraph(footer_text, self.styles['Normal'])
        story.append(footer_para)
        
        # Build PDF
        doc.build(story)
        return filename
    
    def generate_fir_pdf(self, fir_data, filename="fir_draft.pdf"):
        """Generate an FIR draft PDF"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("FIRST INFORMATION REPORT (FIR) - DRAFT", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Date and time
        date_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
        date_para = Paragraph(f"<b>Date:</b> {date_str}", self.styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 0.2*inch))
        
        # Police Station
        if fir_data.get('police_station'):
            ps_para = Paragraph(f"<b>To:</b> {fir_data['police_station']}", self.styles['Normal'])
            story.append(ps_para)
            story.append(Spacer(1, 0.3*inch))
        
        # Informant Details Section
        story.append(Paragraph("<b>INFORMANT/COMPLAINANT DETAILS</b>", self.heading_style))
        
        informant_data = [
            ["Name:", fir_data.get('name', 'N/A')],
            ["Father's/Husband's Name:", fir_data.get('father_name', 'N/A')],
            ["Age:", fir_data.get('age', 'N/A')],
            ["Occupation:", fir_data.get('occupation', 'N/A')],
            ["Phone:", fir_data.get('phone', 'N/A')],
            ["Address:", fir_data.get('address', 'N/A')],
        ]
        
        informant_table = Table(informant_data, colWidths=[2*inch, 4*inch])
        informant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(informant_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Crime Details Section
        story.append(Paragraph("<b>CRIME/INCIDENT DETAILS</b>", self.heading_style))
        
        crime_data = [
            ["Type of Crime:", fir_data.get('crime_type', 'N/A')],
            ["Date & Time of Incident:", fir_data.get('incident_datetime', 'N/A')],
            ["Place of Incident:", fir_data.get('incident_location', 'N/A')],
        ]
        
        crime_table = Table(crime_data, colWidths=[2*inch, 4*inch])
        crime_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(crime_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Accused Details (if any)
        if fir_data.get('accused_details'):
            story.append(Paragraph("<b>ACCUSED DETAILS</b>", self.heading_style))
            accused_para = Paragraph(fir_data['accused_details'], self.styles['Normal'])
            story.append(accused_para)
            story.append(Spacer(1, 0.2*inch))
        
        # Detailed Description
        if fir_data.get('description'):
            story.append(Paragraph("<b>DETAILED DESCRIPTION OF INCIDENT</b>", self.heading_style))
            desc_para = Paragraph(fir_data['description'], self.styles['Normal'])
            story.append(desc_para)
            story.append(Spacer(1, 0.2*inch))
        
        # Applicable Laws Section
        if fir_data.get('applicable_laws'):
            story.append(Paragraph("<b>APPLICABLE LAWS/SECTIONS</b>", self.heading_style))
            laws_para = Paragraph(fir_data['applicable_laws'], self.styles['Normal'])
            story.append(laws_para)
            story.append(Spacer(1, 0.3*inch))
        
        # Signature Section
        story.append(Spacer(1, 0.3*inch))
        signature_data = [
            ["", ""],
            ["Place: Kakinada", "Signature of Informant"],
            [f"Date: {datetime.now().strftime('%d-%m-%Y')}", f"Name: {fir_data.get('name', '')}"]
        ]
        
        sig_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(sig_table)
        
        # Footer note
        story.append(Spacer(1, 0.3*inch))
        footer_text = """<i><b>IMPORTANT:</b> This is a draft FIR for your reference. Please visit the police station in person to file the actual FIR. 
        Carry original documents, evidence, and witness details if available. You have the right to get a copy of the FIR.
        For serious crimes, immediate police assistance can be obtained by calling 100 (Police Emergency) or 112 (National Emergency Number).</i>"""
        footer_para = Paragraph(footer_text, self.styles['Normal'])
        story.append(footer_para)
        
        # Build PDF
        doc.build(story)
        return filename


# Helper function
def create_complaint_pdf(complaint_data, filename="complaint.pdf"):
    """Helper function to create complaint PDF"""
    generator = ComplaintPDFGenerator()
    return generator.generate_complaint_pdf(complaint_data, filename)


def create_fir_pdf(fir_data, filename="fir_draft.pdf"):
    """Helper function to create FIR PDF"""
    generator = ComplaintPDFGenerator()
    return generator.generate_fir_pdf(fir_data, filename)

