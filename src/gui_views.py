"""
Qt Uses the Model-View Paragigm

Views
"""

# Imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout,
                             QApplication)
from PyQt5.QtCore import Qt, QThread, QTimer
from pyqtgraph import ImageView
from gui_models import Camera
import numpy as np


class ColorImageView(ImageView):
    """
    Wrapper around the ImageView to create a color lookup
    table automatically as there seem to be issues with displaying
    color images through pg.ImageView.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lut = None

    def updateImage(self, autoHistogramRange=True):
        super().updateImage(autoHistogramRange)
        self.getImageItem().setLookupTable(self.lut)


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
        self.image_view = ColorImageView()

        # Hide the controls for imageview
        self.image_view.ui.histogram.hide()
        self.image_view.ui.roiBtn.hide()
        self.image_view.ui.menuBtn.hide()

        # Define layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_frame)
        self.layout.addWidget(self.button_movie)
        self.layout.addWidget(self.image_view)
        self.setCentralWidget(self.central_widget)

        # Connect signals and slots
        self.button_frame.clicked.connect(self.update_image)
        self.button_movie.clicked.connect(self.start_movie)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)


    def update_image(self):
        success, frame = self.camera.get_frame()
        self.image_view.setImage(frame.T)


    def update_movie(self):
        self.image_view.setImage(self.camera.last_frame.T)


    def start_movie(self):
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.start()
        self.update_timer.start(90)


class MovieThread(QThread):
    """
    Manage movie as a single thread
    """

    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(800)


if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())
