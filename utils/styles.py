"""Estilos centralizados para la interfaz de GeomAI"""

MAIN_STYLESHEET = """
QMainWindow {
    background-color: #f0f4f8;
}
QWidget {
    background-color: #f0f4f8;
}
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px;
    font-weight: bold;
    font-size: 11px;
}
QPushButton:hover {
    background-color: #2980b9;
}
QPushButton:pressed {
    background-color: #1f618d;
}
QComboBox {
    background-color: white;
    border: 2px solid #3498db;
    border-radius: 5px;
    padding: 5px;
    color: #333;
}
QLabel {
    color: #333;
}
QTextEdit {
    background-color: white;
    border: 2px solid #3498db;
    border-radius: 5px;
    color: #333;
}
QProgressBar {
    border: 2px solid #3498db;
    border-radius: 5px;
    background-color: white;
}
QProgressBar::chunk {
    background-color: #3498db;
}
"""
