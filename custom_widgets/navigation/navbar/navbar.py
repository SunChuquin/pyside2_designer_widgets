from typing import List, Union

from enum import Enum
from decimal import Decimal
from PySide2.QtGui import QColor, QPainter, QLinearGradient, QPen, QFont, QResizeEvent, QMouseEvent, QKeyEvent, QPaintEvent
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
    currentItemChanged: Signal = Signal(int, str)  # int: 当前条目的索引, str: 当前条目的文字

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
        self.__bgColorStart: QColor = QColor(121, 121, 121)
        # 导航条主背景渐变结束颜色
        self.__bgColorEnd: QColor = QColor(78, 78, 78)
        # 用于扁平化切换
        self.__old_bgColorEnd: QColor = self.__bgColorEnd

        # 导航条当前条目渐变开始颜色
        self.__barColorStart: QColor = QColor(46, 132, 243)
        # 导航条当前条目渐变结束颜色
        self.__barColorEnd: QColor = QColor(39, 110, 203)
        # 用于扁平化切换
        self.__old_barColorEnd: QColor = self.__barColorEnd

        # 文字正常颜色
        self.__textNormalColor: QColor = QColor(230, 230, 230)
        # 文字选中颜色
        self.__textSelectColor: QColor = QColor(255, 255, 255)

        # 所有条目文字信息
        self.__items: str = ""
        # 当前选中条目索引
        self.__currentIndex: int = -1
        # 当前选中条目文字
        self.__currentItem: str = ""

        # 背景圆角半径
        self.__bgRadius: int = 0
        # 选中条目背景圆角半径
        self.__barRadius: int = 0
        # 条目元素之间的间距
        self.__space: int = 25

        # 线条宽度
        self.__lineWidth: int = 3
        # 线条颜色
        self.__lineColor: QColor = QColor(255, 107, 107)

        # 选中元素样式
        self.__barStyle: NavBar.BarStyle = NavBar.BarStyle.BARSTYLE_RECT

        # 是否支持按键移动
        self.__keyMove: bool = True
        # 是否横向显示
        self.__horizontal: bool = False
        # 是否扁平化
        self.__flat: bool = False

        # 元素集合,成对出现,元素的名字,矩形区域范围
        self.__listItem: list = []

        # 选中区域的矩形
        self.__barRect: QRectF = QRectF()
        # 目标区域的矩形
        self.__targetRect: QRectF = QRectF()
        # 选中区域的长度
        self.__barLen: Decimal = Decimal(0)
        # 目标区域的长度
        self.__targetLen: Decimal = Decimal(0)

        # 导航条的长度
        self.__initLen: Decimal = Decimal(10)
        # 每次移动的步长
        self.__step: int = 0

        # 是否往前移动
        self.__isForward: bool = True
        # 是否首次处理
        self.__isVirgin: bool = True
        # 滑动绘制定时器
        self.__timer: QTimer = QTimer(self)
        self.__timer.setInterval(10)
        self.__timer.timeout.connect(self.__slide)

        self.setItems("主界面|系统设置|防区管理|警情查询|视频预览")

    @staticmethod
    def __initStep(distance: int) -> int:
        """ 计算步长 """
        n: int = 1
        while True:
            if (n * n) > distance:
                break
            else:
                n += 1

        return int(n * 1.4)

    def resizeEvent(self, event: QResizeEvent):
        """ 控件大小调整事件 """
        index: int = 0
        count: int = len(self.__listItem)
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

    def mousePressEvent(self, event: QMouseEvent):
        """ 鼠标按压信号 """
        self.moveTo_point(event.pos())

    def keyPressEvent(self, event: QKeyEvent):
        """  """
        if not self.__keyMove:
            return

        if (event.key() == Qt.Key_Left) or (event.key() == Qt.Key_Up):
            self.movePrevious()
        elif (event.key() == Qt.Key_Right) or (event.key() == Qt.Key_Down):
            self.moveNext()

    def paintEvent(self, event: QPaintEvent):
        """  """
        # 绘制准备工作，启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景色
        self.drawBg(painter)
        # 绘制当前条目选中背景
        self.drawBar(painter)
        # 绘制条目文字
        self.drawText(painter)

    def drawBg(self, painter: QPainter):
        """ 绘制背景色 """
        painter.save()
        painter.setPen(Qt.NoPen)
        bgGradient: QLinearGradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))
        bgGradient.setColorAt(0.0, self.__bgColorStart)
        bgGradient.setColorAt(1.0, self.__bgColorEnd)
        painter.setBrush(bgGradient)
        painter.drawRoundedRect(self.rect(), self.__bgRadius, self.__bgRadius)
        painter.restore()

    def drawBar(self, painter: QPainter):
        """ 绘制当前条目选中背景 """
        painter.save()
        pen: QPen = QPen()  # PySide2.QtGui.QPen

        barGradient: QLinearGradient = QLinearGradient(self.__barRect.topLeft(), self.__barRect.bottomLeft())
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

        offset: Decimal = Decimal(self.__lineWidth) / 2
        if self.__barStyle == NavBar.BarStyle.BARSTYLE_LINE_TOP:
            painter.drawLine(int(self.__barRect.left()), self.__barRect.top() + offset,
                             int(self.__barRect.right()), self.__barRect.top() + offset)
        elif self.__barStyle == NavBar.BarStyle.BARSTYLE_LINE_TOP:
            painter.drawLine(self.__barRect.right() - offset, int(self.__barRect.top()),
                             self.__barRect.right() - offset, int(self.__barRect.bottom()))
        elif self.__barStyle == NavBar.BarStyle.BARSTYLE_LINE_TOP:
            painter.drawLine(int(self.__barRect.left()), self.__barRect.bottom() - offset,
                             int(self.__barRect.right()), self.__barRect.bottom() - offset)
        elif self.__barStyle == NavBar.BarStyle.BARSTYLE_LINE_TOP:
            painter.drawLine(self.__barRect.left() + offset, int(self.__barRect.top()),
                             self.__barRect.left() + offset, int(self.__barRect.bottom()))

        # 这里还可以增加右侧倒三角型

        painter.restore()

    def drawText(self, painter: QPainter):
        """  """
        painter.save()
        textFont: QFont = QFont()
        textFont.setBold(True)
        painter.setFont(textFont)

        count: int = len(self.__listItem)
        self.__initLen = 0

        # 横向导航时，字符区域取条目元素中最长的字符宽度
        longText: str = ""
        for item in self.__items.split("|"):
            if len(item) > len(longText):
                longText = item

        if self.horizontal:
            textLen: Decimal = Decimal(painter.fontMetrics().width(longText))
        else:
            textLen: Decimal = Decimal(painter.fontMetrics().height())

        # 逐个绘制元素列表中的文字及文字背景
        for i in range(count):
            strText: str = self.__listItem[i][0]
            left: QPointF = QPointF(self.__initLen, 0)
            right: QPointF = QPointF(self.__initLen + textLen + self.__space, self.height())

            if not self.horizontal:
                left = QPointF(0, self.__initLen)
                right = QPointF(self.width(), self.__initLen + textLen + self.__space)

            textRect: QRectF = QRectF(left, right)
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

    def __slide(self):
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

    def getBgColorStart(self) -> QColor:
        """ 读取导航条主背景渐变开始颜色 """
        return self.__bgColorStart

    def setBgColorStart(self, color_start: QColor):
        """ 设置导航条主背景渐变开始颜色 """
        if self.__bgColorStart != color_start:
            self.__bgColorStart = color_start
            self.update()

    def getBgColorEnd(self) -> QColor:
        """ 读取导航条主背景渐变结束颜色 """
        return self.__bgColorEnd

    def setBgColorEnd(self, color_end: QColor):
        """ 设置导航条主背景渐变结束颜色 """
        if self.__bgColorEnd != color_end:
            self.__bgColorEnd = color_end
            self.__old_bgColorEnd = color_end
            self.update()

    def getBarColorStart(self) -> QColor:
        """ 读取导航条当前条目渐变开始颜色 """
        return self.__barColorStart

    def setBarColorStart(self, color_start: QColor):
        """ 设置导航条当前条目渐变开始颜色 """
        if self.__barColorStart != color_start:
            self.__barColorStart = color_start
            self.update()

    def getBarColorEnd(self) -> QColor:
        """ 读取导航条当前条目渐变结束颜色 """
        return self.__barColorEnd

    def setBarColorEnd(self, color_end: QColor):
        """ 设置导航条当前条目渐变结束颜色 """
        if self.__barColorEnd != color_end:
            self.__barColorEnd = color_end
            self.__old_barColorEnd = color_end
            self.update()

    def getTextNormalColor(self) -> QColor:
        """ 读取文字正常颜色 """
        return self.__textNormalColor

    def setTextNormalColor(self, normal_color: QColor):
        """ 设置文字正常颜色 """
        if self.__textNormalColor != normal_color:
            self.__textNormalColor = normal_color
            self.update()

    def getTextSelectColor(self) -> QColor:
        """ 读取文字选中颜色 """
        return self.__textSelectColor

    def setTextSelectColor(self, select_color: QColor):
        """ 设置文字选中颜色 """
        if self.__textSelectColor != select_color:
            self.__textSelectColor = select_color
            self.update()

    def getItems(self) -> str:
        """ 读取所有条目文字信息 """
        return self.__items

    def setItems(self, items: str):
        """ 设置所有条目文字信息 """
        self.__items = items
        self.__listItem.clear()

        for item in items.split("|"):
            self.__listItem.append([item, QRectF()])

        self.update()

    def getCurrentIndex(self) -> int:
        """ 读取当前选中条目索引 """
        return self.__currentIndex

    def setCurrentIndex(self, index: int):
        """ 设置当前选中条目索引 """
        self.moveTo_int(index)

    def getCurrentItem(self) -> str:
        """ 读取当前选中条目文字 """
        return self.__currentItem

    def setCurrentItem(self, item: str):
        """ 设置当前选中条目文字 """
        self.moveTo_str(item)

    def getBgRadius(self) -> int:
        """ 读取背景圆角半径 """
        return self.__bgRadius

    def setBgRadius(self, radius: int):
        """ 设置背景圆角半径 """
        if self.__bgRadius != radius:
            self.__bgRadius = radius
            self.update()

    def getBarRadius(self) -> int:
        """ 读取选中条目背景圆角半径 """
        return self.__barRadius

    def setBarRadius(self, radius: int):
        """ 设置选中条目背景圆角半径 """
        if self.__barRadius != radius:
            self.__barRadius = radius
            self.update()

    def getSpace(self) -> int:
        """ 读取条目元素之间的间距 """
        return self.__space

    def setSpace(self, space: int):
        """ 设置条目元素之间的间距 """
        if self.space != space:
            self.space = space
            self.update()

    def getLineWidth(self) -> int:
        """ 读取线条宽度 """
        return self.__lineWidth

    def setLineWidth(self, line_width: int):
        """ 设置线条宽度 """
        if self.__lineWidth != line_width:
            self.__lineWidth = line_width
            self.update()

    def getLineColor(self) -> QColor:
        """ 读取线条颜色 """
        return self.__lineColor

    def setLineColor(self, line_color: QColor):
        """ 设置线条颜色 """
        if self.__lineColor != line_color:
            self.__lineColor = line_color
            self.update()

    def getBarStyle(self) -> BarStyle:
        """ 读取选中元素样式 """
        return self.__barStyle

    def setBarStyle(self, bar_style: BarStyle):
        """ 设置选中元素样式 """
        if self.__barStyle != bar_style:
            self.__barStyle = bar_style
            self.update()

    def getKeyMove(self) -> bool:
        """ 读取是否支持按键移动 """
        return self.__keyMove

    def setKeyMove(self, key_move: bool):
        """ 设置是否支持按键移动 """
        if self.__keyMove != key_move:
            self.__keyMove = key_move
            if key_move:
                self.setFocusPolicy(Qt.StrongFocus)
            else:
                self.setFocusPolicy(Qt.NoFocus)

    def getHorizontal(self) -> bool:
        """ 读取是否横向显示 """
        return self.__horizontal

    def setHorizontal(self, horizontal: bool):
        """ 设置是否横向显示 """
        if self.__horizontal != horizontal:
            self.__horizontal = horizontal
            self.update()

    def getFlat(self) -> bool:
        """ 读取是否扁平化 """
        return self.__flat

    def setFlat(self, flat: bool):
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

    def sizeHint(self) -> QSize:
        """ 返回控件默认大小 """
        return QSize(400, 30)

    def minimumSizeHint(self) -> QSize:
        """ 返回控件最小大小 """
        return QSize(30, 30)

    def clearItem(self):
        """ 删除所有条目 """
        self.__listItem.clear()
        self.update()

    def moveFirst(self):
        """ 移动到第一个条目 """
        index: int = 0
        if self.__currentIndex != index:
            self.moveTo_int(index)

    def moveLast(self):
        """ 移动到最后一个条目 """
        index = len(self.__listItem) - 1
        if self.__currentIndex != index:
            self.moveTo_int(index)

    def movePrevious(self):
        """ 往前移动条目 """
        if self.__currentIndex > 0:
            self.__currentIndex -= 1
            self.moveTo_int(self.__currentIndex)

    def moveNext(self):
        """ 往后移动条目 """
        if self.__currentIndex < (len(self.__listItem) - 1):
            self.__currentIndex += 1
            self.moveTo_int(self.__currentIndex)

    def moveTo_int(self, index: int):
        """ 移动到指定索引条目 """
        if (index >= 0) and (len(self.__listItem) > index):
            rec: QRectF = QRectF(self.__listItem[index][1])
            pos: QPoint = QPoint(int(rec.x()), int(rec.y()))
            self.moveTo_point(pos)

    def moveTo_str(self, item: str):
        """ 移动到指定文字条目 """
        count: int = len(self.__listItem)
        for i in range(count):
            if self.__listItem[i][0] == item:
                self.moveTo_int(i)
                break

    def moveTo_point(self, point: QPointF):
        """ 移动到指定坐标位置条目 """
        count: int = len(self.__listItem)
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
            distance: int = int(abs(self.__targetLen - self.__barLen))

            # 重新获取每次移动的步长
            self.__step = self.__initStep(int(distance))
            self.__timer.start()

            self.currentItemChanged.emit(self.__currentIndex, self.__currentItem)
            break

    bgColorStart: QColor = property(fget=getBgColorStart, fset=setBgColorStart, fdel=None, doc="导航条主背景渐变开始颜色")
    bgColorEnd: QColor = property(fget=getBgColorEnd, fset=setBgColorEnd, fdel=None, doc="导航条主背景渐变结束颜色")

    barColorStart: QColor = property(fget=getBarColorStart, fset=setBarColorStart, fdel=None, doc="导航条当前条目渐变开始颜色")
    barColorEnd: QColor = property(fget=getBarColorEnd, fset=setBarColorEnd, fdel=None, doc="导航条当前条目渐变结束颜色")

    textNormalColor: QColor = property(fget=getTextNormalColor, fset=setTextNormalColor, fdel=None, doc="文字正常颜色")
    textSelectColor: QColor = property(fget=getTextSelectColor, fset=setTextSelectColor, fdel=None, doc="文字选中颜色")

    items: str = property(fget=getItems, fset=setItems, fdel=None, doc="所有条目文字信息")
    currentIndex: int = property(fget=getCurrentIndex, fset=setCurrentIndex, fdel=None, doc="当前选中条目索引")
    currentItem: str = property(fget=getCurrentItem, fset=setCurrentItem, fdel=None, doc="当前选中条目文字")

    bgRadius: int = property(fget=getBgRadius, fset=setBgRadius, fdel=None, doc="背景圆角半径")
    barRadius: int = property(fget=getBarRadius, fset=setBarRadius, fdel=None, doc="选中条目背景圆角半径")
    space: int = property(fget=getSpace, fset=setSpace, fdel=None, doc="条目元素之间的间距")

    lineWidth: int = property(fget=getLineWidth, fset=setLineWidth, fdel=None, doc="线条宽度")
    lineColor: QColor = property(fget=getLineColor, fset=setLineColor, fdel=None, doc="线条颜色")

    barStyle: BarStyle = property(fget=getBarStyle, fset=setBarStyle, fdel=None, doc="选中元素样式")

    keyMove: bool = property(fget=getKeyMove, fset=setKeyMove, fdel=None, doc="是否支持按键移动")
    horizontal: bool = property(fget=getHorizontal, fset=setHorizontal, fdel=None, doc="是否横向显示")
    flat: bool = property(fget=getFlat, fset=setFlat, fdel=None, doc="是否扁平化")


if __name__ == '__main__':
    import sys

    def printCurrentItem(index: int, item: str):
        print("当前项目：{} - {}".format(index, item))

    app: QApplication = QApplication(sys.argv)

    button: NavBar = NavBar()
    button.setItems("欢迎|编辑|设计|Debug|项目|帮助")
    button.resize(60, 300)
    button.currentItemChanged.connect(printCurrentItem)
    button.show()
    button.moveFirst()

    sys.exit(app.exec_())

