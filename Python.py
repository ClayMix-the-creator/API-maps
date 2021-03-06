import sys
import os

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.map_but.clicked.connect(self.find_map)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.scale_dsp.stepUp()

        if event.key() == Qt.Key_PageDown:
            self.scale_dsp.stepDown()

        if self.line_x.text() != '' and self.line_y.text() != '' and self.scale_dsp.value() != 0:
            self.find_map()

    def getImage(self):
        x = self.line_x.text()
        y = self.line_y.text()
        scale = self.scale_dsp.text()
        scale = '.'.join(scale.split(','))

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={y},{x}&spn={scale},{scale}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def find_map(self):
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.pixmap = self.pixmap.scaled(861, 641)
        self.map.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
