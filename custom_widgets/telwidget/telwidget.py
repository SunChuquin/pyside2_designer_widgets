import random, shiboken2
from typing import List, AnyStr

from PySide2.QtCore import (QSize, QPoint, Signal, QObject, QEvent, QPropertyAnimation, QDateTime,
                            QTimer, Qt, QRectF, QPointF, QRect, QEasingCurve)
from PySide2.QtGui import (QPixmap, QColor, QPaintEvent, QMouseEvent, QResizeEvent, QShowEvent, QPainter, QFont,
                           QPen, QWheelEvent)
from PySide2.QtWidgets import (QWidget, QScrollBar, QScrollArea, QGridLayout, QVBoxLayout, QStyleOptionSlider,
                               QStyle, QApplication, QSpacerItem, QSizePolicy)

from custom_widgets.zhtopy.zhtopy import ZhToPY
from main import *

# 字母高亮背景类
class TelHigh(QWidget):

    def __init__(self, parent: QWidget = None):
        super(TelHigh, self).__init__(parent)
        self.__fontSize: int = 30  # 字体大小
        self.__bgImage: QPixmap = QPixmap()  # 背景图片
        self.__bgColor: QColor = Qt.transparent  # 背景颜色
        self.__text: str = 'A'  # 显示的文字
        self.__textColor: QColor = QColor(255, 255, 255)  # 文字颜色

    def paintEvent(self, event: QPaintEvent) -> None:
        width: int = self.width()
        height: int = self.height()
        side: int = min(width, height) // 2 - 1

        # 设置平滑绘制
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 设置字体大小
        font: QFont = QFont()
        font.setPixelSize(self.__fontSize)
        painter.setFont(font)

        # 优先绘制背景图片,居中绘制
        if self.__bgImage is not None:
            pix: QPixmap = self.__bgImage.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixX: int = self.rect().center().x() - pix.width() // 2
            pixY: int = self.rect().center().y() - pix.height() // 2
            point: QPoint = QPoint(pixX, pixY)
            painter.drawPixmap(point, pix)
            textRect = QRectF(0, 0, width - 40, height - 5)
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.__bgColor)
            painter.drawEllipse(self.rect().center(), side, side)
            textRect = self.rect()

        # 绘制文字
        painter.setPen(self.__textColor)
        painter.drawText(textRect, Qt.AlignCenter, self.__text)

    @property
    def fontSize(self) -> int: return self.__fontSize

    @fontSize.setter
    def fontSize(self, n_size: int) -> None:
        if self.__fontSize == n_size: return
        self.__fontSize = n_size
        self.update()

    @property
    def bgImage(self) -> QPixmap: return self.__bgImage

    @bgImage.setter
    def bgImage(self, bg_image: QPixmap) -> None:
        if self.__bgImage == bg_image: return
        self.__bgImage = bg_image
        self.update()

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def text(self) -> str: return self.__text

    @text.setter
    def text(self, n_text: str) -> None:
        if self.__text == n_text: return
        self.__text = n_text
        self.update()

    @property
    def textColor(self) -> QColor: return self.__textColor

    @textColor.setter
    def textColor(self, text_color: QColor) -> None:
        if self.__textColor == text_color: return
        self.__textColor = text_color
        self.update()

# 中间字母分隔类
class TelBanner(QWidget):
    def __init__(self, parent: QWidget = None):
        super(TelBanner, self).__init__(parent)
        self.__line: bool = False  # 绘制线条
        self.__padding: int = 15  # 离左侧距离
        self.__fontSize: int = 15  # 字体大小
        self.__text: str = 'A'  # 文字标识

        self.__textColor: QColor = QColor(50, 50, 50)  # 字体颜色
        self.__bgColor: QColor = QColor(0, 0, 0, 30)  # 背景颜色
        self.__lineColor: QColor = QColor(0, 0, 0, 180)  # 线条颜色

    def paintEvent(self, event: QPaintEvent) -> None:
        width: int = self.width()
        height: int = self.height()

        # 设置平滑绘制
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 可选绘制顶部线条还是背景颜色
        if self.__line:
            pen: QPen = QPen()
            pen.setWidth(2)
            pen.setColor(self.__lineColor)
            painter.setPen(pen)
            painter.drawLine(QPointF(0, 0), QPointF(width, 0))
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.__bgColor)
            painter.drawRect(0, 0, width, height)

        # 设置字体
        font: QFont = QFont()
        font.setPixelSize(self.__fontSize)
        painter.setFont(font)

        # 绘制文字
        textRect: QRectF = QRectF(self.__padding, 0, width - self.__padding, height)
        painter.setPen(self.__textColor)
        painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, self.__text)

    @property
    def line(self) -> bool: return self.__line

    @line.setter
    def line(self, n_line: bool) -> None:
        if self.__line == n_line: return
        self.__line = n_line
        self.update()

    @property
    def padding(self) -> int: return self.__padding

    @padding.setter
    def padding(self, n_padding: int) -> None:
        if self.__padding == n_padding: return
        self.__padding = n_padding
        self.update()

    @property
    def fontSize(self) -> int: return self.__fontSize

    @fontSize.setter
    def fontSize(self, font_size: int) -> None:
        if self.__fontSize == font_size: return
        self.__fontSize = font_size
        self.update()

    @property
    def text(self) -> str: return self.__text

    @text.setter
    def text(self, n_text: str) -> None:
        if self.__text == n_text: return
        self.__text = n_text
        self.update()

    @property
    def textColor(self) -> QColor: return self.__textColor

    @textColor.setter
    def textColor(self, text_color: QColor) -> None:
        if self.__textColor == text_color: return
        self.__textColor = text_color
        self.update()

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def lineColor(self) -> QColor: return self.__lineColor

    @lineColor.setter
    def lineColor(self, line_color: QColor) -> None:
        if self.__lineColor == line_color: return
        self.__lineColor = line_color
        self.update()

    def sizeHint(self) -> QSize: return QSize(100, 35)

    def minimumSizeHint(self) -> QSize: return QSize(30, 30)

