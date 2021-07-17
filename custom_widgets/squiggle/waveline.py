from typing import List

from PySide2.QtCore import QTimer, QSize, QPoint, Qt, QPointF
from PySide2.QtGui import QColor, QPaintEvent, QPainter, QLinearGradient, QPen
from PySide2.QtWidgets import QWidget


class WaveLine(QWidget):
    """
    直方波形图控件
    作者:feiyangqingyun(QQ:517216493) 2016-11-6
    译者:sunchuquin(QQ:1715216365) 2021-07-17
    1. 可设置最大值
    2. 可设置每次过渡的步长
    3. 可设置item之间的间隔
    4. 可设置渐变的背景颜色
    5. 可设置线条的颜色
    """
    def __init__(self, parent: QWidget = None):
        super(WaveLine, self).__init__(parent)
        self.__maxValue: int = 100  # 最大值
        self.__step: int = 1  # 步长
        self.__space: int = 10  # 间距

        self.__bgColorStart: QColor = QColor(100, 100, 100)  # 背景渐变开始颜色
        self.__bgColorEnd: QColor = QColor(60, 60, 60)  # 背景渐变结束颜色
        self.__lineColor: QColor = QColor(100, 184, 255)  # 线条颜色

        self.__timer: QTimer = QTimer(self)  # 绘制定时器
        self.__timer.setInterval(10)
        self.__timer.timeout.connect(self.updateData)

        self.__currentDataVec: List[int] = []  # 当前数据集合
        self.__dataVec: List[int] = []  # 目标数据集合

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self.drawBg(painter)  # 绘制背景
        self.drawLine(painter)  # 绘制线条

    def drawBg(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)
        bgGradient: QLinearGradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))
        bgGradient.setColorAt(0.0, self.__bgColorStart)
        bgGradient.setColorAt(1.0, self.__bgColorEnd)
        painter.setBrush(bgGradient)
        painter.drawRect(self.rect())
        painter.restore()

    def drawLine(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(QPen(self.__lineColor, 2))

        count: int = len(self.__dataVec)
        increment: float = self.width() / count
        initX: float = 0.0
        pointVec: List[QPointF] = []

        for i in range(count - 1):
            currentValue: float = self.__currentDataVec[i]
            y1: float = self.height() - self.height() / self.__maxValue * currentValue
            nextValue: float = self.__currentDataVec[i + 1]
            y2: float = self.height() - self.height() / self.__maxValue * nextValue

            point1: QPointF = QPointF(initX, y1)
            point2: QPointF = QPointF(initX + increment, y2)
            initX += increment

            pointVec.append(point1)
            pointVec.append(point2)

        painter.drawLines(pointVec)
        painter.restore()

    def updateData(self) -> None:
        count: int = len(self.__dataVec)

        for i in range(count):
            if self.__currentDataVec[i] < self.__dataVec[i]:
                self.__currentDataVec[i] += self.__step
            elif self.__currentDataVec[i] > self.__dataVec[i]:
                self.__currentDataVec[i] -= self.__step

        self.update()

    def setData(self, data_vec: List[int]) -> None:
        count: int = len(data_vec)

        if len(self.__currentDataVec) < count:
            for i in range(count - len(self.__currentDataVec)):
                self.__currentDataVec.insert(0, 0)

        if len(self.__dataVec) < count:
            for i in range(count - len(self.__dataVec)):
                self.__dataVec.insert(0, 0)

        for i in range(count):
            self.__dataVec[i] = data_vec[i]

        if not self.__timer.isActive():
            self.__timer.start()

    @property
    def maxValue(self) -> int: return self.__maxValue

    @maxValue.setter
    def maxValue(self, max_value: int) -> None:
        if self.__maxValue == max_value: return
        self.__maxValue = max_value
        self.update()

    @property
    def step(self) -> int: return self.__step

    @step.setter
    def step(self, n_step: int) -> None:
        if self.__step == n_step: return
        self.__step = n_step
        self.update()

    @property
    def space(self) -> int: return self.__space

    @space.setter
    def space(self, n_space: int) -> None:
        if self.__space == n_space: return
        self.__space = n_space
        self.update()

    @property
    def bgColorStart(self) -> QColor: return self.__bgColorStart

    @bgColorStart.setter
    def bgColorStart(self, bg_color_start: QColor) -> None:
        if self.__bgColorStart == bg_color_start: return
        self.__bgColorStart = bg_color_start
        self.update()

    @property
    def bgColorEnd(self) -> QColor: return self.__bgColorEnd

    @bgColorEnd.setter
    def bgColorEnd(self, bg_color_end: QColor) -> None:
        if self.__bgColorEnd == bg_color_end: return
        self.__bgColorEnd = bg_color_end
        self.update()

    @property
    def lineColor(self) -> QColor: return self.__lineColor

    @lineColor.setter
    def lineColor(self, line_color: QColor) -> None:
        if self.__lineColor == line_color: return
        self.__lineColor = line_color
        self.update()

    def sizeHint(self) -> QSize: return QSize(50, 200)

    def minimumSizeHint(self) -> QSize: return QSize(10, 20)


if __name__ == '__main__':
    import sys, random
    from PySide2.QtCore import QTextCodec
    from PySide2.QtGui import QFont
    from PySide2.QtWidgets import QApplication, QVBoxLayout

    class FrmWaveLine(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmWaveLine, self).__init__(parent)

            layout = QVBoxLayout()
            self.waveLine1 = WaveLine()
            self.waveLine2 = WaveLine()
            self.waveLine3 = WaveLine()
            layout.addWidget(self.waveLine1)
            layout.addWidget(self.waveLine2)
            layout.addWidget(self.waveLine3)
            self.setLayout(layout)

            self.initForm()

        def initForm(self):
            bgColor: QColor = QColor(30, 30, 30)
            self.waveLine1.bgColorStart = bgColor
            self.waveLine1.bgColorEnd = bgColor
            self.waveLine2.bgColorStart = bgColor
            self.waveLine2.bgColorEnd = bgColor
            self.waveLine3.bgColorStart = bgColor
            self.waveLine3.bgColorEnd = bgColor

            self.waveLine2.lineColor = QColor(255, 107, 107)
            self.waveLine3.lineColor = QColor(24, 189, 155)

            timer: QTimer = QTimer(self)
            timer.setInterval(2000)
            timer.timeout.connect(self.updateValue)
            timer.start()
            self.updateValue()

        def updateValue(self):
            data: List[int] = []
            maxValue: int = 100

            for i in range(50):
                rand: int = random.randint(0, 100) % maxValue
                data.append(rand)

            self.waveLine1.maxValue = maxValue
            self.waveLine1.setData(data)

            data.clear()
            maxValue = 50

            for i in range(100):
                rand: int = random.randint(0, 50) % maxValue
                data.append(rand)

            self.waveLine2.maxValue = maxValue
            self.waveLine2.setData(data)

            data.clear()
            maxValue = 100

            for i in range(100):
                rand: int = random.randint(0, 50) % maxValue
                data.append(rand)

            self.waveLine3.maxValue = maxValue
            self.waveLine3.setData(data)

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmWaveLine()
    window.resize(500, 300)
    window.setWindowTitle("直方波形图")
    window.show()
    sys.exit(app.exec_())
