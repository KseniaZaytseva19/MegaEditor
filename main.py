from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QListWidget, QFileDialog, QSlider, QGroupBox)
from PyQt6.QtGui import QPixmap
import os
from PIL import ImageOps, ImageFilter, Image, ImageEnhance, ImageDraw
from PIL.ImageQt import ImageQt
import math
import numpy as np

def min_float(*floats):
    minimum = floats[0]
    for element in floats:
        if element < minimum:
            minimum = element
    return minimum


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
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        left_pic = self.image.rotate(90, expand=1)
        self.image = left_pic
        self.show_image()

    def right(self):
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        self.image = self.image.rotate(- 90, expand=1)
        self.show_image()

    def mirror(self):
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        self.image = ImageOps.mirror(self.image)
        self.show_image()

    def sharpen(self):
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.show_image()

    def gray(self):
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        self.image = ImageOps.grayscale(self.image)
        self.show_image()

    def blur(self):
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        self.image = self.image.filter(ImageFilter.BoxBlur(1))
        self.show_image()

    def contrast(self):
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.show_image()

    def vignette(self, strength=1.0):
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        mask = Image.new('L', self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        center_x, center_y = self.image.width / 2, self.image.height / 2
        max_radius = math.sqrt(center_x ** 2 + center_y ** 2)

        for x in range(self.image.width):
            for y in range(self.image.height):
                d_x, d_y = (x - center_x), (y - center_y)
                distance = math.sqrt(d_x ** 2 + d_y ** 2)
                factor = 1 - min_float(1, (distance / max_radius) * strength)
                mask.putpixel((x, y), int(factor * 255))

        black = Image.new('RGB', self.image.size, 'black')
        self.image = Image.composite(self.image, black, mask)

        self.show_image()

    def save(self):
        if self.image is None:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText('Select a picture!')
            popup.exec()
            return

        save_path = QFileDialog.getSaveFileName()
        if not save_path[0]:
            return
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

vignette_group = QGroupBox()
layout5 = QHBoxLayout()
slider = QSlider(Qt.Orientation.Horizontal)
slider.setRange(1, 100)
slider.setSingleStep(25)
slider.setValue(50)
slider.setTickPosition(QSlider.TickPosition.TicksAbove)
slider.setTickInterval(25)

vignite_button = QPushButton('Vignette')
layout5.addWidget(slider)
layout5.addWidget(vignite_button)
vignette_group.setLayout(layout5)

layout4 = QHBoxLayout()
blur_button = QPushButton('Blur')
contrast_button = QPushButton('Contrast')
save_button = QPushButton('Save')
save_button.setStyleSheet("background-color: green; color: white;")
layout4.addWidget(vignette_group)
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
    if len(workdir_path) == 0:
        return
    filenames = os.listdir(workdir_path)
    filenames = filter_filenames(filenames)
    pictures_list.addItems(filenames)


def filter_filenames(f):
    new_filenames = []
    for name in f:
        check = name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        if check:
            new_filenames.append(name)
    return new_filenames


def show():
    filename = pictures_list.selectedItems()[0].text()
    impr.open(filename)
    impr.show_image()


def apply_vignette():
    strength = slider.value()
    impr.vignette(strength/100 + 0.5)


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
vignite_button.clicked.connect(apply_vignette)

win.show()
app.exec()
