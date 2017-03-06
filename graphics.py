from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import  Qt


def draw_field(field, qp: QPainter, scale):
    for index_x in range(field.width):
        for index_y in range(field.height):
            qp.setBrush(Qt.black)
            cell = field.map[index_x][index_y]
            if (index_x == field.player_pos[0]) and (index_y == field.player_pos[1]):
                qp.setBrush(QColor(0, 255 * field.count_around / 8, 100))
            else:
                if not field.show_map:
                    if cell.hidden:
                         qp.setBrush(Qt.black)
                    elif cell.dang:
                         qp.setBrush(Qt.red)
                    else:
                        qp.setBrush(Qt.white)
                else:
                    if cell.dang:
                         qp.setBrush(Qt.red)
                    else:
                        qp.setBrush(Qt.white)
            pos_x = index_x * scale
            pos_y = index_y * scale
            qp.drawRect(pos_x, pos_y, pos_x + scale, pos_y + scale)
