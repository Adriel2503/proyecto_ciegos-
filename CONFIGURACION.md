# Configuración del Proyecto

## Variables de Entorno

Este proyecto requiere un archivo `.env` en la raíz del proyecto con las siguientes variables:

### 1. OpenAI API (REQUERIDO)

```
OPENAI_API_KEY=sk-proj-xxx...
```

**¿Cómo obtenerlo?**
- Ve a https://platform.openai.com/api-keys
- Crea una nueva API Key
- Cópiala y pégala en `.env`

**¿Por qué se necesita?**
- Para GPT-4 Vision: Análisis técnico de imágenes matemáticas
- Para GPT-4o-mini: Generación de explicaciones educativas

### 2. Google Gemini API (OPCIONAL)

```
GEMINI_API=AIzaSyA...
```

**¿Cómo obtenerlo?**
- Ve a https://makersuite.google.com/app/apikey
- Genera una nueva API key
- Cópiala en `.env`

**¿Por qué se necesita?**
- Alternativa a OpenAI para análisis de imágenes
- Útil para A/B testing de modelos

### 3. Supabase (OPCIONAL)

```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGciOi...
```

**¿Cómo obtenerlo?**
- Crea un proyecto en https://supabase.com
- Ve a Settings > API
- Copia la URL y la anon key

**¿Por qué se necesita?**
- Para guardar datos de usuarios
- Para historial de análisis
- Para seguimiento de progreso

## Configuración del .env

### Paso 1: Crear archivo .env

```bash
# Desde la carpeta raíz del proyecto
cp .env.example .env
```

### Paso 2: Editar .env con tus claves

Abre `.env` y reemplaza los valores:

```
OPENAI_API_KEY=sk-proj-tu_clave_real_aqui
GEMINI_API=tu_clave_gemini_aqui
SUPABASE_URL=tu_url_supabase
SUPABASE_KEY=tu_key_supabase
```

### Paso 3: Verificar que funciona

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('OK' if os.getenv('OPENAI_API_KEY') else 'ERROR')"
```

## Seguridad

- **NUNCA** commitear el archivo `.env` con claves reales
- El `.gitignore` ya ignora `.env`
- Usar `.env.example` para documentar qué variables se necesitan
- Regenerar API keys si las expusiste accidentalmente

## Solución de Problemas

### "No se encontró OPENAI_API_KEY"
- Verifica que `.env` existe en la carpeta raíz
- Verifica que la clave está correctamente escrita
- Reinicia la aplicación después de editar `.env`

### "Error de conexión a la API"
- Verifica que tu API key es válida
- Verifica tu conexión a internet
- Verifica que tienes cuota disponible en tu cuenta OpenAI

### "Error de autorización"
- Tu API key puede haber expirado
- Tu cuenta OpenAI puede no tener acceso a los modelos
- Genera una nueva API key y actualiza `.env`
