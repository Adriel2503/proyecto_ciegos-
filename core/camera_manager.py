import logging

import cv2

from utils.config import CAMERA_WIDTH, CAMERA_HEIGHT

logger = logging.getLogger(__name__)


class CameraManager:
    """Gestor de camaras - maneja deteccion, apertura y captura de frames"""

    def __init__(self):
        self.available_cameras = []
        self.current_camera = None
        self.current_camera_index = 0

    def detect_cameras(self, max_cameras=10):
        """Detecta camaras disponibles"""
        self.available_cameras = []
        logger.info("Detectando camaras...")

        for i in range(max_cameras):
            try:
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                        if i == 0:
                            name = f"[FRONT] Camara Frontal (Indice {i}) - {width}x{height}"
                        elif i == 1:
                            name = f"[USB] Webcam USB (Indice {i}) - {width}x{height}"
                        else:
                            name = f"[CAM] Camara {i} - {width}x{height}"

                        self.available_cameras.append({'index': i, 'name': name})
                        logger.info("Camara encontrada: Indice %d", i)

                    cap.release()
            except Exception as e:
                logger.error("Probando camara %d: %s", i, e)
                continue

        logger.info("Total de camaras encontradas: %d", len(self.available_cameras))
        return self.available_cameras

    def set_camera(self, camera_index):
        """Cambia la camara seleccionada"""
        self.current_camera_index = camera_index
        logger.info("Camara seleccionada: Indice %d", self.current_camera_index)

    def start_camera(self):
        """Inicia la camara"""
        try:
            logger.info("Intentando iniciar camara con indice: %d", self.current_camera_index)
            self.current_camera = cv2.VideoCapture(self.current_camera_index, cv2.CAP_DSHOW)

            if self.current_camera.isOpened():
                self.current_camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
                self.current_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

                ret, frame = self.current_camera.read()
                if ret and frame is not None:
                    logger.info("Camara iniciada correctamente")
                    return True
                else:
                    self.current_camera.release()
                    self.current_camera = None
                    return False
            else:
                return False
        except Exception as e:
            logger.error("Error al iniciar camara: %s", e)
            return False

    def get_frame(self):
        """Obtiene el frame actual"""
        if self.current_camera is None:
            return False, None
        return self.current_camera.read()

    def stop_camera(self):
        """Detiene la camara"""
        if self.current_camera is not None:
            self.current_camera.release()
            self.current_camera = None
            logger.info("Camara detenida")

    def is_camera_running(self):
        """Verifica si la camara esta activa"""
        return self.current_camera is not None and self.current_camera.isOpened()
