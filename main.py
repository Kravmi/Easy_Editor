# создай тут фоторедактор Easy Editor!
import os
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
                            QPushButton, QApplication, QWidget,
                            QListWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QFileDialog)

work_dir = ''


def choose_work_dir():
    """Ищет путь к папке"""
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()


def filter(file_dir, exextensions):
    result = []
    for filename in file_dir:
        for exextension in exextensions:
            if filename.endswith(exextension):
                result.append(filename)
    return result


def show_filenames_list():
    """Позволяет показать файлы с указанными расширениями"""
    extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    choose_work_dir()
    list_files = filter(os.listdir(work_dir), extensions)
    list_dir.clear()
    for file in list_files:
        list_dir.addItem(file)


class ImageProcessor():
    '''Загружает картинку по названию файла, а затем показывает на экране'''
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = "Modified/"

    def load_image(self, filename):
        self.filename = filename
        path_image = os.path.join(work_dir, filename)
        self.image = Image.open(path_image)

    def show_image(self, path):
        picture.hide()
        pix_map_image = QPixmap(path)
        w, h = picture.width(), picture.height()
        pix_map_image = pix_map_image.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pix_map_image)
        picture.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.save_and_show('do_bw')

    def save_image(self, name):
        path = os.path.join(work_dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        self.filename = f'{self.filename[:-4]}_{name}.jpg'
        path_image = os.path.join(work_dir, self.save_dir, self.filename)
        self.image.save(path_image)

    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_and_show('flip')

    def rotate_image(self, angle):
        self.image = self.image.rotate(angle, expand=1)
        self.save_and_show('rotate')

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_and_show('sharp')

    def blur(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur(10))
        self.save_and_show('blur')

    def save_and_show(self, name_filter):
        self.save_image(name_filter)
        path_image = os.path.join(work_dir, self.save_dir, self.filename)
        self.show_image(path_image)


def show_chosen_image():
    '''Позволяет выбрать название файла,
    а затем файл с таким названием отображает на экране'''
    if list_dir.currentRow() >= 0:
        filename = list_dir.currentItem().text()
        current_image.load_image(filename)
        path_image = os.path.join(work_dir, filename)
        current_image.show_image(path_image)


app = QApplication([])
main_win = QWidget()
main_win.resize(700, 500)
main_win.setWindowTitle('Easy Editor')
btn_dir = QPushButton('Папка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_grey = QPushButton('Ч/Б')
btn_save = QPushButton('Сохранить')
btn_blur = QPushButton('Заблюрить')
picture = QLabel('Картинка')
list_dir = QListWidget()
list_dir.currentRowChanged.connect(show_chosen_image)
layout_h1 = QHBoxLayout()
layout_h2 = QHBoxLayout()
layout_v1 = QVBoxLayout()
layout_v2 = QVBoxLayout()
layout_v1.addWidget(btn_dir)
layout_v1.addWidget(list_dir)
layout_v2.addWidget(picture)
layout_h2.addWidget(btn_save)
layout_h2.addWidget(btn_blur)
layout_h2.addWidget(btn_left)
layout_h2.addWidget(btn_right)
layout_h2.addWidget(btn_flip)
layout_h2.addWidget(btn_sharp)
layout_h2.addWidget(btn_grey)
layout_v2.addLayout(layout_h2)
layout_h1.addLayout(layout_v1, 20)
layout_h1.addLayout(layout_v2, 80)
btn_dir.clicked.connect(show_filenames_list)
current_image = ImageProcessor()
btn_grey.clicked.connect(current_image.do_bw)
btn_flip.clicked.connect(current_image.flip)
btn_left.clicked.connect(lambda: current_image.rotate_image(90))
btn_right.clicked.connect(lambda: current_image.rotate_image(270))
btn_save.clicked.connect(current_image.save_image)
btn_sharp.clicked.connect(current_image.sharpen)
btn_blur.clicked.connect(current_image.blur)
main_win.setLayout(layout_h1)
main_win.show()
app.exec()
