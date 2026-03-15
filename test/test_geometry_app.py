"""
Script de prueba para verificar componentes de la aplicación de geometría
"""
import sys
import os
from dotenv import load_dotenv

print("=" * 60)
print("🧪 PRUEBA DE COMPONENTES - Tutor de Geometría Visual")
print("=" * 60)

# 1. Verificar entorno virtual
print("\n1️⃣ Verificando entorno Python...")
print(f"   Python: {sys.version}")
print(f"   Ruta ejecutable: {sys.executable}")

# 2. Verificar dependencias
print("\n2️⃣ Verificando dependencias instaladas...")
dependencies = {
    'PyQt5': None,
    'cv2': 'opencv-python',
    'PIL': 'Pillow',
    'openai': None,
    'pyttsx3': None,
    'dotenv': 'python-dotenv',
    'numpy': None
}

missing = []
for module_name, package_name in dependencies.items():
    try:
        __import__(module_name)
        print(f"   ✅ {package_name or module_name}")
    except ImportError:
        print(f"   ❌ {package_name or module_name} - NO INSTALADO")
        missing.append(package_name or module_name)

if missing:
    print(f"\n   ⚠️ Falta instalar: {', '.join(missing)}")
    print("   Ejecuta: pip install -r requirements.txt")
else:
    print("   ✅ Todas las dependencias están instaladas")

# 3. Verificar API Key
print("\n3️⃣ Verificando configuración de OpenAI...")
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    masked_key = api_key[:8] + "..." + api_key[-4:]
    print(f"   ✅ API Key encontrada: {masked_key}")
else:
    print("   ❌ API Key NO encontrada")
    print("   Crea un archivo .env con: OPENAI_API_KEY=tu_clave_aqui")

# 4. Verificar motor TTS
print("\n4️⃣ Verificando motor de texto a voz...")
try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"   ✅ Motor TTS inicializado")
    print(f"   📢 Voces disponibles: {len(voices)}")
    
    spanish_voices = [v for v in voices if 'spanish' in v.name.lower() or 'es' in v.id.lower()]
    if spanish_voices:
        print(f"   🇪🇸 Voces en español: {len(spanish_voices)}")
    else:
        print("   ⚠️ No se encontraron voces en español")
    
    engine.stop()
except Exception as e:
    print(f"   ❌ Error al inicializar TTS: {e}")

# 5. Verificar cámaras disponibles
print("\n5️⃣ Verificando cámaras disponibles...")
try:
    import cv2
    found_cameras = []
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                found_cameras.append((i, width, height))
            cap.release()
    
    if found_cameras:
        print(f"   ✅ Se encontraron {len(found_cameras)} cámara(s)")
        for idx, width, height in found_cameras:
            print(f"      • Cámara {idx}: {width}x{height}")
    else:
        print("   ⚠️ No se detectaron cámaras")
        print("   La aplicación funcionará pero necesitarás conectar una cámara")
except Exception as e:
    print(f"   ❌ Error al verificar cámaras: {e}")

# 6. Verificar imports del archivo principal
print("\n6️⃣ Verificando imports de math_transcriptor_desktop.py...")
try:
    # Simular imports del archivo principal sin ejecutarlo
    import sys
    import cv2
    import numpy as np
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer, QThread, pyqtSignal
    from PIL import Image
    import openai
    import base64
    import io
    from dotenv import load_dotenv
    import pyttsx3
    print("   ✅ Todos los imports son correctos")
except Exception as e:
    print(f"   ❌ Error en imports: {e}")

# Resumen final
print("\n" + "=" * 60)
print("📊 RESUMEN DE LA PRUEBA")
print("=" * 60)

if not missing and api_key:
    print("✅ El sistema está listo para ejecutar la aplicación")
    print("\n🚀 Para iniciar la aplicación, ejecuta:")
    print("   python math_transcriptor_desktop.py")
else:
    print("⚠️ Se encontraron algunos problemas que debes resolver:")
    if missing:
        print(f"   • Instalar paquetes: {', '.join(missing)}")
    if not api_key:
        print("   • Configurar OPENAI_API_KEY en archivo .env")

print("=" * 60)



