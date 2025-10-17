import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import json
import os
from datetime import datetime
from src.generador_paletas import GeneradorPaletasIA
from src.utils import guardar_datos_paleta, generar_texto_redes_sociales
import threading
from app_config import AppConfig

class GeneradorPaletasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Generador de Paletas IA - Professional")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Configuración
        self.config = AppConfig()
        
        # Configuración del generador
        self.generador = GeneradorPaletasIA()
        self.paleta_actual = None
        self.historial_paletas = []
        self.proyecto_actual = None
        
        # Variables de tema
        self.tema_oscuro = tk.BooleanVar(value=self.config.config.get('tema_oscuro', True))
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar historial
        self.cargar_historial()
        
    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        self.style = ttk.Style()
        
        if self.tema_oscuro.get():
            self.configurar_tema_oscuro()
        else:
            self.configurar_tema_claro()
            
    def configurar_tema_oscuro(self):
        """Configura el tema oscuro"""
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=8)
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#00b4d8')
        self.style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground='#f72585')
        self.style.configure('TLabelframe', background='#2c3e50', foreground='white')
        self.style.configure('TLabelframe.Label', background='#2c3e50', foreground='white')
        self.style.configure('TNotebook', background='#2c3e50')
        self.style.configure('TNotebook.Tab', background='#34495e', foreground='white')
        
    def configurar_tema_claro(self):
        """Configura el tema claro"""
        self.style.configure('TFrame', background='#f8f9fa')
        self.style.configure('TLabel', background='#f8f9fa', foreground='#2c3e50', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=8)
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#0077b6')
        self.style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground='#e63946')
        self.style.configure('TLabelframe', background='#f8f9fa', foreground='#2c3e50')
        self.style.configure('TLabelframe.Label', background='#f8f9fa', foreground='#2c3e50')
        self.style.configure('TNotebook', background='#f8f9fa')
        self.style.configure('TNotebook.Tab', background='#dee2e6', foreground='#2c3e50')
        
    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""
        # Menú principal
        self.crear_menu()
        
        # Frame principal con mejor organización
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights para responsividad
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # La sección de resultados se expande
        
        # Header con título
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="🎨 GENERADOR DE PALETAS IA", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Stats en el header
        self.stats_label = ttk.Label(header_frame, text="Paletas: 0 | Favoritos: 0", style='Subtitle.TLabel')
        self.stats_label.pack(side=tk.RIGHT)
        
        # Sección de entrada (lado izquierdo)
        input_frame = ttk.LabelFrame(main_frame, text="⚙️ CONFIGURACIÓN", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 15), padx=(0, 10))
        
        # Sección de resultados (ocupa el resto del espacio)
        results_frame = ttk.LabelFrame(main_frame, text="🎨 RESULTADOS", padding="10")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Crear las subsecciones
        self.crear_seccion_entrada(input_frame)
        self.crear_seccion_resultados(results_frame)
        self.crear_seccion_consola(main_frame)
        
    def crear_menu(self):
        """Crea el menú principal simplificado"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nueva Paleta", command=self.nuevo_proyecto)
        menu_archivo.add_command(label="Guardar Paleta", command=self.guardar_paleta)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        # Menú Ver
        menu_ver = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=menu_ver)
        menu_ver.add_checkbutton(label="Tema Oscuro", variable=self.tema_oscuro, 
                               command=self.cambiar_tema)
        
    def crear_seccion_entrada(self, parent):
        """Crea la sección de entrada de datos mejorada"""
        parent.columnconfigure(1, weight=1)
        
        # Tema
        ttk.Label(parent, text="Tema o concepto:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.tema_var = tk.StringVar(value="atardecer en la playa")
        tema_entry = ttk.Entry(parent, textvariable=self.tema_var, font=('Arial', 11))
        tema_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        tema_entry.focus()
        
        # Estilo
        ttk.Label(parent, text="Estilo:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.estilo_var = tk.StringVar(value="minimalista")
        estilo_combo = ttk.Combobox(parent, textvariable=self.estilo_var, 
                                   values=["minimalista", "artístico", "vibrante", "suave", "futurista"])
        estilo_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Número de colores
        ttk.Label(parent, text="Número de colores:").grid(row=2, column=0, sticky=tk.W, pady=8)
        colores_frame = ttk.Frame(parent)
        colores_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        self.colores_var = tk.IntVar(value=6)
        colores_scale = ttk.Scale(colores_frame, from_=3, to=10, variable=self.colores_var, 
                                 orient=tk.HORIZONTAL)
        colores_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        colores_label = ttk.Label(colores_frame, textvariable=self.colores_var, width=3)
        colores_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Botones de acción
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        self.btn_generar = ttk.Button(btn_frame, text="🎨 GENERAR PALETA", 
                                     command=self.generar_paleta_thread, width=20)
        self.btn_generar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_aleatorio = ttk.Button(btn_frame, text="🎲 ALEATORIO",
                                       command=self.generar_aleatorio)
        self.btn_aleatorio.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_imagen = ttk.Button(btn_frame, text="🖼️ ANALIZAR IMAGEN",
                                    command=self.analizar_imagen)
        self.btn_imagen.pack(side=tk.LEFT)
        
    def crear_seccion_resultados(self, parent):
        """Crea la sección para mostrar resultados mejorada"""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña de visualización principal
        self.viz_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.viz_frame, text="👁️ VISUALIZACIÓN")
        
        # Pestaña de colores detallados
        self.colors_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.colors_frame, text="🎨 COLORES")
        
        # Pestaña de datos
        self.data_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.data_frame, text="📊 DATOS")
        
        # Pestaña de análisis
        self.analysis_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.analysis_frame, text="📈 ANÁLISIS")
        
        # Configurar pesos para expansión
        self.viz_frame.columnconfigure(0, weight=1)
        self.viz_frame.rowconfigure(0, weight=1)
        self.colors_frame.columnconfigure(0, weight=1)
        self.colors_frame.rowconfigure(0, weight=1)
        
    def crear_seccion_consola(self, parent):
        """Crea la sección de consola/log"""
        console_frame = ttk.LabelFrame(parent, text="📝 ACTIVIDAD", padding="10")
        console_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        console_frame.columnconfigure(0, weight=1)
        
        self.consola = scrolledtext.ScrolledText(console_frame, height=6, 
                                                bg='#1a1a1a', fg='#00ff00', 
                                                font=('Consolas', 9), wrap=tk.WORD)
        self.consola.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.consola.config(state=tk.DISABLED)
        
    # ===== MÉTODOS PRINCIPALES MEJORADOS =====
    
    def mostrar_resultados(self):
        """Muestra los resultados en todas las pestañas - VERSIÓN MEJORADA"""
        if not self.paleta_actual:
            self.log("❌ No hay paleta para mostrar")
            return
            
        self.log("🔄 Actualizando interfaz con los resultados...")
        
        try:
            self.mostrar_visualizacion_mejorada()
            self.mostrar_colores_mejorados()
            self.mostrar_datos()
            self.mostrar_analisis()
            
            # Habilitar botones de exportación
            self.habilitar_botones_exportacion()
            
            self.log("✅ Resultados mostrados correctamente")
            
        except Exception as e:
            self.log(f"❌ Error mostrando resultados: {str(e)}")
            
    def mostrar_visualizacion_mejorada(self):
        """Muestra la visualización de la paleta - VERSIÓN MEJORADA"""
        # Limpiar frame completamente
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
            
        if not self.paleta_actual or 'visualizacion' not in self.paleta_actual:
            self.crear_visualizacion_fallback()
            return
            
        try:
            # Verificar si el archivo existe
            imagen_path = self.paleta_actual['visualizacion']
            if not os.path.exists(imagen_path):
                self.log(f"⚠️ Archivo no encontrado: {imagen_path}")
                self.crear_visualizacion_fallback()
                return
                
            # Cargar y mostrar imagen
            imagen = Image.open(imagen_path)
            
            # Calcular tamaño para mostrar (80% del ancho disponible)
            ancho_max = 800
            alto_max = 500
            
            # Redimensionar manteniendo aspect ratio
            imagen.thumbnail((ancho_max, alto_max), Image.Resampling.LANCZOS)
            
            # Convertir para Tkinter
            photo = ImageTk.PhotoImage(imagen)
            
            # Crear frame para imagen con scrollbars si es necesario
            canvas_frame = ttk.Frame(self.viz_frame)
            canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            canvas_frame.columnconfigure(0, weight=1)
            canvas_frame.rowconfigure(0, weight=1)
            
            # Canvas para la imagen
            canvas = tk.Canvas(canvas_frame, bg='#2c3e50' if self.tema_oscuro.get() else '#f8f9fa')
            canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Mostrar imagen en el canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo  # Mantener referencia
            
            # Configurar scrollbars si la imagen es más grande que el canvas
            if imagen.width > ancho_max or imagen.height > alto_max:
                h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
                v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
                h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
                v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
                
                canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set,
                               scrollregion=(0, 0, imagen.width, imagen.height))
            
            self.log("✅ Visualización cargada correctamente")
            
        except Exception as e:
            self.log(f"❌ Error cargando visualización: {str(e)}")
            self.crear_visualizacion_fallback()
            
    def crear_visualizacion_fallback(self):
        """Crea una visualización de fallback cuando no hay imagen"""
        fallback_frame = ttk.Frame(self.viz_frame)
        fallback_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        fallback_frame.columnconfigure(0, weight=1)
        fallback_frame.rowconfigure(0, weight=1)
        
        # Canvas para dibujar la paleta
        canvas = tk.Canvas(fallback_frame, bg='white', width=600, height=300)
        canvas.grid(row=0, column=0, padx=20, pady=20)
        
        if not self.paleta_actual or 'colores' not in self.paleta_actual:
            canvas.create_text(300, 150, text="No hay paleta para mostrar", 
                             font=('Arial', 14), fill='gray')
            return
            
        colores = self.paleta_actual['colores']
        n_colores = len(colores)
        
        if n_colores == 0:
            canvas.create_text(300, 150, text="No hay colores en la paleta", 
                             font=('Arial', 14), fill='gray')
            return
            
        # Dibujar barras de colores
        bar_width = 580 / n_colores
        x = 10
        
        for i, color_info in enumerate(colores):
            color_hex = color_info['hex']
            
            # Dibujar rectángulo de color
            canvas.create_rectangle(x, 50, x + bar_width, 200, fill=color_hex, outline='')
            
            # Añadir código HEX
            canvas.create_text(x + bar_width/2, 220, text=color_hex, 
                             font=('Arial', 9, 'bold'), fill='#333333')
            
            # Añadir nombre del color
            nombre = color_info.get('nombre', f'Color {i+1}')
            canvas.create_text(x + bar_width/2, 240, text=nombre, 
                             font=('Arial', 8), fill='#666666')
            
            x += bar_width
            
        # Título de la paleta
        titulo = self.paleta_actual.get('tema', 'Paleta de colores')
        canvas.create_text(300, 30, text=titulo, font=('Arial', 16, 'bold'), fill='#333333')
        
        self.log("✅ Visualización de fallback creada")
        
    def mostrar_colores_mejorados(self):
        """Muestra los colores de forma mejorada y organizada"""
        # Limpiar frame completamente
        for widget in self.colors_frame.winfo_children():
            widget.destroy()
            
        if not self.paleta_actual or 'colores' not in self.paleta_actual:
            ttk.Label(self.colors_frame, text="No hay colores para mostrar", 
                     font=('Arial', 12)).pack(pady=50)
            return
            
        colores = self.paleta_actual['colores']
        
        # Frame principal con scrollbar
        main_container = ttk.Frame(self.colors_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar para colores
        canvas = tk.Canvas(main_container, bg='#2c3e50' if self.tema_oscuro.get() else '#f8f9fa')
        scrollbar = ttk.Scrollbar(main_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crear grid de colores (3 columnas)
        for i, color_info in enumerate(colores):
            row = i // 3
            col = i % 3
            
            self.crear_tarjeta_color(scrollable_frame, color_info, row, col)
            
        self.log(f"✅ Mostrando {len(colores)} colores organizados")
        
    def crear_tarjeta_color(self, parent, color_info, row, col):
        """Crea una tarjeta individual para cada color"""
        # Frame de la tarjeta
        card_frame = ttk.Frame(parent, relief='solid', borderwidth=1, padding="10")
        card_frame.grid(row=row, column=col, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       padx=8, pady=8, ipadx=5, ipady=5)
        
        # Configurar pesos para expansión
        parent.columnconfigure(col, weight=1)
        parent.rowconfigure(row, weight=0)
        
        # Muestra de color grande
        color_canvas = tk.Canvas(card_frame, width=120, height=80, 
                                bg=color_info['hex'], highlightthickness=0)
        color_canvas.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Información del color
        nombre_label = ttk.Label(card_frame, text=color_info['nombre'], 
                                font=('Arial', 11, 'bold'))
        nombre_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        hex_label = ttk.Label(card_frame, text=color_info['hex'], 
                             font=('Courier', 10, 'bold'))
        hex_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 2))
        
        rgb_text = f"RGB{tuple(color_info['rgb'])}"
        rgb_label = ttk.Label(card_frame, text=rgb_text, 
                             font=('Courier', 8))
        rgb_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        # Botones de acción
        btn_frame = ttk.Frame(card_frame)
        btn_frame.grid(row=2, column=1, rowspan=2, sticky=(tk.E, tk.S))
        
        btn_copiar = ttk.Button(btn_frame, text="📋", width=3,
                              command=lambda hex=color_info['hex']: self.copiar_portapapeles(hex))
        btn_copiar.pack(side=tk.LEFT, padx=(5, 0))
        
    def mostrar_datos(self):
        """Muestra los datos JSON de la paleta"""
        for widget in self.data_frame.winfo_children():
            widget.destroy()
            
        if not self.paleta_actual:
            ttk.Label(self.data_frame, text="No hay datos para mostrar", 
                     font=('Arial', 12)).pack(pady=50)
            return
            
        # Mostrar JSON formateado
        datos_json = json.dumps(self.paleta_actual, indent=2, ensure_ascii=False)
        
        text_frame = ttk.Frame(self.data_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = scrolledtext.ScrolledText(text_frame, font=('Consolas', 10), 
                                              wrap=tk.WORD)
        text_widget.insert(tk.INSERT, datos_json)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def mostrar_analisis(self):
        """Muestra análisis de la paleta"""
        for widget in self.analysis_frame.winfo_children():
            widget.destroy()
            
        if not self.paleta_actual:
            ttk.Label(self.analysis_frame, text="No hay datos para analizar", 
                     font=('Arial', 12)).pack(pady=50)
            return
            
        # Crear contenido de análisis mejorado
        analisis_text = self.generar_analisis_completo()
        
        text_frame = ttk.Frame(self.analysis_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = scrolledtext.ScrolledText(text_frame, font=('Arial', 11), 
                                              wrap=tk.WORD, spacing1=2, spacing2=1, spacing3=2)
        text_widget.insert(tk.INSERT, analisis_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def generar_analisis_completo(self):
        """Genera un análisis completo de la paleta"""
        colores = self.paleta_actual['colores']
        
        analisis = f"""
