from config import Config
from src.generador_paletas import GeneradorPaletasIA
from src.utils import guardar_datos_paleta, generar_texto_redes_sociales, mostrar_resumen_paleta
import time

def main():
    try:
        # Validar configuración
        Config.validate_config()
        
        # Inicializar generador (sin dependencias externas)
        generador = GeneradorPaletasIA()
        
        # Lista de temas para generar
        temas = [
            "atardecer en la playa tropical",
            "bosque mágico otoñal", 
            "ciudad cyberpunk nocturna",
            "jardín de flores silvestres"
        ]
        
        print("🚀 GENERADOR DE PALETAS - VERSIÓN LOCAL")
        print("=" * 50)
        print("💡 No se requieren APIs externas - 100% funcional")
        
        paletas_generadas = []
        
        for i, tema in enumerate(temas, 1):
            print(f"\n[{i}/{len(temas)}] Procesando: {tema}")
            
            # Generar paleta
            paleta_data = generador.generar_paleta_completa(tema)
            
            if paleta_data:
                # Guardar datos
                guardar_datos_paleta(paleta_data)
                
                # Mostrar resumen
                mostrar_resumen_paleta(paleta_data)
                
                # Guardar para uso posterior
                paletas_generadas.append(paleta_data)
        
        # Mostrar resumen final
        print(f"\n🎉 ¡Generación completada! {len(paletas_generadas)} paletas creadas")
        print("📍 Revisa la carpeta 'outputs' para ver los resultados")
        
        # Generar contenido para redes sociales
        if paletas_generadas:
            ultima_paleta = paletas_generadas[-1]
            print("\n📱 EJEMPLO DE CONTENIDO PARA INSTAGRAM:")
            print("=" * 50)
            print(generar_texto_redes_sociales(ultima_paleta, "instagram"))
            
    except Exception as e:
        print(f"❌ Error en la ejecución: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()