import streamlit as st
import openai
from PIL import Image
import base64
import io
import os
import cv2
import numpy as np
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar la API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def detect_cameras():
    """Detectar cámaras disponibles en el sistema"""
    cameras = []
    
    # Probar hasta 5 índices de cámara
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Obtener información de la cámara
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            
            camera_info = {
                'index': i,
                'name': f"Cámara {i}",
                'resolution': f"{int(width)}x{int(height)}"
            }
            
            # Identificar tipos comunes de cámara
            if i == 0:
                camera_info['name'] = "📱 Cámara Frontal del Laptop"
            elif i == 1:
                camera_info['name'] = "📷 Webcam USB"
            else:
                camera_info['name'] = f"📹 Cámara {i}"
                
            cameras.append(camera_info)
            cap.release()
        else:
            break
    
    return cameras

def capture_frame(camera_index):
    """Capturar un frame de la cámara especificada"""
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        return None
    
    # Configurar la cámara para mejor calidad
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Capturar frame
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # Convertir de BGR a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(frame_rgb)
    else:
        return None

def encode_image(image):
    """Convertir imagen a base64 para enviar a OpenAI"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def transcribe_math_image(image):
    """Enviar imagen a OpenAI GPT-4 Vision para transcripción matemática"""
    
    # Convertir imagen a base64
    base64_image = encode_image(image)
    
    # Prompt del sistema
    system_prompt = """Eres un asistente especializado en transcribir contenido matemático de manera totalmente accesible. Tu tarea es:
1. Transcribir TODO el contenido matemático a palabras
2. No dejar NINGÚN símbolo matemático sin convertir a texto
3. Describir cada operación y relación matemática en palabras naturales
4. Usar un lenguaje claro y consistente
5. Mantener el orden lógico de lectura"""

    # Prompt del usuario
    user_prompt = """Transcribe el contenido de esta imagen matemática convirtiendo TODOS los elementos matemáticos a palabras. 

Sigue estas reglas de transcripción:

Símbolos básicos:
- ∫ → [integral de]
- ∑ → [sumatoria de]
- ∂ → [derivada parcial de]
- √ → [raíz cuadrada de]
- ∞ → [infinito]

Operaciones:
- + → [más]
- - → [menos]
- × o * → [multiplicado por]
- ÷ o / → [dividido por]
- = → [igual a]
- ≠ → [no igual a]
- ≤ → [menor o igual que]
- ≥ → [mayor o igual que]

Potencias y subíndices:
- x² → [x elevado al cuadrado]
- x³ → [x elevado al cubo]
- xⁿ → [x elevado a la n]
- x₁ → [x subíndice uno]
- aᵢ → [a subíndice i]

Fracciones:
- ½ → [un medio]
- ¾ → [tres cuartos]
- a/b → [a dividido por b]

Letras griegas:
- π → [pi]
- θ → [theta]
- α → [alfa]
- β → [beta]
- Σ → [sigma mayúscula]
- σ → [sigma]

Funciones:
- sin → [seno de]
- cos → [coseno de]
- tan → [tangente de]
- log → [logaritmo de]
- ln → [logaritmo natural de]
- lim → [límite cuando]

Ejemplos:
- "∫₀∞ x² dx = 5" → "[integral desde cero hasta infinito de] [x elevado al cuadrado] [diferencial de x] [igual a] [cinco]"
- "y = 2x² + 3x - 5" → "[y igual a] [dos multiplicado por x elevado al cuadrado] [más] [tres multiplicado por x] [menos] [cinco]"

