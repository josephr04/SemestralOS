import os
import platform
import subprocess
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from PIL import Image


def generar_pdf_plato(datos_plato, ruta_imagen=None):
    """
    Genera un PDF con la información del plato.
    
    Args:
        datos_plato: tupla con (ID, Nombre, Precio, Imagen, Fecha)
        ruta_imagen: ruta completa a la imagen del plato
    
    Returns:
        str: ruta del archivo PDF generado
    """
    # Desempaquetar según el nuevo orden: ID, Nombre, Precio, Imagen, Fecha
    id_plato, nombre, precio, imagen_filename, fecha_creacion = datos_plato
    
    # Crear archivo temporal para el PDF
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf_path = temp_pdf.name
    temp_pdf.close()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Contenedor para los elementos
    elementos = []
    
    # Estilos
    estilos = getSampleStyleSheet()
    
    # Estilo para el título
    estilo_titulo = ParagraphStyle(
        'CustomTitle',
        parent=estilos['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#4ECDC4'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    estilo_normal = ParagraphStyle(
        'CustomNormal',
        parent=estilos['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=15,
        fontName='Helvetica'
    )
    
    # Título principal
    titulo = Paragraph("INFORMACIÓN DEL PLATO", estilo_titulo)
    elementos.append(titulo)
    
    elementos.append(Spacer(1, 30))  # Espacio adicional
    
    # Agregar imagen si existe
    if ruta_imagen and os.path.exists(ruta_imagen):
        try:
            # Abrir y redimensionar la imagen
            img = Image.open(ruta_imagen)
            
            # Calcular dimensiones manteniendo aspecto
            max_width = 4 * inch
            max_height = 4 * inch
            
            img_width, img_height = img.size
            aspect = img_height / float(img_width)
            
            if img_width > max_width:
                img_width = max_width
                img_height = img_width * aspect
            
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect
            
            # Agregar imagen al PDF
            imagen_pdf = RLImage(ruta_imagen, width=img_width, height=img_height)
            elementos.append(imagen_pdf)
            elementos.append(Spacer(1, 20))
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
    
    # Crear tabla con la información
    # Convertir precio a float si es string
    try:
        precio_float = float(precio)
        precio_formateado = f'${precio_float:.2f}'
    except (ValueError, TypeError):
        precio_formateado = f'${precio}'
    
    datos_tabla = [
        ['Campo', 'Información'],
        ['Nombre', nombre],
        ['Precio', precio_formateado],
        ['Fecha de Creación', fecha_creacion],
        ['Imagen', imagen_filename if imagen_filename else 'Sin imagen'],
    ]
    
    tabla = Table(datos_tabla, colWidths=[2*inch, 4*inch])
    
    # Estilo de la tabla
    tabla.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4ECDC4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Primera columna (etiquetas)
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f0f0f0')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (0, -1), 10),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.HexColor('#555555')),
        
        # Segunda columna (valores)
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 1), (1, -1), 11),
        ('TEXTCOLOR', (1, 1), (1, -1), colors.HexColor('#333333')),
        
        # Bordes y alineación
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elementos.append(tabla)
    elementos.append(Spacer(1, 30))
    
    # Footer
    footer_texto = "<i>Restaurante App - Sistema de Gestión de Platos</i>"
    footer = Paragraph(footer_texto, estilo_normal)
    elementos.append(footer)
    
    # Construir PDF
    doc.build(elementos)
    
    return pdf_path