"""
Qt Uses the Model-View Paragigm

Views
"""

# Imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout,
                             QApplication, QSlider)
from PyQt5.QtCore import Qt, QThread, QTimer
from pyqtgraph import ImageView
from gui_models import Camera
import numpy as np


class StartWindow(QMainWindow):
    """
    Class for the GUI Window
    """

    def __init__(self, camera: Camera=None):
        super().__init__()
        self.camera = camera

        # Create widgets
        self.central_widget = QWidget()
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)
        self.button_movie = QPushButton('Start Movie', self.central_widget)
        self.image_view = ImageView()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10)

        # Define layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_frame)
        self.layout.addWidget(self.button_movie)
        self.layout.addWidget(self.image_view)
        self.layout.addWidget(self.slider)
        self.setCentralWidget(self.central_widget)

        # Connect signals and slots
        self.button_frame.clicked.connect(self.update_image)
        self.button_movie.clicked.connect(self.start_movie)
        self.slider.valueChanged.connect(self.update_brightness)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)


    def update_image(self):
        frame = self.camera.get_frame()
        self.image_view.setImage(frame.T)


    def update_movie(self):
        self.image_view.setImage(self.camera.last_frame.T)


    def update_brightness(self, value):
        value /= 10
        self.camera.set_brightness(value)


    def start_movie(self):
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.start()
        self.update_timer.start(30)


class MovieThread(QThread):
    """
    Manage movie as a single thread
    """

    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)


if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())
