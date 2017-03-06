import queue
import sys

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from field import Field, plus
from graphics import draw_field


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.field_size = 30, 20
        self.game_field = Field(*self.field_size)
        self.initUI()

    def initUI(self):
        self.scale = 30
        self.setGeometry(100, 100,
                         self.scale * self.field_size[0],
                         self.scale * self.field_size[1])
        self.setWindowTitle('Draw text')
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def keyPressEvent(self, event: QKeyEvent):
        delta = (0, 0)
        if event.key() == Qt.Key_Left:
            delta = (-1, 0)
        elif event.key() == Qt.Key_Right:
            delta = (1, 0)
        elif event.key() == Qt.Key_Up:
            delta = (0, -1)
        elif event.key() == Qt.Key_Down:
            delta = (0, 1)
        elif event.key() == Qt.Key_Space:
            self.game_field.show_map = not self.game_field.show_map
        elif event.key() == Qt.Key_E:
            self.game_field.create_map()
        elif event.key() == Qt.Key_Q:
            self.game_field.show_way()
        elif event.key() == Qt.Key_C:
            self.game_field.show_rand_cell()
        self.game_field.step(delta)
        self.repaint()

    def drawText(self, event, qp):
        qp.setPen(Qt.black)
        qp.setFont(QFont('Decorative', 10))
        draw_field(self.game_field, qp, self.scale)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())