try:
    import requests
    import PIL
    import numpy as np
    from sklearn.cluster import KMeans
    import webcolors
    import matplotlib.pyplot as plt
    import os
    from datetime import datetime
    
    print("✅ Todas las dependencias están instaladas correctamente!")
    print("🚀 Puedes ejecutar: python main.py")
    
except ImportError as e:
    print(f"❌ Error: {e}")
    print("💡 Ejecuta: pip install requests pillow numpy scikit-learn matplotlib webcolors python-dotenv")