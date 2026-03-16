# GeomAI - Tutor de Geometria Visual para Personas Ciegas

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--mini-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Aplicacion desktop que describe figuras geometricas de forma tactil y sensorial para personas ciegas, usando IA en cascada y sintesis de voz.

## Arquitectura en Cascada

El sistema usa dos llamadas secuenciales al mismo modelo con prompts especializados:

```
Webcam (OpenCV)
  |
  v
PIL Image --> base64 PNG
  |
  v
GPT-4.1-mini Vision  (system: especialista tactil/sensorial)
  |  Entrada: imagen base64
  |  Salida:  analisis estructurado (TEXTO, PUNTOS, LINEAS, INTERSECCIONES, TACTIL)
  v
GPT-4.1-mini Educativo  (system: profesor de geometria para ciegos)
  |  Entrada: analisis tecnico del paso anterior
  |  Salida:  3 parrafos sensoriales (que toca, como esta organizado, para que sirve)
  v
pyttsx3 --> WAV temporal --> reproduccion / exportacion
```

### Paso 1: Analisis Tactil (Vision)

`OpenAIAnalyzer.analyze_geometric_figure()` envia la imagen con un prompt que pide describir la figura como si se tocara con las manos. El modelo extrae:

- **TEXTO**: nombre de la figura
- **PUNTOS CLAVE**: posicion de vertices/esquinas
- **LINEAS**: direccion y tipo (rectas, curvas)
- **INTERSECCIONES**: donde se cruzan y angulo que forman
- **TACTIL**: caracteristica principal que sentiria una persona ciega

### Paso 2: Explicacion Sensorial (Educativo)

`OpenAIAnalyzer.generate_educational_explanation()` toma el analisis tecnico y genera 3 parrafos:

1. **Que toca**: que siente la persona al tocar la figura
2. **Como esta organizado**: distribucion de puntos y lineas en el espacio
3. **Para que sirve**: aplicaciones practicas

El prompt usa lenguaje como "si pasas la mano", "sentiras", "los lados se cruzan". Sin emojis, optimizado para escuchar por audio.

### Figuras Soportadas

- Tipos de rectas (paralelas, perpendiculares, secantes)
- Tipos de triangulos (equilatero, isosceles, escaleno)
- Tipos de cuadrilateros (cuadrado, rectangulo, rombo, trapecio)
- Lineas rectas, reglas graduadas, rectas cruzadas, ejes cartesianos

## Estructura del Proyecto

```
Proyecto_Ciegos/
├── math_transcriptor_desktop.py   # Punto de entrada, ventana PyQt5
├── core/
│   ├── camera_manager.py          # Deteccion, apertura y captura de webcam
│   ├── openai_analyzer.py         # Cascada IA: vision tactil + explicacion sensorial
│   └── audio_manager.py           # TTS, generacion WAV, reproduccion y exportacion
├── utils/
│   ├── config.py                  # Constantes y env vars centralizadas
│   └── styles.py                  # QSS stylesheet de la interfaz
├── pyproject.toml                 # Dependencias pinneadas (hatchling)
├── .env.example                   # Template de variables de entorno
└── README.md
```

### Modulos en Detalle

**`math_transcriptor_desktop.py`** - Ventana principal (`MathTranscriptorApp`, hereda `QMainWindow`). Layout de dos paneles: izquierdo para camara y controles, derecho para resultado y audio. El analisis de IA corre en un `QThread` (`TranscriptionWorker`) para no bloquear la UI. Cuando termina, genera el audio WAV automaticamente.

**`core/camera_manager.py`** - `CameraManager` escanea hasta 10 indices de camara usando `cv2.VideoCapture` con backend DirectShow (`CAP_DSHOW`). Etiqueta las camaras como FRONT/USB/CAM segun el indice. Captura a 640x480.

**`core/openai_analyzer.py`** - `OpenAIAnalyzer` con dos metodos principales:
- `analyze_geometric_figure(base64_image)` - envia imagen a Vision con prompt tactil
- `generate_educational_explanation(analysis)` - genera explicacion sensorial desde el analisis
- `analyze_image(pil_image)` - orquesta el flujo completo: encode -> vision -> educativo

**`core/audio_manager.py`** - `AudioManager` inicializa pyttsx3 buscando voz en espanol automaticamente. Genera WAV en directorio temporal con timestamp. Reproduce con `os.startfile` (Windows), `afplay` (macOS) o `aplay` (Linux). Reinicializa el engine en cada generacion para evitar un bug conocido de pyttsx3 que cuelga en el segundo uso.

