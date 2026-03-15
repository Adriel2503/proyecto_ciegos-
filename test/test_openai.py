import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_openai_connection():
    """Probar la conexión con OpenAI API"""
    
    # Configurar la API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: No se encontró OPENAI_API_KEY en el archivo .env")
        return False
    
    print("✅ API Key encontrada en .env")
    print(f"🔑 API Key (primeros 10 caracteres): {api_key[:10]}...")
    
    # Configurar OpenAI
    openai.api_key = api_key
    
    try:
        print("\n🤖 Enviando pregunta de prueba a OpenAI...")
        
        # Hacer una pregunta simple para probar
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user", 
                    "content": "Responde con una sola palabra: ¿Cuál es la capital de España?"
                }
            ],
            max_tokens=10
        )
        
        respuesta = response.choices[0].message.content.strip()
        print(f"📝 Respuesta de OpenAI: {respuesta}")
        
        if "Madrid" in respuesta or "madrid" in respuesta:
            print("✅ ¡Perfecto! La API de OpenAI está funcionando correctamente")
            return True
        else:
            print(f"⚠️  La API respondió, pero la respuesta parece incorrecta: {respuesta}")
            return True
            
    except Exception as e:
        print(f"❌ Error al conectar con OpenAI: {str(e)}")
        
        # Mensajes de ayuda según el tipo de error
        if "authentication" in str(e).lower():
            print("\n💡 Posibles soluciones:")
            print("   - Verifica que tu API key sea correcta")
            print("   - Asegúrate de que tu cuenta de OpenAI tenga créditos")
            print("   - Revisa que no haya espacios extra en el .env")
            
        elif "rate limit" in str(e).lower():
            print("\n💡 Has excedido el límite de requests. Espera un momento e intenta de nuevo.")
            
        elif "quota" in str(e).lower():
            print("\n💡 Has agotado tu cuota de OpenAI. Revisa tu cuenta y agrega créditos.")
            
        return False

def main():
    print("🧪 Probando conexión con OpenAI API...")
    print("=" * 50)
    
    if test_openai_connection():
        print("\n🎉 ¡Todo listo! Puedes usar la aplicación principal.")
    else:
        print("\n🔧 Revisa la configuración antes de usar la aplicación principal.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
