import logging
import os
import platform
import shutil
import tempfile
import time

import pyttsx3

from utils.config import TTS_RATE

logger = logging.getLogger(__name__)


class AudioManager:
    """Gestor de audio - conversion de texto a voz y reproduccion"""

    def __init__(self):
        self.tts_engine = self._init_tts()
        self.audio_file = None

    def _init_tts(self):
        """Inicializa el motor de texto a voz"""
        try:
            engine = pyttsx3.init()

            voices = engine.getProperty('voices')
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break

            engine.setProperty('rate', TTS_RATE)
            logger.info("Motor TTS inicializado correctamente")
            return engine
        except Exception as e:
            logger.error("Error al inicializar TTS: %s", e)
            return None

    def generate_audio(self, text):
        """Genera archivo de audio desde texto"""
        if not text or text.strip() == "":
            logger.warning("Texto vacio, no se puede generar audio")
            return None

        if self.tts_engine is None:
            logger.warning("Motor TTS no disponible")
            return None

        if self.audio_file and os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
            except OSError:
                pass

        try:
            timestamp = int(time.time())
            self.audio_file = os.path.join(
                tempfile.gettempdir(),
                f"geometry_explanation_{timestamp}.wav"
            )

            logger.info("Generando audio en: %s", self.audio_file)
            logger.info("Texto a convertir: %d caracteres", len(text))

            # Reinicializar engine para evitar hang en segundo uso (bug conocido de pyttsx3)
            self.tts_engine = self._init_tts()
            if self.tts_engine is None:
                return None

            self.tts_engine.save_to_file(text, self.audio_file)
            self.tts_engine.runAndWait()

            if os.path.exists(self.audio_file):
                file_size = os.path.getsize(self.audio_file)
                logger.info("Audio generado exitosamente (%d bytes)", file_size)
                return self.audio_file
            else:
                logger.error("Archivo de audio no se creo")
                return None
        except Exception as e:
            logger.error("Error al generar audio: %s", e)
            return None

    def play_audio(self, file_path=None):
        """Reproduce el archivo de audio"""
        audio_to_play = file_path or self.audio_file

        if audio_to_play is None:
            logger.warning("No hay archivo de audio configurado")
            return False

        if not os.path.exists(audio_to_play):
            logger.warning("Archivo no existe: %s", audio_to_play)
            return False

        try:
            file_size = os.path.getsize(audio_to_play)
            logger.info("Reproduciendo audio: %s (%d bytes)", audio_to_play, file_size)

            system = platform.system()
            if system == "Windows":
                os.startfile(audio_to_play)
            elif system == "Darwin":
                os.system(f'afplay "{audio_to_play}" &')
            else:
                os.system(f'aplay "{audio_to_play}" &')

            logger.info("Audio enviado a reproduccion")
            return True
        except Exception as e:
            logger.exception("Error al reproducir audio")
            return False

    def save_audio(self, destination_path, source_path=None):
        """Guarda el archivo de audio en una ubicacion especifica"""
        source = source_path or self.audio_file

        if source is None or not os.path.exists(source):
            logger.warning("No hay audio para guardar")
            return False

        try:
            shutil.copy2(source, destination_path)
            logger.info("Audio guardado en: %s", destination_path)
            return True
        except Exception as e:
            logger.error("Error al guardar audio: %s", e)
            return False

    def cleanup(self):
        """Limpia archivos de audio temporal"""
        if self.audio_file and os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
                logger.info("Archivo temporal eliminado: %s", self.audio_file)
            except Exception as e:
                logger.warning("Error al eliminar archivo temporal: %s", e)
