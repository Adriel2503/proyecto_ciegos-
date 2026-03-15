import os
import csv
import openai
from dotenv import load_dotenv
from supabase import create_client, Client
import time

# Cargar variables de entorno
load_dotenv()

def obtener_embedding(texto, modelo="text-embedding-3-large"):
    """Convierte un texto en un vector de embedding usando OpenAI"""
    try:
        # Configurar la API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ Error: No se encontró OPENAI_API_KEY en el archivo .env")
        
        openai.api_key = api_key
        
        # Limpiar el texto
        texto = texto.replace("\n", " ").strip()
        
        # Obtener el embedding
        response = openai.embeddings.create(
            input=[texto],
            model=modelo
        )
        
        return response.data[0].embedding
        
    except Exception as e:
        print(f"❌ Error al obtener embedding: {str(e)}")
        raise

def concatenar_fila(row, idx):
    """
    Concatena todas las columnas de una fila usando los nombres exactos de las columnas del CSV
    
    Formato: id{número} - Columna1: valor1, Columna2: valor2, ...
    """
    texto = (
        f"id{idx} - "
        f"Codigo_de_Sitio: {row['Codigo_de_Sitio']}, "
        f"Nombre_de_sitio: {row['Nombre_de_sitio']}, "
        f"Tecnologia: {row['Tecnologia']}, "
        f"Departamento: {row['Departamento']}, "
        f"Distrito: {row['Distrito']}, "
        f"Nro_CELDAS_EN_SERVICIO: {row['Nro_CELDAS_EN_SERVICIO']}, "
        f"Poblacion: {row['Poblacion']}, "
        f"Nro_Sitios: {row['Nro_Sitios']}"
    )
    return texto

def conectar_supabase():
    """Conecta con Supabase usando las credenciales del .env"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError(
            "❌ Error: No se encontraron SUPABASE_URL o SUPABASE_KEY en el archivo .env\n"
            "   Agrega estas líneas a tu .env:\n"
            "   SUPABASE_URL=tu_url_del_proyecto\n"
            "   SUPABASE_KEY=tu_api_key"
        )
    
    print(f"✅ Conectando a Supabase: {url[:30]}...")
    return create_client(url, key)

def procesar_y_subir_csv(archivo_csv, nombre_tabla="documents", limite=None):
    """
    Procesa el CSV y sube cada fila a Supabase con su embedding
    
    Args:
        archivo_csv: Ruta al archivo CSV
        nombre_tabla: Nombre de la tabla en Supabase
        limite: Número máximo de filas a procesar (None = todas)
    """
    
    print("=" * 70)
    print("🚀 PROCESO DE CARGA DE SITIOS A SUPABASE CON EMBEDDINGS")
    print("=" * 70)
    print()
    
    # Conectar a Supabase
    try:
        supabase = conectar_supabase()
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return
    
    # Leer el CSV
    print(f"📂 Leyendo archivo: {archivo_csv}")
    
    filas_procesadas = 0
    filas_exitosas = 0
    filas_fallidas = 0
    
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            # Usar ; como delimitador (según tu CSV)
            csv_reader = csv.DictReader(file, delimiter=';')
            
            print(f"📊 Columnas encontradas: {csv_reader.fieldnames}")
            print()
            
            for idx, row in enumerate(csv_reader, 1):
                # Aplicar límite si existe
                if limite and idx > limite:
                    print(f"\n⚠️  Límite de {limite} filas alcanzado")
                    break
                
                try:
                    # Concatenar toda la fila con el índice
                    texto_completo = concatenar_fila(row, idx)
                    
                    print(f"[{idx}] Procesando: {row['Codigo_de_Sitio']} - {row['Nombre_de_sitio']}")
                    print(f"    📝 Texto: {texto_completo[:100]}...")
                    
                    # Generar embedding
                    print(f"    🤖 Generando embedding...")
                    embedding = obtener_embedding(texto_completo)
                    print(f"    ✅ Embedding generado ({len(embedding)} dimensiones)")
                    
                    # Preparar metadata con toda la información del sitio
                    metadata = {
                        "codigo_sitio": row['Codigo_de_Sitio'],
                        "nombre_sitio": row['Nombre_de_sitio'],
                        "tecnologia": row['Tecnologia'],
                        "departamento": row['Departamento'],
                        "distrito": row['Distrito'],
                        "nro_celdas": int(row['Nro_CELDAS_EN_SERVICIO']) if row['Nro_CELDAS_EN_SERVICIO'] else 0,
                        "poblacion": int(row['Poblacion']) if row['Poblacion'] else 0,
                        "nro_sitios": int(row['Nro_Sitios']) if row['Nro_Sitios'] else 0
                    }
                    
                    # Preparar datos para Supabase (usando solo las 4 columnas que tienes)
                    datos = {
                        "content": texto_completo,
                        "metadata": metadata,
                        "embedding": embedding
                    }
                    
                    # Subir a Supabase
                    print(f"    ☁️  Subiendo a Supabase...")
                    result = supabase.table(nombre_tabla).insert(datos).execute()
                    
                    print(f"    ✅ Subido exitosamente")
                    print()
                    
                    filas_exitosas += 1
                    
                    # Pequeña pausa para no saturar la API
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"    ❌ Error procesando fila {idx}: {str(e)}")
                    print()
                    filas_fallidas += 1
                
                filas_procesadas += 1
        
        # Resumen final
        print("=" * 70)
        print("📊 RESUMEN DEL PROCESO")
        print("=" * 70)
        print(f"Total filas procesadas: {filas_procesadas}")
        print(f"✅ Exitosas: {filas_exitosas}")
        print(f"❌ Fallidas: {filas_fallidas}")
        print("=" * 70)
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo_csv}")
    except Exception as e:
        print(f"❌ Error general: {str(e)}")

def crear_tabla_supabase_sql():
    """Muestra el SQL para crear la tabla en Supabase (ACTUALIZADO)"""
    sql = """
