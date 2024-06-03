# GUI module for package vtkmat

import os
from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path
from .vtkfile import Vtkfile


class Window(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VTK to MAT")
        self.layout = QtWidgets.QVBoxLayout(self)

        # File selector
        self.fileOpenLayout = QtWidgets.QHBoxLayout()
        self.setupFileOpen()
        self.layout.addLayout(self.fileOpenLayout)

        # Setup array selection
        self.vtkContentLayout = QtWidgets.QVBoxLayout()
        self.setupVtkContent()
        self.layout.addLayout(self.vtkContentLayout)

        # Setup saveas
        self.fileSaveLayout = QtWidgets.QHBoxLayout()
        self.setupFileSave()
        self.layout.addLayout(self.fileSaveLayout)

        # Set up buttons for cancel and ok
        submitBox = QtWidgets.QHBoxLayout()
        submitBox.addStretch(1)

        btnClose = QtWidgets.QPushButton("Close")
        btnClose.clicked.connect(self.accept)
        submitBox.addWidget(btnClose)

        self.layout.addLayout(submitBox)

    # Generator/Setup functions
    def setupFileOpen(self):
        """Generator function for file opening UI."""
        self.fileOpenLayout.addWidget(QtWidgets.QLabel("Read file: "))
        self.filenameEdit = QtWidgets.QLineEdit()
        # self.filenameEdit.setMinimumWidth(300)
        self.fileOpenLayout.addWidget(self.filenameEdit)

        btnFileDialog = QtWidgets.QPushButton("Browse")
        btnFileDialog.clicked.connect(self.browseOpenFile)
        self.fileOpenLayout.addWidget(btnFileDialog)

    def setupVtkContent(self):
        """Generator function for file related GUI including checkboxes and empty listview."""
        # Setup top level checkboxes
        self.cbCells = QtWidgets.QCheckBox("Extract cells by type")
        self.cbArrays = QtWidgets.QCheckBox("Add arrays: ")
        self.cbArrays.stateChanged.connect(self.switchArrays)

        # Setup list view
        self.model = QtGui.QStandardItemModel()
        listView = QtWidgets.QListView()
        listView.setModel(self.model)

        # Add elements to layout
        self.vtkContentLayout.addWidget(self.cbCells)
        self.vtkContentLayout.addWidget(self.cbArrays)
        self.vtkContentLayout.addWidget(listView)

    def setupFileSave(self):
        """Generator function for file save UI."""
        self.fileSaveLayout.addWidget(QtWidgets.QLabel("Save as: "))
        self.fileSaveEdit = QtWidgets.QLineEdit()
        self.fileSaveLayout.addWidget(self.fileSaveEdit)

        btnFileSave = QtWidgets.QPushButton("Save")
        btnFileSave.clicked.connect(self.saveFile)
        btnFileSaveBrowse = QtWidgets.QPushButton("Browse")
        btnFileSaveBrowse.clicked.connect(self.browseSaveFile)
        self.fileSaveLayout.addWidget(btnFileSave)
        self.fileSaveLayout.addWidget(btnFileSaveBrowse)

    # Callback functions
    def browseOpenFile(self):
        """Callback for file open dialog."""
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        filename, ok = fileDialog.getOpenFileName(
            self,
            "Open VTK file",
            "",
            "VTK file (*.vtk *.vti *.vtp *.vtr  *.vts *.vtu *.pvti *.pvtp *.pvtr  *.pvts *.pvtu)",
        )
        if filename:
            # Generate path from string and set as content for edit field
            filepath = Path(filename)
            self.filenameEdit.setText(str(filepath))

            # Generate Vtkfile object and read array names to fill list
            self.vtkfile = Vtkfile(filepath)
            if self.vtkfile:
                self.cbCells.setCheckState(QtCore.Qt.Checked)
                self.addArraysToList(self.vtkfile.data.array_names)
                self.cbArrays.setCheckState(QtCore.Qt.Checked)
            self.fileSaveEdit.setText(
                f"{self.vtkfile.directory}{os.sep}{self.vtkfile.name}.mat"
            )

    def switchArrays(self):
        """Callback for arrays checkbox to select/unselect all arrays."""
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(self.cbArrays.checkState())

    def browseSaveFile(self):
        """Callback for file save dialog."""
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        fileDialog.setDirectory(self.vtkfile.directory)
        defaultFile = Path(self.fileSaveEdit.text()).stem
        filename, ok = fileDialog.getSaveFileName(
            self, "Save MAT file", defaultFile, "MAT file (*.mat)"
        )
        if filename:
            self.fileSaveEdit.setText(str(Path(filename)))
            self.saveFile()

    def saveFile(self):
        """Callback for saving file."""
        self.getChoices()
        if self.vtkfile and self.fileSaveEdit.text():
            self.vtkfile.write(
                self.fileSaveEdit.text(), self.choices, self.cbCells.isChecked()
            )

    # Additional functions
    def addArraysToList(self, arrays):
        """Populate list with checkable items from arrays input."""
        self.model.clear()
        for arrayKey in arrays:
            item = QtGui.QStandardItem(arrayKey)
            item.setCheckable(True)
            item.setCheckState(QtCore.Qt.Checked)
            self.model.appendRow(item)

    def getChoices(self):
        """Get selected arrays from listview using list comprehension."""
        self.choices = [
            self.model.item(i).text()
            for i in range(self.model.rowCount())
            if self.model.item(i).checkState() == QtCore.Qt.Checked
        ]
