# GeomAI - Tutor de Geometria Visual para Personas Ciegas

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--mini-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Aplicacion desktop que describe figuras geometricas de forma tactil y sensorial para personas ciegas, usando IA en cascada y sintesis de voz.

## Como Funciona

```
Camara/Imagen --> GPT-4.1-mini Vision --> GPT-4.1-mini Educativo --> Audio TTS
                  (analisis tactil)       (explicacion sensorial)    (pyttsx3)
```

La IA analiza la figura y genera una descripcion como si la persona estuviera tocandola con las manos: vertices, lineas, intersecciones, simetria y texturas espaciales.

### Figuras Soportadas

- Tipos de rectas (paralelas, perpendiculares, secantes)
- Tipos de triangulos (equilatero, isosceles, escaleno)
- Tipos de cuadrilateros (cuadrado, rectangulo, rombo, trapecio)
- Lineas rectas, reglas graduadas, rectas cruzadas, ejes cartesianos

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

## Uso

1. **Seleccionar camara** del menu desplegable
2. **Iniciar camara** y enfocar la figura geometrica
3. **Capturar imagen** cuando este bien encuadrada
4. **Analizar Geometria** - el sistema genera la descripcion tactil
5. **Reproducir Audio** para escuchar la explicacion
6. **Guardar Audio** (opcional) para exportar el WAV

## Estructura del Proyecto

```
Proyecto_Ciegos/
├── math_transcriptor_desktop.py   # App principal (PyQt5)
├── core/
│   ├── camera_manager.py          # Gestion de webcam (OpenCV)
│   ├── openai_analyzer.py         # Cascada IA: vision + educativo
│   └── audio_manager.py           # TTS y gestion de audio WAV
├── utils/
│   ├── config.py                  # Configuracion centralizada
│   └── styles.py                  # Estilos PyQt5
├── requirements.txt
├── .env.example
└── README.md
```

## Configuracion

Los modelos y parametros se configuran via variables de entorno (`.env`) o valores por defecto en `utils/config.py`:

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (requerido) | API key de OpenAI |
| `MODEL_VISION` | `gpt-4.1-mini` | Modelo para analisis visual |
| `MODEL_EDUCATIONAL` | `gpt-4.1-mini` | Modelo para explicacion educativa |
| `MAX_TOKENS_VISION` | `400` | Tokens max para analisis |
| `MAX_TOKENS_EDUCATIONAL` | `600` | Tokens max para explicacion |
| `TTS_RATE` | `150` | Velocidad de voz (palabras/min) |

## Tecnologias

- **PyQt5** - Interfaz grafica
- **OpenCV** - Captura de camara
- **OpenAI API** - Analisis visual y generacion educativa
- **pyttsx3** - Sintesis de voz en espanol
- **Pillow** - Manipulacion de imagenes

## Licencia

MIT
