from enum import Enum

from PySide2.QtCore import QTimer, QSize, Slot, Signal, QEnum, Qt, QRect, QObject
from PySide2.QtGui import QColor, QMouseEvent, QResizeEvent, QPaintEvent, QPainter, QPen, QPainterPath, QRadialGradient
from PySide2.QtWidgets import QWidget

class SwitchButton(QWidget):
    """
    开关按钮控件
    作者:feiyangqingyun(QQ:517216493) 2016-11-6
    译者:sunchuquin(QQ:1715216365) 2021-06-20
    1. 可设置开关按钮的样式 圆角矩形/内圆形/外圆形
    2. 可设置选中和未选中时的背景颜色
    3. 可设置选中和未选中时的滑块颜色
    4. 可设置显示的文本
    5. 可设置滑块离背景的间隔
    6. 可设置圆角角度
    7. 可设置是否显示动画过渡效果
    """

    checkedChanged = Signal(bool)  # checked

    @QEnum
    class ButtonStyle(Enum):
        ButtonStyle_Rect = 0  # 圆角矩形
        ButtonStyle_CircleIn = 1  # 内圆形
        ButtonStyle_CircleOut = 2  # 外圆形

    def __init__(self, parent: QWidget = None, default_state: bool = False):
        super(SwitchButton, self).__init__(parent)
        self.__space: int = 2  # 滑块离背景间隔
        self.__rectRadius: int = 5  # 圆角角度
        self.__checked: bool = default_state  # 是否选中
        self.__showText: bool = True  # 显示文字
        self.__showCircle: bool = False  # 显示小圆
        self.__animation: bool = False  # 动画过渡
    
        self.__buttonStyle: SwitchButton.ButtonStyle = SwitchButton.ButtonStyle.ButtonStyle_CircleIn  # 开关按钮样式
    
        self.__bgColorOff: QColor = QColor(111, 122, 126)  # 关闭时背景颜色
        self.__bgColorOn: QColor = QColor(21, 156, 119)  # 打开时背景颜色
        self.__sliderColorOff: QColor = QColor(255, 255, 255)  # 关闭时滑块颜色
        self.__sliderColorOn: QColor = QColor(255, 255, 255)  # 打开时滑块颜色
        self.__textColorOff: QColor = QColor(250, 250, 250)  # 关闭时文字颜色
        self.__textColorOn: QColor = QColor(255, 255, 255)  # 打开时文字颜色
    
        self.__textOff: str = "关闭"  # 关闭时显示的文字
        self.__textOn: str = "开启"  # 打开时显示的文字
    
        self.__step: int = 0  # 每次移动的步长
        self.__startX: int = 0  # 滑块开始X轴坐标
        self.__endX: int = 0  # 滑块结束X轴坐标
        self.__timer: QTimer = QTimer(self)  # 定时器绘制
        self.__timer.setInterval(30)
        self.__timer.timeout.connect(self.__updateValue)

    @property
    def space(self) -> int: return self.__space

    @space.setter
    def space(self, n_space: int) -> None:
        if self.__space == n_space: return
        self.__space = n_space
        self.update()

    @property
    def rectRadius(self) -> int: return self.__rectRadius

    @rectRadius.setter
    def rectRadius(self, rect_radius: int) -> None:
        if self.__rectRadius == rect_radius: return
        self.__rectRadius = rect_radius
        self.update()

    @property
    def checked(self) -> bool: return self.__checked

    @checked.setter
    def checked(self, n_checked: bool) -> None:
        if self.__checked == n_checked: return
        # 如果刚刚初始化完成的属性改变则延时处理
        if self.__step == 0: QTimer.singleShot(10, self.__change)
        else: self.mousePressEvent(None)

    @property
    def showText(self) -> bool: return self.__showText

    @showText.setter
    def showText(self, show_text: bool) -> None:
        if self.__showText == show_text: return
        self.__showText = show_text
        self.update()

    @property
    def showCircle(self) -> bool: return self.__showCircle

    @showCircle.setter
    def showCircle(self, show_circle: bool) -> None:
        if self.__showCircle == show_circle: return
        self.__showCircle = show_circle
        self.update()

    @property
    def animation(self) -> bool: return self.__animation

    @animation.setter
    def animation(self, n_animation: bool) -> None:
        if self.__animation == n_animation: return
        self.__animation = n_animation
        self.update()

    @property
    def buttonStyle(self) -> ButtonStyle: return self.__buttonStyle

    @buttonStyle.setter
    def buttonStyle(self, button_style: ButtonStyle) -> None:
        if self.__buttonStyle == button_style: return
        self.__buttonStyle = button_style
        self.update()

    @property
    def bgColorOff(self) -> QColor: return self.__bgColorOff

    @bgColorOff.setter
    def bgColorOff(self, bg_color_off: QColor) -> None:
        if self.__bgColorOff == bg_color_off: return
        self.__bgColorOff = bg_color_off
        self.update()

    @property
    def bgColorOn(self) -> QColor: return self.__bgColorOn

    @bgColorOn.setter
    def bgColorOn(self, bg_color_on: QColor) -> None:
        if self.__bgColorOn == bg_color_on: return
        self.__bgColorOn = bg_color_on
        self.update()

    @property
    def sliderColorOff(self) -> QColor: return self.__sliderColorOff

    @sliderColorOff.setter
    def sliderColorOff(self, slider_color_off: QColor) -> None:
        if self.__sliderColorOff == slider_color_off: return
        self.__sliderColorOff = slider_color_off
        self.update()

    @property
    def sliderColorOn(self) -> QColor: return self.__sliderColorOn

    @sliderColorOn.setter
    def sliderColorOn(self, slider_color_on: QColor) -> None:
        if self.__sliderColorOn == slider_color_on: return
        self.__sliderColorOn = slider_color_on
        self.update()

    @property
    def textColorOff(self) -> QColor: return self.__textColorOff

    @textColorOff.setter
    def textColorOff(self, text_color_off: QColor) -> None:
        if self.__textColorOff == text_color_off: return
        self.__textColorOff = text_color_off
        self.update()

    @property
    def textColorOn(self) -> QColor: return self.__textColorOn

    @textColorOn.setter
    def textColorOn(self, text_color_on: QColor) -> None:
        if self.__textColorOn == text_color_on: return
        self.__textColorOn = text_color_on
        self.update()

    @property
    def textOff(self) -> str: return self.__textOff

    @textOff.setter
    def textOff(self, text_off: str) -> None:
        if self.__textOff == text_off: return
        self.__textOff = text_off
        self.update()

    @property
    def textOn(self) -> str: return self.__textOn

    @textOn.setter
    def textOn(self, text_on: str) -> None:
        if self.__textOn == text_on: return
        self.__textOn = text_on
        self.update()

    @Slot()
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__checked = not self.__checked
        self.checkedChanged.emit(self.__checked)

        self.__step = self.width() // 7  # 每次移动的步长

        # 状态切换改变后自动计算终点坐标
        if self.__checked:
            if self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_Rect:
                self.__endX = self.width() - self.width() // 2
            elif self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_CircleIn:
                self.__endX = self.width() - self.height()
            elif self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_CircleOut:
                self.__endX = self.width() - self.height()
        else:
            self.__endX = 0

        if self.__animation:
            self.__timer.start()
        else:
            self.__startX = self.__endX
            self.update()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__step = self.width() // 50  # 每次移动的步长为宽度的 50分之一

        # 尺寸大小改变后自动设置起点坐标为终点
        if self.__checked:
            if self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_Rect:
                self.__startX = self.width() - self.width() // 2
            elif self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_CircleIn:
                self.__startX = self.width() - self.height()
            elif self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_CircleOut:
                self.__startX = self.width() - self.height()
        else:
            self.__startX = 0

        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self.drawBg(painter)  # 绘制背景
        self.drawSlider(painter)  # 绘制滑块

    def drawBg(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)

        bgColor: QColor = self.__bgColorOn if self.__checked else self.__bgColorOff
        if not self.isEnabled():
            bgColor.setAlpha(60)

        painter.setBrush(bgColor)

        if self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_Rect:
            painter.drawRoundedRect(self.rect(), self.__rectRadius, self.__rectRadius)
        elif self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_CircleIn:
            rect: QRect = QRect(0, 0, self.width(), self.height())
            side: int = min(rect.width(), rect.height())  # 半径为高度的一半

            # 左侧圆
            path1: QPainterPath = QPainterPath()
            path1.addEllipse(rect.x(), rect.y(), side, side)
            # 右侧圆
            path2: QPainterPath = QPainterPath()
            path2.addEllipse(rect.width() - side, rect.y(), side, side)
            # 中间矩形
            path3: QPainterPath = QPainterPath()
            path3.addRect(rect.x() + side // 2, rect.y(), rect.width() - side, rect.height())

            path: QPainterPath = QPainterPath()
            path = path3 + path1 + path2
            painter.drawPath(path)
        elif self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_CircleOut:
            rect: QRect = QRect(self.height() // 2,
                                self.__space,
                                self.width() - self.height(),
                                self.height() - self.__space * 2)
            painter.drawRoundedRect(rect, self.__rectRadius, self.__rectRadius)

        if self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_Rect or \
                self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_CircleIn:
            # 绘制文本和小圆,互斥
            if self.__showText:
                sliderWidth: int = min(self.width(), self.height()) - self.__space * 2
                if self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_Rect:
                    sliderWidth = self.width() // 2 - 5
                elif self.__buttonStyle is SwitchButton.ButtonStyle.ButtonStyle_CircleIn:
                    sliderWidth -= 5

                if self.__checked:
                    textRect: QRect = QRect(0, 0, self.width() - sliderWidth, self.height())
                    painter.setPen(self.__textColorOn)
                    painter.drawText(textRect, Qt.AlignCenter, self.__textOn)
                else:
                    textRect: QRect = QRect(sliderWidth, 0, self.width() - sliderWidth, self.height())
                    painter.setPen(self.__textColorOff)
                    painter.drawText(textRect, Qt.AlignCenter, self.__textOff)
            elif self.__showCircle:
                side: int = min(self.width(), self.height()) // 2
                y: int = (self.height() - side) // 2

                if self.__checked:
                    circleRect: QRect = QRect(side // 2, y, side, side)
                    pen: QPen = QPen(self.__textColorOn, 2)
                    painter.setPen(pen)
                    painter.setBrush(Qt.NoBrush)
                    painter.drawEllipse(circleRect)
                else:
                    circleRect: QRect = QRect(int(self.width() - (side * 1.5)), y, side, side)
                    pen: QPen = QPen(self.__textColorOff, 2)
                    painter.setPen(pen)
                    painter.setBrush(Qt.NoBrush)
                    painter.drawEllipse(circleRect)

        painter.restore()

    def drawSlider(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)

        if not self.__checked:
            painter.setBrush(self.__sliderColorOff)
        else:
            painter.setBrush(self.__sliderColorOn)

        if self.__buttonStyle == SwitchButton.ButtonStyle.ButtonStyle_Rect:
            sliderWidth: int = self.width() // 2 - self.__space * 2
            sliderHeight: int = self.height() - self.__space * 2
            sliderRect: QRect = QRect(self.__startX + self.__space, self.__space, sliderWidth , sliderHeight)
            painter.drawRoundedRect(sliderRect, self.__rectRadius, self.__rectRadius)
        elif self.__buttonStyle == SwitchButton.ButtonStyle.ButtonStyle_CircleIn:
            rect: QRect = QRect(0, 0, self.width(), self.height())
            sliderWidth: int = min(rect.width(), rect.height()) - self.__space * 2
            sliderRect: QRect = QRect(self.__startX + self.__space, self.__space, sliderWidth, sliderWidth)
            painter.drawEllipse(sliderRect)
        elif self.__buttonStyle == SwitchButton.ButtonStyle.ButtonStyle_CircleOut:
            sliderWidth: int = self.height()
            sliderRect: QRect = QRect(self.__startX, 0, sliderWidth, sliderWidth)

            color1: QColor = Qt.white if self.__checked else self.__bgColorOff
            color2: QColor = self.__sliderColorOn if self.__checked else self.__sliderColorOff

            radialGradient: QRadialGradient = QRadialGradient(sliderRect.center(), sliderWidth // 2)
            radialGradient.setColorAt(0, color1 if self.__checked else color2)
            radialGradient.setColorAt(0.5, color1 if self.__checked else color2)
            radialGradient.setColorAt(0.6, color2 if self.__checked else color1)
            radialGradient.setColorAt(1.0, color2 if self.__checked else color1)
            painter.setBrush(radialGradient)

            painter.drawEllipse(sliderRect)

        painter.restore()

    def sizeHint(self) -> QSize: return QSize(70, 30)
    def minimumSizeHint(self) -> QSize: return QSize(10, 5)

    @Slot()
    def __change(self) -> None:
        self.mousePressEvent(None)

    @Slot()
    def __updateValue(self) -> None:
        if self.__checked:
            if self.__startX < self.__endX:
                self.__startX = self.__startX + self.__step
            else:
                self.__startX = self.__endX
                self.__timer.stop()
        else:
            if self.__startX > self.__endX:
                self.__startX = self.__startX - self.__step
            else:
                self.__startX = self.__endX
                self.__timer.stop()

        self.update()


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication, QGridLayout

    class FrmSwitchButton(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmSwitchButton, self).__init__(parent)
            self.color1 = QColor(34, 163, 169)
            self.color2 = QColor(162, 121, 197)
            self.color3 = QColor(255, 107, 107)
            self.color4 = QColor(72, 103, 149)

            self.switchButton11 = SwitchButton()
            self.switchButton12 = SwitchButton(default_state=True)
            self.switchButton13 = SwitchButton()
            self.switchButton14 = SwitchButton(default_state=True)

            self.switchButton21 = SwitchButton()
            self.switchButton22 = SwitchButton(default_state=True)
            self.switchButton23 = SwitchButton()
            self.switchButton24 = SwitchButton(default_state=True)

            self.switchButton31 = SwitchButton()
            self.switchButton32 = SwitchButton(default_state=True)
            self.switchButton33 = SwitchButton()
            self.switchButton34 = SwitchButton(default_state=True)
            self.initForm()

            layout = QGridLayout()
            layout.addWidget(self.switchButton11, 0, 0)
            self.setLayout(layout)
            layout.addWidget(self.switchButton12, 1, 0)
            layout.addWidget(self.switchButton13, 2, 0)
            layout.addWidget(self.switchButton14, 3, 0)

            layout.addWidget(self.switchButton21, 0, 1)
            layout.addWidget(self.switchButton22, 1, 1)
            layout.addWidget(self.switchButton23, 2, 1)
            layout.addWidget(self.switchButton24, 3, 1)

            layout.addWidget(self.switchButton31, 0, 2)
            layout.addWidget(self.switchButton32, 1, 2)
            layout.addWidget(self.switchButton33, 2, 2)
            layout.addWidget(self.switchButton34, 3, 2)

        def checkedChanged(self, checked: bool):
            print(self.sender(), checked)

        def initForm(self):
            def initBtn1():
                nonlocal self
                self.switchButton11.bgColorOn = self.color1
                self.switchButton12.bgColorOn = self.color2
                self.switchButton13.bgColorOn = self.color3
                self.switchButton14.bgColorOn = self.color4

                self.switchButton11.showText = False
                self.switchButton12.showText = False
                self.switchButton13.showText = True
                self.switchButton14.showText = True
                self.switchButton12.showCircle = True
                self.switchButton14.animation = True

                self.switchButton13.textOff = "停止"
                self.switchButton13.textOn = "启动"
                self.switchButton14.textOff = "禁用"
                self.switchButton14.textOn = "启用"

            def initBtn2():
                self.switchButton21.buttonStyle = SwitchButton.ButtonStyle.ButtonStyle_Rect
                self.switchButton22.buttonStyle = SwitchButton.ButtonStyle.ButtonStyle_Rect
                self.switchButton23.buttonStyle = SwitchButton.ButtonStyle.ButtonStyle_Rect
                self.switchButton24.buttonStyle = SwitchButton.ButtonStyle.ButtonStyle_Rect

                self.switchButton21.bgColorOn = self.color1
                self.switchButton22.bgColorOn = self.color2
                self.switchButton23.bgColorOn = self.color3
                self.switchButton24.bgColorOn = self.color4

                self.switchButton21.showText = False
                self.switchButton22.showText = False
                self.switchButton23.showText = True
                self.switchButton24.showText = True
                self.switchButton22.showCircle = True
                self.switchButton24.animation = True

                self.switchButton23.textOff = "停止"
                self.switchButton23.textOn = "启动"
                self.switchButton24.textOff = "禁用"
                self.switchButton24.textOn = "启用"

            def initBtn3():
                self.switchButton31.buttonStyle = SwitchButton.ButtonStyle.ButtonStyle_CircleOut
                self.switchButton32.buttonStyle = SwitchButton.ButtonStyle.ButtonStyle_CircleOut
                self.switchButton33.buttonStyle = SwitchButton.ButtonStyle.ButtonStyle_CircleOut
                self.switchButton34.buttonStyle = SwitchButton.ButtonStyle.ButtonStyle_CircleOut

                g_space: int = 8
                self.switchButton31.space = g_space
                self.switchButton32.space = g_space
                self.switchButton33.space = g_space
                self.switchButton34.space = g_space

                g_radius: int = 8
                self.switchButton31.rectRadius = g_radius
                self.switchButton32.rectRadius = g_radius
                self.switchButton33.rectRadius = g_radius
                self.switchButton34.rectRadius = g_radius

                self.switchButton31.bgColorOn = self.color1
                self.switchButton32.bgColorOn = self.color2
                self.switchButton33.bgColorOn = self.color3
                self.switchButton34.bgColorOn = self.color4

                self.switchButton31.sliderColorOn = self.color1
                self.switchButton32.sliderColorOn = self.color2
                self.switchButton33.sliderColorOn = self.color3
                self.switchButton34.sliderColorOn = self.color4

                self.switchButton31.showText = False
                self.switchButton32.showText = False
                self.switchButton33.showText = True
                self.switchButton34.showText = True
                self.switchButton34.animation = True

            def initSlot():
                for btn in [
                    self.switchButton11, self.switchButton12, self.switchButton13, self.switchButton14,
                    self.switchButton21, self.switchButton22, self.switchButton23, self.switchButton24,
                    self.switchButton31, self.switchButton32, self.switchButton33, self.switchButton34
                ]:
                    btn.checkedChanged.connect(self.checkedChanged)

            initBtn1()
            initBtn2()
            initBtn3()
            initSlot()

    app = QApplication()
    window = FrmSwitchButton()
    window.show()
    sys.exit(app.exec_())