Transcribe TODO el contenido visible en la imagen."""
    
    try:
        # Llamada a la API de OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error al procesar la imagen: {str(e)}"

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="Transcriptor de Matemáticas Accesible",
        page_icon="📐",
        layout="wide"
    )
    
    # Título principal
    st.title("📐 Transcriptor de Matemáticas Accesible")
    st.markdown("### Convierte contenido matemático en texto accesible para personas ciegas")
    
    # Verificar si la API key está configurada
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ Error: No se encontró la clave de API de OpenAI. Asegúrate de tener un archivo .env con OPENAI_API_KEY")
        return
    
    # Sidebar para configuración de cámara
    with st.sidebar:
        st.header("📷 Configuración de Cámara")
        
        # Detectar cámaras disponibles
        if st.button("🔍 Detectar Cámaras"):
            with st.spinner("Detectando cámaras..."):
                cameras = detect_cameras()
                st.session_state.available_cameras = cameras
        
        # Mostrar cámaras disponibles
        if 'available_cameras' in st.session_state and st.session_state.available_cameras:
            st.success(f"✅ {len(st.session_state.available_cameras)} cámara(s) encontrada(s)")
            
            # Crear opciones para el selectbox
            camera_options = []
            for cam in st.session_state.available_cameras:
                camera_options.append(f"{cam['name']} ({cam['resolution']})")
            
            # Selector de cámara
            selected_camera_display = st.selectbox(
                "Selecciona una cámara:",
                camera_options,
                index=0  # Por defecto la primera (frontal del laptop)
            )
            
            # Obtener el índice de la cámara seleccionada
            selected_index = camera_options.index(selected_camera_display)
            st.session_state.selected_camera_index = st.session_state.available_cameras[selected_index]['index']
            
            st.info(f"📹 Cámara activa: {st.session_state.available_cameras[selected_index]['name']}")
            
        else:
            st.warning("⚠️ Haz clic en 'Detectar Cámaras' para encontrar dispositivos disponibles")
            # Por defecto usar cámara 0
            st.session_state.selected_camera_index = 0
    
    # Crear columnas para la interfaz principal
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📷 Captura de Imagen")
        
        # Área para mostrar vista previa
        preview_placeholder = st.empty()
        
        # Botones de control
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            if st.button("👁️ Vista Previa", type="secondary", use_container_width=True):
                camera_index = st.session_state.get('selected_camera_index', 0)
                with st.spinner("Obteniendo vista previa..."):
                    preview_image = capture_frame(camera_index)
                    if preview_image:
                        preview_placeholder.image(preview_image, caption="Vista previa de la cámara", use_container_width=True)
                        st.session_state.preview_image = preview_image
                    else:
                        st.error("❌ No se pudo acceder a la cámara")
        
        with col1_2:
            if st.button("📸 Capturar Foto", type="primary", use_container_width=True):
                camera_index = st.session_state.get('selected_camera_index', 0)
                with st.spinner("Capturando imagen..."):
                    captured_image = capture_frame(camera_index)
                    if captured_image:
                        st.session_state.captured_image = captured_image
                        preview_placeholder.image(captured_image, caption="Imagen capturada", use_container_width=True)
                        st.success("✅ Imagen capturada exitosamente")
                    else:
                        st.error("❌ No se pudo capturar la imagen")
        
        # Botón para transcribir
        if 'captured_image' in st.session_state:
            if st.button("🔄 Transcribir Contenido", type="primary", use_container_width=True):
                with st.spinner("Procesando imagen con IA..."):
                    resultado = transcribe_math_image(st.session_state.captured_image)
                    st.session_state.resultado_transcripcion = resultado
    
    with col2:
        st.header("📝 Resultado de la Transcripción")
        
        if 'resultado_transcripcion' in st.session_state:
            st.markdown("**Texto transcrito:**")
            
            # Mostrar el resultado en un área de texto
            st.text_area(
                "Contenido transcrito:",
                value=st.session_state.resultado_transcripcion,
                height=300,
                help="Este texto está optimizado para ser leído por lectores de pantalla"
            )
            
            # Botón para copiar al portapapeles
            if st.button("📋 Copiar al Portapapeles", use_container_width=True):
                st.write("📋 Texto copiado (usa Ctrl+C para copiar manualmente)")
            
            # Opción de descarga
            st.download_button(
                label="💾 Descargar como archivo de texto",
                data=st.session_state.resultado_transcripcion,
                file_name="transcripcion_matematica.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("👆 Captura una imagen para ver la transcripción aquí")
    
    # Información adicional
    st.markdown("---")
    st.markdown("### ℹ️ Información")
    st.markdown("""
    Esta aplicación está diseñada para hacer el contenido matemático accesible a personas ciegas:
    - **Selección de cámara** entre frontal del laptop y webcam USB
    - **Vista previa** en tiempo real antes de capturar
    - **Símbolos matemáticos** se convierten en descripciones de texto
    - **Operaciones** se describen en lenguaje natural
    - **Potencias y subíndices** se expresan en palabras
    - El resultado está optimizado para **lectores de pantalla**
    
    ### 🎯 Cómo usar:
    1. **Detectar cámaras** en el sidebar
    2. **Seleccionar** entre cámara frontal o webcam USB
    3. **Vista previa** para enfocar el contenido
    4. **Capturar** la imagen cuando esté bien encuadrada
    5. **Transcribir** para obtener el texto accesible
    """)

if __name__ == "__main__":
    main()
