import pandas as pd
from io import BytesIO
from typing import List, Dict, Any
import csv
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

class ExportService:
    """Service for exporting client data in various formats"""
    
    def export_to_excel(self, clients: List[Dict[str, Any]]) -> bytes:
        """Export client data to Excel format"""
        # Create DataFrame
        df = pd.DataFrame(clients)
        
        # Rename columns for better display
        column_mapping = {
            'id_cliente': 'ID',
            'cpf': 'CPF',
            'nome_completo': 'Nome Completo',
            'data_nascimento': 'Data de Nascimento',
            'sexo': 'Sexo',
            'nome_mae': 'Nome da Mãe',
            'cidade': 'Cidade',
            'uf': 'UF',
            'ativo': 'Status',
            'created_at': 'Data de Cadastro'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Format dates
        if 'Data de Nascimento' in df.columns:
            df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento']).dt.strftime('%d/%m/%Y')
        if 'Data de Cadastro' in df.columns:
            df['Data de Cadastro'] = pd.to_datetime(df['Data de Cadastro']).dt.strftime('%d/%m/%Y %H:%M')
        
        # Format CPF
        if 'CPF' in df.columns:
            df['CPF'] = df['CPF'].apply(lambda x: f"{x[:3]}.{x[3:6]}.{x[6:9]}-{x[9:]}" if len(x) == 11 else x)
        
        # Format sex
        if 'Sexo' in df.columns:
            df['Sexo'] = df['Sexo'].map({'M': 'Masculino', 'F': 'Feminino'})
        
        # Format status
        if 'Status' in df.columns:
            df['Status'] = df['Status'].map({True: 'Ativo', False: 'Inativo'})
        
        # Create Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Clientes', index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Clientes']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Add header formatting
            from openpyxl.styles import Font, PatternFill, Alignment
            
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
        
        output.seek(0)
        return output.getvalue()
    
    def export_to_csv(self, clients: List[Dict[str, Any]]) -> bytes:
        """Export client data to CSV format"""
        # Create DataFrame
        df = pd.DataFrame(clients)
        
        # Rename columns
        column_mapping = {
            'id_cliente': 'ID',
            'cpf': 'CPF',
            'nome_completo': 'Nome Completo',
            'data_nascimento': 'Data de Nascimento',
            'sexo': 'Sexo',
            'nome_mae': 'Nome da Mãe',
            'cidade': 'Cidade',
            'uf': 'UF',
            'ativo': 'Status',
            'created_at': 'Data de Cadastro'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Format data
        if 'Data de Nascimento' in df.columns:
            df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento']).dt.strftime('%d/%m/%Y')
        if 'Data de Cadastro' in df.columns:
            df['Data de Cadastro'] = pd.to_datetime(df['Data de Cadastro']).dt.strftime('%d/%m/%Y %H:%M')
        
        # Format sex
        if 'Sexo' in df.columns:
            df['Sexo'] = df['Sexo'].map({'M': 'Masculino', 'F': 'Feminino'})
        
        # Format status
        if 'Status' in df.columns:
            df['Status'] = df['Status'].map({True: 'Ativo', False: 'Inativo'})
        
        # Create CSV
        output = BytesIO()
        df.to_csv(output, index=False, encoding='utf-8-sig', sep=';')
        output.seek(0)
        return output.getvalue()
    
    def export_to_pdf(self, clients: List[Dict[str, Any]]) -> bytes:
        """Export client data to PDF format"""
        output = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Title
        title = Paragraph("Relatório de Clientes", title_style)
        elements.append(title)
        
        # Date
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        date_para = Paragraph(f"Data de geração: {date_str}", styles['Normal'])
        elements.append(date_para)
        elements.append(Spacer(1, 20))
        
        # Prepare data for table
        headers = ['ID', 'Nome', 'CPF', 'Data Nasc.', 'Sexo', 'Cidade', 'UF', 'Status']
        data = [headers]
        
        for client in clients:
            row = [
                str(client.get('id_cliente', '')),
                client.get('nome_completo', ''),
                self._format_cpf(client.get('cpf', '')),
                self._format_date(client.get('data_nascimento', '')),
                self._format_sex(client.get('sexo', '')),
                client.get('cidade', ''),
                client.get('uf', ''),
                'Ativo' if client.get('ativo') else 'Inativo'
            ]
            data.append(row)
        
        # Create table
        table = Table(data)
        
        # Table style
        table.setStyle(TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data style
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        # Adjust column widths
        col_widths = [30, 150, 100, 80, 40, 100, 30, 50]
        table._argW = col_widths
        
        elements.append(table)
        
        # Footer with total count
        elements.append(Spacer(1, 20))
        total_para = Paragraph(f"Total de clientes: {len(clients)}", styles['Normal'])
        elements.append(total_para)
        
        # Build PDF
        doc.build(elements)
        
        output.seek(0)
        return output.getvalue()
    
    def _format_cpf(self, cpf: str) -> str:
        """Format CPF with dots and dash"""
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    
    def _format_date(self, date_str: str) -> str:
        """Format date string to Brazilian format"""
        if not date_str:
            return ""
        try:
            date_obj = pd.to_datetime(date_str)
            return date_obj.strftime('%d/%m/%Y')
        except:
            return str(date_str)
    
    def _format_sex(self, sex: str) -> str:
        """Format sex code to full text"""
        mapping = {'M': 'Masculino', 'F': 'Feminino'}
        return mapping.get(sex, sex)
