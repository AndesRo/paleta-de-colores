import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from datetime import datetime
import json

class VisualizadorRedesSociales:
    def __init__(self):
        # Configuración para diferentes plataformas
        self.tamanos = {
            'instagram_cuadrado': (1080, 1080),
            'instagram_historia': (1080, 1920),
            'twitter': (1200, 675),
            'linkedin': (1200, 627),
            'tiktok': (1080, 1920)
        }
        
        # Colores de la marca
        self.colores_marca = {
            'fondo': '#1a1a2e',
            'texto': '#ffffff',
            'acento': '#00b4d8',
            'secundario': '#f72585'
        }
    
    def crear_banner_proyecto(self, plataforma='instagram_cuadrado'):
        """Crea un banner atractivo para presentar el proyecto"""
        ancho, alto = self.tamanos[plataforma]
        
        fig, ax = plt.subplots(figsize=(ancho/100, alto/100), dpi=100)
        fig.patch.set_facecolor(self.colores_marca['fondo'])
        ax.set_facecolor(self.colores_marca['fondo'])
        
        # Título principal
        ax.text(0.5, 0.7, 'GENERADOR DE\nPALETAS CON IA', 
                transform=ax.transAxes, ha='center', va='center',
                fontsize=48, fontweight='bold', color=self.colores_marca['texto'],
                linespacing=1.2)
        
        # Subtítulo
        ax.text(0.5, 0.5, 'Python + Machine Learning + Creatividad',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=24, color=self.colores_marca['acento'],
                style='italic')
        
        # Características
        caracteristicas = [
            "🎨 Paletas únicas desde cualquier tema",
            "🤖 Algoritmos de color HSL + K-means", 
            "💻 100% código Python",
            "🚀 Listo para redes sociales"
        ]
        
        for i, caracteristica in enumerate(caracteristicas):
            ax.text(0.5, 0.35 - i*0.08, caracteristica,
                    transform=ax.transAxes, ha='center', va='center',
                    fontsize=18, color=self.colores_marca['texto'])
        
        # Footer
        ax.text(0.5, 0.1, '@TuUsuario • #ArteGenerativo #Python #IA',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=14, color=self.colores_marca['secundario'])
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Guardar
        os.makedirs('redes_sociales', exist_ok=True)
        filename = f"redes_sociales/banner_proyecto_{plataforma}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor=self.colores_marca['fondo'])
        plt.close()
        
        print(f"✅ Banner creado: {filename}")
        return filename
    
    def crear_carousel_paleta(self, paleta_data, plataforma='instagram_cuadrado'):
        """Crea un carousel para mostrar una paleta específica"""
        ancho, alto = self.tamanos[plataforma]
        tema = paleta_data['tema']
        colores = paleta_data['colores']
        
        # Crear múltiples slides para el carousel
        slides = []
        
        # Slide 1: Presentación de la paleta
        slides.append(self._crear_slide_presentacion(tema, colores, ancho, alto))
        
        # Slide 2: Colores individuales
        slides.append(self._crear_slide_colores_detalle(tema, colores, ancho, alto))
        
        # Slide 3: Aplicaciones prácticas
        slides.append(self._crear_slide_aplicaciones(tema, colores, ancho, alto))
        
        # Slide 4: Código y tecnología
        slides.append(self._crear_slide_tecnologia(tema, ancho, alto))
        
        return slides
    
    def _crear_slide_presentacion(self, tema, colores, ancho, alto):
        """Slide 1: Presentación principal de la paleta"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(ancho/100, alto/100), 
                                      gridspec_kw={'height_ratios': [2, 1]})
        fig.patch.set_facecolor(self.colores_marca['fondo'])
        ax1.set_facecolor(self.colores_marca['fondo'])
        ax2.set_facecolor(self.colores_marca['fondo'])
        
        # Título
        ax1.text(0.5, 0.8, f'PALETA: {tema.upper()}', 
                transform=ax1.transAxes, ha='center', va='center',
                fontsize=32, fontweight='bold', color=self.colores_marca['texto'])
        
        # Paleta de colores
        for i, color_info in enumerate(colores):
            color = color_info['rgb']
            rect = patches.Rectangle((i/len(colores), 0.3), 1/len(colores), 0.4,
                                   facecolor=np.array(color)/255.0)
            ax1.add_patch(rect)
            
            # Texto del color
            ax1.text((i + 0.5)/len(colores), 0.2, color_info['hex'],
                    ha='center', va='center', fontsize=14, 
                    color='white' if sum(color) < 450 else 'black',
                    fontweight='bold')
        
        # Información
        ax2.text(0.05, 0.8, "🎨 Paleta generada automáticamente con IA",
                transform=ax2.transAxes, ha='left', va='center',
                fontsize=16, color=self.colores_marca['texto'])
        
        ax2.text(0.05, 0.5, f"🌈 {len(colores)} colores únicos",
                transform=ax2.transAxes, ha='left', va='center',
                fontsize=14, color=self.colores_marca['acento'])
        
        ax2.text(0.05, 0.2, "👉 Desliza para más detalles",
                transform=ax2.transAxes, ha='left', va='center',
                fontsize=12, color=self.colores_marca['secundario'])
        
        for ax in [ax1, ax2]:
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        filename = f"redes_sociales/carousel_{tema.replace(' ', '_')}_slide1.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor=self.colores_marca['fondo'])
        plt.close()
        
        return filename
    
    def _crear_slide_colores_detalle(self, tema, colores, ancho, alto):
        """Slide 2: Detalle de cada color"""
        fig, ax = plt.subplots(figsize=(ancho/100, alto/100))
        fig.patch.set_facecolor(self.colores_marca['fondo'])
        ax.set_facecolor(self.colores_marca['fondo'])
        
        ax.text(0.5, 0.9, 'DETALLE DE COLORES', 
                transform=ax.transAxes, ha='center', va='center',
                fontsize=28, fontweight='bold', color=self.colores_marca['texto'])
        
        # Mostrar cada color con su información
        for i, color_info in enumerate(colores):
            y_pos = 0.75 - i * 0.12
            color = color_info['rgb']
            
            # Cuadrado de color
            rect = patches.Rectangle((0.1, y_pos - 0.04), 0.1, 0.08,
                                   facecolor=np.array(color)/255.0)
            ax.add_patch(rect)
            
            # Información del color
            ax.text(0.25, y_pos, color_info['nombre'],
                    transform=ax.transAxes, ha='left', va='center',
                    fontsize=16, color=self.colores_marca['texto'])
            
            ax.text(0.25, y_pos - 0.03, color_info['hex'],
                    transform=ax.transAxes, ha='left', va='center',
                    fontsize=14, color=self.colores_marca['acento'],
                    fontfamily='monospace')
            
            ax.text(0.6, y_pos - 0.03, f"RGB{tuple(color)}",
                    transform=ax.transAxes, ha='left', va='center',
                    fontsize=12, color=self.colores_marca['texto'],
                    fontfamily='monospace')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        filename = f"redes_sociales/carousel_{tema.replace(' ', '_')}_slide2.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor=self.colores_marca['fondo'])
        plt.close()
        
        return filename
    
    def _crear_slide_aplicaciones(self, tema, colores, ancho, alto):
        """Slide 3: Aplicaciones prácticas de la paleta"""
        fig, ax = plt.subplots(figsize=(ancho/100, alto/100))
        fig.patch.set_facecolor(self.colores_marca['fondo'])
        ax.set_facecolor(self.colores_marca['fondo'])
        
        ax.text(0.5, 0.9, 'APLICACIONES PRÁCTICAS', 
                transform=ax.transAxes, ha='center', va='center',
                fontsize=28, fontweight='bold', color=self.colores_marca['texto'])
        
        aplicaciones = [
            "🎨 Diseño gráfico y branding",
            "🌐 Diseño web y UI/UX",
            "📱 Redes sociales y marketing",
            "🎭 Arte digital e ilustración",
            "🏠 Decoración de interiores",
            "👗 Diseño de moda y textiles"
        ]
        
        for i, aplicacion in enumerate(aplicaciones):
            y_pos = 0.75 - i * 0.1
            ax.text(0.1, y_pos, aplicacion,
                    transform=ax.transAxes, ha='left', va='center',
                    fontsize=16, color=self.colores_marca['texto'])
        
        # Mini paleta de referencia
        for i, color_info in enumerate(colores[:3]):
            rect = patches.Rectangle((0.7 + i*0.08, 0.2), 0.07, 0.1,
                                   facecolor=np.array(color_info['rgb'])/255.0)
            ax.add_patch(rect)
        
        ax.text(0.5, 0.1, "¿Para qué usarías esta paleta? 👇",
                transform=ax.transAxes, ha='center', va='center',
                fontsize=14, color=self.colores_marca['secundario'])
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        filename = f"redes_sociales/carousel_{tema.replace(' ', '_')}_slide3.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor=self.colores_marca['fondo'])
        plt.close()
        
        return filename
    
    def _crear_slide_tecnologia(self, tema, ancho, alto):
        """Slide 4: Tecnología utilizada"""
        fig, ax = plt.subplots(figsize=(ancho/100, alto/100))
        fig.patch.set_facecolor(self.colores_marca['fondo'])
        ax.set_facecolor(self.colores_marca['fondo'])
        
        ax.text(0.5, 0.9, 'TECNOLOGÍA UTILIZADA', 
                transform=ax.transAxes, ha='center', va='center',
                fontsize=28, fontweight='bold', color=self.colores_marca['texto'])
        
        tecnologias = [
            "🐍 Python 3.x",
            "🤖 Algoritmo K-means clustering", 
            "🎨 Modelo de color HSL",
            "📊 Matplotlib para visualización",
            "🖼️ PIL (Pillow) para procesamiento",
            "📈 Scikit-learn para machine learning"
        ]
        
        for i, tech in enumerate(tecnologias):
            y_pos = 0.75 - i * 0.1
            ax.text(0.1, y_pos, tech,
                    transform=ax.transAxes, ha='left', va='center',
                    fontsize=16, color=self.colores_marca['texto'])
        
        ax.text(0.5, 0.2, "💡 Proyecto 100% código abierto",
                transform=ax.transAxes, ha='center', va='center',
                fontsize=18, color=self.colores_marca['acento'])
        
        ax.text(0.5, 0.1, "@TuUsuario • #Python #MachineLearning #IA",
                transform=ax.transAxes, ha='center', va='center',
                fontsize=14, color=self.colores_marca['secundario'])
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        filename = f"redes_sociales/carousel_{tema.replace(' ', '_')}_slide4.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor=self.colores_marca['fondo'])
        plt.close()
        
        return filename
    
    def crear_video_presentacion(self, paletas_generadas):
        """Crea un script para video presentación (Reels/TikTok)"""
        script = {
            'titulo': '🎨 Generando Paletas de Colores con IA y Python',
            'duracion_estimada': '45-60 segundos',
            'escenas': []
        }
        
        # Escena 1: Introducción
        script['escenas'].append({
            'duracion': '5s',
            'visual': 'Banner del proyecto con título animado',
            'audio': 'Música de fondo épica',
            'texto': '¿Qué pasa si la IA puede crear paletas de colores únicas?'
        })
        
        # Escena 2: Demostración del código
        script['escenas'].append({
            'duracion': '10s', 
            'visual': 'Pantalla de código Python (time-lapse)',
            'audio': 'Sonido de teclado',
            'texto': 'Usando Python + Machine Learning...'
        })
        
        # Escena 3: Resultados
        for i, paleta in enumerate(paletas_generadas[:3]):
            script['escenas'].append({
                'duracion': '8s',
                'visual': f'Paleta: {paleta["tema"]} - transición suave',
                'audio': 'Efecto de transición',
                'texto': f'Paleta: {paleta["tema"].title()}'
            })
        
        # Escena 4: Llamado a la acción
        script['escenas'].append({
            'duracion': '5s',
            'visual': 'Todas las paletas juntas en grid',
            'audio': 'Música culmina',
            'texto': '¿Qué tema quieres que transforme en colores? 👇'
        })
        
        # Guardar script
        with open('redes_sociales/script_video_presentacion.json', 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        
        print("✅ Script de video creado: redes_sociales/script_video_presentacion.json")
        return script

    def generar_kit_redes(self, paletas_generadas):
        """Genera un kit completo para redes sociales"""
        print("🚀 GENERANDO KIT COMPLETO PARA REDES SOCIALES...")
        
        # Crear banners para diferentes plataformas
        plataformas = ['instagram_cuadrado', 'instagram_historia', 'twitter', 'linkedin']
        
        for plataforma in plataformas:
            self.crear_banner_proyecto(plataforma)
        
        # Crear carousels para las primeras 3 paletas
        for i, paleta in enumerate(paletas_generadas[:3]):
            print(f"📱 Creando carousel para: {paleta['tema']}")
            self.crear_carousel_paleta(paleta)
        
        # Crear script de video
        self.crear_video_presentacion(paletas_generadas)
        
        # Crear archivo README para el kit
        self._crear_readme_kit()
        
        print("🎉 ¡Kit de redes sociales generado exitosamente!")
        print("📍 Revisa la carpeta 'redes_sociales'")
    
    def _crear_readme_kit(self):
        """Crea un archivo README con instrucciones"""
        contenido = """# 🎨 KIT REDES SOCIALES - Generador de Paletas IA

