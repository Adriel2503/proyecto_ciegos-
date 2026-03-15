import openai
import os
from dotenv import load_dotenv
import numpy as np

# Cargar variables de entorno
load_dotenv()

def obtener_embedding(texto, modelo="text-embedding-3-small"):
    """
    Convierte un texto en un vector de embedding usando OpenAI
    
    Args:
        texto (str): La oración o texto a convertir
        modelo (str): Modelo de embedding a usar (por defecto text-embedding-3-small)
    
    Returns:
        list: Vector de embedding
    """
    # Configurar la API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("❌ Error: No se encontró OPENAI_API_KEY en el archivo .env")
    
    openai.api_key = api_key
    
    try:
        # Limpiar el texto
        texto = texto.replace("\n", " ")
        
        # Obtener el embedding
        response = openai.embeddings.create(
            input=[texto],
            model=modelo
        )
        
        embedding = response.data[0].embedding
        return embedding
        
    except Exception as e:
        print(f"❌ Error al obtener embedding: {str(e)}")
        raise

def calcular_similitud_coseno(embedding1, embedding2):
    """Calcula la similitud coseno entre dos embeddings"""
    # Convertir a arrays de numpy
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    
    # Calcular similitud coseno
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    similitud = dot_product / (norm1 * norm2)
    return similitud

def test_embeddings():
    """Prueba la generación de embeddings con varios ejemplos"""
    
    print("=" * 60)
    print("🧪 TEST DE EMBEDDINGS CON OPENAI")
    print("=" * 60)
    print()
    
    # Ejemplos de oraciones
    oraciones = [
        "El gato duerme en el sofá",
        "Un felino descansa en el sillón",
        "Me gusta programar en Python",
        "El sol brilla en el cielo"
    ]
    
    print("📝 Oraciones a procesar:")
    for i, oracion in enumerate(oraciones, 1):
        print(f"   {i}. {oracion}")
    print()
    
    # Obtener embeddings
    print("🤖 Generando embeddings...")
    embeddings = []
    
    for i, oracion in enumerate(oraciones, 1):
        try:
            embedding = obtener_embedding(oracion)
            embeddings.append(embedding)
            print(f"✅ Embedding {i} generado - Dimensiones: {len(embedding)}")
            print(f"   Primeros 5 valores: {embedding[:5]}")
            print()
        except Exception as e:
            print(f"❌ Error procesando oración {i}: {str(e)}")
            return False
    
    # Calcular similitudes
    print("=" * 60)
    print("📊 ANÁLISIS DE SIMILITUD ENTRE ORACIONES")
    print("=" * 60)
    print()
    
    # Comparar todas las oraciones entre sí
    for i in range(len(oraciones)):
        for j in range(i + 1, len(oraciones)):
            similitud = calcular_similitud_coseno(embeddings[i], embeddings[j])
            print(f"Similitud entre oración {i+1} y {j+1}: {similitud:.4f}")
            print(f"  '{oraciones[i]}'")
            print(f"  '{oraciones[j]}'")
            
            # Interpretación
            if similitud > 0.8:
                print(f"  → 🟢 Muy similares")
            elif similitud > 0.6:
                print(f"  → 🟡 Similares")
            elif similitud > 0.4:
                print(f"  → 🟠 Algo relacionadas")
            else:
                print(f"  → 🔴 Poco relacionadas")
            print()
    
    return True

def ejemplo_simple():
    """Ejemplo simple de uso"""
    print("=" * 60)
    print("💡 EJEMPLO SIMPLE DE USO")
    print("=" * 60)
    print()
    
    texto = "Python es un lenguaje de programación increíble"
    print(f"📝 Texto: '{texto}'")
    print()
    
    embedding = obtener_embedding(texto)
    
    print(f"✅ Embedding generado exitosamente")
    print(f"📏 Dimensiones del vector: {len(embedding)}")
    print(f"🔢 Tipo de datos: {type(embedding)}")
    print(f"📊 Primeros 10 valores:")
    for i, valor in enumerate(embedding[:10]):
        print(f"   [{i}]: {valor:.6f}")
    print(f"   ...")
    print()
    
    # Estadísticas
    embedding_array = np.array(embedding)
    print("📈 Estadísticas del embedding:")
    print(f"   Media: {embedding_array.mean():.6f}")
    print(f"   Desviación estándar: {embedding_array.std():.6f}")
    print(f"   Valor mínimo: {embedding_array.min():.6f}")
    print(f"   Valor máximo: {embedding_array.max():.6f}")
    print()

if __name__ == "__main__":
    try:
        # Primero mostrar un ejemplo simple
        ejemplo_simple()
        
        print()
        
        # Luego hacer el test completo con comparaciones
        resultado = test_embeddings()
        
        print("=" * 60)
        if resultado:
            print("✅ TEST COMPLETADO EXITOSAMENTE")
        else:
            print("❌ TEST FALLIDO")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        print("\n💡 Verifica que:")
        print("   1. Tu API key de OpenAI sea válida")
        print("   2. Tengas instaladas las librerías necesarias:")
        print("      pip install openai python-dotenv numpy")

