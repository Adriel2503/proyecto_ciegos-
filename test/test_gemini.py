import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

def test_gemini_connection():
    """Probar la conexión con Gemini API"""
    
    # Configurar la API key
    api_key = os.getenv("GEMINI_API")
    
    if not api_key:
        print("❌ Error: No se encontró GEMINI_API en el archivo .env")
        return False
    
    print("✅ API Key encontrada en .env")
    print(f"🔑 API Key (primeros 10 caracteres): {api_key[:10]}...")
    
    # Configurar Gemini
    genai.configure(api_key=api_key)
    
    try:
        print("\n🤖 Enviando pregunta de prueba a Gemini...")
        
        # Crear el modelo
        model = genai.GenerativeModel('gemini-pro')
        
        # Hacer una pregunta simple para probar
        response = model.generate_content("Responde con una sola palabra: ¿Cuál es la capital de Francia?")
        
        respuesta = response.text.strip()
        print(f"📝 Respuesta de Gemini: {respuesta}")
        
        if "París" in respuesta or "Paris" in respuesta or "paris" in respuesta:
            print("✅ ¡Perfecto! La API de Gemini está funcionando correctamente")
            return True
        else:
            print(f"⚠️  La API respondió, pero la respuesta parece incorrecta: {respuesta}")
            return True
            
    except Exception as e:
        print(f"❌ Error al conectar con Gemini: {str(e)}")
        print("\n💡 Verifica que:")
        print("   1. Tu API key sea válida")
        print("   2. Tengas instalada la librería: pip install google-generativeai")
        print("   3. Tu API key tenga permisos para usar Gemini")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 TEST DE CONEXIÓN CON GEMINI API")
    print("=" * 50)
    print()
    
    resultado = test_gemini_connection()
    
    print()
    print("=" * 50)
    if resultado:
        print("✅ TEST COMPLETADO EXITOSAMENTE")
    else:
        print("❌ TEST FALLIDO")
    print("=" * 50)