-- SQL para crear la tabla en Supabase
-- Ve a SQL Editor en tu dashboard de Supabase y ejecuta esto:

-- Habilitar extensión de vectores
CREATE EXTENSION IF NOT EXISTS vector;

-- Crear tabla con estructura simple
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,                -- Texto completo concatenado
    metadata JSONB,              -- Información del sitio en formato JSON
    embedding VECTOR(3072),      -- Vector de embeddings (text-embedding-3-large)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear índice para búsquedas vectoriales rápidas
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Crear índice para búsquedas en metadata
CREATE INDEX idx_metadata_gin ON documents USING gin(metadata);

-- Función para búsqueda semántica
CREATE OR REPLACE FUNCTION match_documents (
    query_embedding VECTOR(3072),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id BIGINT,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        documents.id,
        documents.content,
        documents.metadata,
        1 - (documents.embedding <=> query_embedding) AS similarity
    FROM documents
    WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
    ORDER BY documents.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
"""
    return sql

if __name__ == "__main__":
    # Mostrar SQL para crear la tabla
    print("💡 IMPORTANTE: Primero debes crear la tabla en Supabase")
    print("   Copia y ejecuta este SQL en tu Supabase SQL Editor:")
    print()
    print(crear_tabla_supabase_sql())
    print()
    
    respuesta = input("¿Ya creaste la tabla en Supabase? (s/n): ")
    
    if respuesta.lower() == 's':
        print()
        # Preguntar si quiere procesar todo o hacer una prueba
        respuesta_test = input("¿Quieres hacer una prueba con solo 5 filas primero? (s/n): ")
        
        if respuesta_test.lower() == 's':
            limite = 5
        else:
            limite = None
        
        print()
        # Procesar y subir
        procesar_y_subir_csv(
            archivo_csv="sitios_demo.csv",
            nombre_tabla="documents",  # Cambia aquí si quieres otro nombre: "sitios", "sitios_telecom", etc.
            limite=limite
        )
    else:
        print("\n⚠️  Por favor, crea la tabla primero usando el SQL mostrado arriba.")
        print("   Luego vuelve a ejecutar este script.")

