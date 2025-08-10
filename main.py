from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QListWidget, QLineEdit, QFileDialog)
import os

workdir_path = ''
app = QApplication([])
win = QWidget()
win.setFixedSize(700, 500)
win.setWindowTitle('Editor')

layout1 = QVBoxLayout()
folder_button = QPushButton('Open folder')
pictures_list = QListWidget()
layout1.addWidget(folder_button)
layout1.addWidget(pictures_list)

layout2 = QHBoxLayout()
left_button = QPushButton('Left')
right_button = QPushButton('Right')
mirror_button = QPushButton('Mirror')
sharpness_button = QPushButton('Sharpness')
gray_button = QPushButton('Gray')
layout2.addWidget(left_button)
layout2.addWidget(right_button)
layout2.addWidget(mirror_button)
layout2.addWidget(sharpness_button)
layout2.addWidget(gray_button)

layout4 = QHBoxLayout()
vignite_button = QPushButton('Vignite')
blur_button = QPushButton('Blur')
contrast_button = QPushButton('Contrast')
save_button = QPushButton('Save')
save_button.setStyleSheet("background-color: green; color: white;")
layout4.addWidget(vignite_button)
layout4.addWidget(blur_button)
layout4.addWidget(contrast_button)
layout4.addWidget(save_button)

layout3 = QVBoxLayout()
picture = QLabel('Picture')
layout3.addWidget(picture)
layout3.addLayout(layout2)
layout3.addLayout(layout4)

layout_main = QHBoxLayout()
layout_main.addLayout(layout1)
layout_main.addLayout(layout3)

win.setLayout(layout_main)

def open_folder():
    global workdir_path
    workdir_path = QFileDialog.getExistingDirectory()
    filenames = os.listdir(workdir_path)

    print(filenames)

folder_button.clicked.connect(open_folder)

win.show()
app.exec()