**`utils/config.py`** - Todas las constantes configurables. Los valores de OpenAI y TTS se leen de `.env` con fallback a defaults. Los valores de UI son fijos.

## Interfaz Grafica

La ventana de 1400x800 tiene dos paneles:

```
+---------------------------+----------------------------------------+
|  PANEL IZQUIERDO (400px)  |  PANEL DERECHO                         |
|                           |                                        |
|  [Selector de camara v]   |  Explicacion                           |
|  [Refrescar Camaras]      |  +------------------------------------+|
|                           |  |                                    ||
|  +-------------------+    |  |  (texto de la explicacion          ||
|  | Vista previa      |    |  |   tactil/sensorial aparece aca)   ||
|  | camara (320x240)  |    |  |                                    ||
|  +-------------------+    |  |                                    ||
|                           |  +------------------------------------+|
|  +-------------------+    |                                        |
|  | Imagen capturada  |    |  [Reproducir] [Guardar] [Copiar] [X]  |
|  | (320x240)         |    |                                        |
|  +-------------------+    |                                        |
|                           |                                        |
|  [Iniciar Camara]         |                                        |
|  [Capturar Imagen]        |                                        |
|  [Analizar Geometria]     |                                        |
|  [====== progreso ======] |                                        |
+---------------------------+----------------------------------------+
```

### Flujo de la UI

1. Al iniciar, `detect_cameras()` escanea camaras y llena el combo
2. "Iniciar Camara" abre el `VideoCapture` y arranca un `QTimer` a 30 FPS que actualiza la vista previa
3. "Capturar Imagen" toma el frame actual, lo convierte BGR -> RGB -> PIL Image y lo muestra en el panel de captura
4. "Analizar Geometria" lanza el `TranscriptionWorker` en un hilo separado. Muestra barra de progreso indeterminada
5. Al completarse, el resultado se muestra en el `QTextEdit` y se genera el WAV automaticamente
6. Los botones de audio se habilitan: Reproducir, Guardar (abre dialogo `QFileDialog`), Copiar texto
7. "Limpiar" borra el texto y elimina el WAV temporal. `closeEvent` limpia camara y audio al cerrar

## Instalacion

### Requisitos
- Python 3.12+
- Camara web (USB o integrada)
- Conexion a internet
- API Key de OpenAI

### Pasos

```bash
# 1. Clonar e instalar
git clone <url-del-repositorio>
cd Proyecto_Ciegos
pip install -r requirements.txt

# 2. Configurar API key
cp .env.example .env
# Editar .env y agregar tu OPENAI_API_KEY

# 3. Ejecutar
python math_transcriptor_desktop.py
```

### Con uv (alternativa)

```bash
uv sync
uv run python math_transcriptor_desktop.py
```

## Configuracion

Variables de entorno en `.env` (o defaults en `utils/config.py`):

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (requerido) | API key de OpenAI |
| `MODEL_VISION` | `gpt-4.1-mini` | Modelo para analisis visual tactil |
| `MODEL_EDUCATIONAL` | `gpt-4.1-mini` | Modelo para explicacion sensorial |
| `MAX_TOKENS_VISION` | `400` | Tokens max del analisis |
| `MAX_TOKENS_EDUCATIONAL` | `600` | Tokens max de la explicacion |
| `TTS_RATE` | `150` | Velocidad de voz (palabras/min) |

Constantes fijas (no configurables via `.env`):

| Constante | Valor | Donde se usa |
|-----------|-------|--------------|
| `CAMERA_WIDTH` | 640 | Resolucion de captura |
| `CAMERA_HEIGHT` | 480 | Resolucion de captura |
| `CAMERA_FPS` | 30 | Tasa de refresco del preview |
| `WINDOW_WIDTH` | 1400 | Ancho de la ventana |
| `WINDOW_HEIGHT` | 800 | Alto de la ventana |
| `PANEL_MAX_WIDTH` | 400 | Ancho max del panel izquierdo |

## Tecnologias

| Paquete | Version | Uso |
|---------|---------|-----|
| PyQt5 | 5.15.11 | Interfaz grafica, hilos con QThread |
| OpenCV | 4.13.0 | Captura de camara (DirectShow en Windows) |
| OpenAI | 2.28.0 | API de chat completions con vision |
| pyttsx3 | 2.99 | Text-to-Speech offline, genera WAV |
| Pillow | 12.1.1 | Conversion de frames a PNG base64 |
| numpy | 2.4.3 | Arrays para frames de OpenCV |
| python-dotenv | 1.2.2 | Carga de .env |

## Licencia

MIT
