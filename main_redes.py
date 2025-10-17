from src.generador_paletas import GeneradorPaletasIA
from visualizador_redes import VisualizadorRedesSociales
from src.utils import guardar_datos_paleta
import os

def main():
    print("🎨 GENERADOR DE CONTENIDO PARA REDES SOCIALES")
    print("=" * 60)
    
    # Inicializar generador y visualizador
    generador = GeneradorPaletasIA()
    visualizador = VisualizadorRedesSociales()
    
    # Temas para generar (elige los más visuales)
    temas_redes = [
        "atardecer en la playa tropical",
        "ciudad cyberpunk futurista", 
        "bosque mágico de hadas",
        "galaxia espacial profunda",
        "festival de colores vibrantes",
        "café vintage parisino"
    ]
    
    print("🖌️ Generando paletas para redes sociales...")
    paletas_generadas = []
    
    for i, tema in enumerate(temas_redes, 1):
        print(f"\n[{i}/{len(temas_redes)}] Creando: {tema}")
        
        paleta_data = generador.generar_paleta_completa(tema)
        if paleta_data:
            guardar_datos_paleta(paleta_data)
            paletas_generadas.append(paleta_data)
    
    print(f"\n✅ {len(paletas_generadas)} paletas generadas")
    
    # Generar kit completo para redes sociales
    print("\n📱 CREANDO CONTENIDO PARA REDES SOCIALES...")
    visualizador.generar_kit_redes(paletas_generadas)
    
    # Mostrar resumen
    print(f"\n🎉 ¡CONTENIDO LISTO PARA COMPARTIR!")
    print("=" * 50)
    print("📁 Carpeta 'redes_sociales' contiene:")
    print("   🖼️  Banners para todas las plataformas")
    print("   🎠  Carousels para Instagram")
    print("   🎬  Script para videos/TikTok/Reels")
    print("   📖  Guía completa de uso")
    print("\n🚀 ¡Ahora comparte tu proyecto en redes!")
    print("   📸 Instagram: Sube los carousels")
    print("   🐦 Twitter: Comparte los banners")
    print("   💼 LinkedIn: Posts profesionales")
    print("   ⏰ TikTok/Reels: Sigue el script")

if __name__ == "__main__":
    main()