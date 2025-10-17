import os
import json
from datetime import datetime

class AppConfig:
    """Configuración avanzada de la aplicación"""
    
    def __init__(self):
        self.config_dir = os.path.expanduser('~/.generador_paletas')
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self.proyectos_dir = os.path.join(self.config_dir, 'proyectos')
        self.exportaciones_dir = os.path.join(self.config_dir, 'exportaciones')
        
        # Crear directorios si no existen
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.proyectos_dir, exist_ok=True)
        os.makedirs(self.exportaciones_dir, exist_ok=True)
        
        self.config = self.cargar_config()
        
    def cargar_config(self):
        """Carga la configuración desde archivo"""
        config_default = {
            'ultimo_tema': 'atardecer en la playa',
            'ultimo_estilo': 'minimalista',
            'num_colores': 6,
            'directorio_guardado': os.path.expanduser('~/PaletasGeneradas'),
            'tema_oscuro': True,
            'historial_temas': [],
            'historial_paletas': [],
            'favoritos': [],
            'proyectos_recientes': [],
            'configuracion_exportacion': {
                'css': True,
                'json': True,
                'png': True,
                'svg': False
            },
            'preferencias_redes': {
                'incluir_hashtags': True,
                'incluir_tecnologia': True,
                'usuario_redes': '@tucuenta'
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Actualizar configuración por defecto con la cargada
                    config_default.update(loaded_config)
                    return config_default
            else:
                self.guardar_config(config_default)
                return config_default
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return config_default
            
    def guardar_config(self, config=None):
        """Guarda la configuración en archivo"""
        if config is None:
            config = self.config
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            
    def actualizar_historial(self, tema):
        """Actualiza el historial de temas"""
        if tema not in self.config['historial_temas']:
            self.config['historial_temas'].append(tema)
            # Mantener solo los últimos 20 temas
            self.config['historial_temas'] = self.config['historial_temas'][-20:]
            self.guardar_config()
            
    def guardar_proyecto(self, proyecto_data):
        """Guarda un proyecto en archivo separado"""
        try:
            nombre_archivo = f"{proyecto_data['nombre']}.json"
            archivo_path = os.path.join(self.proyectos_dir, nombre_archivo)
            
            with open(archivo_path, 'w', encoding='utf-8') as f:
                json.dump(proyecto_data, f, indent=2, ensure_ascii=False)
                
            # Actualizar proyectos recientes
            if archivo_path not in self.config['proyectos_recientes']:
                self.config['proyectos_recientes'].append(archivo_path)
                # Mantener solo los últimos 10 proyectos
                self.config['proyectos_recientes'] = self.config['proyectos_recientes'][-10:]
                self.guardar_config()
                
            return archivo_path
        except Exception as e:
            print(f"Error guardando proyecto: {e}")
            return None
            
    def cargar_proyecto(self, archivo_path):
        """Carga un proyecto desde archivo"""
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando proyecto: {e}")
            return None
            
    def get_proyectos_recientes(self):
        """Obtiene la lista de proyectos recientes"""
        return [os.path.basename(path) for path in self.config['proyectos_recientes']]