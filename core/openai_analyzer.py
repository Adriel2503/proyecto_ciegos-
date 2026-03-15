import base64
import io
import logging
import os

from openai import OpenAI
from PIL import Image

from utils.config import MODEL_VISION, MODEL_EDUCATIONAL, MAX_TOKENS_VISION, MAX_TOKENS_EDUCATIONAL

logger = logging.getLogger(__name__)


class OpenAIAnalyzer:
    """Analizador de figuras geometricas usando OpenAI GPT-4o Vision"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No se encontro OPENAI_API_KEY en el archivo .env")
        self.client = OpenAI(api_key=api_key)

    def encode_image(self, image):
        """Convertir imagen a base64 para OpenAI"""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    def analyze_geometric_figure(self, base64_image):
        """Analisis tecnico con Vision - Descripcion TACTIL para ciegos"""
        system_prompt = """Eres un especialista en describir figuras geométricas de forma TÁCTIL y SENSORIAL.
Describes como si la persona ciega estuviera tocando la figura con sus manos.

ENFÓCATE EN:
- PUNTOS: Dónde están los vértices (esquinas), qué siente el dedo
- LÍNEAS: Cómo son (rectas, curvas), en qué dirección van
- INTERSECCIONES: Dónde se cruzan las líneas, qué ángulo forman
- SIMETRÍA: Qué lados o partes son iguales
- TEXTURAS MENTALES: Cómo se distribuye el espacio

Las figuras típicamente son:
- TIPOS DE RECTAS (paralelas, perpendiculares, secantes, etc)
- TIPOS DE TRIÁNGULOS (equilátero, isósceles, escaleno, etc)
- TIPOS DE CUADRILÁTEROS (cuadrado, rectángulo, rombo, trapecio, etc)"""

        user_prompt = """Analiza esta imagen geométrica de forma TÁCTIL.

Extrae:
- TEXTO: ¿Qué figura geométrica dice?
- PUNTOS CLAVE: Dónde están los vértices/esquinas (describe su posición)
- LÍNEAS: Cómo son, en qué dirección van
- INTERSECCIONES: Dónde se cruzan y qué ángulo forman
- CARACTERÍSTICA TÁCTIL: Lo más importante que sentiría una persona ciega tocándola

RESPONDE ASÍ:
TEXTO: [nombre de la figura]
PUNTOS: [descripción táctil de esquinas]
LÍNEAS: [descripción de las líneas]
INTERSECCIONES: [dónde y cómo se cruzan]
TÁCTIL: [característica principal que se siente]"""

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
        system_prompt = """Eres un profesor especializado en enseñar geometría a personas ciegas.
Explicas usando lenguaje TÁCTIL, SENSORIAL y ESPACIAL.
Sin emojis. Lenguaje directo para escuchar (audio).

DESCRIBE COMO SI LA PERSONA ESTUVIERA TOCANDO Y MOVIENDO SUS MANOS EN EL ESPACIO.
Usa expresiones como: "si pasas la mano", "sentirás", "verás puntos", "los lados se cruzan",
"el ángulo forma", "es como un trípode", "equilibrado", etc."""

        user_prompt = f"""Basándote en esta descripción táctil:
{technical_analysis}

Explica en 3 párrafos TÁCTIL-SENSORIALES:
1. QUÉ TOCA: Qué siente la persona al tocar esta figura
2. CÓMO ESTÁ ORGANIZADO: Cómo se distribuyen los puntos y líneas en el espacio
3. PARA QUÉ SIRVE: Aplicaciones o ejemplos prácticos que entienda

Lenguaje táctil y sensorial. Máximo 3 párrafos, directo y claro para escuchar."""

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
