from PySide2.QtCore import QTimer, QSize, Signal, Qt, QRectF, QPoint
from PySide2.QtGui import QPaintEvent, QPainter, QColor, QPen, QPolygon
from PySide2.QtWidgets import QWidget

import math


class GaugePanel(QWidget):
    """
    面板仪表盘控件
    作者:feiyangqingyun(QQ:517216493) 2019-7-3
    译者:sunchuquin(QQ:1715216365) 2021-07-13
    1. 可设置范围值,支持负数值
    2. 可设置精确度+刻度尺精确度,最大支持小数点后3位
    3. 可设置大刻度数量/小刻度数量
    4. 可设置开始旋转角度/结束旋转角度
    5. 可设置是否启用动画效果以及动画效果每次移动的步长
    6. 可设置刻度颜色+文字颜色+圆环的宽度和颜色
    7. 自适应窗体拉伸,刻度尺和文字自动缩放
    8. 可设置单位以及仪表盘名称
    """
    valueChanged = Signal(int)  # value

    def __init__(self, parent: QWidget = None):
        super(GaugePanel, self).__init__(parent)
        self.__minValue: float = 0  # 最小值
        self.__maxValue: float = 100  # 最大值
        self.__value: float = 0  # 目标值
        self.__precision: int = 0  # 精确度,小数点后几位
        self.__scalePrecision: int = 0  # 刻度尺精确度,小数点后几位

        self.__scaleMajor: int = 10  # 大刻度数量
        self.__scaleMinor: int = 5  # 小刻度数量
        self.__startAngle: int = 45  # 开始旋转角度
        self.__endAngle: int = 45  # 结束旋转角度

        self.__animation: bool = False  # 是否启用动画显示
        self.__animationStep: float = 0.5  # 动画显示时步长

        self.__ringWidth: int = 10  # 圆环宽度
        self.__ringColor: QColor = QColor(54, 192, 254)  # 圆环颜色

        self.__scaleColor: QColor = QColor(34, 163, 169)  # 刻度颜色
        self.__pointerColor: QColor = QColor(34, 163, 169)  # 指针颜色
        self.__bgColor: QColor = QColor(Qt.transparent)  # 背景颜色
        self.__textColor: QColor = QColor(50, 50, 50)  # 文字颜色
        self.__unit: str = 'V'  # 单位
        self.__text: str = '电压'  # 描述文字

        self.__reverse: bool = False  # 是否往回走
        self.__currentValue: float = 0  # 当前值
        self.__timer: QTimer = QTimer(self)  # 定时器绘制动画
        self.__timer.setInterval(10)
        self.__timer.timeout.connect(self.updateValue)

    def paintEvent(self, event: QPaintEvent = None) -> None:
        width: int = self.width()
        height: int = self.height()
        side: int = min(width, height)
    
        # 绘制准备工作,启用反锯齿,平移坐标轴中心,等比例缩放
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景
        if self.__bgColor != Qt.transparent:
            painter.setPen(Qt.NoPen)
            painter.fillRect(self.rect(), self.__bgColor)

        painter.translate(width / 2, height / 2)
        painter.scale(side / 200.0, side / 200.0)

        self.drawRing(painter)  # 绘制圆环
        self.drawScale(painter)  # 绘制刻度线
        self.drawScaleNum(painter)  # 绘制刻度值
        self.drawPointer(painter)  # 绘制指示器
        self.drawValue(painter)  # 绘制当前值

    def drawRing(self, painter: QPainter = None) -> None:
        radius: int = 70
        painter.save()

        pen: QPen = QPen()
        pen.setCapStyle(Qt.FlatCap)
        pen.setWidthF(self.__ringWidth)
        pen.setColor(self.__ringColor)
        painter.setPen(pen)

        radius = radius - self.__ringWidth
        rect: QRectF = QRectF(-radius, -radius, radius * 2, radius * 2)
        angleAll: float = 360.0 - self.__startAngle - self.__endAngle
        painter.drawArc(rect, (270 - self.__startAngle - angleAll) * 16, angleAll * 16)

        painter.restore()

    def drawScale(self, painter: QPainter = None) -> None:
        radius: int = 80
        painter.save()

        painter.rotate(self.__startAngle)
        steps: int = (self.__scaleMajor * self.__scaleMinor)
        angleStep: float = (360.0 - self.__startAngle - self.__endAngle) / steps

        pen: QPen = QPen()
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.__scaleColor)

        for i in range(steps + 1):
            if i % self.__scaleMinor == 0:
                pen.setWidthF(1.5)
                painter.setPen(pen)
                painter.drawLine(0, radius - 8, 0, radius + 5)
            else:
                pen.setWidthF(0.5)
                painter.setPen(pen)
                painter.drawLine(0, radius - 8, 0, radius - 3)

            painter.rotate(angleStep)

        painter.restore()

    def drawScaleNum(self, painter: QPainter = None) -> None:
        radius: int = 95
        painter.save()
        painter.setPen(self.__scaleColor)

        startRad: float = (360 - self.__startAngle - 90) * (math.pi / 180)
        deltaRad: float = (360 - self.__startAngle - self.__endAngle) * (math.pi / 180) / self.__scaleMajor

        for i in range(self.__scaleMajor + 1):
            sina: float = math.sin(startRad - i * deltaRad)
            cosa: float = math.cos(startRad - i * deltaRad)
            value: float = 1.0 * i * ((self.__maxValue - self.__minValue) / self.__scaleMajor) + self.__minValue

            strValue: str = '%s' % round(value, self.__scalePrecision) if self.__scalePrecision else str(int(value))
            textWidth: float = self.fontMetrics().width(strValue)
            textHeight: float = self.fontMetrics().height()
            x: int = int(radius * cosa - textWidth / 2)
            y: int = int(-radius * sina + textHeight / 4)
            painter.drawText(x, y, strValue)

        painter.restore()

    def drawPointer(self, painter: QPainter = None) -> None:
        radius: int = 70
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__pointerColor)

        pts: QPolygon = QPolygon()
        pts.append(QPoint(4, -5))
        pts.append(QPoint(0, 0))
        pts.append(QPoint(-8, 5))
        pts.append(QPoint(0, 0))
        pts.append(QPoint(0, radius))

        painter.rotate(self.__startAngle)
        degRotate: float = (360.0 - self.__startAngle - self.__endAngle) / \
                           (self.__maxValue - self.__minValue) * \
                           (self.__currentValue - self.__minValue)
        painter.rotate(degRotate)
        painter.drawConvexPolygon(pts)

        painter.restore()

    def drawValue(self, painter: QPainter = None) -> None:
        radius: int = 100
        painter.save()
        painter.setPen(self.__textColor)

        font: QFont = QFont()
        font.setPixelSize(15)
        painter.setFont(font)

        strValue: str = '%s' % round(self.__currentValue, self.__precision) if self.__precision else str(int(self.__currentValue))
        strValue = "%s %s" % (strValue, self.__unit)
        valueRect: QRectF = QRectF(-radius, radius / 3.5, radius * 2, radius / 3.5)
        painter.drawText(valueRect, Qt.AlignCenter, strValue)

        textRect: QRectF = QRectF(-radius, radius / 2.5, radius * 2, radius / 2.5)
        font.setPixelSize(12)
        painter.setFont(font)
        painter.drawText(textRect, Qt.AlignCenter, self.__text)

        painter.restore()

    def updateValue(self) -> None:
        if not self.__reverse:
            if self.__currentValue >= self.__value:
                self.__timer.stop()
            else:
                self.__currentValue += self.__animationStep
        else:
            if self.__currentValue <= self.__value:
                self.__timer.stop()
            else:
                self.__currentValue -= self.__animationStep

        self.update()

    def setRange(self, min_value, max_value) -> None:
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
        self.value = float(n_value)

    @value.setter
    def value(self, n_value: float) -> None:
        # 值和当前值一致则无需处理
        if n_value == self.__value: return

        # 值小于最小值则取最小值,大于最大值则取最大值
        if n_value < self.__minValue:
            n_value = self.__minValue
        elif n_value > self.__maxValue:
            n_value = self.__maxValue

        if n_value > self.__value:
            self.__reverse = False
        elif n_value < self.__value:
            self.__reverse = True

        self.__value = n_value
        self.valueChanged.emit(n_value)

        if not self.__animation:
            self.__currentValue = self.__value
            self.update()
        else:
            self.__timer.start()

    @property
    def precision(self) -> int: return self.__precision

    @precision.setter
    def precision(self, n_precision: int) -> None:
        if 3 < n_precision == self.__precision: return
        self.__precision = n_precision
        self.update()

    @property
    def scalePrecision(self) -> int: return self.__scalePrecision

    @scalePrecision.setter
    def scalePrecision(self, scale_precision: int) -> None:
        if 2 < scale_precision == self.__scalePrecision: return
        self.__scalePrecision = scale_precision
        self.update()

    @property
    def scaleMajor(self) -> int: return self.__scaleMajor

    @scaleMajor.setter
    def scaleMajor(self, scale_major: int) -> None:
        if 0 >= scale_major == self.__scaleMajor: return
        self.__scaleMajor = scale_major
        self.update()

    @property
    def scaleMinor(self) -> int: return self.__scaleMinor

    @scaleMinor.setter
    def scaleMinor(self, scale_minor: int) -> None:
        if self.__scaleMinor == scale_minor: return
        self.__scaleMinor = scale_minor
        self.update()

    @property
    def startAngle(self) -> int: return self.__startAngle

    @startAngle.setter
    def startAngle(self, start_angle: int) -> None:
        if self.__startAngle == start_angle: return
        self.__startAngle = start_angle
        self.update()

    @property
    def endAngle(self) -> int: return self.__endAngle

    @endAngle.setter
    def endAngle(self, end_angle: int) -> None:
        if self.__endAngle == end_angle: return
        self.__endAngle = end_angle
        self.update()

    @property
    def animation(self) -> bool: return self.__animation

    @animation.setter
    def animation(self, n_animation: bool) -> None:
        if self.__animation == n_animation: return
        self.__animation = n_animation
        self.update()

    @property
    def animationStep(self) -> float: return self.__animationStep

    @animationStep.setter
    def animationStep(self, animation_step: float) -> None:
        if self.__animationStep == animation_step: return
        self.__animationStep = animation_step
        self.update()

    @property
    def ringWidth(self) -> int: return self.__ringWidth

    @ringWidth.setter
    def ringWidth(self, ring_width: int) -> None:
        if self.__ringWidth == ring_width: return
        self.__ringWidth = ring_width
        self.update()

    @property
    def ringColor(self) -> QColor: return self.__ringColor

    @ringColor.setter
    def ringColor(self, ring_color: QColor) -> None:
        if self.__ringColor == ring_color: return
        self.__ringColor = ring_color
        self.update()

    @property
    def scaleColor(self) -> QColor: return self.__scaleColor

    @scaleColor.setter
    def scaleColor(self, scale_color: QColor) -> None:
        if self.__scaleColor == scale_color: return
        self.__scaleColor = scale_color
        self.update()

    @property
    def pointerColor(self) -> QColor: return self.__pointerColor

    @pointerColor.setter
    def pointerColor(self, pointer_color: QColor) -> None:
        if self.__pointerColor == pointer_color: return
        self.__pointerColor = pointer_color
        self.update()

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def textColor(self) -> QColor: return self.__textColor

    @textColor.setter
    def textColor(self, text_color: QColor) -> None:
        if self.__textColor == text_color: return
        self.__textColor = text_color
        self.update()

    @property
    def unit(self) -> str: return self.__unit

    @unit.setter
    def unit(self, n_unit: str) -> None:
        if self.__unit == n_unit: return
        self.__unit = n_unit
        self.update()

    @property
    def text(self) -> str: return self.__text

    @text.setter
    def text(self, n_text: str) -> None:
        if self.__text == n_text: return
        self.__text = n_text
        self.update()

    def sizeHint(self) -> QSize: return QSize(200, 200)

    def minimumSizeHint(self) -> QSize: return QSize(50, 50)