# 右侧字母导航类
class TelLetter(QWidget):

    letterClicked = Signal(str, int)  # letter, letterY

    def __init__(self, parent: QWidget = None):
        super(TelLetter, self).__init__(parent)
        self.__letters: str = '*ABCDEFGHIJKLMNOPQRSTUVWXYZ#'  # 字母集合
        self.__highLetter: str = 'A'  # 高亮字母

        self.__normalColor: QColor = QColor(100, 100, 100)  # 正常文字颜色
        self.__highColor: QColor = QColor(34, 163, 169)  # 高亮文字颜色

        self.__pressed: bool = False  # 鼠标按下

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__checkPos(event.pos())
        self.__pressed = True

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.__pressed = False

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.__pressed: self.__checkPos(event.pos())

    def paintEvent(self, event: QPaintEvent) -> None:
        width: int = self.width()
        height: int = self.height()

        # 设置平滑绘制
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 计算当前高度每个字母所占的高度
        lists: List[AnyStr] = [item for item in self.__letters]
        count: int = lists.__len__()
        letterHeight: int = height // count

        # 在最右侧垂直依次绘制
        letterY: int = 0
        font: QFont = QFont()
        for i in range(0, count):
            item = lists[i]
            textRect: QRect = QRect(0, letterY, width, letterHeight)

            # 突出显示高亮字母
            if item == self.__highLetter:
                font.setBold(True)
                painter.setPen(self.__highColor)
            else:
                font.setBold(False)
                painter.setPen(self.__normalColor)

            painter.setFont(font)
            painter.drawText(textRect, Qt.AlignCenter, item)
            letterY += letterHeight

    def __checkPos(self, pos: QPoint) -> None:
        # 根据按下处的坐标
        letterY: int = pos.y()

        # 如果超过当前窗体范围则不处理
        if letterY < 30 or letterY > (self.height() - 30): return

        # 计算当前高度每个字母所占的高度
        lists: List[AnyStr] = [item for item in self.__letters]
        count: int = lists.__len__()
        letterHeight: int = self.height() // (count - 2)

        # 找到对应的索引高亮显示,发出信号通知
        letterIndex: int = letterY // letterHeight
        self.highLetter = lists[letterIndex + 1]
        self.letterClicked.emit(self.__highLetter, letterIndex * letterHeight)

    @property
    def letters(self) -> str: return self.__letters

    @letters.setter
    def letters(self, n_letters: str) -> None:
        if self.__letters == n_letters: return
        self.__letters = n_letters
        self.update()

    @property
    def highLetter(self) -> str: return self.__highLetter

    @highLetter.setter
    def highLetter(self, high_letter: str) -> None:
        if self.__highLetter == high_letter: return
        self.__highLetter = high_letter
        self.update()

    @property
    def normalColor(self) -> QColor: return self.__normalColor

    @normalColor.setter
    def normalColor(self, normal_color: QColor) -> None:
        if self.__normalColor == normal_color: return
        self.__normalColor = normal_color
        self.update()

    @property
    def highColor(self) -> QColor: return self.__highColor

    @highColor.setter
    def highColor(self, high_color: QColor) -> None:
        if self.__highColor == high_color: return
        self.__highColor = high_color
        self.update()

