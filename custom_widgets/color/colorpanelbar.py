from PySide2.QtCore import QRect, QSize, Signal, Qt, QPoint, QPointF
from PySide2.QtGui import QColor, QShowEvent, QResizeEvent, QMouseEvent, QPaintEvent, QPainter, QPixmap, \
    QLinearGradient, QPen, QFont
from PySide2.QtWidgets import QWidget


class ColorPanelBar(QWidget):

    """
    颜色面板柱状条
    作者:feiyangqingyun(QQ:517216493) 2017-11-21
    译者:sunchuquin(QQ:1715216365) 2021-07-03
    1. 可设置边框宽度/圆角角度/颜色
    2. 可设置百分比选取框高度/边框宽度/圆角角度/颜色
    3. 可设置上部分颜色/下部分颜色/禁用状态下背景颜色
    4. 可设置是否遮住上部分/遮住颜色
    5. 可设置显示为HSB模式
    6. 可设置是否显示当前值或者当前值百分比
    7. 可设置上下高度对应的范围值
    8. 可设置初始值及初始百分比
    """

    colorChanged = Signal(QColor, float, float)  # color, value, percent

    def __init__(self, parent: QWidget = None):
        super(ColorPanelBar, self).__init__(parent)
        self.__borderWidth: int = 2  # 边框宽度
        self.__borderRadius: int = 0  # 边框圆角
        self.__borderColor: QColor = QColor(255, 0, 0)  # 边框颜色

        self.__autoHeight: bool = True  # 自动高度
        self.__percentHeight: int = 25  # 百分比选中框的高度
        self.__percentBorder: int = 2  # 百分比选中框的边框宽度
        self.__percentRadius: int = 0  # 百分比选中框的边框圆角
        self.__percentColor: QColor = QColor(240, 240, 240)  # 百分比选中框的颜色

        self.__topColor: QColor = QColor(255, 0, 0)  # 顶部颜色
        self.__bottomColor: QColor = QColor(0, 0, 0)  # 底部颜色
        self.__disableColor: QColor = QColor(50, 50, 50)  # 禁用状态下背景颜色

        self.__showOverlay: bool = False  # 是否遮住上部分
        self.__overlayColor: QColor = QColor(30, 30, 30)  # 遮住颜色

        self.__staticMode: bool = True  # 静态颜色模式
        self.__outMode: bool = False  # 突出模式
        self.__hsbMode: bool = False  # 显示HSB颜色
        self.__showValue: bool = False  # 显示当前值

        self.__minValue: float = 0.0  # 最小值
        self.__maxValue: float = 360.0  # 最大值
        self.__value: float = 360.0  # 当前值
        self.__percent: float = self.__value / (self.__maxValue - self.__minValue) * 100  # 当前百分比
        self.__color: QColor = self.__topColor  # 当前颜色

        self.__rightHeight: int = 0  # 右侧百分比移动区域的高度
        self.__isPressed: bool = False  # 鼠标是否按下

        self.__bgPix: QPixmap = QPixmap()  # 背景颜色图片
        self.__bgRect: QRect = QRect()  # 背景色区域
        self.__overlayRect: QRect = QRect()  # 遮住部分区域

    def showEvent(self, event: QShowEvent = None) -> None:
        # 首次显示记住当前背景截图,用于获取颜色值
        self.__bgPix = QPixmap(self.width(), self.height())
        self.__bgPix.fill(Qt.transparent)
        painter: QPainter = QPainter()
        painter.begin(self.__bgPix)

        linearGradient: QLinearGradient = QLinearGradient()

        if self.__hsbMode:
            # 起始坐标和结束坐标换个位置可改变颜色顺序
            linearGradient.setStart(QPoint(self.__bgRect.x(), self.__bgRect.height()))
            linearGradient.setFinalStop(QPoint(self.__bgRect.x(), self.__bgRect.y()))

            # 由下往上,饱和度百分值由0增加到1.0
            for i in [i * 0.0625 for i in range(17)]:
                linearGradient.setColorAt(i, QColor.fromHsvF(i, 1, 1, 1))
        else:
            linearGradient.setStart(QPointF(0, 0))
            linearGradient.setFinalStop(QPointF(0, self.height()))
            linearGradient.setColorAt(0.0, self.__topColor)
            linearGradient.setColorAt(1.0, self.__bottomColor)

        painter.setPen(Qt.NoPen)
        painter.setBrush(linearGradient)

        rect: QRect = QRect(self.__borderWidth // 2,
                            self.__borderWidth // 2,
                            self.width() - self.__borderWidth,
                            self.height() - self.__borderWidth)
        painter.drawRect(rect)
        painter.end()

        self.initColor()

    def resizeEvent(self, event: QResizeEvent = None) -> None:
        if self.__autoHeight:
            self.__percentHeight = self.height() / 13

        self.__rightHeight = self.height() - self.__percentHeight - self.__borderWidth * 2 - self.__percentBorder * 2
        if self.__outMode:
            self.__bgRect = QRect(self.__borderWidth // 2,
                                  int(self.__borderWidth / 2 + self.__percentHeight / 2),
                                  self.width() - self.__borderWidth,
                                  int(self.height() - self.__borderWidth - self.__percentHeight))
        else:
            self.__bgRect = QRect(self.__borderWidth // 2,
                                  self.__borderWidth // 2,
                                  self.width() - self.__borderWidth,
                                  self.height() - self.__borderWidth)

        self.showEvent()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__isPressed = True
        self.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.__isPressed = False
        self.mouseMoveEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        y: int = event.pos().y()

        # Y轴必须是在高度范围内
        topY: int = (y - self.__percentHeight // 2)
        if 0 <= topY <= self.__rightHeight and y < self.height():
            # 自动计算纵坐标,转换成当前百分比
            self.__percent = (1 - ((y - self.__percentHeight / 2) / self.__rightHeight)) * 100
            # 计算当前百分比对应的当前值
            self.__value = self.__percent / 100 * (self.__maxValue - self.__minValue)
            # 计算当前背景图片对应百分比处中心点像素
            self.initColor()
        elif topY <= 0:
            self.__value = self.__maxValue
            self.__percent = 100.0
            self.__color = self.__topColor
        elif topY >= self.__rightHeight:
            self.__value = self.__minValue
            self.__percent = 0.0
            self.__color = self.__bottomColor

        self.update()
        self.colorChanged.emit(self.__color, self.__value, self.__percent)

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景颜色
        self.drawBg(painter)
        # 绘制遮住颜色
        self.drawOverlay(painter)
        # 绘制百分比选中框
        self.drawPercent(painter)

    def drawBg(self, painter: QPainter) -> None:
        painter.save()

        # 不可用背景灰色
        if self.isEnabled():
            linearGradient: QLinearGradient = QLinearGradient()

            if self.__hsbMode:
                # 起始坐标和结束坐标换个位置可改变颜色顺序
                linearGradient.setStart(QPoint(self.__bgRect.x(), self.__bgRect.height()))
                linearGradient.setFinalStop(QPoint(self.__bgRect.x(), self.__bgRect.y()))

                # 由下往上,饱和度百分值由0增加到1.0
                for i in [i * 0.0625 for i in range(17)]:
                    linearGradient.setColorAt(i, QColor.fromHsvF(i, 1, 1, 1))

                painter.setPen(Qt.NoPen)
            else:
                linearGradient.setStart(QPointF(0, 0))
                linearGradient.setFinalStop(QPointF(0, self.height()))
                linearGradient.setColorAt(0.0, self.__topColor)
                linearGradient.setColorAt(1.0, self.__bottomColor)

                pen: QPen = QPen()
                pen.setWidthF(self.__borderWidth)
                pen.setColor(self.__borderColor)
                pen.setCapStyle(Qt.RoundCap)
                pen.setJoinStyle(Qt.RoundJoin)
                painter.setPen(pen)

            painter.setBrush(linearGradient)
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.__disableColor)

        painter.drawRoundedRect(self.__bgRect, self.__borderRadius, self.__borderRadius)

        painter.restore()

    def drawOverlay(self, painter: QPainter) -> None:
        # 如果没有启用绘制遮住颜色或者当前不可用则不用绘制
        if not self.__showOverlay or not self.isEnabled():
            return

        painter.save()

        # 根据当前百分比计算高度
        width: int = self.__bgRect.width() - self.__borderWidth
        height: int = self.__bgRect.height() - self.__borderWidth
        height = height - (self.__percent / 100) * self.__height

        if self.__outMode:
            overlayRect = QRect(self.__borderWidth,
                                self.__borderWidth + self.__percentHeight // 2,
                                width,
                                height)
        else:
            overlayRect = QRect(self.__borderWidth,
                                self.__borderWidth,
                                width,
                                height)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__overlayColor)
        painter.drawRect(overlayRect)

        painter.restore()

    def drawPercent(self, painter: QPainter) -> None:
        painter.save()

        # 百分比选择框的区域要小于边框宽度,同时偏移一点,是的看起来美观
        offset: int = self.__borderWidth + 2
        y: int = int(self.__rightHeight * (1 - self.__percent / 100))

        # 禁用状态颜色要变暗
        pen: QPen = QPen()
        pen.setWidthF(self.__percentBorder)
        pen.setColor(self.__percentColor if self.isEnabled() else self.__disableColor.name())

        painter.setPen(pen)
        painter.setBrush(QColor(0, 0, 0, 50))

        rect: QRect = QRect(offset, y + offset, self.width() - offset * 2, self.__percentHeight)
        painter.drawRoundedRect(rect, self.__percentRadius, self.__percentRadius)

        textFont: QFont = QFont()
        textFont.setPixelSize(rect.width() // 3)
        painter.setFont(textFont)

        if self.__showValue:
            painter.drawText(rect, Qt.AlignCenter, '%d' % round(self.__value))
        else:
            painter.drawText(rect, Qt.AlignCenter, '%d%%' % round(self.__percent))

        painter.restore()

    def initColor(self) -> None:
        """ 获取对应百分比处的颜色 """
        height: int = self.height()
        posY: int = int(height - ((self.__percent / 100) * height) + 1)
        if posY >= height:
            posY = height - 1

        self.__color = self.__bgPix.toImage().pixel(self.__bgRect.width() / 2, posY)

    @property
    def borderWidth(self) -> int: return self.__borderWidth

    @borderWidth.setter
    def borderWidth(self, border_width: int) -> None:
        if self.__borderWidth == border_width: return
        self.__borderWidth = border_width
        self.update()

    @property
    def borderRadius(self) -> int: return self.__borderRadius

    @borderRadius.setter
    def borderRadius(self, border_radius: int) -> None:
        if self.__borderRadius == border_radius: return
        self.__borderRadius = border_radius
        self.update()

    @property
    def borderColor(self) -> QColor: return self.__borderColor

    @borderColor.setter
    def borderColor(self, border_color: QColor) -> None:
        if self.__borderColor == border_color: return
        self.__borderColor = border_color
        self.update()

    @property
    def autoHeight(self) -> bool: return self.__autoHeight

    @autoHeight.setter
    def autoHeight(self, auto_height: bool) -> None:
        if self.__autoHeight == auto_height: return
        self.__autoHeight = auto_height
        self.update()

    @property
    def percentHeight(self) -> int: return self.__percentHeight

    @percentHeight.setter
    def percentHeight(self, percent_height: int) -> None:
        if self.__percentHeight == percent_height: return
        self.__percentHeight = percent_height
        self.resizeEvent()
        self.update()

    @property
    def percentBorder(self) -> int: return self.__percentBorder

    @percentBorder.setter
    def percentBorder(self, percent_border: int) -> None:
        if self.__percentBorder == percent_border: return
        self.__percentBorder = percent_border
        self.update()

    @property
    def percentRadius(self) -> int: return self.__percentRadius

    @percentRadius.setter
    def percentRadius(self, percent_radius: int) -> None:
        if self.__percentRadius == percent_radius: return
        self.__percentRadius = percent_radius
        self.update()

    @property
    def percentColor(self) -> QColor: return self.__percentColor

    @percentColor.setter
    def percentColor(self, percent_color: QColor) -> None:
        if self.__percentColor == percent_color: return
        self.__percentColor = percent_color
        self.update()

    @property
    def topColor(self) -> QColor: return self.__topColor

    @topColor.setter
    def topColor(self, top_color: QColor) -> None:
        if self.__topColor == top_color: return
        self.__topColor = top_color
        self.update()

        # 非静态模式重新采样
        if not self.__staticMode:
            self.showEvent()

    @property
    def bottomColor(self) -> QColor: return self.__bottomColor

    @bottomColor.setter
    def bottomColor(self, bottom_color: QColor) -> None:
        if self.__bottomColor == bottom_color: return
        self.__bottomColor = bottom_color
        self.update()

        # 非静态模式重新采样
        if not self.__staticMode:
            self.showEvent()

    @property
    def disableColor(self) -> QColor: return self.__disableColor

    @disableColor.setter
    def disableColor(self, disable_color: QColor) -> None:
        if self.__disableColor == disable_color: return
        self.__disableColor = disable_color
        self.update()

    @property
    def showOverlay(self) -> bool: return self.__showOverlay

    @showOverlay.setter
    def showOverlay(self, show_overlay: bool) -> None:
        if self.__showOverlay == show_overlay: return
        self.__showOverlay = show_overlay
        self.update()

    @property
    def overlayColor(self) -> QColor: return self.__overlayColor

    @overlayColor.setter
    def overlayColor(self, overlay_color: QColor) -> None:
        if self.__overlayColor == overlay_color: return
        self.__overlayColor = overlay_color
        self.update()

    @property
    def staticMode(self) -> bool: return self.__staticMode

    @staticMode.setter
    def staticMode(self, static_mode: bool) -> None:
        if self.__staticMode == static_mode: return
        self.__staticMode = static_mode
        self.update()

    @property
    def outMode(self) -> bool: return self.__outMode

    @outMode.setter
    def outMode(self, out_mode: bool) -> None:
        if self.__outMode == out_mode: return
        self.__outMode = out_mode
        self.update()

    @property
    def hsbMode(self) -> bool: return self.__hsbMode

    @hsbMode.setter
    def hsbMode(self, hsb_mode: bool) -> None:
        if self.__hsbMode == hsb_mode: return
        self.__hsbMode = hsb_mode
        self.update()

    @property
    def showValue(self) -> bool: return self.__showValue

    @showValue.setter
    def showValue(self, show_value: bool) -> None:
        if self.__showValue == show_value: return
        self.__showValue = show_value
        self.update()

    @property
    def minValue(self) -> float: return self.__minValue

    @minValue.setter
    def minValue(self, min_value: float) -> None:
        if self.__minValue == min_value: return
        self.__minValue = min_value
        self.__percent = self.__value / (self.__maxValue - min_value) * 100
        self.update()

    @property
    def maxValue(self) -> float: return self.__maxValue

    @maxValue.setter
    def maxValue(self, max_value: float) -> None:
        if self.__maxValue == max_value: return
        self.__maxValue = max_value
        self.__percent = self.__value / (max_value - self.__minValue) * 100
        self.update()

    @property
    def value(self) -> float: return self.__value

    @value.setter
    def value(self, n_value: float) -> None:
        if self.__value == n_value and self.__minValue > n_value > self.__maxValue: return
        self.__value = n_value
        self.__percent = n_value / (self.__maxValue - self.__minValue) * 100
        self.update()

    @property
    def percent(self) -> float: return self.__percent

    @percent.setter
    def percent(self, n_percent: float) -> None:
        if self.__percent == n_percent: return
        self.__percent = n_percent
        self.__value = n_percent / 100 * (self.__maxValue - self.__minValue)
        self.update()

    @property
    def color(self) -> QColor: return self.__color

    @color.setter
    def color(self, n_color: QColor) -> None:
        if self.__color == n_color: return
        self.__color = n_color
        self.update()

    def sizeHint(self) -> QSize: return QSize(50, 200)

    def minimumSizeHint(self) -> QSize: return QSize(30, 120)


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)

    window = QWidget()
    a = ColorPanelBar(window)
    a.resize(60, 325)
    window.staticMode = False
    window.show()
    sys.exit(app.exec_())
