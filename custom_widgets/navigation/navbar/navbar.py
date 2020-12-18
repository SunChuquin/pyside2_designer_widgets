
from enum import Enum
from decimal import Decimal
from PySide2.QtGui import QColor, QPainter, QLinearGradient, QPen, QFont
from PySide2.QtCore import Slot, Signal, QRectF, QTimer, QSize, QPointF, QEnum, Qt, QPoint
from PySide2.QtWidgets import QApplication, QWidget


class NavBar(QWidget):
    """
    滑动导航条控件
    作者:feiyangqingyun(QQ:517216493) 2016-10-8
    译者:sunchuquin(QQ:1715216365) 2020-12-15
    1. 可键盘按键上下移动元素功能
    2. 支持窗体大小改变控件自动拉伸
    3. 支持移动到第一个/末一个/上移/下移/移动到指定索引/移动到指定元素
    4. 支持扁平处理
    5. 支持纵向风格
    6. 可设置圆角角度,包括主背景和选中元素背景
    7. 可设置间距
    8. 可设置导航条主背景渐变色
    9. 可设置当前条目选中背景渐变色
    10. 可设置条目未选中和选中的文字颜色
    11. 可设置五种选中风格样式
    12. 可设置线条颜色和宽度
    13. 选中条目的宽度为条目文字集合中最长的一个
    """

    # 当前条目改变信号
    currentItemChanged = Signal(int, str)  # int: 当前条目的索引, str: 当前条目的文字

    @QEnum
    class BarStyle(Enum):
        BARSTYLE_RECT = 0  # 圆角矩形
        BARSTYLE_LINE_TOP = 1  # 顶部线条
        BARSTYLE_LINE_RIGHT = 2  # 右侧线条
        BARSTYLE_LINE_BOTTOM = 3  # 底部线条
        BARSTYLE_LINE_LEFT = 4  # 左侧线条

    def __init__(self, parent=None):
        super(NavBar, self).__init__(parent)

        # 导航条主背景渐变开始颜色
        self.__bgColorStart = QColor(121, 121, 121)  # PySide2.QtGui.QColor
        # 导航条主背景渐变结束颜色
        self.__bgColorEnd = QColor(78, 78, 78)  # PySide2.QtGui.QColor
        # 用于扁平化切换
        self.__old_bgColorEnd = self.__bgColorEnd  # PySide2.QtGui.QColor

        # 导航条当前条目渐变开始颜色
        self.__barColorStart = QColor(46, 132, 243)  # PySide2.QtGui.QColor
        # 导航条当前条目渐变结束颜色
        self.__barColorEnd = QColor(39, 110, 203)  # PySide2.QtGui.QColor
        # 用于扁平化切换
        self.__old_barColorEnd = self.__barColorEnd  # PySide2.QtGui.QColor

        # 文字正常颜色
        self.__textNormalColor = QColor(230, 230, 230)  # PySide2.QtGui.QColor
        # 文字选中颜色
        self.__textSelectColor = QColor(255, 255, 255)  # PySide2.QtGui.QColor

        # 所有条目文字信息
        self.__items = ""  # str
        # 当前选中条目索引
        self.__currentIndex = -1  # int
        # 当前选中条目文字
        self.__currentItem = ""  # str

        # 背景圆角半径
        self.__bgRadius = 0  # int
        # 选中条目背景圆角半径
        self.__barRadius = 0  # int
        # 条目元素之间的间距
        self.__space = 25  # int

        # 线条宽度
        self.__lineWidth = 3  # int
        # 线条颜色
        self.__lineColor = QColor(255, 107, 107)  # PySide2.QtGui.QColor

        # 选中元素样式
        self.__barStyle = NavBar.BarStyle.BARSTYLE_RECT  # typing.enum[NavBar.BarStyle])

        # 是否支持按键移动
        self.__keyMove = True  # bool
        # 是否横向显示
        self.__horizontal = False  # bool
        # 是否扁平化
        self.__flat = False  # bool

        # 元素集合,成对出现,元素的名字,矩形区域范围
        self.__listItem = []  # typing.List[typing.Tuple[str, PySide2.QtCore.QRectF]]

        # 选中区域的矩形
        self.__barRect = QRectF()  # PySide2.QtCore.QRectF
        # 目标区域的矩形
        self.__targetRect = QRectF()  # PySide2.QtCore.QRectF
        # 选中区域的长度
        self.__barLen = Decimal(0)  # decimal.Decimal
        # 目标区域的长度
        self.__targetLen = Decimal(0)  # decimal.Decimal

        # 导航条的长度
        self.__initLen = Decimal(10)  # decimal.Decimal
        # 每次移动的步长
        self.__step = 0  # int

        # 是否往前移动
        self.__isForward = True  # bool
        # 是否首次处理
        self.__isVirgin = True  # bool
        # 滑动绘制定时器
        self.__timer = QTimer(self)  # PySide2.QtCore.QTimer
        self.__timer.setInterval(10)
        self.__timer.timeout.connect(self.__slide)

        self.setItems("主界面|系统设置|防区管理|警情查询|视频预览")
    # __init__

    def __del__(self):
        pass
    # __def__

    @staticmethod
    def __initStep(distance):  # initStp(self, distance: int) -> int
        """ 计算步长 """
        n = 1  # int
        while True:
            if (n * n) > distance:
                break
            else:
                n += 1
        return n * 1.4
    # __initStep

    def resizeEvent(self, event):  # resizeEvent(self, event: PySide2.QtGui.QResizeEvent)
        """  """
        index = 0  # int
        count = len(self.__listItem)  # int
        if count == 0:
            return

        if (count > 0) and (not self.__currentItem):
            # 相当于初始化，只会执行一次
            self.__currentIndex = 0
            self.__currentItem = self.__listItem[0][0]

        for i in range(count):
            if self.__listItem[i][0] == self.__currentItem:
                index = i
                break

        self.moveTo_int(index)
    # resizeEvent

    def mousePressEvent(self, event):  # mousePressEvent(self, event: PySide2.QtGui.QMouseEvent)
        """  """
        self.moveTo_point(event.pos())
    # mousePressEvent

    def keyPressEvent(self, event):  # keyPressEvent(self, event: PySide2.QtGui.QKeyEvent)
        """  """
        if not self.__keyMove:
            return

        if (event.key() == Qt.Key_Left) or (event.key() == Qt.Key_Up):
            self.movePrevious()
        elif (event.key() == Qt.Key_Right) or (event.key() == Qt.Key_Down):
            self.moveNext()
    # keyPressEvent

    def paintEvent(self, event):  # paintEvent(self, event: PySide2.QtGui.QPaintEvent)
        """  """
        # 绘制准备工作，启用反锯齿
        painter = QPainter(self)  # PySide2.QtGui.QPainter
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景色
        self.drawBg(painter)
        # 绘制当前条目选中背景
        self.drawBar(painter)
        # 绘制条目文字
        self.drawText(painter)
    # paintEvent

    def drawBg(self, painter):  # drawBg(self, painter: PySide2.QtGui.QPainter)
        """  """
        painter.save()
        painter.setPen(Qt.NoPen)
        bgGradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))  # PySide2.QtGui.QLinearGradient
        bgGradient.setColorAt(0.0, self.__bgColorStart)
        bgGradient.setColorAt(1.0, self.__bgColorEnd)
        painter.setBrush(bgGradient)
        painter.drawRoundedRect(self.rect(), self.__bgRadius, self.__bgRadius)
        painter.restore()
    # drawBg

    def drawBar(self, painter):  # drawBar(self, painter: PySide2.QtGui.QPainter)
        """  """
        painter.save()
        pen = QPen()  # PySide2.QtGui.QPen

        barGradient = QLinearGradient(self.__barRect.topLeft(), self.__barRect.bottomLeft())
        barGradient.setColorAt(0.0, self.__barColorStart)
        barGradient.setColorAt(1.0, self.__barColorEnd)
        painter.setBrush(barGradient)

        if self.barStyle == NavBar.BarStyle.BARSTYLE_RECT:
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.__barRect, self.__barRadius, self.__barRadius)
            painter.restore()
            return
        else:
            pen.setWidthF(self.__lineWidth)
            pen.setBrush(barGradient)
            painter.setPen(pen)
            painter.drawRoundedRect(self.__barRect, self.__barRadius, self.__barRadius)

        pen.setColor(self.__lineColor)
        painter.setPen(pen)

        offset = Decimal(self.__lineWidth) / 2  # decimal.Decimal
        if self.__barStyle == NavBar.BarStyle.BARSTYLE_LINE_TOP:
            painter.drawLine(self.__barRect.left(), self.__barRect.top() + offset,
                             self.__barRect.right(), self.__barRect.top() + offset)
        elif self.__barStyle == NavBar.BarStyle.BARSTYLE_LINE_TOP:
            painter.drawLine(self.__barRect.right() - offset, self.__barRect.top(),
                             self.__barRect.right() - offset, self.__barRect.bottom())
        elif self.__barStyle == NavBar.BarStyle.BARSTYLE_LINE_TOP:
            painter.drawLine(self.__barRect.left(), self.__barRect.bottom() - offset,
                             self.__barRect.right(), self.__barRect.bottom() - offset)
        elif self.__barStyle == NavBar.BarStyle.BARSTYLE_LINE_TOP:
            painter.drawLine(self.__barRect.left() + offset, self.__barRect.top(),
                             self.__barRect.left() + offset, self.__barRect.bottom())

        # 这里还可以增加右侧倒三角型

        painter.restore()
    # drawBar

    def drawText(self, painter):  # drawText(self, painter: PySide2.QtGui.QPainter)
        """  """
        painter.save()
        textFont = QFont()  # PySide2.QtGui.QFont
        textFont.setBold(True)
        painter.setFont(textFont)

        count = len(self.__listItem)  # int
        self.__initLen = 0

        # 横向导航时，字符区域取条目元素中最长的字符宽度
        longText = ""  # str
        for item in self.__items.split("|"):
            if len(item) > len(longText):
                longText = item

        if self.horizontal:
            textLen = painter.fontMetrics().width(longText)  # decimal.Decimal
        else:
            textLen = painter.fontMetrics().height()  # decimal.Decimal

        # 逐个绘制元素列表中的文字及文字背景
        for i in range(count):
            strText = self.__listItem[i][0]  # str
            left = QPointF(self.__initLen, 0)
            right = QPointF(self.__initLen + textLen + self.__space, self.height())

            if not self.horizontal:
                left = QPointF(0, self.__initLen)
                right = QPointF(self.width(), self.__initLen + textLen + self.__space)

            textRect = QRectF(left, right)
            self.__listItem[i][1] = textRect

            if self.__isVirgin:
                self.__barRect = textRect
                self.__isVirgin = False

            # 当前选中区域的文字显示选中文字颜色
            if textRect == self.__listItem[self.__currentIndex][1]:
                painter.setPen(self.__textSelectColor)
            else:
                painter.setPen(self.__textNormalColor)

            painter.drawText(textRect, Qt.AlignCenter, strText)
            self.__initLen += textLen + self.__space

        painter.restore()
    # drawText

    def __slide(self):  # __slide(self)
        """ 滑动绘制 """
        if self.__step > 1:
            self.__step -= 1

        if self.horizontal:
            self.__barLen = self.__barRect.topLeft().x()
        else:
            self.__barLen = self.__barRect.topLeft().y()

        if self.__isForward:
            self.__barLen += self.__step
            if self.__barLen >= self.__targetLen:
                self.__barLen = self.__targetLen
                self.__timer.stop()
        else:
            self.__barLen -= self.__step
            if self.__barLen <= self.__targetLen:
                self.__barLen = self.__targetLen
                self.__timer.stop()

        if self.horizontal:
            self.__barRect = QRectF(QPointF(self.__barLen, 0),
                                    QPointF(self.__barLen + self.__barRect.width(), self.height()))
        else:
            self.__barRect = QRectF(QPointF(0, self.__barLen),
                                    QPointF(self.width(), self.__barLen + self.__barRect.height()))

        self.update()
    # __slide

    def getBgColorStart(self):  # getBgColorStart() -> PySide2.QtGui.QColor
        """ 读取导航条主背景渐变开始颜色 """
        return self.__bgColorStart
    # getBgColorStart

    def setBgColorStart(self, color_start):  # setBgColorStart(self, color_start: PySide2.QtGui.QColor)
        """ 设置导航条主背景渐变开始颜色 """
        if self.__bgColorStart != color_start:
            self.__bgColorStart = color_start
            self.update()
    # setBgColorStart

    def getBgColorEnd(self):  # getBgColorEnd(self) -> PySide2.QtGui.QColor
        """ 读取导航条主背景渐变结束颜色 """
        return self.__bgColorEnd
    # getBgColorEnd

    def setBgColorEnd(self, color_end):  # setBgColorEnd(self, color_end: PySide2.QtGui.QColor)
        """ 设置导航条主背景渐变结束颜色 """
        if self.__bgColorEnd != color_end:
            self.__bgColorEnd = color_end
            self.__old_bgColorEnd = color_end
            self.update()
    # setBgColorEnd

    def getBarColorStart(self):  # getBarColorStart(self) -> PySide2.QtGui.QColor
        """ 读取导航条当前条目渐变开始颜色 """
        return self.__barColorStart
    # getBarColorStart

    def setBarColorStart(self, color_start):  # setBarColorStart(self, color_start: PySide2.QtGui.QColor)
        """ 设置导航条当前条目渐变开始颜色 """
        if self.__barColorStart != color_start:
            self.__barColorStart = color_start
            self.update()
    # setBarColorStart

    def getBarColorEnd(self):  # getBarColorEnd(self) -> PySide2.QtGui.QColor
        """ 读取导航条当前条目渐变结束颜色 """
        return self.__barColorEnd
    # getBarColorEnd

    def setBarColorEnd(self, color_end):  # setBarColorEnd(self, color_end: PySide2.QtGui.QColor)
        """ 设置导航条当前条目渐变结束颜色 """
        if self.__barColorEnd != color_end:
            self.__barColorEnd = color_end
            self.__old_barColorEnd = color_end
            self.update()
    # setBarColorEnd

    def getTextNormalColor(self):  # getTextNormalColor(self) -> PySide2.QtGui.QColor
        """ 读取文字正常颜色 """
        return self.__textNormalColor
    # getTextNormalColor

    def setTextNormalColor(self, normal_color):  # setTextNormalColor(self, normal_color: PySide2.QtGui.QColor)
        """ 设置文字正常颜色 """
        if self.__textNormalColor != normal_color:
            self.__textNormalColor = normal_color
            self.update()
    # setTextNormalColor

    def getTextSelectColor(self):  # getTextSelectColor(self) -> PySide2.QtGui.QColor
        """ 读取文字选中颜色 """
        return self.__textSelectColor
    # getTextSelectColor

    def setTextSelectColor(self, select_color):  # setTextSelectColor(self, select_color: PySide2.QtGui.QColor)
        """ 设置文字选中颜色 """
        if self.__textSelectColor != select_color:
            self.__textSelectColor = select_color
            self.update()
    # setTextSelectColor

    def getItems(self):  # getItems(self) -> str
        """ 读取所有条目文字信息 """
        return self.__items
    # getItems

    def setItems(self, items):  # setItems(self, items: str)
        """ 设置所有条目文字信息 """
        self.__items = items
        self.__listItem.clear()

        for item in items.split("|"):
            self.__listItem.append([item, QRectF()])

        self.update()
    # setItems

    def getCurrentIndex(self):  # getCurrentIndex(self) -> int
        """ 读取当前选中条目索引 """
        return self.__currentIndex
    # getCurrentIndex

    def setCurrentIndex(self, index):  # setCurrentIndex(self, index: int)
        """ 设置当前选中条目索引 """
        self.moveTo_int(index)
    # setCurrentIndex

    def getCurrentItem(self):  # getCurrentItem(self) -> str
        """ 读取当前选中条目文字 """
        return self.__currentItem
    # getCurrentItem

    def setCurrentItem(self, item):  # setCurrentItem(self, item: str)
        """ 设置当前选中条目文字 """
        self.moveTo_str(item)
    # setCurrentItem

    def getBgRadius(self):  # getBgRadius(self) -> int
        """ 读取背景圆角半径 """
        return self.__bgRadius
    # getBgRadius

    def setBgRadius(self, radius):  # setBgRadius(self, radius: int)
        """ 设置背景圆角半径 """
        if self.__bgRadius != radius:
            self.__bgRadius = radius
            self.update()
    # setBgRadius

    def getBarRadius(self):  # getBarRadius(self) -> int
        """ 读取选中条目背景圆角半径 """
        return self.__barRadius
    # getBarRadius

    def setBarRadius(self, radius):  # setBarRadius(self, radius: int)
        """ 设置选中条目背景圆角半径 """
        if self.__barRadius != radius:
            self.__barRadius = radius
            self.update()
    # setBarRadius

    def getSpace(self):  # getSpace(self) -> int
        """ 读取条目元素之间的间距 """
        return self.__space
    # getSpace

    def setSpace(self, space):  # setSpace(self, space: int)
        """ 设置条目元素之间的间距 """
        if self.space != space:
            self.space = space
            self.update()
    # setSpace

    def getLineWidth(self):  # getLineWidth(self) -> int
        """ 读取线条宽度 """
        return self.__lineWidth
    # getLineWidth

    def setLineWidth(self, line_width):  # setLineWidth(self, line_width: int)
        """ 设置线条宽度 """
        if self.__lineWidth != line_width:
            self.__lineWidth = line_width
            self.update()
    # setLineWidth

    def getLineColor(self):  # getLineColor(self) -> PySide2.QtGui.QColor
        """ 读取线条颜色 """
        return self.__lineColor
    # getLineColor

    def setLineColor(self, line_color):  # setLineColor(self, line_color: PySide2.QtGui.QColor)
        """ 设置线条颜色 """
        if self.__lineColor != line_color:
            self.__lineColor = line_color
            self.update()
    # setLineColor

    def getBarStyle(self):  # getBarStyle(self) -> typing.enum[BarStyle]
        """ 读取选中元素样式 """
        return self.__barStyle
    # getBarStyle

    def setBarStyle(self, bar_style):  # setBarStyle(self, bar_style: typing.enum[BarStyle])
        """ 设置选中元素样式 """
        if self.__barStyle != bar_style:
            self.__barStyle = bar_style
            self.update()
    # setBarStyle

    def getKeyMove(self):  # getKeyMove(self) -> bool
        """ 读取是否支持按键移动 """
        return self.__keyMove
    # getKeyMove

    def setKeyMove(self, key_move):  # setKeyMove(self, key_move: bool)
        """ 设置是否支持按键移动 """
        if self.__keyMove != key_move:
            self.__keyMove = key_move
            if key_move:
                self.setFocusPolicy(Qt.StrongFocus)
            else:
                self.setFocusPolicy(Qt.NoFocus)
    # setKeyMove

    def getHorizontal(self):  # getHorizontal(self) -> bool
        """ 读取是否横向显示 """
        return self.__horizontal
    # getHorizontal

    def setHorizontal(self, horizontal):  # setHorizontal(self, horizontal: bool)
        """ 设置是否横向显示 """
        if self.__horizontal != horizontal:
            self.__horizontal = horizontal
            self.update()
    # setHorizontal

    def getFlat(self):  # getFlat(self) -> bool
        """ 读取是否扁平化 """
        return self.__flat
    # getFlat

    def setFlat(self, flat):  # setFlat(self, flat: bool)
        """ 设置是否扁平化 """
        if self.__flat != flat:
            # 扁平后将初始颜色赋值给结束颜色达到扁平的效果，如果取消扁平则再次恢复原有的颜色
            if flat:
                self.__bgColorEnd = self.__bgColorStart
                self.__barColorEnd = self.__barColorStart
            else:
                self.__bgColorEnd = self.__old_bgColorEnd
                self.__barColorEnd = self.__old_barColorEnd

            self.__flat = flat
            self.update()
    # setFlat

    def sizeHint(self):  # sizeHint(self) -> PySide2.QtCore.QSize
        """ 返回控件默认大小 """
        return QSize(400, 30)
    # sizeHint

    def minimumSizeHint(self):  # minimumSizeHint(self) -> PySide2.QtCore.QSize
        """ 返回控件最小大小 """
        return QSize(30, 30)
    # minimumSizeHint

    def clearItem(self):  # clearItem(self)
        """ 删除所有条目 """
        self.__listItem.clear()
        self.update()
    # clearItem

    def moveFirst(self):  # moveFirst(self)
        """ 移动到第一个条目 """
        index = 0  # int
        if self.__currentIndex != index:
            self.moveTo_int(index)
    # moveFirst

    def moveLast(self):  # moveFirst(self)
        """ 移动到最后一个条目 """
        index = len(self.__listItem) - 1
        if self.__currentIndex != index:
            self.moveTo_int(index)
    # moveLast

    def movePrevious(self):  # movePrevious(self)
        """ 往前移动条目 """
        if self.__currentIndex > 0:
            self.__currentIndex -= 1
            self.moveTo_int(self.__currentIndex)
    # movePrevious

    def moveNext(self):  # moveNext(self)
        """ 往后移动条目 """
        if self.__currentIndex < (len(self.__listItem) - 1):
            self.__currentIndex += 1
            self.moveTo_int(self.__currentIndex)
    # moveNext

    def moveTo_int(self, index):  # moveTo(self, index: int)
        """ 移动到指定索引条目 """
        if (index >= 0) and (len(self.__listItem) > index):
            rec = QRectF(self.__listItem[index][1])  # PySide2.QtCore.QRectF
            pos = QPoint(int(rec.x()), int(rec.y()))  # PySide2.QtCore.QPoint
            self.moveTo_point(pos)
    # moveTo

    def moveTo_str(self, item):  # moveTo(self, item: str)
        """ 移动到指定文字条目 """
        count = len(self.__listItem)  # int
        for i in range(count):
            if self.__listItem[i][0] == item:
                self.moveTo_int(i)
                break
    # moveTo

    def moveTo_point(self, point):  # moveTo(self, point: PySide2.QtCore.QPointF)
        """ 移动到指定坐标位置条目 """
        count = len(self.__listItem)
        for i in range(count):
            # 如果不是最后一个，则辨别指定项
            if i != (count - 1):
                # 辨别方法，如果不在两项之间，则不是指定项
                if self.__horizontal:
                    if not ((point.x() >= self.__listItem[i][1].topLeft().x()) and
                            (point.x() < self.__listItem[i + 1][1].topLeft().x())):
                        continue
                else:
                    if not ((point.y() >= self.__listItem[i][1].topLeft().y()) and
                            (point.y() < self.__listItem[i + 1][1].topLeft().y())):
                        continue

            self.__currentIndex = i
            self.__currentItem = self.__listItem[i][0]
            self.__targetRect = self.__listItem[i][1]

            if self.__horizontal:
                self.__targetLen = self.__targetRect.topLeft().x()
                self.__barLen = self.__barRect.topLeft().x()
            else:
                self.__targetLen = self.__targetRect.topLeft().y()
                self.__barLen = self.__barRect.topLeft().y()

            self.__isForward = (self.__targetLen > self.__barLen)
            distance = abs(self.__targetLen - self.__barLen)  # int

            # 重新获取每次移动的步长
            self.__step = self.__initStep(distance)
            self.__timer.start()

            self.currentItemChanged.emit(self.__currentIndex, self.__currentItem)
            break
    # moveTo

    bgColorStart = property(fget=getBgColorStart, fset=setBgColorStart, fdel=None, doc="导航条主背景渐变开始颜色")  # PySide2.QtGui.QColor
    bgColorEnd = property(fget=getBgColorEnd, fset=setBgColorEnd, fdel=None, doc="导航条主背景渐变结束颜色")  # PySide2.QtGui.QColor

    barColorStart = property(fget=getBarColorStart, fset=setBarColorStart, fdel=None, doc="导航条当前条目渐变开始颜色")  # PySide2.QtGui.QColor
    barColorEnd = property(fget=getBarColorEnd, fset=setBarColorEnd, fdel=None, doc="导航条当前条目渐变结束颜色")  # PySide2.QtGui.QColor

    textNormalColor = property(fget=getTextNormalColor, fset=setTextNormalColor, fdel=None, doc="文字正常颜色")  # PySide2.QtGui.QColor
    textSelectColor = property(fget=getTextSelectColor, fset=setTextSelectColor, fdel=None, doc="文字选中颜色")  # PySide2.QtGui.QColor

    items = property(fget=getItems, fset=setItems, fdel=None, doc="所有条目文字信息")  # str
    currentIndex = property(fget=getCurrentIndex, fset=setCurrentIndex, fdel=None, doc="当前选中条目索引")  # int
    currentItem = property(fget=getCurrentItem, fset=setCurrentItem, fdel=None, doc="当前选中条目文字")  # str

    bgRadius = property(fget=getBgRadius, fset=setBgRadius, fdel=None, doc="背景圆角半径")  # int
    barRadius = property(fget=getBarRadius, fset=setBarRadius, fdel=None, doc="选中条目背景圆角半径")  # int
    space = property(fget=getSpace, fset=setSpace, fdel=None, doc="条目元素之间的间距")  # int

    lineWidth = property(fget=getLineWidth, fset=setLineWidth, fdel=None, doc="线条宽度")  # int
    lineColor = property(fget=getLineColor, fset=setLineColor, fdel=None, doc="线条颜色")  # PySide2.QtGui.QColor

    barStyle = property(fget=getBarStyle, fset=setBarStyle, fdel=None, doc="选中元素样式")  # typing.enum[NavBar.BarStyle])

    keyMove = property(fget=getKeyMove, fset=setKeyMove, fdel=None, doc="是否支持按键移动")  # bool
    horizontal = property(fget=getHorizontal, fset=setHorizontal, fdel=None, doc="是否横向显示")  # bool
    flat = property(fget=getFlat, fset=setFlat, fdel=None, doc="是否扁平化")  # bool


if __name__ == '__main__':
    import sys

    def printCurrentItem(index, item):  # printCurrentItem(index: int, item: str)
        print("当前项目：{} - {}".format(index, item))

    app = QApplication(sys.argv)

    button = NavBar()
    button.setItems("欢迎|编辑|设计|Debug|项目|帮助")
    button.resize(60, 300)
    button.currentItemChanged.connect(printCurrentItem)
    button.show()
    button.moveFirst()

    app.exec_()

