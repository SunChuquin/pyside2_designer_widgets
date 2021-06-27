import sys
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QApplication, QFrame, QWidget, QVBoxLayout, QHBoxLayout


class Line(QFrame):
    """
    光晕日历控件
    来源: https://stackoverflow.com/questions/51056997/how-to-set-color-of-frame-of-qframe
    1. 可设置线的颜色
    2. 可设置线的方向
    """

    def __init__(self, parent=None, shape=QFrame.HLine, color=QColor("black")):
        super(Line, self).__init__(parent)
        self.setFrameShape(shape)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(0)
        self.setMidLineWidth(3)
        self.setContentsMargins(0, 0, 0, 0)
        self.setColor(color)

    def setColor(self, color):
        pal = self.palette()
        pal.setColor(QPalette.WindowText, color)
        self.setPalette(pal)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(400, 400)
    lay_1 = QVBoxLayout()
    lay_1.addWidget(Line(shape=QFrame.VLine, color=QColor("black")))
    lay_1.addWidget(Line(shape=QFrame.VLine, color=QColor("red")))
    lay_1.addWidget(Line(shape=QFrame.VLine, color=QColor(0, 255, 0)))
    lay_1.addWidget(Line(shape=QFrame.VLine, color=QColor(Qt.blue)))
    lay_2 = QVBoxLayout()
    lay_2.addWidget(Line(shape=QFrame.HLine, color=QColor("black")))
    lay_2.addWidget(Line(shape=QFrame.HLine, color=QColor("red")))
    lay_2.addWidget(Line(shape=QFrame.HLine, color=QColor(0, 255, 0)))
    lay_2.addWidget(Line(shape=QFrame.HLine, color=QColor(Qt.blue)))
    layout = QHBoxLayout()
    layout.addLayout(lay_1)
    layout.addLayout(lay_2)
    w.setLayout(layout)
    w.show()
    sys.exit(app.exec_())
