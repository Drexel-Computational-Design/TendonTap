"""
This script serves as the entry point for the GUI
"""

# Imports
from PyQt5.QtWidgets import QApplication
from gui_models import Camera
from gui_views import StartWindow

# Initialize camera
camera = Camera(0)
camera.initialize()


# Launch app
app = QApplication([])
start_window = StartWindow(camera)
start_window.show()
app.exit(app.exec_())
