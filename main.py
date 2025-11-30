import tkinter as tk
import unicodedata
import shutil
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from customtkinter import CTkImage
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk
import platform
import subprocess
import io
import os
from crud import agregar_plato, obtener_platos, actualizar_plato, eliminar_plato, existe_plato
from validaciones import validar_dinero

COLOR_BG = "#f9f9f9"
COLOR_ACCENT = "#FF6B6B"
COLOR_BTN = "#4ECDC4"
COLOR_IMP = "#2d3741"
COLOR_TXT = "#333"
FUENTE_TXT = "Inter" 

class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍴 Restaurante App")

        ancho, alto = 900, 600
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2) - 50
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.root.config(bg=COLOR_BG)
        self.ventana_platos()

    # --- VENTANA DE PLATOS ---
    def ventana_platos(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if not hasattr(self, 'titulo_original'):
            self.titulo_original = self.root.title()

        self.root.title("📋 Gestión de Platos")

        self.root.geometry("900x600")
        frame = tk.Frame(self.root, bg=COLOR_BG)
        frame.pack(expand=True)

        tk.Label(frame, text="Gestión de Platos", font=(FUENTE_TXT, 25, "bold"), bg=COLOR_BG, fg=COLOR_TXT).pack(pady=10)

        form = tk.Frame(frame, bg=COLOR_BG)
        form.pack(pady=10)

        vcmd = self.root.register(validar_dinero)
        
        # Campos
        self._add_field(form, "Nombre:", 0)

        # Campo de Precio con validación
        tk.Label(form, text="Precio:", bg=COLOR_BG, fg=COLOR_TXT, anchor="w", font=(FUENTE_TXT, 12)).grid(
        row=2, column=0, sticky="w", pady=5)
        self.precio_var = tk.StringVar()
        entry_precio = ctk.CTkEntry(
            form,
            textvariable=self.precio_var,
            height=21,
            width=185,
            border_width=1,
            border_color="#A2A2A2",
            corner_radius=0,
            fg_color="#ffffff",
            text_color="black",
            placeholder_text="Precio...",
            validate="key",
            validatecommand=(vcmd, "%P")
        )
        entry_precio.grid(row=2, column=1, columnspan=2, pady=5)

        # Campo de Fecha de Creación
        tk.Label(form, text="Fecha de Creación:", bg=COLOR_BG, fg=COLOR_TXT, anchor="w", font=(FUENTE_TXT, 12)).grid(
            row=3, column=0, sticky="w", pady=5)
        self.fecha_var = tk.StringVar()
        
        # Establecer fecha actual por defecto
        from datetime import datetime
        self.fecha_var.set(datetime.now().strftime("%Y-%m-%d"))

        entry_fecha = ctk.CTkEntry(
            form,
            textvariable=self.fecha_var,
            height=21,
            width=185,
            border_width=1,
            border_color="#A2A2A2",
            corner_radius=0,
            fg_color="#ffffff",
            text_color="#8D8D8D",
            placeholder_text="YYYY-MM-DD",
            state="disabled"
        )
        entry_fecha.grid(row=3, column=1, columnspan=2, pady=5)

        tk.Label(form, text="Imagen:", bg=COLOR_BG, fg=COLOR_TXT, anchor="w", font=(FUENTE_TXT, 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.imagen_path = tk.StringVar()
        ctk.CTkEntry(
            form,
            textvariable=self.imagen_path,
            height=21,
            width=180,
            border_width=1,
            border_color="#A2A2A2",
            corner_radius=0,
            fg_color="#ffffff",
            text_color="black",
            placeholder_text="Ruta de la imagen..."
        ).grid(row=4, column=1, pady=5)

        ctk.CTkButton(form, 
            text="Seleccionar",
            font=(FUENTE_TXT, 12, "bold"),
            fg_color=COLOR_BTN,
            hover_color="#119b97",
            text_color="white",
            corner_radius=6,    
            width=80,
            height=21,
            cursor="hand2",
            command=self.seleccionar_imagen).grid(row=4, column=2, padx=5)

        # Miniatura
        placeholder = Image.new('RGB', (188, 188), color='#ddd')
        self.placeholder_img = ImageTk.PhotoImage(placeholder)

        # Miniatura con texto centrado sobre la imagen
        self.preview = tk.Label(
            form,
            bg="#ddd",
            image=self.placeholder_img,
            text="Sin imagen",
            compound="center",  # <-- texto centrado sobre la imagen
            font=("Arial", 12, "italic"),
            fg="#555"  # <-- color del texto
        )
        self.preview.grid(row=0, column=3, rowspan=5, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(frame, bg=COLOR_BG)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, 
            text="➕ Agregar",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color=COLOR_ACCENT,
            hover_color="#e6734d",
            text_color="white",
            corner_radius=6,
            width=80,
            height=22,
            cursor="hand2",
            command=self.agregar).pack(side="left", padx=8)   
             
        ctk.CTkButton(btn_frame, 
            text="✏️ Actualizar",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color=COLOR_BTN,
            hover_color="#119b97",
            text_color="white",
            corner_radius=6,
            width=80,
            height=22,
            cursor="hand2",
            command=self.actualizar).pack(side="left", padx=8)
            
        ctk.CTkButton(btn_frame, 
            text="❌ Eliminar",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color="#E94E77",
            hover_color="#d63860",
            text_color="white",
            corner_radius=6,
            width=80,
            height=22,
            cursor="hand2",
            command=self.eliminar).pack(side="left", padx=8)
        
        ctk.CTkButton(btn_frame, 
            text="🧹 Limpiar",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color="#999",
            hover_color="#777",
            text_color="white",
            corner_radius=6,
            width=80,
            height=22,
            cursor="hand2",
            command=self.limpiar).pack(side="left", padx=8)
        
        ctk.CTkButton(btn_frame, 
            text="📄 Imprimir",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color="#555",
            hover_color="#333",
            text_color="white",
            corner_radius=6,
            width=80,
            height=22,
            cursor="hand2",
            command=self.imprimir).pack(side="left", padx=8) # <- Funcion para imprimir platos!!

        # ====================================================================
        # TABLA CON ESTILOS PERSONALIZADOS PARA CUSTOMTKINTER
        # ====================================================================
        
        # Frame contenedor para la tabla y scrollbar
        tabla_frame = tk.Frame(frame, bg=COLOR_BG)
        tabla_frame.pack(pady=10, padx=20, fill="both", expand=True)  # ← Agregado padx=20 para márgenes laterales

        # Configurar estilo de la tabla
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Colores que combinan con CustomTkinter (mismos que categorías)
        estilo.configure("Custom.Treeview",
            background="#FFFFFF",
            foreground="#333333",
            fieldbackground="#FFFFFF",
            borderwidth=1,
            font=(FUENTE_TXT, 12),
            rowheight=30)

        estilo.configure("Custom.Treeview.Heading",
            background=COLOR_BTN,          # #14b0ab (turquesa)
            foreground="white",
            borderwidth=1,
            relief="flat",
            font=(FUENTE_TXT, 13, 'bold'))

        # Colores cuando seleccionas una fila
        estilo.map('Custom.Treeview',
            background=[('selected', COLOR_ACCENT)],   # #ff825a (naranja)
            foreground=[('selected', 'white')])

        # Color cuando pasas el mouse sobre el encabezado
        estilo.map('Custom.Treeview.Heading',
            background=[('active', '#119b97')])        # Un poco más oscuro que COLOR_BTN

        # Crear Treeview con el estilo personalizado
        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=("ID", "Nombre", "Precio", "Imagen", "FechaCreacion"),
            show="headings",
            height=10,
            style="Custom.Treeview"
        )

        # Configurar columnas
        self.tabla.heading("ID", text="ID")
        self.tabla.column("ID", anchor="center", width=50, minwidth=50)

        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.column("Nombre", anchor="center", width=190, minwidth=100)

        self.tabla.heading("Precio", text="Precio")
        self.tabla.column("Precio", anchor="center", width=100, minwidth=80)

        self.tabla.heading("Imagen", text="Imagen")
        self.tabla.column("Imagen", anchor="center", width=150, minwidth=100)

        self.tabla.heading("FechaCreacion", text="Fecha Creación")
        self.tabla.column("FechaCreacion", anchor="center", width=150, minwidth=100)

        # Scrollbar personalizada con CustomTkinter
        scrollbar = ctk.CTkScrollbar(tabla_frame, command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_tabla)

        self.cargar_tabla()

    def ventana_vista_previa(self, pdf_path, datos_plato):
        """
        Muestra una vista previa del PDF dentro de la misma ventana de la aplicación.
        Usa PyMuPDF (fitz) en lugar de pdf2image - NO requiere Poppler.
        """
        
        try:
            import fitz  # PyMuPDF
        except ImportError:
            # Si no está instalado, mostrar mensaje
            messagebox.showerror(
                "Biblioteca faltante",
                "Para ver la vista previa necesitas instalar PyMuPDF:\n\n"
                "pip install PyMuPDF\n\n"
                "Por ahora se abrirá el PDF en tu visor externo."
            )
            # Abrir en visor externo como alternativa
            sistema = platform.system()
            if sistema == 'Windows':
                os.startfile(pdf_path)
            elif sistema == 'Linux':
                subprocess.Popen(['xdg-open', pdf_path])
            return
        
        # Limpiar ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("📄 Vista Previa de Impresión")
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg=COLOR_BG)
        frame_principal.pack(fill="both", expand=True)
        
        # Header con título
        header = tk.Frame(frame_principal, bg=COLOR_BTN, height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"Vista Previa: {datos_plato[1]}",
            font=(FUENTE_TXT, 18, "bold"),
            bg=COLOR_BTN,
            fg="white"
        ).pack(side="left", padx=20, pady=15)
        
        # Frame para los botones superiores
        frame_botones_top = tk.Frame(header, bg=COLOR_BTN)
        frame_botones_top.pack(side="right", padx=20)
        
        # Botón volver
        ctk.CTkButton(
            frame_botones_top,
            text="← Volver",
            font=(FUENTE_TXT, 12, "bold"),
            fg_color="#555",
            hover_color="#333",
            text_color="white",
            corner_radius=6,
            width=100,
            height=30,
            cursor="hand2",
            command=self.ventana_platos
        ).pack(side="left", padx=5)
        
        # Frame para el contenido (imagen del PDF)
        frame_contenido = tk.Frame(frame_principal, bg=COLOR_BG)
        frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Canvas con scrollbar para mostrar el PDF
        canvas = tk.Canvas(frame_contenido, bg="white", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(frame_contenido, command=canvas.yview)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Frame interno para las páginas
        frame_paginas = tk.Frame(canvas, bg="white")
        canvas_window = canvas.create_window((0, 0), window=frame_paginas, anchor="nw")
        
        # Convertir PDF a imágenes usando PyMuPDF
        try:
            # Abrir el PDF con PyMuPDF
            pdf_documento = fitz.open(pdf_path)
            
            # Mostrar cada página
            self.imagenes_tk = []  # Mantener referencia
            
            for num_pagina in range(len(pdf_documento)):
                # Obtener la página
                pagina = pdf_documento[num_pagina]
                
                # Renderizar la página como imagen (zoom para mejor calidad)
                zoom = 2  # Mayor zoom = mejor calidad
                mat = fitz.Matrix(zoom, zoom)
                pix = pagina.get_pixmap(matrix=mat)
                
                # Convertir a PIL Image
                img_data = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_data))
                
                # Redimensionar para que quepa bien en la ventana
                ancho_max = 700
                ratio = ancho_max / img.width
                nuevo_alto = int(img.height * ratio)
                img_resized = img.resize((ancho_max, nuevo_alto), Image.Resampling.LANCZOS)
                
                # Convertir a PhotoImage
                img_tk = ImageTk.PhotoImage(img_resized)
                self.imagenes_tk.append(img_tk)
                
                # Mostrar la imagen
                label_img = tk.Label(frame_paginas, image=img_tk, bg="white")
                label_img.pack(pady=10)
                
                # Separador entre páginas (si hay más de una)
                if num_pagina < len(pdf_documento) - 1:
                    tk.Frame(frame_paginas, bg="#ddd", height=2).pack(fill="x", pady=5)
            
            # Cerrar el documento PDF
            pdf_documento.close()
            
            # Actualizar región de scroll
            frame_paginas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            
            # Ajustar ancho del canvas al frame
            def ajustar_ancho(event):
                canvas.itemconfig(canvas_window, width=event.width)
            canvas.bind('<Configure>', ajustar_ancho)
            
        except Exception as e:
            tk.Label(
                frame_paginas,
                text=f"⚠️ No se pudo cargar la vista previa\n\n{str(e)}\n\n"
                    "Instala PyMuPDF con:\npip install PyMuPDF",
                font=(FUENTE_TXT, 12),
                bg="white",
                fg="#666",
                justify="center"
            ).pack(pady=50)
        
        # Frame inferior con botones de acción
        frame_botones = tk.Frame(frame_principal, bg=COLOR_BG, height=80)
        frame_botones.pack(fill="x", side="bottom")
        frame_botones.pack_propagate(False)
        
        botones_container = tk.Frame(frame_botones, bg=COLOR_BG)
        botones_container.pack(expand=True)

        def imprimir_directo():
            """Imprime el PDF directamente usando win32print en Windows"""
            import platform
            import subprocess
            import tempfile
            import time
            
            sistema = platform.system()
            
            try:
                if sistema == 'Windows':
                    # ===== IMPRESIÓN DIRECTA EN WINDOWS CON WIN32PRINT =====
                    try:
                        import win32print
                        import win32ui
                        from PIL import Image as PILImage, ImageWin
                        import fitz  # PyMuPDF
                        
                        # Obtener impresora predeterminada
                        printer_name = win32print.GetDefaultPrinter()
                        
                        # Crear contexto de impresión
                        hDC = win32ui.CreateDC()
                        hDC.CreatePrinterDC(printer_name)
                        hDC.StartDoc(f"Plato - {datos_plato[1]}")
                        hDC.StartPage()
                        
                        # Convertir PDF a imagen de alta resolución
                        pdf_doc = fitz.open(pdf_path)
                        pagina = pdf_doc[0]  # Primera página
                        
                        # Renderizar con alta resolución (300 DPI)
                        zoom = 3  # zoom 3 = aproximadamente 300 DPI
                        mat = fitz.Matrix(zoom, zoom)
                        pix = pagina.get_pixmap(matrix=mat)
                        
                        # Guardar temporalmente como PNG
                        temp_img_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                        temp_img_path = temp_img_file.name
                        temp_img_file.close()
                        
                        pix.save(temp_img_path)
                        
                        # Abrir imagen con PIL
                        bmp = PILImage.open(temp_img_path)
                        dib = ImageWin.Dib(bmp)
                        
                        # Obtener dimensiones de la impresora
                        printer_width = hDC.GetDeviceCaps(110)   # HORZRES
                        printer_height = hDC.GetDeviceCaps(111)  # VERTRES
                        
                        # Calcular escala para ajustar a la página
                        scale = min(
                            printer_width / bmp.size[0], 
                            printer_height / bmp.size[1]
                        )
                        new_width = int(bmp.size[0] * scale)
                        new_height = int(bmp.size[1] * scale)
                        
                        # Centrar en la página
                        x = (printer_width - new_width) // 2
                        y = (printer_height - new_height) // 2
                        
                        # Dibujar/Imprimir la imagen
                        dib.draw(hDC.GetHandleOutput(), 
                                (x, y, x + new_width, y + new_height))
                        
                        # Finalizar impresión
                        hDC.EndPage()
                        hDC.EndDoc()
                        hDC.DeleteDC()
                        
                        # IMPORTANTE: Cerrar y liberar recursos ANTES de eliminar
                        pdf_doc.close()
                        del bmp  # Liberar imagen de PIL
                        del dib  # Liberar DIB de Windows
                        
                        # Esperar un momento para asegurar que se liberó el archivo
                        time.sleep(0.1)
                        
                        # Intentar eliminar el archivo temporal
                        try:
                            os.unlink(temp_img_path)
                        except PermissionError:
                            # Si no se puede eliminar, programar para eliminar después
                            import atexit
                            atexit.register(lambda: os.unlink(temp_img_path) if os.path.exists(temp_img_path) else None)
                        
                    except ImportError as ie:
                        # Si falta alguna biblioteca
                        messagebox.showerror(
                            "Biblioteca faltante",
                            f"Falta instalar una biblioteca:\n\n{str(ie)}\n\n"
                            "Instala con:\npip install pywin32 PyMuPDF\n\n"
                            "Se abrirá el PDF en tu visor."
                        )
                        abrir_en_visor()
                        
                    except Exception as e:
                        # Cualquier otro error en Windows
                        messagebox.showerror(
                            "Error de impresión",
                            f"No se pudo imprimir directamente:\n{str(e)}\n\n"
                            "Se abrirá el PDF para que imprimas manualmente."
                        )
                        abrir_en_visor()
                        
                elif sistema == 'Linux':
                    # ===== IMPRESIÓN EN LINUX CON LPR =====
                    try:
                        subprocess.run(['lp', pdf_path], check=True)
                        messagebox.showinfo(
                            "✓ Enviado a impresora", 
                            "Documento enviado a la impresora predeterminada."
                        )
                    except FileNotFoundError:
                        messagebox.showerror(
                            "Comando no encontrado",
                            "No se encontró el comando 'lpr'.\n"
                            "Se abrirá el PDF para imprimir manualmente."
                        )
                        abrir_en_visor()
                    except subprocess.CalledProcessError as e:
                        messagebox.showerror(
                            "Error de impresión",
                            f"Error al enviar a impresora:\n{str(e)}\n\n"
                            "Se abrirá el PDF para imprimir manualmente."
                        )
                        abrir_en_visor()
                        
                else:
                    # macOS u otros sistemas
                    messagebox.showinfo(
                        "Imprimir manualmente",
                        "Tu sistema operativo requiere impresión manual.\n"
                        "Se abrirá el PDF en tu visor."
                    )
                    abrir_en_visor()
                    
            except Exception as e:
                # Error general
                messagebox.showerror(
                    "Error inesperado",
                    f"Ocurrió un error:\n{str(e)}\n\n"
                    "Usa el botón 'Abrir en Visor' para imprimir manualmente."
                )

        def abrir_en_visor():
            """Abre el PDF en el visor externo del sistema"""
            sistema = platform.system()
            try:
                if sistema == 'Windows':
                    os.startfile(pdf_path)
                elif sistema == 'Linux':
                    subprocess.Popen(['xdg-open', pdf_path])
                else:
                    subprocess.Popen(['open', pdf_path])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir: {e}")
        
        def guardar_pdf():
            """Guarda una copia del PDF"""
            ruta_guardar = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf")],
                initialfile=f"plato_{datos_plato[1].replace(' ', '_')}.pdf"
            )
            if ruta_guardar:
                import shutil
                shutil.copy2(pdf_path, ruta_guardar)
                messagebox.showinfo("Guardado", f"PDF guardado en:\n{ruta_guardar}")
        
        # Botones de acción
        ctk.CTkButton(
            botones_container,
            text="🖨️ Imprimir",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color=COLOR_ACCENT,
            hover_color="#e6734d",
            text_color="white",
            corner_radius=6,
            width=120,
            height=35,
            cursor="hand2",
            command=imprimir_directo
        ).pack(side="left", padx=8)
        
        ctk.CTkButton(
            botones_container,
            text="📂 Abrir en Visor",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color=COLOR_BTN,
            hover_color="#119b97",
            text_color="white",
            corner_radius=6,
            width=140,
            height=35,
            cursor="hand2",
            command=abrir_en_visor
        ).pack(side="left", padx=8)
        
        ctk.CTkButton(
            botones_container,
            text="💾 Guardar en PDF",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            text_color="white",
            corner_radius=6,
            width=140,
            height=35,
            cursor="hand2",
            command=guardar_pdf
        ).pack(side="left", padx=8)
        
        ctk.CTkButton(
            botones_container,
            text="❌ Cancelar",
            font=(FUENTE_TXT, 13, "bold"),
            fg_color="#999",
            hover_color="#777",
            text_color="white",
            corner_radius=6,
            width=100,
            height=35,
            cursor="hand2",
            command=self.ventana_platos
        ).pack(side="left", padx=8)

    def imprimir(self):
        """Genera PDF y muestra vista previa integrada en la aplicación"""
        from imprimir_plato import generar_pdf_plato
        
        # Verificar que hay un elemento seleccionado
        selected = self.tabla.selection()
        if not selected:
            messagebox.showwarning(
                "Aviso", 
                "Por favor, selecciona un plato de la tabla para imprimir."
            )
            return
        
        try:
            # Obtener los datos del plato seleccionado
            valores = self.tabla.item(selected[0])["values"]
            
            # Construir la ruta completa de la imagen
            imagen_filename = valores[3]
            ruta_imagen = None
            
            if imagen_filename:
                CARPETA_IMAGENES = os.path.join(os.getcwd(), "img", "platos")
                ruta_imagen = os.path.join(CARPETA_IMAGENES, imagen_filename)
                
                if not os.path.exists(ruta_imagen):
                    print(f"Advertencia: Imagen no encontrada en {ruta_imagen}")
                    ruta_imagen = None
            
            # Generar el PDF
            pdf_path = generar_pdf_plato(valores, ruta_imagen)
            
            # Mostrar ventana de vista previa integrada
            self.ventana_vista_previa(pdf_path, valores)
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al generar el documento:\n{e}"
            )

    # --- FUNCIONES AUXILIARES ---
    def _add_field(self, parent, label, row):
        tk.Label(parent, text=label, bg=COLOR_BG, fg=COLOR_TXT, anchor="w", font=(FUENTE_TXT, 12)).grid(row=row, column=0, sticky="w", pady=5)
        entry = ctk.CTkEntry(
            parent,
            height=21,
            width=185,
            border_width=1,
            border_color="#A2A2A2",
            corner_radius=0,
            fg_color="#ffffff",
            text_color="black",
        )
        entry.grid(row=row, column=1, columnspan=2, pady=5)

        # quitar acentos y minúsculas para que el atributo sea fácil de usar
        attr_name = ''.join(
            c for c in unicodedata.normalize('NFD', label[:-1].lower())
            if unicodedata.category(c) != 'Mn'
        )
        setattr(self, attr_name, entry)

    def poner_fondo(self):
        fondo = ctk.CTkLabel(self.root, text="", image=self.bg_img)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)

    def seleccionar_imagen(self):
        path_origen = filedialog.askopenfilename(
            initialdir="img/platos", 
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
        )
        
        if path_origen:
            self.ruta_imagen_temporal = path_origen 
            filename = os.path.basename(path_origen)
            self.imagen_path.set(filename)
            self.mostrar_preview(path_origen)

    def mostrar_preview(self, path):
            ruta_completa_imagen = path
            if path and not os.path.isabs(path):
                ruta_completa_imagen = os.path.join(os.getcwd(), "img", "platos", path)
            if not ruta_completa_imagen or not os.path.exists(ruta_completa_imagen):
                self.preview.config(image=self.placeholder_img, text="Sin imagen")
                return

            try:
                img = Image.open(ruta_completa_imagen)
                img = img.resize((190, 190))
                self.tk_img = ImageTk.PhotoImage(img)
                self.preview.config(image=self.tk_img, text="")
                self.preview.image = self.tk_img
            except Exception as e:
                self.preview.config(image=self.placeholder_img, text="[Error]")
                print(f"Error al cargar imagen: {e}")

    def cargar_tabla(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for plato in obtener_platos():
            self.tabla.insert("", "end", values=plato)

    # --- CRUD ---
    def agregar(self):
        nombre = self.nombre.get().strip()
        precio_str = self.precio_var.get().strip()
        fecha_creacion = self.fecha_var.get().strip()  # ← AGREGAR
        imagen = self.imagen_path.get()
        
        if not nombre or not precio_str or not fecha_creacion or not imagen:  # ← AGREGAR fecha
            messagebox.showerror("Error de Validación", "Por favor, complete todos los campos.")
            return
        
        # Validar formato de fecha
        try:
            datetime.strptime(fecha_creacion, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error de Fecha", "Formato de fecha inválido. Use YYYY-MM-DD")
            return
        
        if existe_plato(nombre):
            messagebox.showerror("Error de Duplicado", "Este plato ya existe.")
            return
            
        if not hasattr(self, 'ruta_imagen_temporal') or not self.ruta_imagen_temporal:
            messagebox.showerror("Error de Imagen", "Por favor, seleccione una imagen válida.")
            return
            
        confirmar = messagebox.askokcancel("Confirmar", "¿Deseas agregar este plato?")
        if not confirmar:
            return
            
        try:
            CARPETA_DESTINO = os.path.join(os.getcwd(), "img", "platos")
            os.makedirs(CARPETA_DESTINO, exist_ok=True)
            path_destino = os.path.join(CARPETA_DESTINO, imagen)
            
            shutil.copy2(self.ruta_imagen_temporal, path_destino) 
            
            precio_float = float(precio_str)
            agregar_plato(nombre, precio_float, imagen, fecha_creacion)  # ← ORDEN CORRECTO
            
            self.ruta_imagen_temporal = None
            self.cargar_tabla()
            self.limpiar()
            messagebox.showinfo("Éxito", "Plato agregado.")
            
        except ValueError:
            messagebox.showerror("Error", "El valor del Precio no es un número válido.")
        except Exception as e:
            messagebox.showerror("Error de Archivo", f"Error al guardar la imagen o conectar con DB: {e}")

    def actualizar(self):
        selected = self.tabla.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un plato para actualizar.")
            return

        # --- Obtener datos del formulario ---
        nombre = self.nombre.get().strip()
        precio_str = self.precio_var.get().strip()
        fecha_creacion = self.fecha_var.get().strip()  # ← AGREGAR
        imagen = self.imagen_path.get()

        # --- Validaciones ---
        if not nombre or not precio_str or not fecha_creacion or not imagen:  # ← AGREGAR fecha
            messagebox.showerror("Error de Validación", "Por favor, complete todos los campos.")
            return

        # Validar formato de fecha
        from datetime import datetime
        try:
            datetime.strptime(fecha_creacion, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error de Fecha", "Formato de fecha inválido. Use YYYY-MM-DD")
            return

        try:
            precio_float = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "El valor del Precio no es un número válido.")
            return

        confirmar = messagebox.askokcancel("Confirmar", "¿Deseas actualizar este plato?")
        if not confirmar:
            return

        try:
            # --- ID del plato seleccionado ---
            id_ = int(self.tabla.item(selected[0])["values"][0])

            # --- Carpeta donde se guardan las imágenes ---
            CARPETA_DESTINO = os.path.join(os.getcwd(), "img", "platos")
            os.makedirs(CARPETA_DESTINO, exist_ok=True)
            path_destino = os.path.join(CARPETA_DESTINO, imagen)

            # --- Si el usuario seleccionó una nueva imagen temporal ---
            if hasattr(self, 'ruta_imagen_temporal') and self.ruta_imagen_temporal:
                # Borrar imagen anterior si existe
                datos_actuales = self.tabla.item(selected[0])["values"]
                imagen_anterior = datos_actuales[3]  # ← CAMBIAR: columna 3 es "Imagen"
                path_imagen_anterior = os.path.join(CARPETA_DESTINO, imagen_anterior)
                if os.path.exists(path_imagen_anterior):
                    try:
                        os.remove(path_imagen_anterior)
                    except Exception as e:
                        print(f"No se pudo eliminar la imagen anterior: {e}")

                # Copiar la nueva imagen
                shutil.copy2(self.ruta_imagen_temporal, path_destino)
                self.ruta_imagen_temporal = None

            # --- Actualizar datos en la base de datos ---
            actualizar_plato(id_, nombre, precio_float, imagen)

            # --- Refrescar tabla y limpiar formulario ---
            self.cargar_tabla()
            self.limpiar()

            messagebox.showinfo("Éxito", "Plato actualizado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al actualizar el plato:\n{e}")

    def eliminar(self):
        selected = self.tabla.selection()
        if not selected:
            return messagebox.showwarning("Aviso", "Selecciona un plato.")
        
        vals = self.tabla.item(selected[0])["values"]
        id_ = int(vals[0])
        imagen_filename = str(vals[3])  # ← CAMBIAR: columna 3 es "Imagen"
        
        if messagebox.askyesno("Confirmar", "¿Eliminar este plato?"):
            try:
                eliminar_plato(id_)
                if imagen_filename:
                    CARPETA_IMAGENES = os.path.join(os.getcwd(), "img", "platos")
                    path_completo_imagen = os.path.join(CARPETA_IMAGENES, imagen_filename)
                    if os.path.exists(path_completo_imagen):
                        os.remove(path_completo_imagen)
                    else:
                        print(f"Advertencia: El archivo de imagen '{imagen_filename}' no se encontró localmente.")
                self.cargar_tabla()
                self.limpiar()
                messagebox.showinfo("Eliminado", "Plato eliminado.")
            
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

    def limpiar(self):
        self.nombre.delete(0, tk.END)
        self.precio_var.set("")
        self.imagen_path.set("")
        self.fecha_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.preview.config(image=self.placeholder_img, text="Sin imagen")
        self.tabla.selection_remove(self.tabla.selection())

    def seleccionar_tabla(self, event):
        selected = self.tabla.selection()
        if selected:
            vals = self.tabla.item(selected[0])["values"]

            self.nombre.delete(0, tk.END)
            self.nombre.insert(0, vals[1])
            self.precio_var.set(vals[2])
            self.imagen_path.set(vals[3] if len(vals) > 3 else "")
            self.fecha_var.set(vals[4] if len(vals) > 4 else "")
            
            # Mostrar vista previa de la imagen
            self.mostrar_preview(self.imagen_path.get())

# --- INICIO APP ---
if __name__ == "__main__":
    root = ctk.CTk()
    app = RestauranteApp(root)
    root.mainloop()