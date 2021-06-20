from PySide2.QtCore import QSize, Signal, Slot, Qt, QRect, QTimer, QRectF
from PySide2.QtGui import QPainter, QFont, QColor, QPen, QResizeEvent, QMouseEvent, QPaintEvent
from PySide2.QtWidgets import QWidget

class ProgressButton(QWidget):
    """
    按钮进度条控件
    作者:倪大侠(QQ:393320854 zyb920@hotmail.com) 2019-4-17
    译者:sunchuquin(QQ:1715216365) 2021-06-20
    1. 可设置进度线条宽度+颜色
    2. 可设置边框宽度+颜色
    3. 可设置圆角角度+背景颜色
    """

    valueChanged = Signal(int)  # value

    def __init__(self, parent: QWidget = None):
        super(ProgressButton, self).__init__(parent)
        self.__lineWidth: int = 8  # 线条宽度
        self.__lineColor: QColor = QColor(250, 250, 250)  # 线条颜色
        self.__borderWidth: int = 0  # 边框宽度
        self.__borderColor: QColor = QColor(14, 153, 160)  # 边框颜色
        self.__borderRadius: int = 5  # 圆角角度
        self.__bgColor: QColor = QColor(34, 163, 169)  # 背景颜色

        self.__value: float = 0.0  # 当前值
        self.__status: int = 0  # 状态
        self.__tempWidth: int = 0  # 动态改变宽度
        self.__timer: QTimer = QTimer(self)  # 定时器改变进度
        self.__timer.setInterval(10)
        self.__timer.timeout.connect(self.__progress)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__tempWidth = event.size().width()
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.__timer.isActive(): return
        self.__status = 0
        self.__value = 0.0
        self.__tempWidth = self.width()
        self.__timer.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 1: 绘制当前进度; 否则绘制按钮背景
        if 1 is self.__status:  self.drawProgress(painter)
        else: self.drawBg(painter)

    def drawBg(self, painter: QPainter) -> None:
        painter.save()
        width: int = self.width()
        height: int = self.height()
        side: int = min(width, height)

        pen: QPen = QPen()
        pen.setWidth(self.__borderWidth)
        pen.setColor(self.__borderColor)
        painter.setPen(pen if self.__borderWidth > 0 else Qt.NoPen)
        painter.setBrush(self.bgColor)

        rect: QRect = QRect(((width - self.__tempWidth) // 2) + self.__borderWidth,
                            self.__borderWidth,
                            self.__tempWidth - (self.__borderWidth * 2),
                            height - (self.__borderWidth * 2))
        painter.drawRoundedRect(rect, self.__borderRadius, self.__borderRadius)

        font: QFont = QFont()
        font.setPixelSize(side - 18)
        painter.setFont(font)
        painter.setPen(self.__lineColor)
        painter.drawText(rect, Qt.AlignCenter, "完成" if self.__status == 2 else "开始")

        painter.restore()

    def drawProgress(self, painter: QPainter) -> None:
        painter.save()

        width: int = self.width()
        height: int = self.height()
        side: int = min(width, height)
        radius: int = 99 - self.__borderWidth

        # 绘制外圆
        pen: QPen = QPen()
        pen.setWidth(self.__borderWidth)
        pen.setColor(self.__borderColor)
        painter.setPen(pen if self.__borderWidth > 0 else Qt.NoPen)
        painter.setBrush(self.__bgColor)

        # 平移坐标轴中心, 等比例缩放
        rectCircle: QRect = QRect(-radius, -radius, radius * 2, radius * 2)
        painter.translate(width / 2, height / 2)
        painter.scale(side / 200.0, side / 200.0)
        painter.drawEllipse(rectCircle)

        # 绘制圆弧进度
        pen.setWidth(self.__lineWidth)
        pen.setColor(self.__lineColor)
        painter.setPen(pen)

        offset: int = radius - self.__lineWidth - 5
        rectArc: QRectF = QRectF(-offset, -offset, offset * 2, offset * 2)
        startAngle: int = offset * 16
        spanAngle: int = int(-self.__value * 16)
        painter.drawArc(rectArc, startAngle, spanAngle)

        # 绘制进度文字
        font: QFont = QFont()
        font.setPixelSize(offset - 15)
        painter.setFont(font)
        strValue: str = str(int(self.__value) * 100 // 360) + '%'
        painter.drawText(rectCircle, Qt.AlignCenter, strValue)

        painter.restore()

    @Slot()
    def __progress(self):
        if 0 is self.__status:
            self.__tempWidth -= 5
            if self.__tempWidth < self.height() / 2:
                self.__tempWidth = self.height() / 2
                self.__status = 1
        elif 1 is self.__status:
            self.__value += 1.0
            if self.__value >= 360:
                self.__value = 360.0
                self.__status = 2
        elif 2 is self.__status:
            self.__tempWidth += 5
            if self.__tempWidth > self.width():
                self.__tempWidth = self.width()
                self.__timer.stop()

        self.update()

    def sizeHint(self) -> QSize: return QSize(200, 80)
    def minimumSizeHint(self) -> QSize: return QSize(30, 15)

    @property
    def lineWidth(self) -> int: return self.__lineWidth

    @lineWidth.setter
    def lineWidth(self, line_width: int) -> None:
        if self.__lineWidth == line_width: return
        self.__lineWidth = line_width
        self.update()

    @property
    def lineColor(self) -> QColor: return self.__lineColor

    @lineColor.setter
    def lineColor(self, line_color: QColor) -> None:
        if self.__lineColor == line_color: return
        self.__lineColor = line_color
        self.update()

    @property
    def borderWidth(self) -> int: return self.__borderWidth

    @borderWidth.setter
    def borderWidth(self, border_width: int) -> None:
        if self.__borderWidth == border_width: return
        self.__borderWidth = border_width
        self.update()

    @property
    def borderColor(self) -> QColor: return self.__borderColor

    @borderColor.setter
    def borderColor(self, border_color: QColor) -> None:
        if self.__borderColor == border_color: return
        self.__borderColor = border_color
        self.update()

    @property
    def borderRadius(self) -> int: return self.__borderRadius

    @borderRadius.setter
    def borderRadius(self, border_radius: int) -> None:
        if self.__borderRadius == border_radius: return
        self.__borderRadius = border_radius
        self.update()

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QVBoxLayout, QApplication

    class FrmProgressButton(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmProgressButton, self).__init__(parent)
            self.progressbutton2 = ProgressButton()
            self.progressbutton3 = ProgressButton()
            self.progressbutton4 = ProgressButton()
            self.progressbutton5 = ProgressButton()
            self.progressbutton6 = ProgressButton()
            layout = QVBoxLayout()
            layout.addWidget(self.progressbutton2)
            layout.addWidget(self.progressbutton3)
            layout.addWidget(self.progressbutton4)
            layout.addWidget(self.progressbutton5)
            layout.addWidget(self.progressbutton6)
            self.setLayout(layout)
            self.initForm()

        def initForm(self) -> None:
            self.progressbutton2.bgColor = QColor(40, 45, 48)
            self.progressbutton3.bgColor = QColor(214, 77, 84)
            self.progressbutton4.bgColor = QColor(162, 121, 197)
            self.progressbutton5.bgColor = QColor(0, 150, 121)
            self.progressbutton6.bgColor = QColor(71, 164, 233)

    app = QApplication()
    window = FrmProgressButton()
    window.show()
    sys.exit(app.exec_())