if __name__ == '__main__':
    import sys
    from typing import List
    from PySide2.QtCore import Qt, QTextCodec
    from PySide2.QtGui import QFont
    from PySide2.QtWidgets import QApplication, QSlider, QGridLayout

    class FrmGaugePanel(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmGaugePanel, self).__init__(parent)
            layout = QGridLayout()

            self.gaugePanel1 = GaugePanel()
            self.gaugePanel2 = GaugePanel()
            self.gaugePanel3 = GaugePanel()
            self.horizontalSlider1 = QSlider(Qt.Horizontal)
            self.horizontalSlider2 = QSlider(Qt.Horizontal)
            self.horizontalSlider3 = QSlider(Qt.Horizontal)
            layout.addWidget(self.gaugePanel1, 0, 0)
            layout.addWidget(self.gaugePanel2, 0, 1)
            layout.addWidget(self.gaugePanel3, 0, 2)
            layout.addWidget(self.horizontalSlider1, 1, 0)
            layout.addWidget(self.horizontalSlider2, 1, 1)
            layout.addWidget(self.horizontalSlider3, 1, 2)

            self.gaugePanel4 = GaugePanel()
            self.gaugePanel5 = GaugePanel()
            self.gaugePanel6 = GaugePanel()
            self.horizontalSlider4 = QSlider(Qt.Horizontal)
            self.horizontalSlider5 = QSlider(Qt.Horizontal)
            self.horizontalSlider6 = QSlider(Qt.Horizontal)
            layout.addWidget(self.gaugePanel4, 2, 0)
            layout.addWidget(self.gaugePanel5, 2, 1)
            layout.addWidget(self.gaugePanel6, 2, 2)
            layout.addWidget(self.horizontalSlider4, 3, 0)
            layout.addWidget(self.horizontalSlider5, 3, 1)
            layout.addWidget(self.horizontalSlider6, 3, 2)
            self.setLayout(layout)
            self.initForm()

        def initForm(self) -> None:
            # 通过设置样式来设置颜色,另类的方法,也可以直接调用函数设置
            self.setStyleSheet("background:#222939;")

            # 设置单位
            self.gaugePanel1.unit = "V"
            self.gaugePanel2.unit = "A"
            self.gaugePanel3.unit = "m"
            self.gaugePanel4.unit = "kW"
            self.gaugePanel5.unit = "kWh"
            self.gaugePanel6.unit = "Hz"

            for gaugePanel in [self.gaugePanel1, self.gaugePanel2, self.gaugePanel3,
                               self.gaugePanel4, self.gaugePanel5, self.gaugePanel6]:
                gaugePanel.ringColor = QColor('#393F4D')
                gaugePanel.scaleColor = QColor('#03B7C9')
                gaugePanel.pointerColor = QColor('#03B7C9')
                gaugePanel.textColor = QColor('#EEEEEE')

            # 设置名称
            self.gaugePanel1.text = "电压"
            self.gaugePanel2.text = "电流"
            self.gaugePanel3.text = "水位"
            self.gaugePanel4.text = "有功功率"
            self.gaugePanel5.text = "有功电能"
            self.gaugePanel6.text = "电网频率"

            # 设置小数点
            self.gaugePanel3.precision = 1
            self.gaugePanel4.precision = 2
            self.gaugePanel5.precision = 1
            self.gaugePanel3.scalePrecision = 1

            # 设置启用动画
            self.gaugePanel4.animation = True
            self.gaugePanel5.animation = True
            self.gaugePanel5.animationStep = 0.2

            # 设置范围值
            self.gaugePanel1.setRange(0, 500)
            self.gaugePanel2.setRange(0, 60)
            self.gaugePanel3.setRange(0, 2)
            self.gaugePanel4.setRange(0, 50)
            self.gaugePanel5.setRange(0, 70)
            self.gaugePanel6.setRange(0, 100)

            self.horizontalSlider1.setRange(0, 500)
            self.horizontalSlider2.setRange(0, 60)
            self.horizontalSlider3.setRange(0, 200)
            self.horizontalSlider4.setRange(0, 50)
            self.horizontalSlider5.setRange(0, 70)
            self.horizontalSlider6.setRange(0, 100)

            # 绑定滑块
            self.horizontalSlider1.valueChanged.connect(self.gaugePanel1.setValue)
            self.horizontalSlider2.valueChanged.connect(self.gaugePanel2.setValue)
            self.horizontalSlider3.valueChanged.connect(self.on_horizontalSlider3_valueChanged)
            self.horizontalSlider4.valueChanged.connect(self.gaugePanel4.setValue)
            self.horizontalSlider5.valueChanged.connect(self.gaugePanel5.setValue)
            self.horizontalSlider6.valueChanged.connect(self.gaugePanel6.setValue)

            # 设置初始值
            self.horizontalSlider1.value = 220
            self.horizontalSlider2.value = 32
            self.horizontalSlider3.value = 150
            self.horizontalSlider4.value = 6.34
            self.horizontalSlider5.value = 6.28
            self.horizontalSlider6.value = 50

        def on_horizontalSlider3_valueChanged(self, value: int) -> None:
            v = value / 100
            self.gaugePanel3.value = v

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmGaugePanel()
    window.resize(500, 300)
    window.setWindowTitle("面板仪表盘")
    window.show()
    sys.exit(app.exec_())
