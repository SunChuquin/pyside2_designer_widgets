from PySide2.QtCore import QPoint, QSize, Signal, Qt, QPointF
from PySide2.QtGui import QColor, QShowEvent, QResizeEvent, QMouseEvent, QPaintEvent, QPainter, QPixmap, \
    QLinearGradient, QPen, QFont, QFontMetrics, QPainterPath
from PySide2.QtWidgets import QWidget


class ColorPanelHSB(QWidget):
    """
    颜色选取面板
    作者:feiyangqingyun(QQ:517216493) 2017-11-17
    译者:sunchuquin(QQ:1715216365) 2021-07-03
    1. 可设置当前百分比,用于控制指针大小
    2. 可设置边框宽度
    3. 可设置边框颜色
    4. 可设置指针颜色
    """
    colorChanged = Signal(QColor, float, float)  # color, hue, sat

    def __init__(self, parent: QWidget = None):
        super(ColorPanelHSB, self).__init__(parent)
        self.__percent: int = 100  # 当前百分比
        self.__borderWidth: int = 10  # 边框宽度
        self.__borderColor: QColor = QColor(0, 0, 0, 50)  # 边框颜色
        self.__cursorColor: QColor = QColor(0, 0, 0)  # 鼠标按下处的文字形状颜色

        self.__color: QColor = QColor(255, 0, 0)  # 鼠标按下处的颜色
        self.__hue: float = 0  # hue值
        self.__sat: float = 100  # sat值

        self.__lastPos: QPoint = QPoint(self.__borderWidth, self.__borderWidth)  # 最后鼠标按下去的坐标
        self.__bgPix: QPixmap = QPixmap()  # 背景颜色图片

    def showEvent(self, event: QShowEvent = None) -> None:
        width: int = self.width()
        height: int = self.height()

        # 首次显示记住当前背景截图,用于获取颜色值
        self.__bgPix = QPixmap(width, height)
        self.__bgPix.fill(Qt.transparent)
        painter: QPainter = QPainter()
        painter.begin(self.__bgPix)

        colorStart: QColor = QColor()
        colorCenter: QColor = QColor()
        colorEnd: QColor = QColor()
        for i in range(width):
            colorStart.setHslF(i / width, 1, 0)
            colorCenter.setHslF(i / width, 1, 0.5)
            colorEnd.setHslF(i / width, 1, 1)

            linearGradient: QLinearGradient = QLinearGradient()
            linearGradient.setStart(QPointF(i, -height))
            linearGradient.setFinalStop(QPointF(i, height))
            linearGradient.setColorAt(0.0, colorStart)
            linearGradient.setColorAt(0.5, colorCenter)
            linearGradient.setColorAt(1.0, colorEnd)

            painter.setPen(QPen(linearGradient, 1))
            painter.drawLine(QPointF(i, 0), QPointF(i, height))

        painter.end()

    def resizeEvent(self, event: QResizeEvent = None) -> None:
        self.showEvent()

    def mousePressEvent(self, event: QMouseEvent = None) -> None:
        self.mouseMoveEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent = None) -> None:
        x: int = event.pos().x()
        y: int = event.pos().y()

        # 矫正X轴的偏差
        if x <= self.__borderWidth:
            x = self.__borderWidth
        elif x >= self.width() - self.__borderWidth:
            x = self.width() - self.__borderWidth

        # 矫正Y轴的偏差
        if y <= self.__borderWidth:
            y = self.__borderWidth
        elif y >= self.height() - self.__borderWidth:
            y = self.height() - self.__borderWidth

        # 指针必须在范围内
        self.__lastPos = QPoint(x, y)

        # 获取当前坐标处的颜色值
        self.__color = QColor(self.__bgPix.toImage().pixel(self.__lastPos))

        # X坐标所在360分比为hue值
        self.__hue = ((x - self.__borderWidth) / (self.width() - self.__borderWidth * 2)) * 360
        # Y坐标所在高度的100分比sat值
        self.__sat = 100 - ((y - self.__borderWidth) / (self.height() - self.__borderWidth * 2) * 100)

        self.update()
        self.colorChanged.emit(self.__color, self.__hue, self.__sat)

    def paintEvent(self, event: QPaintEvent = None) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景颜色
        self.drawBg(painter)
        # 绘制按下出的形状
        self.drawCursor(painter)
        # 绘制边框
        self.drawBorder(painter)

    def drawBg(self, painter: QPainter = None) -> None:
        painter.save()

        if not self.__bgPix.isNull():
            painter.drawPixmap(0, 0, self.__bgPix)

        painter.restore()

    def drawCursor(self, painter: QPainter = None) -> None:
        painter.save()
        painter.setPen(self.__cursorColor)

        text: str = "+"

        # 根据右侧的百分比显示字体大小
        textFont: QFont = QFont()
        size: int = int(20 + (35 * self.__percent / 100))
        textFont.setPixelSize(size)

        # 计算文字的宽度高度,自动移到鼠标按下处的中心点
        fm: QFontMetrics = QFontMetrics(textFont)
        textWidth: int = fm.width(text)
        textHeight: int = fm.height()
        textPoint: QPoint = self.__lastPos - QPoint(textWidth // 2, -(textHeight // 4))

        path: QPainterPath = QPainterPath()
        path.addText(textPoint, textFont, text)
        painter.drawPath(path)

        painter.restore()

    def drawBorder(self, painter: QPainter = None) -> None:
        painter.save()

        width: int = self.width()
        height: int = self.height()
        offset: int = self.__borderWidth

        pen: QPen = QPen()
        pen.setWidth(offset)
        pen.setColor(self.__borderColor)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.MiterJoin)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(offset // 2, offset // 2, width - offset, height - offset)

        painter.restore()

    def sizeHint(self) -> QSize: return QSize(500, 350)

    def minimumSizeHint(self) -> QSize: return QSize(100, 60)

    @property
    def percent(self) -> int: return self.__percent

    @percent.setter
    def percent(self, n_percent: int) -> None:
        if self.__percent == n_percent: return
        self.__percent = n_percent
        self.update()

    @property
    def borderColor(self) -> QColor: return self.__borderColor

    @borderColor.setter
    def borderColor(self, border_color: QColor) -> None:
        if self.__borderColor == border_color: return
        self.__borderColor = border_color
        self.update()

    @property
    def cursorColor(self) -> QColor: return self.__cursorColor

    @cursorColor.setter
    def cursorColor(self, cursor_color: QColor) -> None:
        if self.__cursorColor == cursor_color: return
        self.__cursorColor = cursor_color
        self.update()

    @property
    def color(self) -> QColor: return self.__color

    @property
    def hue(self) -> float: return self.__hue

    @property
    def sat(self) -> float: return self.__sat


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication, QHBoxLayout, QLabel

    from custom_widgets.color.colorpanelbar import ColorPanelBar

    class FrmColorPanelHSB(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmColorPanelHSB, self).__init__(parent)

            self.colorPanelHSB = ColorPanelHSB()
            self.colorPanelBar = ColorPanelBar()
            self.labColor = QLabel()
            self.labColor.setMinimumWidth(50)
            self.labColor.setMaximumWidth(50)

            layout = QHBoxLayout()
            layout.addWidget(self.colorPanelHSB)
            layout.addWidget(self.colorPanelBar)
            layout.addWidget(self.labColor)
            self.setLayout(layout)

            self.colorPanelHSB.colorChanged.connect(self.colorChangedHSB)
            self.colorPanelBar.colorChanged.connect(self.colorChangedBar)

            self.colorPanelBar.staticMode = False
            self.colorChangedBar(QColor(255, 0, 0), self.colorPanelBar.value, self.colorPanelBar.percent)

        def colorChangedHSB(self, color: QColor, hue: float, sat: float) -> None:
            self.colorPanelBar.topColor = color
            self.colorPanelBar.borderColor = color
            self.colorChangedBar(self.colorPanelBar.color,
                                 self.colorPanelBar.value,
                                 self.colorPanelBar.percent)

        def colorChangedBar(self, color: QColor, value: float, percent: float) -> None:
            self.colorPanelHSB.percent = percent
            self.labColor.setStyleSheet("QLabel{background:%s;}" % color.name())

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmColorPanelHSB()
    window.setWindowTitle("颜色选取面板")
    window.show()
    sys.exit(app.exec_())
