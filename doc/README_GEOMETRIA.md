# 📐 Tutor de Geometría Visual - Asistente Educativo con Audio

## 🎯 Descripción

Aplicación de escritorio que ayuda a estudiantes a comprender figuras geométricas mediante análisis visual con inteligencia artificial y explicaciones en audio.

## ✨ Características Principales

### 🔍 Reconocimiento de Figuras Geométricas
La aplicación puede identificar y analizar **5 tipos** de imágenes geométricas:

1. **📏 Línea Recta** - Líneas simples (horizontales, verticales o diagonales)
2. **📐 Regla Graduada en Centímetros** - Reglas con escala métrica
3. **📏 Regla Graduada en Pulgadas** - Reglas con escala imperial
4. **✖️ Rectas Cruzadas** - Dos o más líneas que se intersectan
5. **📊 Ejes Cartesianos** - Sistema de coordenadas con ejes X e Y

### 👨‍🏫 Explicación Educativa
- Análisis detallado por un "profesor virtual de geometría"
- Explicaciones estructuradas en 6 secciones:
  - **Identificación**: Tipo de figura
  - **Definición**: Concepto geométrico formal
  - **Características**: Descripción detallada de lo observado
  - **Propiedades**: Propiedades geométricas importantes
  - **Aplicaciones**: Usos en la vida real
  - **Conceptos Relacionados**: Conexiones con otros temas

### 🔊 Audio Integrado
- Generación automática de audio de la explicación
- Botón **▶️ Reproducir Audio** para escuchar la explicación
- Botón **💾 Guardar Audio** para exportar el archivo WAV
- Compatible con Windows, macOS y Linux

## 🛠️ Tecnologías Utilizadas

- **Python 3.12**
- **PyQt5** - Interfaz gráfica de usuario
- **OpenCV** - Captura de cámara y procesamiento de imágenes
- **OpenAI GPT-4o** - Análisis visual de imágenes geométricas
- **OpenAI GPT-4o-mini** - Generación de explicaciones educativas
- **pyttsx3** - Síntesis de voz (Text-to-Speech)

## 📋 Requisitos Previos

### Dependencias
```bash
pip install -r requirements.txt
```

### Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:
```
OPENAI_API_KEY=tu_clave_api_aqui
```

## 🚀 Instalación

1. **Clonar o descargar el proyecto**

2. **Activar entorno virtual** (Git Bash en Windows):
```bash
source venv/Scripts/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar API Key de OpenAI**:
   - Crear archivo `.env` con tu clave API

5. **Ejecutar la aplicación**:
```bash
python math_transcriptor_desktop.py
```

## 📖 Guía de Uso

### Paso 1: Configurar la Cámara
1. Selecciona tu cámara del menú desplegable
2. Presiona **▶️ Iniciar Cámara**
3. Verás la vista previa en tiempo real

### Paso 2: Capturar la Figura
1. Coloca la figura geométrica frente a la cámara
2. Ajusta el encuadre para que la figura sea visible
3. Presiona **📸 Capturar Imagen**
4. La imagen capturada aparecerá en el panel izquierdo

### Paso 3: Analizar la Geometría
1. Presiona **📐 Analizar Geometría**
2. Espera mientras el sistema analiza (verás barra de progreso)
3. El análisis usa dos modelos de IA:
   - **GPT-4o Vision**: Identifica el tipo de figura y características
   - **GPT-4o-mini**: Genera explicación educativa detallada

### Paso 4: Escuchar la Explicación
1. Automáticamente se genera el audio
2. Presiona **▶️ Reproducir Audio** para escuchar
3. Opcional: **💾 Guardar Audio** para exportar el archivo

### Funciones Adicionales
- **📋 Copiar Texto**: Copia la explicación al portapapeles
- **🗑️ Limpiar**: Borra el resultado y audio para nuevo análisis
- **🔄 Refrescar Cámaras**: Detecta nuevas cámaras conectadas

## 🎓 Ejemplo de Explicación Generada

Para **Ejes Cartesianos**, la aplicación genera:

```
Identificación: Observamos un sistema de ejes cartesianos, 
también conocido como plano coordenado.

Definición: Los ejes cartesianos son un sistema de referencia 
formado por dos rectas numéricas perpendiculares...

Características: En la imagen podemos ver que ambos ejes 
se cruzan en el punto de origen...

[continúa con Propiedades, Aplicaciones y Conceptos Relacionados]
```

## ⚙️ Arquitectura Técnica

### Flujo de Procesamiento
```
📷 Cámara → 📸 Captura → 🔍 GPT-4o Vision (análisis técnico)
           ↓
👨‍🏫 GPT-4o-mini (explicación educativa) → 🔊 Generación de Audio
           ↓
▶️ Reproducción / 💾 Guardar
```

### Componentes Principales
- **`TranscriptionWorker`**: Hilo separado para procesamiento IA (no bloquea UI)
- **`MathTranscriptorApp`**: Ventana principal con PyQt5
- **Prompts especializados**: Instrucciones optimizadas para cada modelo

## 🔧 Solución de Problemas

### No se detecta la cámara
- Verificar que la cámara esté conectada
- Presionar **🔄 Refrescar Cámaras**
- Probar con diferentes índices de cámara

### Error de API Key
- Verificar que el archivo `.env` existe
- Confirmar que `OPENAI_API_KEY` está configurada correctamente
- Revisar que la clave API es válida

### Audio no se reproduce
- Verificar que el motor TTS está instalado
- En Windows: pyttsx3 usa SAPI5 (incluido en el sistema)
- Revisar la configuración de audio del sistema

### Análisis toma mucho tiempo
- El análisis usa dos modelos de IA (puede tomar 10-30 segundos)
- Verificar conexión a internet
- La barra de progreso indica que el proceso está activo

## 📝 Notas de Desarrollo

### Diferencias con la Versión Original
Esta versión está adaptada de `math_transcriptor_desktop.py` con los siguientes cambios:

- ✅ Prompts rediseñados para geometría (antes: matemáticas de primaria)
- ✅ Detección de 5 tipos de figuras geométricas
- ✅ Explicaciones más técnicas y detalladas
- ✅ Audio generado automáticamente en archivo WAV
- ✅ Botón Play para reproducción inmediata
- ✅ Función de guardar audio en ubicación elegida
- ✅ Limpieza automática de archivos temporales

## 🎯 Casos de Uso

### Educación
- Profesores explicando conceptos geométricos
- Estudiantes con discapacidad visual
- Aprendizaje remoto y clases online

### Auto-estudio
- Comprensión de figuras en libros de texto
- Repaso de conceptos geométricos
- Práctica con diferentes tipos de figuras

### Accesibilidad
- Descripción auditiva de figuras geométricas
- Apoyo para estudiantes con dificultades de lectura
- Material educativo inclusivo

## 📄 Licencia

Este proyecto es educativo y de código abierto.

## 🤝 Contribuciones

Las mejoras y sugerencias son bienvenidas. Áreas de mejora potenciales:
- Soporte para más tipos de figuras geométricas
- Múltiples idiomas
- Mejoras en la calidad del audio
- Exportación a más formatos (MP3, texto, PDF)
- Historial de análisis

## 📧 Contacto

Para preguntas o sugerencias sobre esta aplicación, por favor abre un issue en el repositorio.

---

**Desarrollado con ❤️ para facilitar el aprendizaje de geometría**

