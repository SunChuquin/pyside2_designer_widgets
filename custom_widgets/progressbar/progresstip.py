from PySide2.QtCore import QSize, Signal, Qt, QRect, QPoint
from PySide2.QtGui import QColor, QBrush, QPaintEvent, QPainter, QPolygon
from PySide2.QtWidgets import QWidget


class ProgressTip(QWidget):
    """
    提示进度条控件
    作者:feiyangqingyun(QQ:517216493) 2019-10-05
    译者:sunchuquin(QQ:1715216365) 2021-07-18
    1. 可设置最小值/最大值/范围值/当前值
    2. 可设置是否百分比显示
    3. 可设置边距,流出空隙防止提示信息跑到外面
    4. 可设置进度的颜色,可以是渐变画刷
    5. 可设置背景颜色/文字颜色/提示背景
    6. 可设置圆角角度
    7. 如果设置了进度画刷则提示背景也采用该画刷
    """
    valueChanged = Signal(float)  # value

    def __init__(self, parent: QWidget = None):
        super(ProgressTip, self).__init__(parent)
        self.__minValue: float = 0  # 最小值
        self.__maxValue: float = 100  # 最大值
        self.__value: float = 0  # 目标值

        self.__percent: bool = True  # 百分比显示
        self.__padding: int = 20  # 边距
        self.__radius: int = 0  # 圆角角度

        self.__valueBrush: QBrush = Qt.NoBrush  # 进度画刷
        self.__valueColor: QColor = QColor(34, 163, 169)  # 进度颜色
        self.__bgColor: QColor = QColor(100, 100, 100)  # 背景颜色
        self.__tipColor: QColor = QColor(34, 163, 169)  # 提示背景颜色
        self.__textColor: QColor = QColor(255, 255, 255)  # 文字颜色

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿,平移坐标轴中心,等比例缩放
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self.drawBg(painter)  # 绘制背景
        self.drawTip(painter)  # 绘制上部分提示信息
        self.drawValue(painter)  # 绘制进度

    def drawBg(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__bgColor)

        rect: QRect = QRect(self.__padding,
                            self.height() // 3 * 2,
                            self.width() - self.__padding * 2,
                            self.height() // 3)
        painter.drawRoundedRect(rect, self.__radius, self.__radius)

        painter.restore()

    def drawTip(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.__tipColor if self.__valueBrush == Qt.NoBrush else self.__valueBrush))

        # 计算当前值对应的百分比
        step: float = self.__value / (self.__maxValue - self.__minValue)
        progress: int = int((self.width() - self.__padding * 2) * step)

        # 绘制上部分提示信息背景
        rect: QRect = QRect(progress, 0, self.__padding * 2, int(self.height() / 2.1))
        painter.drawRoundedRect(rect, 2, 2)

        # 绘制倒三角
        centerX: int = rect.center().x()
        initY: int = rect.height()
        offset: int = 5

        pts: QPolygon = QPolygon()
        pts.append(QPoint(centerX - offset, initY))
        pts.append(QPoint(centerX + offset, initY))
        pts.append(QPoint(centerX, initY + offset))
        painter.drawPolygon(pts)

        # 绘制文字
        strValue: str = ''
        if self.__percent:
            temp: float = self.__value / (self.__maxValue - self.__minValue) * 100
            strValue = "%s%%" % int(temp)
        else:
            strValue = "%s" % int(self.__value)

        painter.setPen(self.__textColor)
        painter.drawText(rect, Qt.AlignCenter, strValue)

        painter.restore()

    def drawValue(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)

        # 定义了画刷则取画刷,可以形成渐变效果
        painter.setBrush(QBrush(self.__valueColor if self.__valueBrush == Qt.NoBrush else self.__valueBrush))

        # 计算当前值对应的百分比
        step: float = self.__value / (self.__maxValue - self.__minValue)
        progress: int = int((self.width() - self.__padding * 2) * step)

        rect: QRect = QRect(self.__padding, (self.height() // 3) * 2, progress, int(self.height() / 3))
        painter.drawRoundedRect(rect, self.__radius, self.__radius)

        painter.restore()

    def setRange(self, min_value: float, max_value: float) -> None:
        # 如果最小值大于或者等于最大值则不设置
        if min_value >= max_value: return

        self.__minValue = min_value
        self.__maxValue = max_value

        # 如果目标值不在范围值内,则重新设置目标值
        # 值小于最小值则取最小值,大于最大值则取最大值
        if self.__value < min_value: self.value = min_value
        elif self.__value > max_value: self.value = max_value

        self.update()

    @property
    def minValue(self) -> float: return self.__minValue

    @minValue.setter
    def minValue(self, min_value: float) -> None:
        self.setRange(min_value, self.__maxValue)

    @property
    def maxValue(self) -> float: return self.__maxValue

    @maxValue.setter
    def maxValue(self, max_value: float) -> None:
        self.setRange(self.__minValue, max_value)

    @property
    def value(self) -> float: return self.__value

    def setValue(self, n_value: int) -> None:
        self.value = n_value

    @value.setter
    def value(self, n_value: float) -> None:
        # 值和当前值一致则无需处理
        if n_value == self.__value: return

        # 值小于最小值则取最小值,大于最大值则取最大值
        if n_value < self.__minValue: n_value = self.__minValue
        elif n_value > self.__maxValue: n_value = self.__maxValue

        self.__value = n_value
        self.update()
        self.valueChanged.emit(n_value)

    @property
    def percent(self) -> bool: return self.__percent

    @percent.setter
    def percent(self, n_percent: bool) -> None:
        if self.__percent == n_percent: return
        self.__percent = n_percent
        self.update()

    @property
    def padding(self) -> int: return self.__padding

    @padding.setter
    def padding(self, n_padding: int) -> None:
        if self.__padding == n_padding: return
        self.__padding = n_padding
        self.update()

    @property
    def radius(self) -> int: return self.__radius

    @radius.setter
    def radius(self, n_radius: int) -> None:
        if self.__radius == n_radius: return
        self.__radius = n_radius
        self.update()

    @property
    def valueBrush(self) -> QBrush: return self.__valueBrush

    @valueBrush.setter
    def valueBrush(self, value_brush: QBrush) -> None:
        if self.__valueBrush == value_brush: return
        self.__valueBrush = value_brush
        self.update()

    @property
    def valueColor(self) -> QColor: return self.__valueColor

    @valueColor.setter
    def valueColor(self, value_color: QColor) -> None:
        if self.__valueColor == value_color: return
        self.__valueColor = value_color
        self.update()

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def tipColor(self) -> QColor: return self.__tipColor

    @tipColor.setter
    def tipColor(self, tip_color: QColor) -> None:
        if self.__tipColor == tip_color: return
        self.__tipColor = tip_color
        self.update()

    @property
    def textColor(self) -> QColor: return self.__textColor

    @textColor.setter
    def textColor(self, text_color: QColor) -> None:
        if self.__textColor == text_color: return
        self.__textColor = text_color
        self.update()

    def sizeHint(self) -> QSize: return QSize(300, 50)

    def minimumSizeHint(self) -> QSize: return QSize(50, 30)


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import Qt, QTextCodec
    from PySide2.QtGui import QFont, QLinearGradient
    from PySide2.QtWidgets import QApplication, QSlider, QVBoxLayout, QSizePolicy

    class FrmProgressTip(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmProgressTip, self).__init__(parent)
            layout = QVBoxLayout()

            self.progressTip1 = ProgressTip()
            self.progressTip2 = ProgressTip()
            self.progressTip3 = ProgressTip()
            self.progressTip4 = ProgressTip()
            self.horizontalSlider = QSlider(Qt.Horizontal)

            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.progressTip1.setSizePolicy(sizePolicy)
            self.progressTip2.setSizePolicy(sizePolicy)
            self.progressTip3.setSizePolicy(sizePolicy)
            self.progressTip4.setSizePolicy(sizePolicy)

            layout.addWidget(self.progressTip1)
            layout.addWidget(self.progressTip2)
            layout.addWidget(self.progressTip3)
            layout.addWidget(self.progressTip4)
            layout.addWidget(self.horizontalSlider)
            layout.setSpacing(10)

            self.setLayout(layout)
            self.initForm()

        def initForm(self) -> None:
            brush: QLinearGradient = QLinearGradient(0, 0, self.progressTip1.width(), 0)

            brush.setColorAt(0, "#49AFFB")
            brush.setColorAt(1, "#5D51FF")
            self.progressTip1.valueBrush = QBrush(brush)

            brush.setColorAt(0, "#32B9CF")
            brush.setColorAt(1, "#C13256")
            self.progressTip2.valueBrush = QBrush(brush)

            brush.setColorAt(0, "#C13256")
            brush.setColorAt(1, "#32B9CF")
            self.progressTip3.valueBrush = QBrush(brush)

            self.progressTip3.radius = 7
            self.progressTip4.radius = 7
            self.progressTip3.valueColor = QColor("#FA358A")
            self.progressTip4.valueColor = QColor("#2EA3EF")
            self.progressTip3.tipColor = QColor("#FA358A")
            self.progressTip4.tipColor = QColor("#2EA3EF")

            self.horizontalSlider.valueChanged.connect(self.progressTip1.setValue)
            self.horizontalSlider.valueChanged.connect(self.progressTip2.setValue)
            self.horizontalSlider.valueChanged.connect(self.progressTip3.setValue)
            self.horizontalSlider.valueChanged.connect(self.progressTip4.setValue)
            self.horizontalSlider.setValue(88)
            self.horizontalSlider.setMaximum(100)

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmProgressTip()
    window.resize(500, 300)
    window.setWindowTitle("提示进度条")
    window.show()
    sys.exit(app.exec_())
