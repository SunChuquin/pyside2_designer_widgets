import random
import math
from enum import Enum

from PySide2.QtCore import QEnum, QEvent, QPropertyAnimation, QPointF, Signal, QTime, Qt, QRectF, QSize, QPoint
from PySide2.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QLinearGradient, QPolygon, QPen, QFont
from PySide2.QtWidgets import QWidget


class GaugeProgress(QWidget):
    """
    进度条仪表盘控件
    作者:feiyangqingyun(QQ:517216493) 2016-12-03
    译者:sunchuquin(QQ:1715216365) 2021-07-04
    1. 支持指示器样式选择 圆形指示器/指针指示器/圆角指针指示器/三角形指示器
    2. 支持鼠标按下旋转改变值
    3. 支持负数范围值
    4. 支持设置当前值及范围值
    5. 支持设置起始旋转角度和结束旋转角度
    6. 支持设置背景色/进度颜色/中间圆渐变颜色
    7. 随窗体拉伸自动变化
    8. 支持鼠标进入和离开动画效果
    9. 可设置是否显示当前值
    10. 可设置是否显示指示器
    """

    @QEnum
    class PointerStyle(Enum):
        PointerStyle_Circle = 0  # 圆形指示器
        PointerStyle_Indicator = 1  # 指针指示器
        PointerStyle_IndicatorR = 2  # 圆角指针指示器
        PointerStyle_Triangle = 3  # 三角形指示器

    valueChanged = Signal(int)  # value

    def __init__(self, parent: QWidget = None):
        super(GaugeProgress, self).__init__(parent)
        self.__minValue: float = 0  # 最小值
        self.__maxValue: float = 100  # 最大值
        self.__value: float = 0  # 目标值
        self.__precision: int = 0  # 精确度,小数点后几位

        self.__startAngle: int = 0  # 开始旋转角度
        self.__endAngle: int = 0  # 结束旋转角度

        self.__bgColor: QColor = QColor(30, 30, 30)  # 背景色
        self.__progressColor: QColor = QColor(100, 184, 255)  # 当前进度颜色
        self.__progressBgColor: QColor = QColor(50, 50, 50)  # 进度背景颜色
        self.__circleColorStart: QColor = QColor(80, 80, 80)  # 中间圆渐变开始颜色
        self.__circleColorEnd: QColor = QColor(50, 50, 50)  # 中间圆渐变结束颜色
        self.__textColor: QColor = QColor(200, 200, 200)  # 文字颜色

        self.__showPointer: bool = True  # 是否显示指示器
        self.__showValue: bool = False  # 是否显示当前值
        self.__pointerStyle: GaugeProgress.PointerStyle = GaugeProgress.PointerStyle.PointerStyle_Circle  # 指针样式

        self.__hover: bool = False  # 是否鼠标悬停
        self.__radiusCoverCircle: int = 85  # 覆盖圆半径
        self.__radiusCircle: int = 80  # 中间圆半径
        self.__animation: QPropertyAnimation = QPropertyAnimation(self, b'')  # 动画对象

        self.__pressed: bool = False  # 鼠标是否按下

        self.__animation.setStartValue(0)
        self.__animation.setEndValue(10)
        self.__animation.setDuration(300)
        self.__animation.valueChanged.connect(self.updateRadius)

        self.setFont(QFont("Arial", 9))

    def enterEvent(self, event: QEvent) -> None:
        self.__hover = True
        self.__animation.stop()
        self.__animation.start()

    def leaveEvent(self, event: QEvent) -> None:
        self.__hover = False
        self.__animation.stop()
        self.__animation.start()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__pressed = True
        self.setPressedValue(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.__pressed = False

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.__pressed: return
        self.setPressedValue(event.pos())

    def paintEvent(self, event: QPaintEvent) -> None:
        width: int = self.width()
        height: int = self.height()
        side: int = min(width, height)

        # 绘制准备工作,启用反锯齿,平移坐标轴中心,等比例缩放
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.translate(width / 2, height / 2)
        painter.scale(side / 200.0, side / 200.0)

        self.drawBg(painter)  # 绘制背景
        self.drawColorPie(painter)  # 绘制饼圆
        self.drawCoverCircle(painter)  # 绘制覆盖圆 用以遮住饼圆多余部分
        self.drawCircle(painter)  # 绘制中心圆

        # 根据指示器形状绘制指示器
        if self.__pointerStyle == GaugeProgress.PointerStyle.PointerStyle_Circle:
            self.drawPointerCircle(painter)
        elif self.__pointerStyle == GaugeProgress.PointerStyle.PointerStyle_Indicator:
            self.drawPointerIndicator(painter)
        elif self.__pointerStyle == GaugeProgress.PointerStyle.PointerStyle_IndicatorR:
            self.drawPointerIndicatorR(painter)
        elif self.__pointerStyle == GaugeProgress.PointerStyle.PointerStyle_Triangle:
            self.drawPointerTriangle(painter)

        self.drawValue(painter)  # 绘制当前值

    def drawBg(self, painter: QPainter) -> None:
        radius: int = 99
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__bgColor)
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        painter.restore()

    def drawColorPie(self, painter: QPainter) -> None:
        radius: int = 95
        painter.save()
        painter.setPen(Qt.NoPen)

        rect: QRectF = QRectF(-radius, -radius, radius * 2, radius * 2)

        # 计算总范围角度,当前值范围角度,剩余值范围角度
        angleAll: float = 360.0 - self.__startAngle - self.__endAngle
        angleCurrent: float = angleAll * ((self.__value - self.__minValue) / (self.__maxValue - self.__minValue))
        angleOther: float = angleAll - angleCurrent

        # 绘制当前值饼圆
        painter.setBrush(self.__progressColor)
        painter.drawPie(rect, (270 - self.__startAngle - angleCurrent) * 16, angleCurrent * 16)

        # 绘制剩余值饼圆
        painter.setBrush(self.__progressBgColor)
        painter.drawPie(rect, (270 - self.__startAngle - angleCurrent - angleOther) * 16, angleOther * 16)

        painter.restore()

    def drawCoverCircle(self, painter: QPainter) -> None:
        radius: int = self.__radiusCoverCircle
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__bgColor)
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        painter.restore()

    def drawCircle(self, painter: QPainter) -> None:
        radius: int = self.__radiusCircle
        painter.save()
        painter.setPen(Qt.NoPen)
        bgGradient: QLinearGradient = QLinearGradient(0, -radius, 0, radius)
        bgGradient.setColorAt(0.0, self.__circleColorStart)
        bgGradient.setColorAt(1.0, self.__circleColorEnd)
        painter.setBrush(bgGradient)

        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        painter.restore()

    def drawPointerCircle(self, painter: QPainter) -> None:
        if not self.__showPointer: return

        radius: int = 15
        offset: int = self.__radiusCircle - 60
        painter.save()
        painter.setPen(Qt.NoPen)

        painter.rotate(self.__startAngle)
        degRotate: float = (360.0 - self.__startAngle - self.__endAngle) / (self.__maxValue - self.__minValue) * (self.__value - self.__minValue)
        painter.rotate(degRotate)

        painter.setBrush(self.__progressColor)
        painter.drawEllipse(-radius, radius + offset, radius * 2, radius * 2)

        painter.restore()

    def drawPointerIndicator(self, painter: QPainter) -> None:
        if not self.__showPointer: return

        radius: int = self.__radiusCircle - 15
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__progressColor)

        pts: QPolygon = QPolygon()
        pts.append(QPoint(-8, 0))
        pts.append(QPoint(8, 0))
        pts.append(QPoint(0, radius))

        painter.rotate(self.__startAngle)
        degRotate: float = (360.0 - self.__startAngle - self.__endAngle) / (self.__maxValue - self.__minValue) * (self.__value - self.__minValue)
        painter.rotate(degRotate)
        painter.drawConvexPolygon(pts)

        # 绘制中心圆点
        radius = radius // 4
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)

        painter.restore()

    def drawPointerIndicatorR(self, painter: QPainter) -> None:
        if not self.__showPointer: return

        radius: int = self.__radiusCircle - 15
        painter.save()

        pen: QPen = QPen()
        pen.setWidth(1)
        pen.setColor(self.__progressColor)
        painter.setPen(pen)
        painter.setBrush(self.__progressColor)

        pts: QPolygon = QPolygon()
        pts.append(QPoint(-8, 0))
        pts.append(QPoint(8, 0))
        pts.append(QPoint(0, radius))

        painter.rotate(self.__startAngle)
        degRotate: float = (360.0 - self.__startAngle - self.__endAngle) / (self.__maxValue - self.__minValue) * (self.__value - self.__minValue)
        painter.rotate(degRotate)
        painter.drawConvexPolygon(pts)

        # 增加绘制圆角直线,与之前三角形重叠,形成圆角指针
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidthF(4)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, radius)

        # 绘制中心圆点
        radius = radius // 4
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)

        painter.restore()

    def drawPointerTriangle(self, painter: QPainter) -> None:
        if not self.__showPointer: return

        radius: int = 20
        offset: int = self.__radiusCircle - 25
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__progressColor)

        pts: QPolygon = QPolygon()
        pts.append(QPoint(-radius // 2, offset))
        pts.append(QPoint(radius // 2, offset))
        pts.append(QPoint(0, radius + offset))

        painter.rotate(self.__startAngle)
        degRotate: float = (360.0 - self.__startAngle - self.__endAngle) / (self.__maxValue - self.__minValue) * (self.__value - self.__minValue)
        painter.rotate(degRotate)
        painter.drawConvexPolygon(pts)

        painter.restore()

    def drawValue(self, painter: QPainter) -> None:
        if not self.__showValue: return

        radius: int = 100
        painter.save()
        painter.setPen(self.__textColor)

        font: QFont = QFont()
        font.setPixelSize(radius - 50 if self.__showPointer else radius - 15)
        font.setBold(True)
        painter.setFont(font)

        textRect: QRectF = QRectF(-radius, -radius, radius * 2, radius * 2)
        value = round(self.__value, self.__precision)
        strValue: str = str(int(value)) if self.__precision is 0 else str(value)
        painter.drawText(textRect, Qt.AlignCenter, strValue)
        painter.restore()

    def setEasingCurve(self) -> None:
        # 随机选择一种动画效果
        index: int = random.randint(0, 40)
        self.__animation.setEasingCurve(index)

    def updateRadius(self, radius) -> None:
        # 如果鼠标悬停则逐渐变小,鼠标移开则逐渐变大直到恢复
        step: int = int(radius)

        if self.__hover:
            self.__radiusCoverCircle = 85 - step
            self.__radiusCircle = 80 - step
        else:
            self.__radiusCoverCircle = 75 + step
            self.__radiusCircle = 70 + step

        self.update()

    def setPressedValue(self, pressed_point: QPointF) -> None:
        """ 根据鼠标按下的坐标设置当前按下坐标处的值 """
        # 计算总角度
        length: float = 360 - self.__startAngle - self.__endAngle

        # 计算最近的刻度
        point: QPointF = pressed_point - self.rect().center()
        theta: float = -math.atan2(-point.x(), -point.y()) * 180 / math.pi
        theta = theta + length / 2

        # 计算每一个角度对应值移动多少
        increment: float = (self.__maxValue - self.__minValue) / length
        currentValue: float = (theta * increment) + self.__minValue

        # 过滤圆弧外的值
        if currentValue <= self.__minValue:
            currentValue = self.__minValue
        elif currentValue >= self.__maxValue:
            currentValue = self.__maxValue

        self.setValue(round(currentValue, 0))

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

    @value.setter
    def value(self, n_value) -> None:
        # 值和当前值一致则无需处理
        if n_value == self.__value: return

        # 值小于最小值则取最小值,大于最大值则取最大值
        if n_value < self.__minValue: n_value = self.__minValue
        elif n_value > self.__maxValue: n_value = self.__maxValue

        self.__value = n_value
        self.update()
        self.valueChanged.emit(n_value)

    def setValue(self, value) -> None:
        self.value = value

    @property
    def precision(self) -> int: return self.__precision

    @precision.setter
    def precision(self, n_precision: int) -> None:
        # 最大精确度为 3
        if 3 >= n_precision != self.__precision:
            self.__precision = n_precision
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
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def progressColor(self) -> QColor: return self.__progressColor

    @progressColor.setter
    def progressColor(self, progress_color: QColor) -> None:
        if self.__progressColor == progress_color: return
        self.__progressColor = progress_color
        self.update()

    @property
    def progressBgColor(self) -> QColor: return self.__progressBgColor

    @progressBgColor.setter
    def progressBgColor(self, progress_bg_color: QColor) -> None:
        if self.__progressBgColor == progress_bg_color: return
        self.__progressBgColor = progress_bg_color
        self.update()

    @property
    def circleColorStart(self) -> QColor: return self.__circleColorStart

    @circleColorStart.setter
    def circleColorStart(self, circle_color_start: QColor) -> None:
        if self.__circleColorStart == circle_color_start: return
        self.__circleColorStart = circle_color_start
        self.update()

    @property
    def circleColorEnd(self) -> QColor: return self.__circleColorEnd

    @circleColorEnd.setter
    def circleColorEnd(self, circle_color_end: QColor) -> None:
        if self.__circleColorEnd == circle_color_end: return
        self.__circleColorEnd = circle_color_end
        self.update()

    @property
    def textColor(self) -> QColor: return self.__textColor

    @textColor.setter
    def textColor(self, text_color: QColor) -> None:
        if self.__textColor == text_color: return
        self.__textColor = text_color
        self.update()

    @property
    def showPointer(self) -> bool: return self.__showPointer

    @showPointer.setter
    def showPointer(self, show_pointer: bool) -> None:
        if self.__showPointer == show_pointer: return
        self.__showPointer = show_pointer
        self.update()

    @property
    def showValue(self) -> bool: return self.__showValue

    @showValue.setter
    def showValue(self, show_value: bool) -> None:
        if self.__showValue == show_value: return
        self.__showValue = show_value
        self.update()

    @property
    def pointerStyle(self) -> PointerStyle: return self.__pointerStyle

    @pointerStyle.setter
    def pointerStyle(self, pointer_style: PointerStyle) -> None:
        if self.__pointerStyle == pointer_style: return
        self.__pointerStyle = pointer_style
        self.update()

    def sizeHint(self) -> QSize: return QSize(200, 200)

    def minimumSizeHint(self) -> QSize: return QSize(20, 20)

    def setRange(self, min_value: float, max_value: float) -> None:
        # 如果最小值大于或者等于最大值则不设置
        if min_value >= max_value: return

        self.__minValue = min_value
        self.__maxValue = max_value

        # 如果目标值不在范围值内,则重新设置目标值
        # 值小于最小值则取最小值,大于最大值则取最大值
        if self.__value < min_value: self.setValue(min_value)
        elif self.__value > max_value: self.setValue(max_value)

        self.update()


if __name__ == '__main__':
    import sys
    from typing import List
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QCheckBox, QComboBox, QGridLayout, QHBoxLayout, QSlider

    class FrmGaugeProgress(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmGaugeProgress, self).__init__(parent)

            self.gauges: List[GaugeProgress] = []

            layout = QHBoxLayout()
            self.cboxPointerStyle = QComboBox()
            self.cboxPointerStyle.clear()
            self.cboxPointerStyle.addItems(['圆形指示器', '指针指示器', '圆角指针指示器', '三角指示器'])
            self.ckShowPointer = QCheckBox('显示指针')
            self.ckShowValue = QCheckBox('显示值')
            self.horizontalSlider = QSlider(Qt.Horizontal)
            self.horizontalSlider.setMaximum(100)
            layout.addWidget(self.ckShowPointer)
            layout.addWidget(self.ckShowValue)
            layout.addWidget(self.cboxPointerStyle)
            layout.addWidget(self.horizontalSlider)

            layout2 = QGridLayout()
            self.gaugeProgress1 = GaugeProgress()
            self.gaugeProgress2 = GaugeProgress()
            self.gaugeProgress3 = GaugeProgress()
            self.gaugeProgress4 = GaugeProgress()
            self.gaugeProgress5 = GaugeProgress()
            self.gaugeProgress6 = GaugeProgress()
            layout2.addWidget(self.gaugeProgress1, 0, 0)
            layout2.addWidget(self.gaugeProgress2, 0, 1)
            layout2.addWidget(self.gaugeProgress3, 0, 2)
            layout2.addWidget(self.gaugeProgress4, 1, 0)
            layout2.addWidget(self.gaugeProgress5, 1, 1)
            layout2.addWidget(self.gaugeProgress6, 1, 2)

            layout3 = QVBoxLayout()
            layout3.addLayout(layout2)
            layout3.addLayout(layout)
            self.setLayout(layout3)
            self.initForm()

            self.ckShowPointer.stateChanged.connect(self.on_ckShowPointer_stateChanged)
            self.ckShowValue.stateChanged.connect(self.on_ckShowValue_stateChanged)
            self.cboxPointerStyle.currentIndexChanged.connect(self.on_cboxPointerStyle_currentIndexChanged)

        def initForm(self) -> None:
            self.ckShowPointer.setChecked(True)
            self.gauges.append(self.gaugeProgress1)
            self.gauges.append(self.gaugeProgress2)
            self.gauges.append(self.gaugeProgress3)
            self.gauges.append(self.gaugeProgress4)
            self.gauges.append(self.gaugeProgress5)
            self.gauges.append(self.gaugeProgress6)

            colors: List[QColor] = [
                QColor("#47A4E9"),
                QColor("#00B17D"),
                QColor("#D64D54"),
                QColor("#DEAF39"),
                QColor("#A279C5"),
                QColor("#009679")
            ]

            count: int = len(self.gauges)
            for i in range(count):
                self.gauges[i].progressColor = colors[i]
                self.horizontalSlider.valueChanged.connect(self.gauges[i].setValue)

            self.horizontalSlider.setValue(88)

        def on_ckShowPointer_stateChanged(self, arg1: int) -> None:
            check: bool = arg1 != 0
            count: int = len(self.gauges)
            for i in range(count):
                self.gauges[i].showPointer = check

        def on_ckShowValue_stateChanged(self, arg1: int) -> None:
            check: bool = arg1 != 0
            count: int = len(self.gauges)
            for i in range(count):
                self.gauges[i].showValue = check

        def on_cboxPointerStyle_currentIndexChanged(self, index: int) -> None:
            style: GaugeProgress.PointerStyle = GaugeProgress.PointerStyle(index)
            count: int = len(self.gauges)
            for i in range(count):
                self.gauges[i].pointerStyle = style

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmGaugeProgress()
    window.resize(500, 300)
    window.setWindowTitle("进度条仪表盘")
    window.show()
    sys.exit(app.exec_())
