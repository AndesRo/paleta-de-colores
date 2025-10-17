from config import Config
from src.generador_paletas import GeneradorPaletasIA
from src.utils import mostrar_resumen_paleta
import os

def prueba_rapida():
    """Script de prueba rápida con DALL-E Mini"""
    try:
        print("🧪 EJECUTANDO PRUEBA RÁPIDA CON DALL-E MINI")
        print("=" * 50)
        
        # Validar configuración
        Config.validate_config()
        
        # Inicializar generador
        generador = GeneradorPaletasIA()
        
        # Probar con un solo tema
        tema_prueba = "atardecer en la playa"
        print(f"🎨 Tema de prueba: {tema_prueba}")
        print("🤖 Usando: DALL-E Mini (Craiyon) - Gratuito")
        
        # Generar paleta
        resultado = generador.generar_paleta_completa(tema_prueba)
        
        if resultado:
            print("\n✅ ¡PRUEBA EXITOSA!")
            mostrar_resumen_paleta(resultado)
            
            # Mostrar archivos generados
            print("\n📁 ARCHIVOS GENERADOS:")
            if os.path.exists('outputs'):
                archivos = os.listdir('outputs')
                for archivo in archivos:
                    if tema_prueba.replace(' ', '_') in archivo:
                        print(f"   📄 {archivo}")
        else:
            print("❌ PRUEBA FALLIDA")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        print("\n💡 POSIBLES SOLUCIONES:")
        print("   1. Verifica tu conexión a internet")
        print("   2. Asegúrate de tener las dependencias instaladas")
        print("   3. El servicio Craiyon podría estar temporalmente no disponible")

if __name__ == "__main__":
    prueba_rapida()