# 通讯录按钮类
class TelButton(QWidget):

    btnPressed = Signal()
    btnRelease = Signal()

    def __init__(self, parent: QWidget = None):
        super(TelButton, self).__init__(parent)
        self.__pixVisible: bool = True  # 图标可见
        self.__padding: int = 30  # 左侧图标离左边的距离
        self.__space: int = 10  # 图标与右侧文字之间的间隔

        self.__pixmap: QPixmap = QPixmap(":/image/tel.png")  # 左侧小图标
        self.__name: str = "张三"  # 姓名
        self.__belong: str = "公司"  # 类型
        self.__tel: str = "13888888888"  # 电话

        self.__bgColor: QColor = QColor(0, 0, 0, 30)  # 背景颜色
        self.__nameColor: QColor = QColor(0, 0, 0)  # 姓名颜色
        self.__belongColor: QColor = QColor(100, 100, 100)  # 类型颜色

        self.__pressed: bool = False  # 鼠标是否按下
        self.__lastPos: QPoint = QPoint(0, 0)  # 按下坐标

        self.__letter: str = ''  # 字母属性

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__lastPos = event.pos()
        self.btnPressed.emit()
        self.__pressed = True
        self.update()
        super(TelButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        # 鼠标按下与松开同一个位置才算
        if self.__lastPos == event.pos():
            self.btnRelease.emit()

        self.__pressed = False
        self.update()
        super(TelButton, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super(TelButton, self).mouseMoveEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        width: int = self.width()
        height: int = self.height()
        pixSize: int = int(min(width, height) / 1.5)

        # 设置平滑绘制
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.drawRect(self.rect())

        # 如果鼠标按下则绘制背景
        if self.__pressed:
            painter.setPen(self.__bgColor)
            painter.setBrush(self.__bgColor)
            painter.drawRect(self.rect())

        # 绘制左侧小图标
        rectPix: QRect = QRect(self.__padding, height // 2 - pixSize // 2, pixSize, pixSize)
        if self.__pixVisible:
            pix: QPixmap = self.__pixmap.scaled(pixSize, pixSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(rectPix.x(), rectPix.y(), pix)

        # 绘制姓名
        p: QPoint = rectPix.topRight()
        rectName: QRect = QRect(p.x() + self.__space, 0, width - p.x() - self.__space, int(height / 1.5))
        painter.setPen(self.__nameColor)
        painter.drawText(rectName, Qt.AlignLeft | Qt.AlignVCenter, self.__name)

        # 绘制类型,需要重新设置字体,更小
        font: QFont = QFont()
        font.setPixelSize(font.pixelSize() - 2)
        painter.setFont(font)
        rectType: QRect = QRect(p.x() + self.__space, height // 2, width - p.x() - self.__space, height // 2)
        painter.setPen(self.__belongColor)
        painter.drawText(rectType, Qt.AlignLeft | Qt.AlignTop, self.__belong)

    @property
    def letter(self) -> str: return self.__letter

    @letter.setter
    def letter(self, n_letter: str) -> None:
        self.__letter = n_letter

    @property
    def pixVisible(self) -> bool: return self.__pixVisible

    @pixVisible.setter
    def pixVisible(self, pix_visible: bool) -> None:
        self.__pixVisible = pix_visible

    @property
    def padding(self) -> int: return self.__padding

    @padding.setter
    def padding(self, n_padding: int) -> None:
        if self.__padding == n_padding: return
        self.__padding = n_padding
        self.update()

    @property
    def space(self) -> int: return self.__space

    @space.setter
    def space(self, n_space: int) -> None:
        if self.__space == n_space: return
        self.__space = n_space
        self.update()

    @property
    def pixmap(self) -> QPixmap: return self.__pixmap

    @pixmap.setter
    def pixmap(self, n_pixmap: QPixmap) -> None:
        self.__pixmap = n_pixmap
        self.update()

    @property
    def name(self) -> str: return self.__name

    @name.setter
    def name(self, n_name: str) -> None:
        if self.__name == n_name: return
        self.__name = n_name
        self.update()

    @property
    def belong(self) -> str: return self.__belong

    @belong.setter
    def belong(self, n_belong: str) -> None:
        if self.__belong == n_belong: return
        self.__belong = n_belong
        self.update()

    @property
    def tel(self) -> str: return self.__tel

    @tel.setter
    def tel(self, n_tel: str) -> None:
        if self.__tel == n_tel: return
        self.__tel = n_tel
        self.update()

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def nameColor(self) -> QColor: return self.__nameColor

    @nameColor.setter
    def nameColor(self, name_color: QColor) -> None:
        if self.__nameColor == name_color: return
        self.__nameColor = name_color
        self.update()

    @property
    def belongColor(self) -> QColor: return self.__belongColor

    @belongColor.setter
    def belongColor(self, belong_color: QColor) -> None:
        if self.__belongColor == belong_color: return
        self.__belongColor = belong_color
        self.update()

    def sizeHint(self) -> QSize: return QSize(60, 40)

    def minimumSizeHint(self) -> QSize: return QSize(50, 40)

# 自定义滚动条类
class ScrollBar(QScrollBar):
    def __init__(self, parent: QScrollBar = None):
        super(ScrollBar, self).__init__(parent)

    def getSliderHeight(self) -> int:
        opt: QStyleOptionSlider = QStyleOptionSlider()
        self.initStyleOption(opt)
        rect: QRect = self.style().subControlRect(QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self)
        return rect.height()

# 通讯录面板类
class TelPanel(QWidget):

    positionChanged = Signal(int)  # value

    def __init__(self, parent: QWidget = None):
        super(TelPanel, self).__init__(parent)

        self.__step: int = 1200  # 移动的步长
        self.__margin: int = 0  # 边距
        self.__space: int = 0  # 设备之间的间隔
        self.__autoWidth: bool = False  # 宽度自动拉伸
        self.__autoHeight: bool = False  # 高度自动拉伸

        self.__normalColor: QColor = QColor(0, 0, 0, 35)  # 滚动条正常颜色
        self.__highColor: QColor = QColor(0, 0, 0, 75)  # 滚动条高亮颜色

        self.__columnCount: int = 1  # 面板列数
        self.__items: List[QWidget] = []  # 元素窗体集合
        self.__indexs: List[int] = []  # 分割窗体位置索引
        self.__banners: List[QWidget] = []  # 分割窗体集合

        self.__scrollArea: QScrollArea = QScrollArea(self)  # 滚动区域
        self.__animation: QPropertyAnimation = QPropertyAnimation(self.__scrollArea.verticalScrollBar(), b"value")  # 动画滑动
        self.__scrollBar: QScrollBar = QScrollBar(Qt.Vertical, self)  # 滚动条
        self.__widget: QWidget = QWidget(self.__scrollArea)  # 滚动区域载体,自动变宽变高
        self.__gridLayout: QGridLayout = QGridLayout(self.__widget)  # 表格布局

        self.__movetop: bool = False  # 是否上滑
        self.__pressed: bool = False  # 鼠标按下
        self.__pressedY: int = 0  # 鼠标按下处Y轴坐标
        self.__pressedPos: QPoint = QPoint(0, 0)  # 鼠标按下处坐标
        self.__pressedTime: QDateTime = QDateTime()  # 鼠标按下时间
        self.__timer: QTimer = QTimer(self)  # 定时器控制滚动条隐藏

        self.initControl()
        self.initForm()
        self.initBar()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.__widget:
            if event.type() == QEvent.Resize:
                self.initBar()

        return super(TelPanel, self).eventFilter(watched, event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__scrollArea.resize(self.size())

        # 根据宽度比例调整滚动条占的区域
        width: int = self.width()
        height: int = self.height()
        scrollWidth: int = 10
        offset: int = 3
        self.__scrollBar.setGeometry(width - scrollWidth - offset, offset, scrollWidth, height - offset * 2)

    def enterEvent(self, event: QEvent) -> None:
        pass

    def leaveEvent(self, event: QEvent) -> None:
        pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__pressed = True
        self.__pressedPos = event.pos()
        self.__pressedY = event.pos().y()
        self.__pressedTime = QDateTime.currentDateTime()
        self.__scrollBar.show()
        self.__animation.stop()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.__pressed = False

        # 说明是单击按钮
        if self.__pressedPos == event.pos(): return

        # 判断当前时间和鼠标按下事件比较,时间短则说明是滑动
        now: QDateTime = QDateTime.currentDateTime()
        if self.__pressedTime.time().msecsTo(now.time()) > 600:
            return

        # 可以改变下面的值来调整幅度
        offset: int = self.__step if self.__movetop else -self.__step
        value: int = self.__scrollArea.verticalScrollBar().value()
        self.__animation.setStartValue(value)
        self.__animation.setEndValue(value + offset)
        self.__animation.start()
        self.__timer.start(800)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        currentY: int = event.pos().y()
        offset: int = self.__pressedY - currentY
        scal: int = offset * 2
        self.__movetop = offset > 0

        # 如果滚动条已经在顶部且当前下滑或者在底部且当前上滑则无需滚动
        value: int = self.__scrollArea.verticalScrollBar().value()
        height: int = self.__scrollArea.verticalScrollBar().height()
        if (value == 0 and not self.__movetop) or ((value + height) == self.__widget.height() and self.__movetop):
            return

        if self.__pressedY != currentY:
            # 设置滚轮位置
            self.position += scal
            self.__pressedY = currentY

    def initControl(self) -> None:
        """ 初始化控件 """

        # 滚动条区域
        self.__scrollArea.setObjectName("TelPanel_ScrollArea")
        self.__scrollArea.setWidgetResizable(True)
        self.__scrollArea.setStyleSheet("QScrollArea#TelPanel_ScrollArea{border:none;background:transparent;}")

        # 替换垂直滚动条,以便获取滚动条手柄的高度
        bar: ScrollBar = ScrollBar()
        self.__scrollArea.setVerticalScrollBar(bar)

        # 设置滚动条不显示,用自定义的滚动条
        self.__scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 滚动条
        self.__scrollBar.setVisible(False)
        self.__scrollArea.verticalScrollBar().valueChanged.connect(self.__scrollBar.setValue)
        self.__scrollBar.valueChanged.connect(self.__scrollArea.verticalScrollBar().setValue)
        self.__scrollArea.verticalScrollBar().rangeChanged.connect(self.setRange)
        self.__scrollBar.valueChanged.connect(self.positionChanged)

        # 元素载体窗体
        self.__widget.installEventFilter(self)
        self.__widget.setObjectName("TelPanel_Widget")
        self.__widget.setGeometry(QRect(0, 0, 100, 100))
        self.__widget.setStyleSheet("QWidget#TelPanel_Widget{background:transparent;}")
        self.__scrollArea.setWidget(self.__widget)

        # 表格布局
        self.__gridLayout.setSpacing(0)
        self.__gridLayout.setContentsMargins(0, 0, 0, 0)

    def initForm(self) -> None:
        """ 初始化窗体 """

        # 定义动画产生平滑数值
        self.__animation.setEasingCurve(QEasingCurve.OutCirc)
        self.__animation.setDuration(500)

        # 启动定时器隐藏滚动条
        self.__timer.timeout.connect(self.checkBar)

    def initBar(self) -> None:
        """ 初始化滚动条 """

        # 获取到原有滚动条手柄的高度,重新设置新的滚动条的手柄高度
        bar: ScrollBar = self.__scrollArea.verticalScrollBar()
        # 原有高度可能太小,在此基础上加点
        sliderHeight: int = bar.getSliderHeight() + 50
        sliderHeight = self.height() if sliderHeight > self.height() else sliderHeight

        # 滚动条样式
        lists: List[str] = [
            "QScrollBar:vertical{background:transparent;padding:0px;}",
            "QScrollBar::handle:vertical{min-height:%dpx;}" % sliderHeight,
            "QScrollBar::handle:vertical{background:rgba(%d,%d,%d,%d);border-radius:5px;}" % (
                self.__normalColor.red(), self.__normalColor.green(), self.__normalColor.blue(), self.__normalColor.alpha()),
            "QScrollBar::handle:vertical:hover,QScrollBar::handle:vertical:pressed{background:rgba(%d,%d,%d,%d);}" % (
                self.__highColor.red(), self.__highColor.green(), self.__highColor.blue(), self.__highColor.alpha()),
            "QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:none;}",
            "QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{background:none;}"
        ]
        self.__scrollBar.setStyleSheet(''.join(lists))

    def checkBar(self) -> None:
        """ 处理滚动条隐藏 """

        # 如果当前为按下则不需要隐藏
        if self.__pressed: return

        self.__scrollBar.hide()
        self.__timer.stop()

    def setRange(self, n_min: int, n_max: int) -> None:
        """ 设置滚动条范围值 """
        self.__scrollBar.setRange(n_min, n_max)

    @property
    def step(self) -> int: return self.__step

    @property
    def margin(self) -> int: return self.__margin

    @property
    def space(self) -> int: return self.__space

    @property
    def autoWidth(self) -> bool: return self.__autoWidth

    @property
    def autoHeight(self) -> bool: return self.__autoHeight

    @property
    def normalColor(self) -> QColor: return self.__normalColor

    @property
    def highColor(self) -> QColor: return self.__highColor

    @property
    def position(self) -> int: return self.__scrollBar.value()

    @property
    def columnCount(self) -> int: return self.__columnCount

    @property
    def items(self) -> List[QWidget]: return self.__items

    @property
    def indexs(self) -> List[int]: return self.__indexs

    @property
    def banners(self) -> List[QWidget]: return self.__banners

    def sizeHint(self) -> QSize: return QSize(300, 200)

    def minimumSizeHint(self) -> QSize: return QSize(20, 20)

    @step.setter
    def step(self, n_step: int) -> None:
        """ 设置每次滚动条移动的步长 """
        if self.__step != n_step: self.__step = n_step

    @margin.setter
    def margin(self, n_margin: int) -> None:
        """ 设置四个方位边距 """
        self.__margin = n_margin

    def setMargin(self, left: int, top: int, right: int, bottom: int) -> None:
        """ 设置四个方位边距 """
        self.__gridLayout.setContentsMargins(left, top, right, bottom)

    @space.setter
    def space(self, n_space: int) -> None:
        """ 设置元素间距 """
        if self.__space != n_space: self.__gridLayout.setSpacing(n_space)

    @autoWidth.setter
    def autoWidth(self, auto_width: bool) -> None:
        """ 设置是否自动宽度 """
        if self.__autoWidth != auto_width: self.__autoWidth = auto_width

    @autoHeight.setter
    def autoHeight(self, auto_height: bool) -> None:
        """ 设置是否自动高度 """
        if self.__autoHeight != auto_height: self.__autoHeight = auto_height

    @position.setter
    def position(self, value: int):
        """ 设置滚动条位置 """
        self.__scrollBar.setValue(value)

    @normalColor.setter
    def normalColor(self, normal_color: QColor) -> None:
        """ 设置滚动条正常颜色 """
        if self.__normalColor != normal_color:
            self.__normalColor = normal_color
            self.initBar()

    @highColor.setter
    def highColor(self, high_color: QColor) -> None:
        """ 设置滚动条高亮颜色 """
        if self.__highColor != high_color:
            self.__highColor = high_color
            self.initBar()

    @indexs.setter
    def indexs(self, n_indexs: List[int]) -> None:
        """ 设置分割窗体 """
        if self.__indexs != n_indexs: self.__indexs = n_indexs

    @banners.setter
    def banners(self, n_banners: List[QWidget]) -> None:
        """ 设置索引位置 """
        self.__banners = n_banners

    @columnCount.setter
    def columnCount(self, column_count: int) -> None:
        """ 设置窗体元素列数 """
        if self.__columnCount != column_count: self.__columnCount = column_count

    @items.setter
    def items(self, n_items: List[QWidget]) -> None:
        """ 设置窗体元素集合 """
        self.__items = n_items.copy()

        row: int = 0
        column: int = 0
        count: int = 0
        temp: int = 0

        # 单独添加第一行标识符
        if self.__indexs.__len__() > 0 and self.__indexs[0] == 0:
            self.__gridLayout.addWidget(self.__banners[0], row, column, 1, self.__columnCount)
            row += 1

        for item in n_items:
            # 逐行添加元素到表格布局
            self.__gridLayout.addWidget(item, row, column)
            column += 1
            count += 1
            temp += 1

            # 强制插入分割控件,另起一行
            index: int = self.__indexs.index(count) if count in self.__indexs else -1
            if index >= 0:
                row += 1
                column = 0
                self.__gridLayout.addWidget(self.__banners[index], row, column, 1, self.__columnCount)

                # 奇数偶数增加的数量不一样
                if temp % self.__columnCount == 0: temp += self.__columnCount
                else: temp += 1

                row += 1

            # 如果到了列数则换行
            if temp % self.__columnCount == 0:
                row += 1
                column = 0

        row += 1

        # 设置右边弹簧
        if not self.__autoWidth:
            hSpacer: QSpacerItem = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.__gridLayout.addItem(hSpacer, 0, self.__gridLayout.columnCount())

        # 设置底边弹簧
        if not self.__autoHeight:
            vSpacer: QSpacerItem = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.__gridLayout.addItem(vSpacer, row, 0)

# 通讯录控件
class TelWidget(QWidget):

    """
    通讯录控件
    作者:feiyangqingyun(QQ:517216493) 2018-9-30
    译者:sunchuquin(QQ:1715216365) 2021-06-21
    1. 可设置信息集合(图标+姓名+类型+电话)以及添加单个联系人
    2. 可设置背景图片+背景颜色
    3. 可设置右侧导航字母的列表+默认颜色+高亮颜色
    4. 可设置联系人按钮姓名颜色+姓名字体
    5. 可设置联系人按钮类型颜色+姓名字体
    6. 可设置联系人按钮选中背景颜色
    7. 可设置字母导航的风格(背景颜色+线条)
    8. 可设置字母导航的颜色+字体大小
    9. 可设置各种边距+联系人列数+元素间隔等
    10. 支持悬浮滚动条,可设置悬停时间
    11. 可设置悬浮滚动条的正常颜色+高亮颜色
    12. 支持滑动,可设置滑动的步长速度
    13. 支持单击右侧字母导航定位+文本突出显示
    14. 单击发出当前联系人的姓名+类型+电话等信息
    15. 根据汉字字母排序从小到大排列联系人,自带汉字转拼音功能
    """

    telClicked = Signal(str, str, str)  # name, type, tel

    class TelInfo:
        """ 联系人结构体 """
        def __init__(self):
            self.letter: str = ''
            self.name: str = ''
            self.n_type: str = ''
            self.tel: str = ''
            self.pixmap: QPixmap = QPixmap()

        def __lt__(self, other):
            return self.letter < other.letter

        def __le__(self, other):
            return self.letter > other.letter

    def __init__(self, parent: QWidget = None):
        super(TelWidget, self).__init__(parent)

        self.zhtopy = ZhToPY()

        self.__names: List[AnyStr] = []  # 姓名集合
        self.__types: List[AnyStr] = []  # 类型集合
        self.__tels: List[AnyStr] = []  # 电话集合

        self.__bgImage: QPixmap = QPixmap()  # 背景图片
        self.__bgColor: QColor = Qt.transparent  # 背景颜色

        self.__lastPosition: int = 0  # 最后滚动条位置
        self.__telPanel: TelPanel = TelPanel(self)  # 通讯录面板
        self.__telHigh: TelHigh = TelHigh(self.__telPanel)  # 高亮字母标签
        self.__telBanner: TelBanner = TelBanner(self.__telPanel)  # 顶部间隔字母导航
        self.__telLetter: TelLetter = TelLetter(self.__telPanel)  # 右侧字母标签

        self.__telHighFontSize: int = self.__telHigh.fontSize  # 高亮标签字体大小
        self.__telHighBgImage: QPixmap = self.__telHigh.bgImage  # 高亮标签背景图片
        self.__telHighBgColor: QColor = self.__telHigh.bgColor  # 高亮标签背景颜色
        self.__telHighTextColor: QColor = self.__telHigh.textColor  # 高亮标签文字颜色

        self.__telBannerBgColor: QColor = self.__telBanner.bgColor  # 顶部字母导航背景颜色
        self.__telBannerTextColor: QColor = self.__telBanner.textColor  # 顶部字母导航文字颜色
        self.__telBannerLineColor: QColor = self.__telBanner.lineColor  # 顶部字母导航线条颜色

        self.__telLetterNormalColor: QColor = self.__telLetter.normalColor  # 右侧字母导航正常颜色
        self.__telLetterHighColor: QColor = self.__telLetter.highColor  # 右侧字母导航高亮颜色

        self.__telButtonBgColor: QColor = QColor(0, 0, 0, 30)  # 通讯录按钮背景颜色
        self.__telButtonNameColor: QColor = QColor(0, 0, 0)  # 通讯录按钮姓名颜色
        self.__telButtonBelongColor: QColor = QColor(100, 100, 100)  # 通讯录按钮类型颜色

        self.__telPanelNormalColor: QColor = self.__telPanel.normalColor  # 滚动条正常颜色
        self.__telPanelHighColor: QColor = self.__telPanel.highColor  # 滚动条高亮颜色

        self.__items: List[QWidget] = []  # 通讯录按钮集合
        self.__banners: List[QWidget] = []  # 通讯录字母分割集合
        self.__pixmaps: List[QPixmap] = []  # 联系人图片集合
        self.__timer: QTimer = QTimer(self)  # 隐藏高亮标签定时器

        self.initControl()
        # self.initForm()

    def setInfo(self) -> None:
        if not self.__names or not self.__types or not self.__tels: return

        # 行标识符文字集合
        texts: List[AnyStr] = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "#"
        ]
        
        if self.__names.__len__() == self.__types.__len__() or \
                self.__types.__len__() == self.__tels.__len__() or \
                self.__tels.__len__() == self.__pixmaps.__len__():
            
            # 取出对应汉字首字母,先对所有姓名按照字母从小到大排序
            poundInfos: List[TelWidget.TelInfo] = []
            telInfos: List[TelWidget.TelInfo] = []
            for i in range(self.__names.__len__()):
                telInfo: TelWidget.TelInfo = TelWidget.TelInfo()
                telInfo.name = self.__names[i]
                telInfo.n_type = self.__types[i]
                telInfo.tel = self.__tels[i]
                telInfo.pixmap = self.__pixmaps[i]
    
                # 如果首字母未找到字母则归结到 '#' 分类中
                letter: str = self.zhtopy.zhToZM(self.__names[i][0])
                if letter in texts:
                    telInfo.letter = self.zhtopy.zhToJP(self.__names[i])
                    telInfos.append(telInfo)
                else:
                    telInfo.letter = "#"
                    poundInfos.append(telInfo)
    
            # 对信息集合进行升序排序
            telInfos.sort()
    
            # 对最后的 '#' 类别追加到末尾
            for n_telInfo in poundInfos:
                telInfos.append(n_telInfo)

            # 先要清空所有元素
            for i in self.__items: shiboken2.delete(i)
            for i in self.__banners: shiboken2.delete(i)
            self.__items.clear()
            self.__banners.clear()
    
            # 生成电话本按钮
            for i in range(self.__names.__len__()):
                telInfo: TelWidget.TelInfo = telInfos[i]
                btn: TelButton = TelButton()
                btn.btnPressed.connect(self.btnPressed)
                btn.btnRelease.connect(self.btnRelease)
    
                # 设置字母属性
                letter: str = telInfo.letter[0]
                btn.letter = letter
    
                # 设置头像+姓名+类型+电话
                btn.pixmap = telInfo.pixmap
                btn.name = telInfo.name
                btn.belong = telInfo.n_type
                btn.tel = telInfo.tel
                self.__items.append(btn)
    
            # 逐个计算字母对应的索引
            tempIndex: List[int] = []
            textCount: int = texts.__len__()
            for j in range(textCount):
                text: str = texts[j]
                index: int = -1
                for k in range(self.__items.__len__()):
                    if str(self.__items[k].letter) == text:
                        index = k
                        break
    
                tempIndex.append(index)
    
            # 过滤索引,标识符索引>=0才算数
            indexs: List[int] = []
            for j in range(textCount):
                index: int = tempIndex[j]
                if index >= 0:
                    banner: TelBanner = TelBanner()
                    banner.text = texts[j]
                    self.__banners.append(banner)
                    indexs.append(index)
    
            # 设置标识符+元素集合
            self.__telPanel.indexs = indexs.copy()
            self.__telPanel.banners = self.__banners.copy()
            self.__telPanel.items = self.__items.copy()
    
            # 重新设置颜色
            self.telHighBgColor = self.__telHighBgColor
            self.telBannerBgColor = self.__telBannerBgColor
            self.telBannerTextColor = self.__telBannerTextColor
            self.telLetterNormalColor = self.__telLetterNormalColor
            self.telLetterHighColor = self.__telLetterHighColor
            self.telButtonNameColor = self.__telButtonNameColor
            self.telButtonBelongColor = self.__telButtonBelongColor
            self.telPanelNormalColor = self.__telPanelNormalColor
            self.telPanelHighColor = self.__telPanelHighColor
    
    def addInfo(self, n_name: str, n_type: str, n_tel: str, n_pixmap: QPixmap):
        self.__names.append(n_name)
        self.__types.append(n_type)
        self.__tels.append(n_tel)
        self.__pixmaps.append(n_pixmap)
        self.setInfo()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.showEvent()

    def showEvent(self, event: QShowEvent = None) -> None:
        width: int = 18
        x: int = self.__telPanel.width() - width * 2
        y: int = 0
        height: int = self.__telPanel.height()
        self.__telLetter.setGeometry(x, y, width, height)

        # 设置中间字母导航间隔标签位置
        self.__telBanner.resize(self.__telPanel.width(), 30)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter: QPainter = QPainter(self)

        # 优先绘制背景图片
        if self.__bgImage is not None:
            pix: QPixmap = self.__bgImage.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, pix)
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.__bgColor)
            painter.drawRect(self.rect())

    def sizeHint(self) -> QSize: return QSize(300, 500)
    def minimumSizeHint(self) -> QSize: return QSize(50, 150)

    def initControl(self) -> None:
        verticalLayout: QVBoxLayout = QVBoxLayout(self)
        verticalLayout.setObjectName("verticalLayout")
        verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.__telPanel.setObjectName("telPanel")
        verticalLayout.addWidget(self.__telPanel)

        # 设置面板的元素间距
        self.__telPanel.setMargin(0, 0, 0, 0)
        # 设置是否自动拉伸元素的宽度
        self.__telPanel.autoWidth = True
        # 设置列数
        self.__telPanel.columnCount = 2

        # 突出显示字母
        self.__telHigh.setVisible(False)

        # 顶部间隔字母导航
        self.__telBanner.setVisible(False)

        # 右侧字母列表
        self.__telLetter.letterClicked.connect(self.letterClicked)

        # 绑定面板滑动位置改变信号槽,计算当前字母
        self.__telPanel.positionChanged.connect(self.positionChanged)

        # 定时器隐藏突出显示字母
        self.__timer.timeout.connect(self.__telHigh.hide)
        self.__timer.setInterval(1000)

    def initForm(self) -> None:
        zimus = {
            10: "A", 23: "B", 45: "C", 80: "D", 100: "E", 130: "F", 160: "G",
            180: "H", 200: "I", 230: "J", 250: "K", 260: "L", 270: "M", 280: "N",
            290: "O", 300: "P", 310: "Q", 330: "R", 350: "S", 380: "T", 400: "U",
            430: "V", 450: "W", 470: "X", 500: "Y"
        }

        # 设置联系人信息集合
        lists: List[AnyStr] = ["住宅", "家里", "公司"]
        for i in range(550):  # 设置字母属性
            for z in zimus.keys():
                if i < z:
                    letter = zimus[z]
                    break
            else:
                letter = 'Z'

            # 统计下当前该字母的有多少
            count: int = 1
            for name in self.__names:
                if name[0] == letter:
                    count += 1

            self.__names.append("{} {}".format(letter, str(count).rjust(2, '0')))
            self.__types.append(lists[random.randint(0, 100) % 3])
            self.__tels.append("1381234{}".format(str(random.randint(0, 100)).rjust(3, '0')))
            self.__pixmaps.append(QPixmap(":/image/img{}.jpg".format(random.randint(0, 100) % 10)))

        self.setInfo()

    def btnPressed(self) -> None:
        # 记录下滚动条位置,过滤鼠标松开地方
        self.__lastPosition = self.__telPanel.position

    def btnRelease(self) -> None:
        # 如果鼠标按下时候和松开时候的滚动条位置一致则说明是单击
        position: int = self.__telPanel.position
        if self.__lastPosition == position:
            btn: TelButton = self.sender()
            self.telClicked.emit(btn.name, btn.belong, btn.tel)

    def positionChanged(self, value: int) -> None:
        # 找到当前位置的按钮的姓名的首字母
        for i in range(self.__items.__len__()):
            item: QWidget = self.__items[i]
            p: QPoint = item.pos()

            # 相邻近似算法,当前滚动条的值需要加上按钮的高度,不然找到的是上一个
            offset: int = abs(p.y() - (value + 20))
            if offset < 5:
                btn: TelButton = item
                letter: str = str(btn.letter)
                self.__telLetter.highLetter = letter
                self.__telBanner.text = letter
                return

    def letterClicked(self, letter: str, letter_y: int) -> None:
        # 找到当前字母所在的第一行,滚动条滚过去
        for i in range(self.__items.__len__()):
            w: QWidget = self.__items[i]
            text = str(w.letter)
            if text == letter:
                # 需要减去字母导航标签的高度
                self.__telPanel.position = w.pos().y() - 30
                break

        # 根据不同的类型移动到不同的位置
        if not self.__telHigh.bgImage.isNull():
            self.__telHigh.resize(100, 55)
            self.__telHigh.move(self.__telPanel.width() - self.__telHigh.width() - 12, letter_y - 15)
        else:
            self.__telHigh.resize(55, 55)
            self.__telHigh.move(int((self.__telPanel.width() - self.__telHigh.width()) / 2),
                                int((self.__telPanel.height() - self.__telHigh.height()) / 2))

        self.__telHigh.text = letter
        self.__telHigh.show()
        self.__timer.stop()
        self.__timer.start()

    @property
    def names(self) -> List[AnyStr]: return self.__names

    @names.setter
    def names(self, n_names: List[AnyStr]) -> None:
        if self.__names == n_names: return
        self.__names = n_names
        self.setInfo()

    @property
    def types(self) -> List[AnyStr]: return self.__types

    @types.setter
    def types(self, n_types: List[AnyStr]) -> None:
        if self.__types == n_types: return
        self.__types = n_types
        self.setInfo()

    @property
    def tels(self) -> List[AnyStr]: return self.__tels

    @tels.setter
    def tels(self, n_tels: List[AnyStr]) -> None:
        if self.__tels == n_tels: return
        self.__tels = n_tels
        self.setInfo()

    @property
    def pixmaps(self) -> List[QPixmap]: return self.__pixmaps

    @pixmaps.setter
    def pixmaps(self, n_pixmaps: List[QPixmap]) -> None:
        if self.__pixmaps == n_pixmaps: return
        self.__pixmaps = n_pixmaps
        self.setInfo()

    @property
    def bgImage(self) -> QPixmap: return self.__bgImage

    @bgImage.setter
    def bgImage(self, bg_image: QPixmap) -> None:
        self.__bgImage = bg_image
        self.update()

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        self.__bgColor = bg_color
        self.update()

    @property
    def telHighFontSize(self) -> int: return self.__telHighFontSize

    @telHighFontSize.setter
    def telHighFontSize(self, tel_high_font_size: int) -> None:
        self.__telHighFontSize = tel_high_font_size
        self.__telHigh.fontSize = tel_high_font_size

    @property
    def telHighBgImage(self) -> QPixmap: return self.__telHighBgImage

    @telHighBgImage.setter
    def telHighBgImage(self, tel_high_bg_image: QPixmap) -> None:
        self.__telHighBgImage = tel_high_bg_image
        self.__telHigh.bgImage = tel_high_bg_image

    @property
    def telHighBgColor(self) -> QColor: return self.__telHighBgColor

    @telHighBgColor.setter
    def telHighBgColor(self, tel_high_bg_color: QColor) -> None:
        self.__telHighBgColor = tel_high_bg_color
        self.__telHigh.bgColor = tel_high_bg_color

    @property
    def telHighTextColor(self) -> QColor: return self.__telHighTextColor

    @telHighTextColor.setter
    def telHighTextColor(self, tel_high_text_color: QColor) -> None:
        self.__telHighTextColor = tel_high_text_color
        self.__telHigh.textColor = tel_high_text_color

    @property
    def telBannerBgColor(self) -> QColor: return self.__telBannerBgColor

    @telBannerBgColor.setter
    def telBannerBgColor(self, tel_banner_bg_color: QColor) -> None:
        self.__telBannerBgColor = tel_banner_bg_color
        self.__telBanner.bgColor = tel_banner_bg_color
        for bannerr in self.__banners:
            b: TelBanner = bannerr
            b.bgColor = tel_banner_bg_color

    @property
    def telBannerTextColor(self) -> QColor: return self.__telBannerTextColor

    @telBannerTextColor.setter
    def telBannerTextColor(self, tel_banner_text_color: QColor) -> None:
        self.__telBannerTextColor = tel_banner_text_color
        self.__telBanner.textColor = tel_banner_text_color
        for banner in self.__banners:
            b: TelBanner = banner
            b.textColor = tel_banner_text_color

    @property
    def telBannerLineColor(self) -> QColor: return self.__telBannerLineColor

    @telBannerLineColor.setter
    def telBannerLineColor(self, tel_banner_line_color: QColor) -> None:
        self.__telBannerLineColor = tel_banner_line_color
        self.__telBanner.lineColor = tel_banner_line_color
        for banner in self.__banners:
            b: TelBanner = banner
            b.lineColor = tel_banner_line_color

    @property
    def telLetterNormalColor(self) -> QColor: return self.__telLetterNormalColor

    @telLetterNormalColor.setter
    def telLetterNormalColor(self, tel_letter_normal_color: QColor) -> None:
        self.__telLetterNormalColor = tel_letter_normal_color
        self.__telLetter.normalColor = tel_letter_normal_color

    @property
    def telLetterHighColor(self) -> QColor: return self.__telLetterHighColor

    @telLetterHighColor.setter
    def telLetterHighColor(self, tel_letter_high_color: QColor) -> None:
        self.__telLetterHighColor = tel_letter_high_color
        self.__telLetter.highColor = tel_letter_high_color

    @property
    def telButtonBgColor(self) -> QColor: return self.__telButtonBgColor

    @telButtonBgColor.setter
    def telButtonBgColor(self, tel_button_bg_color: QColor) -> None:
        self.__telButtonBgColor = tel_button_bg_color
        for item in self.__items:
            btn: TelButton = item
            btn.bgColor = tel_button_bg_color

    @property
    def telButtonNameColor(self) -> QColor: return self.__telButtonNameColor

    @telButtonNameColor.setter
    def telButtonNameColor(self, tel_button_name_color: QColor) -> None:
        self.__telButtonNameColor = tel_button_name_color
        for item in self.__items:
            btn: TelButton = item
            btn.nameColor = tel_button_name_color

    @property
    def telButtonBelongColor(self) -> QColor: return self.__telButtonBelongColor

    @telButtonBelongColor.setter
    def telButtonBelongColor(self, tel_button_belong_color: QColor) -> None:
        self.__telButtonBelongColor = tel_button_belong_color
        for item in self.__items:
            btn: TelButton = item
            btn.belongColor = tel_button_belong_color

    @property
    def telPanelNormalColor(self) -> QColor: return self.__telPanelNormalColor

    @telPanelNormalColor.setter
    def telPanelNormalColor(self, tel_panel_normal_color: QColor) -> None:
        self.__telPanelNormalColor = tel_panel_normal_color
        self.__telPanel.normalColor = tel_panel_normal_color

    @property
    def telPanelHighColor(self) -> QColor: return self.__telPanelHighColor

    @telPanelHighColor.setter
    def telPanelHighColor(self, tel_panel_high_color: QColor) -> None:
        self.__telPanelHighColor = tel_panel_high_color
        self.__telPanel.highColor = tel_panel_high_color


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import (QMessageBox, QApplication, QHBoxLayout, QVBoxLayout,
                                   QPushButton, QLineEdit)

    class FrmTelWidget(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmTelWidget, self).__init__(parent)
            self.telWidget = TelWidget()
            self.telWidget.telClicked.connect(self.telClicked)
            self.telWidget.bgImage = QPixmap(":/image/bg.jpg")

            sublayout = QHBoxLayout()
            self.txtName = QLineEdit('阿波')
            self.txtType = QLineEdit('公司')
            self.txtTel = QLineEdit('1388888888')
            self.btnAdd = QPushButton('添加')
            self.btnAdd.clicked.connect(self.on_btnAdd_clicked)
            sublayout.addWidget(self.txtName)
            sublayout.addWidget(self.txtType)
            sublayout.addWidget(self.txtTel)
            sublayout.addWidget(self.btnAdd)

            layout = QVBoxLayout()
            layout.addWidget(self.telWidget)
            layout.addLayout(sublayout)
            self.setLayout(layout)

            # 设置类北京图片则优先取背景图片，否则样式未中间圆形
            # self.telWidget.telHighBgImage = QPixmap(":/image/letter.png")
            self.telWidget.telHighBgColor = QColor(0, 0, 0, 130)

            if True:
                self.telWidget.telHighBgColor = QColor(255, 255, 255, 100)
                self.telWidget.telBannerBgColor = QColor(255, 255, 255, 50)
                self.telWidget.telBannerTextColor = QColor(255, 255, 255)
                self.telWidget.telLetterNormalColor = QColor(255, 255, 255)
                self.telWidget.telLetterHighColor = QColor(27, 188, 155)
                self.telWidget.telButtonNameColor = QColor(255, 255, 255)
                self.telWidget.telButtonTypeColor = QColor(200, 200, 200)
                self.telWidget.telPanelNormalColor = QColor(255, 255, 255, 100)
                self.telWidget.telPanelHighColor = QColor(255, 255, 255, 200)

            zimus = {
                10: "A", 23: "B", 45: "C", 80: "D", 100: "E", 130: "F", 160: "G",
                180: "H", 200: "I", 230: "J", 250: "K", 260: "L", 270: "M", 280: "N",
                290: "O", 300: "P", 310: "Q", 330: "R", 350: "S", 380: "T", 400: "U",
                430: "V", 450: "W", 470: "X", 500: "Y"
            }

            # 设置联系人信息集合
            self.telWidget.names.clear()
            self.telWidget.types.clear()
            self.telWidget.tels.clear()
            self.telWidget.pixmaps.clear()

            lists: List[AnyStr] = ["住宅", "家里", "公司"]
            for i in range(550):  # 设置字母属性
                for z in zimus.keys():
                    if i < z:
                        letter = zimus[z]
                        break
                else:
                    letter = 'Z'

                # 统计下当前该字母的有多少
                count: int = 1
                for name in self.telWidget.names:
                    if name[0] == letter:
                        count += 1

                self.telWidget.names.append("{} {}".format(letter, str(count).rjust(2, '0')))
                self.telWidget.types.append(lists[random.randint(0, 100) % 3])
                self.telWidget.tels.append("1381234{}".format(str(random.randint(0, 100)).rjust(3, '0')))
                self.telWidget.pixmaps.append(QPixmap(":/image/img{}.jpg".format(random.randint(0, 100) % 10)))

            self.telWidget.setInfo()

        def telClicked(self, n_name: str, n_type: str, n_tel: str) -> None:
            info: str = '姓名: {}   类型: {}   电话: {}'.format(n_name, n_type, n_tel)
            QMessageBox.information(self, '单击', info)

        def on_btnAdd_clicked(self):
            n_name: str = self.txtName.text()
            n_type: str = self.txtType.text()
            n_tel: str = self.txtTel.text()
            self.telWidget.addInfo(n_name, n_type, n_tel, QPixmap(":/image/tel.png"))

    app = QApplication()
    window = FrmTelWidget()
    window.show()
    sys.exit(app.exec_())
