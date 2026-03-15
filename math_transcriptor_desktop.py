import logging
import os
import sys

import cv2
from dotenv import load_dotenv
from PIL import Image
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QLabel, QComboBox, QTextEdit,
                             QMessageBox, QProgressBar, QFileDialog)

from core.camera_manager import CameraManager
from core.openai_analyzer import OpenAIAnalyzer
from core.audio_manager import AudioManager
from utils.config import WINDOW_WIDTH, WINDOW_HEIGHT, PANEL_MAX_WIDTH, CAMERA_FPS
from utils.styles import MAIN_STYLESHEET

load_dotenv()

logger = logging.getLogger(__name__)


class TranscriptionWorker(QThread):
    """Hilo para procesar la transcripcion sin bloquear la UI"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress_update = pyqtSignal(str)

    def __init__(self, image, analyzer):
        super().__init__()
        self.image = image
        self.analyzer = analyzer

    def run(self):
        try:
            logger.info("Worker: Iniciando analisis...")
            self.progress_update.emit("Analizando la imagen matematica...")

            resultado_educativo = self.analyzer.analyze_image(self.image)
            self.finished.emit(resultado_educativo)
        except Exception as e:
            logger.error("Worker: Error durante procesamiento: %s", e)
            self.error.emit(f"Error al procesar la imagen: {e}")


class MathTranscriptorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GeomAI - Tutor de Geometria Visual")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Inicializar gestores (Dependency Injection ready)
        self.camera_manager = CameraManager()
        self.audio_manager = AudioManager()
        self.analyzer = OpenAIAnalyzer()

        # Verificar API key
        if not os.getenv("OPENAI_API_KEY"):
            QMessageBox.critical(self, "Error", "No se encontro OPENAI_API_KEY en el archivo .env")
            sys.exit(1)

        # Variables
        self.timer = QTimer()
        self.captured_image = None

        self.init_ui()
        self.detect_cameras()
        self.setStyleSheet(MAIN_STYLESHEET)

    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Panel izquierdo: Controles de camara
        left_panel = QWidget()
        left_panel.setMaximumWidth(PANEL_MAX_WIDTH)
        left_layout = QVBoxLayout(left_panel)

        title_label = QLabel("Captura")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(title_label)

        # Selector de camara
        self.camera_combo = QComboBox()
        self.camera_combo.currentIndexChanged.connect(self.change_camera)
        left_layout.addWidget(QLabel("Seleccionar camara:"))
        left_layout.addWidget(self.camera_combo)

        self.refresh_button = QPushButton("Refrescar Camaras")
        self.refresh_button.clicked.connect(self.detect_cameras)
        left_layout.addWidget(self.refresh_button)

        # Vista previa de la camara
        self.camera_label = QLabel("Vista previa de la camara")
        self.camera_label.setMinimumSize(320, 240)
        self.camera_label.setStyleSheet("border: 2px solid gray; background-color: black;")
        self.camera_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.camera_label)

        # Imagen capturada
        self.captured_label = QLabel("Imagen capturada aparecera aqui")
        self.captured_label.setMinimumSize(320, 240)
        self.captured_label.setStyleSheet("border: 2px solid blue; background-color: lightgray;")
        self.captured_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.captured_label)

        # Botones de camara
        self.start_button = QPushButton("Iniciar Camara")
        self.start_button.clicked.connect(self.start_camera)
        left_layout.addWidget(self.start_button)

        self.capture_button = QPushButton("Capturar Imagen")
        self.capture_button.clicked.connect(self.capture_image)
        self.capture_button.setEnabled(False)
        left_layout.addWidget(self.capture_button)

        self.transcribe_button = QPushButton("Analizar Geometria")
        self.transcribe_button.clicked.connect(self.transcribe_image)
        self.transcribe_button.setEnabled(False)
        left_layout.addWidget(self.transcribe_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)

        left_layout.addStretch()

        # Panel derecho: Resultado
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        result_title = QLabel("Explicacion")
        result_title.setFont(QFont("Arial", 12, QFont.Bold))
        right_layout.addWidget(result_title)

        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText(
            "La explicacion geometrica aparecera aqui...\n\n"
            "Puedo analizar:\n"
            "- Linea recta\n"
            "- Regla graduada en centimetros\n"
            "- Regla graduada en pulgadas\n"
            "- Rectas cruzadas\n"
            "- Ejes cartesianos\n\n"
            "Pon la figura geometrica frente a la camara"
        )
        self.result_text.setFont(QFont("Arial", 12))
        right_layout.addWidget(self.result_text)

        # Botones de resultado
        result_buttons = QHBoxLayout()

        self.play_button = QPushButton("Reproducir Audio")
        self.play_button.clicked.connect(self.play_audio)
        self.play_button.setEnabled(False)
        result_buttons.addWidget(self.play_button)

        self.save_audio_button = QPushButton("Guardar Audio")
        self.save_audio_button.clicked.connect(self.save_audio_file)
        self.save_audio_button.setEnabled(False)
        result_buttons.addWidget(self.save_audio_button)

        self.copy_button = QPushButton("Copiar Texto")
        self.copy_button.clicked.connect(self.copy_text)
        result_buttons.addWidget(self.copy_button)

        self.clear_button = QPushButton("Limpiar")
        self.clear_button.clicked.connect(self.clear_result)
        result_buttons.addWidget(self.clear_button)

        right_layout.addLayout(result_buttons)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        self.timer.timeout.connect(self.update_frame)

    # -- Camera --

    def detect_cameras(self):
        """Detectar camaras disponibles"""
        cameras = self.camera_manager.detect_cameras()
        self.camera_combo.blockSignals(True)
        self.camera_combo.clear()
        for camera in cameras:
            self.camera_combo.addItem(camera['name'], camera['index'])
        self.camera_combo.blockSignals(False)

        if not cameras:
            QMessageBox.warning(self, "Advertencia", "No se encontraron camaras disponibles")

    def change_camera(self):
        """Cambiar la camara seleccionada"""
        if self.camera_manager.is_camera_running():
            self._stop_camera_ui()

        camera_index = self.camera_combo.currentData()
        if camera_index is not None:
            self.camera_manager.set_camera(camera_index)

    def start_camera(self):
        """Iniciar o detener la camara"""
        if not self.camera_manager.is_camera_running():
            if self.camera_manager.start_camera():
                self.timer.start(1000 // CAMERA_FPS)
                self.start_button.setText("Detener Camara")
                self.capture_button.setEnabled(True)
            else:
                QMessageBox.critical(self, "Error", "No se pudo abrir la camara")
        else:
            self._stop_camera_ui()

    def _stop_camera_ui(self):
        """Detiene camara y resetea controles de UI"""
        self.camera_manager.stop_camera()
        self.timer.stop()
        self.start_button.setText("Iniciar Camara")
        self.capture_button.setEnabled(False)
        self.camera_label.setText("Vista previa de la camara")
        self.camera_label.setStyleSheet("border: 2px solid gray; background-color: black;")

    # -- Frame conversion --

    def _frame_to_pixmap(self, frame):
        """Convierte un frame BGR de OpenCV a QPixmap y retorna tambien el frame RGB."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_image), rgb_frame

    def update_frame(self):
        """Actualizar el frame de la vista previa"""
        ret, frame = self.camera_manager.get_frame()
        if ret:
            pixmap, _ = self._frame_to_pixmap(frame)
            scaled = pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.camera_label.setPixmap(scaled)
            self.camera_label.setStyleSheet("border: 2px solid green;")

    def capture_image(self):
        """Capturar la imagen actual"""
        ret, frame = self.camera_manager.get_frame()
        if ret and frame is not None:
            pixmap, rgb_frame = self._frame_to_pixmap(frame)
            self.captured_image = Image.fromarray(rgb_frame)

            scaled = pixmap.scaled(self.captured_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.captured_label.setPixmap(scaled)
            self.captured_label.setStyleSheet("border: 3px solid green; background-color: white;")

            self.transcribe_button.setEnabled(True)
            logger.info("Imagen capturada correctamente")
            QMessageBox.information(self, "Exito", "Figura geometrica capturada correctamente\nAhora presiona 'Analizar Geometria'")
        else:
            QMessageBox.warning(self, "Error", "No se pudo capturar la imagen")

    # -- Transcription --

    def transcribe_image(self):
        """Analizar la figura geometrica capturada"""
        if self.captured_image is None:
            QMessageBox.warning(self, "Advertencia", "Primero debes capturar la figura geometrica")
            return

        logger.info("Iniciando analisis de geometria (imagen: %s)", self.captured_image.size)

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.transcribe_button.setEnabled(False)

        self.worker = TranscriptionWorker(self.captured_image, self.analyzer)
        self.worker.finished.connect(self.on_transcription_finished)
        self.worker.error.connect(self.on_transcription_error)
        self.worker.progress_update.connect(self.on_progress_update)
        self.worker.start()

    def on_transcription_finished(self, result):
        """Manejar el resultado de la transcripcion"""
        logger.info("Transcripcion completada: %d caracteres", len(result))
        self.progress_bar.setVisible(False)
        self.transcribe_button.setEnabled(True)
        self.result_text.setText(result)

        self._generate_audio(result)

        QMessageBox.information(self, "Exito", "Analisis geometrico completado\nLa explicacion esta lista\nAudio generado")

    def on_transcription_error(self, error_msg):
        """Manejar errores de transcripcion"""
        logger.error("Error en transcripcion: %s", error_msg)
        self.progress_bar.setVisible(False)
        self.transcribe_button.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Error en transcripcion:\n{error_msg}")

    def on_progress_update(self, message):
        """Actualizar el mensaje de progreso"""
        logger.debug("Progreso: %s", message)

    # -- Audio --

    def _generate_audio(self, text):
        """Generar archivo de audio desde el texto"""
        if not text:
            return
        audio_file = self.audio_manager.generate_audio(text)
        if audio_file:
            self.play_button.setEnabled(True)
            self.save_audio_button.setEnabled(True)

    def play_audio(self):
        """Reproducir el archivo de audio generado"""
        if self.audio_manager.play_audio():
            QMessageBox.information(self, "Reproduciendo", "Reproduciendo explicacion de geometria")
        else:
            QMessageBox.warning(self, "Advertencia", "No hay audio disponible para reproducir")

    def save_audio_file(self):
        """Guardar el archivo de audio en una ubicacion elegida por el usuario"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Audio",
            "explicacion_geometria.wav",
            "Archivos de Audio (*.wav)"
        )

        if file_path:
            if self.audio_manager.save_audio(file_path):
                QMessageBox.information(self, "Exito", f"Audio guardado en:\n{file_path}")
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar el audio")

    # -- Utilities --

    def copy_text(self):
        """Copiar el texto al portapapeles"""
        text = self.result_text.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Exito", "Texto copiado al portapapeles")

    def clear_result(self):
        """Limpiar el area de resultado"""
        self.result_text.clear()
        self.audio_manager.cleanup()
        self.play_button.setEnabled(False)
        self.save_audio_button.setEnabled(False)

    def closeEvent(self, event):
        """Manejar el cierre de la aplicacion"""
        self.camera_manager.stop_camera()
        self.audio_manager.cleanup()
        event.accept()


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    app = QApplication(sys.argv)
    window = MathTranscriptorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