## 📁 CONTENIDO GENERADO

### 🖼️ BANNERS
- `banner_proyecto_instagram_cuadrado.png` - Para feed de Instagram
- `banner_proyecto_instagram_historia.png` - Para Stories/Reels
- `banner_proyecto_twitter.png` - Para Twitter/LinkedIn
- `banner_proyecto_linkedin.png` - Para LinkedIn

### 🎠 CAROUSELS
- Archivos `carousel_*_slide*.png` - Para posts de carousel en Instagram

### 🎬 VIDEO
- `script_video_presentacion.json` - Guión para Reels/TikTok

## 📱 CÓMO USAR

### INSTAGRAM
1. **Feed**: Usa los banners cuadrados
2. **Carousel**: Sube las 4 slides de cada tema en orden
3. **Stories**: Usa los banners de historia

### TIKTOK/REELS
1. Sigue el script del video
2. Usa transiciones suaves entre paletas
3. Añade música trending

### TWITTER/LINKEDIN
1. Usa los banners específicos
2. Comparte el proceso técnico
3. Incluye snippets de código

## 🎯 TEXTO SUGERIDO

### POST PRINCIPAL
\"¡Transformo conceptos en paletas de colores con Python! 🎨

Mi nuevo proyecto usa IA y Machine Learning para generar combinaciones de colores únicas desde cualquier tema.

🤖 Tecnología: Python + K-means + HSL color model
🎨 Resultados: Paletas listas para diseño
💡 Aplicaciones: UI/UX, branding, arte digital

¿Qué tema te gustaría que convierta en colores? 👇

#Python #IA #MachineLearning #ArteGenerativo #Diseño #Programación\"

### STORIES/REELS
\"De idea → código → paleta 🎨
Watch how AI transforms concepts into color magic! ✨
Swipe up for the code! 👆\"

## 🏷️ HASHTAGS SUGERIDOS
#Python #IA #MachineLearning #ArteGenerativo #DataScience #Programación #Diseño #PaletaDeColores #OpenSource #Tech

---
Generado automáticamente por el Generador de Paletas IA
"""
        
        with open('redes_sociales/INSTRUCCIONES_REDES.md', 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print("✅ Guía de redes creada: redes_sociales/INSTRUCCIONES_REDES.md")