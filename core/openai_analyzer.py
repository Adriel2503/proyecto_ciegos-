import base64
import io
import logging
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from openai import OpenAI
from PIL import Image

from utils.config import MODEL_VISION, MODEL_EDUCATIONAL, MAX_TOKENS_VISION, MAX_TOKENS_EDUCATIONAL

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent / "prompts"


class OpenAIAnalyzer:
    """Analizador de figuras geometricas usando OpenAI Vision"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No se encontro OPENAI_API_KEY en el archivo .env")
        self.client = OpenAI(api_key=api_key)
        self.jinja_env = Environment(loader=FileSystemLoader(PROMPTS_DIR))

    def encode_image(self, image):
        """Convertir imagen a base64 para OpenAI"""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    def analyze_geometric_figure(self, base64_image):
        """Analisis tecnico con Vision - Descripcion TACTIL para ciegos"""
        system_prompt = self.jinja_env.get_template("vision_system.j2").render()
        user_prompt = self.jinja_env.get_template("vision_user.j2").render()

        try:
            logger.info("Enviando request a %s (vision)...", MODEL_VISION)
            response = self.client.chat.completions.create(
                model=MODEL_VISION,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=MAX_TOKENS_VISION
            )

            analisis = response.choices[0].message.content
            logger.info("Analisis tecnico obtenido: %d caracteres", len(analisis))
            return analisis
        except Exception as e:
            logger.error("Error en analisis tecnico: %s", e)
            raise

    def generate_educational_explanation(self, technical_analysis):
        """Generacion educativa - Explicacion TACTIL para ciegos"""
        system_prompt = self.jinja_env.get_template("educational_system.j2").render()
        user_prompt = self.jinja_env.get_template("educational_user.j2").render(
            technical_analysis=technical_analysis
        )

        try:
            logger.info("Enviando request a %s (educativo)...", MODEL_EDUCATIONAL)
            response = self.client.chat.completions.create(
                model=MODEL_EDUCATIONAL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=MAX_TOKENS_EDUCATIONAL
            )

            explicacion = response.choices[0].message.content
            logger.info("Explicacion educativa generada: %d caracteres", len(explicacion))
            return explicacion
        except Exception as e:
            logger.error("Error en explicacion educativa: %s", e)
            raise

    def analyze_image(self, pil_image):
        """Flujo completo: Analisis tecnico + Explicacion educativa"""
        base64_image = self.encode_image(pil_image)
        logger.info("Imagen convertida a base64: %d caracteres", len(base64_image))

        analisis_tecnico = self.analyze_geometric_figure(base64_image)
        explicacion = self.generate_educational_explanation(analisis_tecnico)
        return explicacion
