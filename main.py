from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QListWidget, QLineEdit, QFileDialog)
from PyQt6.QtGui import QPixmap
import os
from PIL import ImageOps, ImageFilter, Image, ImageEnhance
from PIL.ImageQt import ImageQt

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = ''
        self.filepath = ''

    def open(self, filename):
        self.filepath = os.path.join(workdir_path, filename)
        self.filename = filename
        self.image = Image.open(self.filepath)

    def show_image(self):
        q_image = ImageQt(self.image)
        pixmap = QPixmap.fromImage(q_image)
        height, width = picture.height(), picture.width()
        pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        picture.setPixmap(pixmap)

    def left(self):
        left_pic = self.image.rotate(90)
        self.image = left_pic
        self.show_image()

    def right(self):
        self.image = self.image.rotate(270)
        self.show_image()

    def mirror(self):
        self.image = ImageOps.mirror(self.image)
        self.show_image()

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.show_image()

    def gray(self):
        self.image = ImageOps.grayscale(self.image)
        self.show_image()

    def blur(self):
        self.image = self.image.filter(ImageFilter.BoxBlur(1))
        self.show_image()

    def contrast(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.show_image()

    def save(self):
        save_path = QFileDialog.getSaveFileName()
        self.image.save(save_path[0])

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
vignite_button = QPushButton('Vignette')
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

impr = ImageProcessor()

def open_folder():
    global workdir_path
    workdir_path = QFileDialog.getExistingDirectory()
    filenames = os.listdir(workdir_path)
    filter_filenames(filenames)
    pictures_list.addItems(filenames)

def filter_filenames(f):
    for name in f:
        check = name.endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        if not check:
            f.remove(name)

def show():
    filename = pictures_list.selectedItems()[0].text()
    impr.open(filename)
    impr.show_image()

folder_button.clicked.connect(open_folder)
pictures_list.itemClicked.connect(show)
left_button.clicked.connect(impr.left)
right_button.clicked.connect(impr.right)
mirror_button.clicked.connect(impr.mirror)
sharpness_button.clicked.connect(impr.sharpen)
gray_button.clicked.connect(impr.gray)
blur_button.clicked.connect(impr.blur)
contrast_button.clicked.connect(impr.contrast)
save_button.clicked.connect(impr.save)

win.show()
app.exec()