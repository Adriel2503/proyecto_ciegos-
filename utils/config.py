# Configuracion centralizada para Math Transcriptor Desktop
import os

# Logging - niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Camara
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
CAMERA_PREVIEW_SIZE = (320, 240)

# OpenAI - configurables via .env
MODEL_VISION = os.getenv("MODEL_VISION", "gpt-4.1-mini")
MODEL_EDUCATIONAL = os.getenv("MODEL_EDUCATIONAL", "gpt-4.1-mini")
MAX_TOKENS_VISION = int(os.getenv("MAX_TOKENS_VISION", "400"))
MAX_TOKENS_EDUCATIONAL = int(os.getenv("MAX_TOKENS_EDUCATIONAL", "600"))

# Audio/TTS
TTS_RATE = int(os.getenv("TTS_RATE", "150"))
TTS_OUTPUT_FORMAT = "wav"

# UI
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
PANEL_MAX_WIDTH = 400

