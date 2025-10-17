import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # No necesitamos API key para Craiyon
    @classmethod
    def validate_config(cls):
        print("✅ Configuración validada - Usando DALL-E Mini (Gratuito)")
        return True