📊 ANÁLISIS COMPLETO DE LA PALETA
{'=' * 40}

🎨 INFORMACIÓN GENERAL:
• Tema: {self.paleta_actual.get('tema', 'No especificado')}
• Total de colores: {len(colores)}
• Estilo: {self.paleta_actual.get('estilo', 'No especificado')}
• Fecha de generación: {self.paleta_actual.get('timestamp', 'No disponible')}

📈 ESTADÍSTICAS DE COLOR:
• Rango de colores: {self.calcular_rango_colores()}
• Saturación promedio: {self.calcular_saturacion_promedio():.1f}%
• Balance tonal: {self.analizar_balance_colores()}
• Variedad cromática: {self.calcular_variedad_cromatica()}

🌈 DISTRIBUCIÓN DE COLORES:
{self.generar_distribucion_colores()}

💡 RECOMENDACIONES DE USO:
{self.generar_recomendaciones_detalladas()}

🎯 APLICACIONES SUGERIDAS:
{self.generar_aplicaciones_sugeridas()}
        """
        
        return analisis
        
    def calcular_variedad_cromatica(self):
        """Calcula qué tan variada es la paleta"""
        if not self.paleta_actual:
            return "N/A"
            
        colores = [color['rgb'] for color in self.paleta_actual['colores']]
        if len(colores) < 2:
            return "Mínima (solo un color)"
            
        # Calcular diferencias entre colores
        diferencias = []
        for i in range(len(colores)):
            for j in range(i+1, len(colores)):
                diff = sum(abs(a - b) for a, b in zip(colores[i], colores[j]))
                diferencias.append(diff)
                
        promedio_diff = sum(diferencias) / len(diferencias) if diferencias else 0
        
        if promedio_diff > 200:
            return "Alta (colores muy distintos)"
        elif promedio_diff > 100:
            return "Media (buen contraste)"
        else:
            return "Baja (colores similares)"
            
    def generar_recomendaciones_detalladas(self):
        """Genera recomendaciones detalladas basadas en la paleta"""
        colores = [color['rgb'] for color in self.paleta_actual['colores']]
        saturacion_promedio = self.calcular_saturacion_promedio()
        variedad = self.calcular_variedad_cromatica()
        
        recomendaciones = []
        
        if saturacion_promedio > 70:
            recomendaciones.append("• Excelente para diseño web y aplicaciones móviles")
            recomendaciones.append("• Ideal para llamadas a la acción y elementos importantes")
            recomendaciones.append("• Perfecta para branding juvenil y moderno")
        elif saturacion_promedio > 40:
            recomendaciones.append("• Versátil para múltiples propósitos")
            recomendaciones.append("• Adecuada para interfaces de usuario profesionales")
            recomendaciones.append("• Buena para contenido corporativo y educativo")
        else:
            recomendaciones.append("• Ideal para fondos y elementos secundarios")
            recomendaciones.append("• Perfecta para interfaces minimalistas")
            recomendaciones.append("• Excelente para aplicaciones de productividad")
            
        if "Alta" in variedad:
            recomendaciones.append("• Paleta contrastante - ideal para jerarquía visual")
        elif "Media" in variedad:
            recomendaciones.append("• Balance perfecto entre armonía y contraste")
        else:
            recomendaciones.append("• Paleta monocromática - excelente para coherencia")
            
        return "\n".join(recomendaciones)
        
    def generar_aplicaciones_sugeridas(self):
        """Genera aplicaciones sugeridas para la paleta"""
        aplicaciones = [
            "🎨 Diseño gráfico y branding",
            "🌐 Diseño web y UI/UX", 
            "📱 Aplicaciones móviles",
            "📊 Presentaciones y infografías",
            "🏠 Diseño de interiores",
            "👗 Diseño de moda",
            "🎭 Arte digital e ilustración",
            "📚 Material educativo",
            "📱 Redes sociales y marketing",
            "🎬 Producción audiovisual"
        ]
        
        return "\n".join([f"• {app}" for app in aplicaciones])
        
    def habilitar_botones_exportacion(self):
        """Habilita los botones de exportación en una barra de herramientas"""
        # Crear barra de herramientas si no existe
        toolbar = getattr(self, 'toolbar_frame', None)
        if toolbar is not None:
            try:
                toolbar.destroy()
            except Exception:
                pass
            
        self.toolbar_frame = ttk.Frame(self.viz_frame)
        self.toolbar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(self.toolbar_frame, text="Exportar:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(self.toolbar_frame, text="💾 Guardar Paleta", 
                  command=self.guardar_paleta).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(self.toolbar_frame, text="📱 Redes Sociales", 
                  command=self.mostrar_contenido_redes).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(self.toolbar_frame, text="⭐ Favorito", 
                  command=self.marcar_favorito).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(self.toolbar_frame, text="📤 Exportar Todo", 
                  command=self.exportar_todo).pack(side=tk.LEFT)
        
    # ===== MÉTODOS EXISTENTES (simplificados para el ejemplo) =====
    
    def log(self, mensaje):
        """Añade un mensaje a la consola"""
        self.consola.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.consola.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.consola.see(tk.END)
        self.consola.config(state=tk.DISABLED)
        self.root.update_idletasks()
        
    def generar_paleta_thread(self):
        """Inicia la generación en un hilo separado"""
        tema = self.tema_var.get().strip()
        if not tema:
            messagebox.showwarning("Advertencia", "Por favor ingresa un tema")
            return
            
        self.btn_generar.config(state="disabled")
        self.log("🔄 Iniciando generación de paleta...")
        
        thread = threading.Thread(target=self.generar_paleta)
        thread.daemon = True
        thread.start()
        
    def generar_paleta(self):
        """Genera la paleta de colores"""
        try:
            tema = self.tema_var.get().strip()
            estilo = self.estilo_var.get()
            
            self.log(f"🎨 Generando paleta para: {tema}")
            
            # Generar paleta
            self.paleta_actual = self.generador.generar_paleta_completa(tema, estilo)
            
            if self.paleta_actual:
                self.log("✅ Paleta generada exitosamente")
                self.mostrar_resultados()
                self.actualizar_estadisticas()
            else:
                self.log("❌ Error al generar la paleta")
                
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
        finally:
            self.btn_generar.config(state="normal")
            
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas en el header"""
        historial_count = len(self.config.config.get('historial_paletas', []))
        favoritos_count = len(self.config.config.get('favoritos', []))
        self.stats_label.config(text=f"Paletas: {historial_count} | Favoritos: {favoritos_count}")
        
    def cargar_historial(self):
        """Carga el historial de temas"""
        historial_temas = self.config.config.get('historial_temas', [])
        # No usamos combobox en esta versión simplificada
        
    def copiar_portapapeles(self, texto):
        """Copia texto al portapapeles"""
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        self.log(f"📋 Copiado: {texto}")
        messagebox.showinfo("Copiado", f"Texto copiado:\n{texto}")
        
    def cambiar_tema(self):
        """Cambia entre tema oscuro y claro"""
        if self.tema_oscuro.get():
            self.configurar_tema_oscuro()
        else:
            self.configurar_tema_claro()
        
        self.config.config['tema_oscuro'] = self.tema_oscuro.get()
        self.config.guardar_config()
        self.log("✅ Tema cambiado")
        
    def generar_aleatorio(self):
        """Genera una paleta con tema aleatorio"""
        temas_aleatorios = [
            "universo infinito", "cascada tropical", "mercado oriental",
            "fiesta mexicana", "noche estrellada", "amanecer dorado",
            "bosque encantado", "ciudad bajo la lluvia", "playa tropical"
        ]
        
        import random
        tema_aleatorio = random.choice(temas_aleatorios)
        self.tema_var.set(tema_aleatorio)
        self.generar_paleta_thread()
        
    def analizar_imagen(self):
        """Analiza una imagen para extraer colores"""
        messagebox.showinfo("Análisis de Imagen", 
                           "Esta funcionalidad estará disponible en la próxima versión")
        
    def marcar_favorito(self):
        """Marca la paleta actual como favorita"""
        if self.paleta_actual:
            favoritos = self.config.config.get('favoritos', [])
            favoritos.append(self.paleta_actual)
            self.config.config['favoritos'] = favoritos
            self.config.guardar_config()
            self.log("⭐ Paleta añadida a favoritos")
            self.actualizar_estadisticas()
            
    def mostrar_contenido_redes(self):
        """Muestra el contenido para redes sociales"""
        if not self.paleta_actual:
            return
            
        redes_window = tk.Toplevel(self.root)
        redes_window.title("📱 Contenido para Redes Sociales")
        redes_window.geometry("600x500")
        
        notebook = ttk.Notebook(redes_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        plataformas = ['instagram', 'twitter', 'tiktok']
        
        for plataforma in plataformas:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=plataforma.title())
            
            texto = generar_texto_redes_sociales(self.paleta_actual, plataforma)
            
            text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=20)
            text_widget.insert(tk.INSERT, texto)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            btn_copiar = ttk.Button(frame, text="📋 Copiar Texto",
                                  command=lambda t=texto: self.copiar_portapapeles(t))
            btn_copiar.pack(pady=5)
            
    def exportar_todo(self):
        """Exporta todo el proyecto"""
        messagebox.showinfo("Exportar", "Función de exportación completa en desarrollo")
        
    def guardar_paleta(self):
        """Guarda la paleta actual"""
        if not self.paleta_actual:
            return
            
        try:
            directorio = filedialog.askdirectory(title="Selecciona donde guardar la paleta")
            if directorio:
                archivo_json = os.path.join(directorio, f"paleta_{self.paleta_actual['tema'].replace(' ', '_')}.json")
                with open(archivo_json, 'w', encoding='utf-8') as f:
                    json.dump(self.paleta_actual, f, indent=2, ensure_ascii=False)
                    
                self.log(f"💾 Paleta guardada en: {archivo_json}")
                messagebox.showinfo("Éxito", f"Paleta guardada en:\n{directorio}")
                
        except Exception as e:
            self.log(f"❌ Error guardando: {e}")
            
    def nuevo_proyecto(self):
        """Crea un nuevo proyecto"""
        self.paleta_actual = None
        self.tema_var.set("")
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        for widget in self.colors_frame.winfo_children():
            widget.destroy()
        for widget in self.data_frame.winfo_children():
            widget.destroy()
        for widget in self.analysis_frame.winfo_children():
            widget.destroy()
            
        self.log("🆕 Nuevo proyecto listo")
        
    # ===== MÉTODOS DE ANÁLISIS (mantenidos del código anterior) =====
    
    def calcular_rango_colores(self):
        """Calcula el rango de colores en la paleta"""
        if not self.paleta_actual:
            return "N/A"
            
        colores = [color['rgb'] for color in self.paleta_actual['colores']]
        rojos = [c[0] for c in colores]
        verdes = [c[1] for c in colores]
        azules = [c[2] for c in colores]
        
        return f"R({min(rojos)}-{max(rojos)}), G({min(verdes)}-{max(verdes)}), B({min(azules)}-{max(azules)})"
        
    def calcular_saturacion_promedio(self):
        """Calcula la saturación promedio de los colores"""
        if not self.paleta_actual:
            return 0
            
        saturaciones = []
        for color in self.paleta_actual['colores']:
            r, g, b = color['rgb']
            max_val = max(r, g, b)
            min_val = min(r, g, b)
            if max_val == 0:
                saturaciones.append(0)
            else:
                saturaciones.append((max_val - min_val) / max_val * 100)
                
        return sum(saturaciones) / len(saturaciones) if saturaciones else 0
        
    def analizar_balance_colores(self):
        """Analiza el balance de colores en la paleta"""
        if not self.paleta_actual:
            return "N/A"
            
        colores = [color['rgb'] for color in self.paleta_actual['colores']]
        promedios = [sum(color) / 3 for color in colores]
        
        claro = sum(1 for p in promedios if p > 150)
        medio = sum(1 for p in promedios if 80 <= p <= 150)
        oscuro = sum(1 for p in promedios if p < 80)
        
        return f"Claros: {claro}, Medios: {medio}, Oscuros: {oscuro}"
        
    def generar_distribucion_colores(self):
        """Genera una representación visual de la distribución"""
        if not self.paleta_actual:
            return ""
            
        distribucion = ""
        for color in self.paleta_actual['colores']:
            nombre = color['nombre'][:15].ljust(15)
            hex_code = color['hex']
            distribucion += f"  {nombre} {hex_code} {'█' * 8}\n"
            
        return distribucion

def main():
    """Función principal de la aplicación"""
    root = tk.Tk()
    app = GeneradorPaletasApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()