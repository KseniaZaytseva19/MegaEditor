from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QListWidget, QLineEdit)


app = QApplication([])
win = QWidget()
win.setFixedSize(700, 500)
win.setWindowTitle('Editor')

layout1 = QVBoxLayout()
folder_button = QPushButton('Folder')
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

layout3 = QVBoxLayout()
picture = QLabel('Picture')
layout3.addWidget(picture)
layout3.addLayout(layout2)

layout_main = QHBoxLayout()
layout_main.addLayout(layout1)
layout_main.addLayout(layout3)

win.setLayout(layout_main)

win.show()
app.exec()