import sys
from PySide6 import QtWidgets
from .gui import Window

# Main script for package vtkmat

app = QtWidgets.QApplication([])
window = Window()
window.show()
sys.exit(app.exec())