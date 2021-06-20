from typing import List, AnyStr
from PySide2.QtCore import QSize, Signal, Qt, QRect
from PySide2.QtGui import QColor, QWheelEvent, QMouseEvent, QPaintEvent, QPainter, QFont, QPen
from PySide2.QtWidgets import QWidget

class Tumbler(QWidget):
    """
    滑动选择器控件
    作者:feiyangqingyun(QQ:517216493) 2016-11-24
    译者:sunchuquin(QQ:1715216365) 2021-06-20
    1. 可设置数据队列值
    2. 可设置当前队列索引及当前值
    2. 支持任意窗体大小缩放
    3. 支持背景色前景色文字颜色线条颜色设置
    4. 支持左右滑动和上下滑动两种形式
    5. 支持鼠标滚动切换元素
    6. 中间值自动放大显示且居中
    """

    currentIndexChanged = Signal(int)  # currentIndex
    currentValueChanged = Signal(str)  # currentValue

    def __init__(self, parent: QWidget = None):
        super(Tumbler, self).__init__(parent)
        self.__listValue: List[AnyStr] = list(str(i) for i in range(1, 13))  # 值队列
        self.__currentIndex: int = 0  # 当前索引
        self.__currentValue: str = '1'  # 当前值
        self.__horizontal: bool = False  # 是否横向显示

        self.__foreground: QColor = QColor(140, 140, 140)  # 前景色
        self.__background: QColor = QColor(40, 40, 40)  # 背景色
        self.__lineColor: QColor = QColor(46, 142, 180, 200)  # 线条颜色
        self.__textColor: QColor = QColor(255, 255, 255)  # 当前文本颜色

        self.__percent: int = 3  # 比例
        self.__offset: int = 0  # 偏离值
        self.__pressed: bool = False  # 鼠标是否按下
        self.__pressedPos: int = 0  # 按下处坐标
        self.__currentPos: int = 0  # 当前值对应起始坐标

        self.__oldIndex: int = -1  # 记录上一次的索引

        self.setFont(QFont("Arial", 8))

    @property
    def listValue(self) -> List[AnyStr]: return self.__listValue

    @listValue.setter
    def listValue(self, list_value: List[AnyStr]) -> None:
        if list_value.__len__() <= 0: return

        self.__listValue = list_value
        self.currentIndex = 0
        self.currentValue = list_value[0]
        self.update()

    @property
    def currentIndex(self) -> int: return self.__currentIndex

    @currentIndex.setter
    def currentIndex(self, current_index: int) -> None:
        if current_index < 0: return

        self.__currentIndex = current_index
        self.__currentValue = self.__listValue[current_index]
        self.currentIndexChanged.emit(self.__currentIndex)
        self.currentValueChanged.emit(self.__currentValue)
        self.update()

    @property
    def currentValue(self) -> str: return self.__currentValue

    @currentValue.setter
    def currentValue(self, current_value: str) -> None:
        if not self.__listValue.count(current_value): return

        self.__currentValue = current_value
        self.__currentIndex = self.__listValue.index(current_value)
        self.currentIndexChanged.emit(self.currentIndex)
        self.currentValueChanged.emit(self.currentValue)
        self.update()

    @property
    def horizontal(self) -> bool: return self.__horizontal

    @horizontal.setter
    def horizontal(self, n_horizontal: bool) -> None:
        if self.__horizontal == n_horizontal: return

        self.__horizontal = n_horizontal
        self.update()

    @property
    def foreground(self) -> QColor: return self.__foreground

    @foreground.setter
    def foreground(self, n_foreground: QColor) -> None:
        if self.__horizontal == n_foreground: return

        self.__foreground = n_foreground
        self.update()

    @property
    def background(self) -> QColor: return self.__background

    @background.setter
    def background(self, n_background: QColor) -> None:
        if self.__horizontal == n_background: return

        self.__background = n_background
        self.update()

    @property
    def lineColor(self) -> QColor: return self.__lineColor

    @lineColor.setter
    def lineColor(self, line_color: QColor) -> None:
        if self.__horizontal == line_color: return

        self.__lineColor = line_color
        self.update()

    @property
    def textColor(self) -> QColor: return self.__textColor

    @textColor.setter
    def textColor(self, text_color: QColor) -> None:
        if self.__horizontal == text_color: return

        self.__textColor = text_color
        self.update()

    def wheelEvent(self, event: QWheelEvent) -> None:
        degrees: int = event.delta() // 8  # 滚动的角度,*8就是鼠标滚动的距离
        steps: int = degrees // 15  # 滚动的步数,*15就是鼠标滚动的角度

        # 如果是正数代表为左边移动,负数代表为右边移动
        if event.orientation() is Qt.Vertical:
            index: int = self.__currentIndex - steps
            if steps > 0:
                if index > 0: self.currentIndex = index
                else: self.currentIndex = 0
            else:
                if index < self.__listValue.__len__() - 1: self.currentIndex = index
                else: self.currentIndex = self.__listValue.__len__() - 1

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__pressed = True
        self.__pressedPos = event.pos().x() if self.__horizontal else event.pos().y()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        count: int = self.__listValue.__len__()
        if count <= 1: return

        pos: int = event.pos().x() if self.__horizontal else event.pos().y()
        target: int = self.width() if self.__horizontal else self.height()
        index: int = self.__listValue.index(self.__currentValue)

        if self.__pressed:
            # 数值到边界时,阻止继续往对应方向移动
            if index is 0 and pos >= self.__pressedPos or index is count - 1 and pos <= self.__pressedPos: return

            self.__offset = pos - self.__pressedPos

            # 若移动速度过快时进行限制
            if self.__offset > target // self.__percent:
                self.__offset = target // self.__percent
            elif self.__offset < -target // self.__percent:
                self.__offset = -target // self.__percent

            if self.__oldIndex != index:
                self.currentIndexChanged.emit(index)
                self.currentValueChanged.emit(self.__listValue[index])
                self.__oldIndex = index

            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if not self.__pressed: return
        pressed = False
        self.__checkPosition()  # 矫正到居中位置

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        count: int = self.__listValue.__len__()
        if count <= 1: return
        target: int = self.width() if self.__horizontal else self.height()
        index: int = self.__listValue.index(self.__currentValue) if self.__listValue.count(self.__currentValue) else -1

        # 当右移偏移量大于比例且当前值不是第一个则索引-1
        if self.__offset >= target // self.__percent and index > 0:
            self.__pressedPos += target // self.__percent
            self.__offset -= target // self.__percent
            index -= 1

        # 当左移偏移量小于比例且当前值不是末一个则索引+1
        if self.__offset <= -target // self.__percent and index < count - 1:
            self.__pressedPos -= target // self.__percent
            self.__offset += target // self.__percent
            index += 1

        self.__currentIndex = index
        self.__currentValue = self.__listValue[index]

        self.drawBg(painter)  # 绘制背景
        self.drawLine(painter)  # 绘制线条

        # 绘制中间值
        painter.setPen(self.__textColor)
        self.drawText(painter, index, self.__offset)
        painter.setPen(self.__foreground)

        if index != 0: self.drawText(painter, index - 1, self.__offset - target // self.__percent)  # 绘制左侧值
        if index != count - 1: self.drawText(painter, index + 1, self.__offset + target // self.__percent)  # 绘制右侧值

    def drawBg(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__background)
        painter.drawRect(self.rect())
        painter.restore()

    def drawLine(self, painter: QPainter) -> None:
        # 上下部分偏移量
        offset: int = 10
        width: int = self.width()
        height: int = self.height()

        painter.save()
        painter.setBrush(Qt.NoBrush)

        pen: QPen = QPen()
        pen.setWidth(3)
        pen.setColor(self.__lineColor)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        # 每次同时存在三个元素
        if self.__horizontal:
            painter.drawLine(width // 3 * 1, offset, width // 3 * 1, height - offset)
            painter.drawLine(width // 3 * 2, offset, width // 3 * 2, height - offset)
        else:
            painter.drawLine(offset, height // 3 * 1, width - offset,  height // 3 * 1)
            painter.drawLine(offset, height // 3 * 2, width - offset,  height // 3 * 2)

        painter.restore()

    def drawText(self, painter: QPainter, index: int, offset: int) -> None:
        painter.save()

        width: int = self.width()
        height: int = self.height()
        strValue: str = str(self.__listValue[index])

        target: int = width if self.__horizontal else height

        font: QFont = painter.font()
        font.setPixelSize((target - abs(offset)) // 8)
        painter.setFont(font)

        if self.__horizontal:
            textWidth: int = painter.fontMetrics().width(strValue)
            initX: int = width // 2 + offset - textWidth // 2
            painter.drawText(QRect(initX, 0, textWidth, height), Qt.AlignCenter, strValue)

            # 计算最后中间值停留的起始坐标,以便鼠标松开时矫正居中
            if index is self.__currentIndex: self.__currentPos = initX
        else:
            textHeight: int = painter.fontMetrics().height()
            initY: int = height // 2 + offset - textHeight // 2
            painter.drawText(QRect(0, initY, width, textHeight), Qt.AlignCenter, strValue)

            # 计算最后中间值停留的起始坐标,以便鼠标松开时矫正居中
            if index is self.__currentIndex: self.__currentPos = initY

        painter.restore()

    def __checkPosition(self) -> None:
        target: int = self.width() if self.__horizontal else self.height()

        # 左右滑动样式,往左滑动时,offset为负数,当前值所在X轴坐标小于宽度的一半,则将当前值设置为下一个值
        # 左右滑动样式,往右滑动时,offset为正数,当前值所在X轴坐标大于宽度的一半,则将当前值设置为上一个值
        # 上下滑动样式,往上滑动时,offset为负数,当前值所在Y轴坐标小于高度的一半,则将当前值设置为下一个值
        # 上下滑动样式,往下滑动时,offset为正数,当前值所在Y轴坐标大于高度的一半,则将当前值设置为上一个值
        if self.__offset < 0 and self.__offset != -1:
            if self.__currentPos < target / 2:
                self.__offset = 0
                self.currentIndex = self.__currentIndex + 1
        else:
            if self.__currentPos > target / 2:
                self.__offset = 0
                self.currentIndex = self.__currentIndex - 1

    def sizeHint(self) -> QSize: return QSize(50, 150)

    def minimumSizeHint(self) -> QSize: return QSize(10, 10)


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout

    class FrmTumbler(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmTumbler, self).__init__(parent)
            self.tumbler1 = Tumbler()
            self.tumbler2 = Tumbler()
            self.tumbler3 = Tumbler()
            self.tumbler4 = Tumbler()
            self.tumbler5 = Tumbler()
            self.tumbler6 = Tumbler()

            right_layout = QVBoxLayout()
            right_layout.addWidget(self.tumbler1)
            right_layout.addWidget(self.tumbler2)
            right_layout.addWidget(self.tumbler3)

            left_layout = QHBoxLayout()
            left_layout.addWidget(self.tumbler4)
            left_layout.addWidget(self.tumbler5)
            left_layout.addWidget(self.tumbler6)

            layout = QHBoxLayout()
            layout.addLayout(right_layout)
            layout.addLayout(left_layout)
            self.setLayout(layout)
            self.initForm()

        def initForm(self):
            self.tumbler1.textColor = QColor(100, 184, 255)
            self.tumbler2.textColor = QColor(255, 107, 107)
            self.tumbler3.textColor = QColor(24, 189, 155)
            self.tumbler4.textColor = QColor(100, 184, 255)
            self.tumbler5.textColor = QColor(255, 107, 107)
            self.tumbler6.textColor = QColor(24, 189, 155)

            g_listValue: List[AnyStr] = []
            for i in range(101): g_listValue.append(str(i))

            self.tumbler2.listValue = g_listValue.copy()
            self.tumbler3.listValue = g_listValue.copy()

            self.tumbler1.currentIndex = 5
            self.tumbler2.currentIndex = 30
            self.tumbler3.currentValue = "50"

            self.tumbler1.horizontal = True
            self.tumbler2.horizontal = True
            self.tumbler3.horizontal = True
            self.tumbler4.horizontal = False
            self.tumbler5.horizontal = False
            self.tumbler6.horizontal = False

            self.tumbler5.listValue = g_listValue.copy()
            self.tumbler5.currentIndex = 10

            g_listValue.clear()

            for i in range(2010, 2031): g_listValue.append(str(i))

            self.tumbler6.listValue = g_listValue.copy()
            self.tumbler6.currentValue = "2016"

            g_listValue.clear()
            for item in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
                g_listValue.append(item)

            self.tumbler4.listValue = g_listValue.copy()
            self.tumbler4.currentValue = "Nov"

    app = QApplication()
    window = FrmTumbler()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec_())

