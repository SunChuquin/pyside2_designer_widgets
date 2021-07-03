from typing import List

from PySide2.QtCore import QObject, QEvent, QSize, Signal, Qt
from PySide2.QtGui import QColor, QPaintEvent, QPainter
from PySide2.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy

from custom_widgets.color.colorpanelbar import ColorPanelBar


class ColorPanelFader(QWidget):
    """
    颜色滑块面板
    作者:feiyangqingyun(QQ:517216493) 2017-11-17
    译者:sunchuquin(QQ:1715216365) 2021-07-03
    1. 可设置滑块条之间的间隔
    2. 可设置滑块组之间的间隔
    3. 可设置背景颜色
    """

    colorChanged = Signal(QColor, float, float, float)  # color, hue, sat, bright
    
    def __init__(self, parent: QWidget = None):
        super(ColorPanelFader, self).__init__(parent)
        self.__barSpace: int = 6  # 柱状条间隔
        self.__groupSpace: int = 20  # 分组间隔
        self.__bgColor: QColor = QColor(70, 70, 70)  # 背景颜色

        self.__layout: QHBoxLayout = QHBoxLayout()
        self.__spacer1: QSpacerItem = QSpacerItem(self.groupSpace, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.__spacer2: QSpacerItem = QSpacerItem(self.groupSpace, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.__items: List[ColorPanelBar] = []
        self.setLayout(self.__layout)

        self.initForm()

    def initForm(self):
        topColors: List[QColor] = [
            Qt.red, Qt.red, Qt.red, Qt.cyan, Qt.magenta, Qt.yellow, Qt.red, Qt.green, Qt.blue
        ]
        bottomColors: List[QColor] = [
            Qt.red, Qt.white, Qt.black, Qt.cyan, Qt.magenta, Qt.yellow, Qt.black, Qt.black, Qt.black
        ]

        for i in range(9):
            item: ColorPanelBar = ColorPanelBar()
            item.colorChanged.connect(self.updateColor)

            item.installEventFilter(self)
            item.setObjectName("colorPanelBar" + str(i))
            item.borderColor = topColors[i]
            item.topColor = topColors[i]
            item.bottomColor = bottomColors[i]
            item.outMode = True

            if i > 2:
                item.showOverlay = True

            if i is 3:
                self.__layout.addItem(self.__spacer1)
            elif i is 6:
                self.__layout.addItem(self.__spacer2)

            self.__layout.addWidget(item)
            self.__items.append(item)

        # 初始化默认颜色值
        self.__items[0].hsbMode = True
        self.__items[0].showValue = True
        self.__items[1].staticMode = False
        self.__items[2].staticMode = False
        self.__items[3].percent = 0
        self.__items[7].percent = 0
        self.__items[8].percent = 0

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() is QEvent.MouseButtonPress:
            item: ColorPanelBar = watched
            index: int = self.__items.index(item)
            if index >= 6:
                self.__items[0].setEnabled(False)
                self.__items[1].setEnabled(False)
                self.__items[2].setEnabled(False)
                self.__items[3].setEnabled(False)
                self.__items[4].setEnabled(False)
                self.__items[5].setEnabled(False)
            elif index >= 3:
                self.__items[0].setEnabled(False)
                self.__items[1].setEnabled(False)
                self.__items[2].setEnabled(False)
                self.__items[6].setEnabled(False)
                self.__items[7].setEnabled(False)
                self.__items[8].setEnabled(False)
            elif index >= 0:
                self.__items[3].setEnabled(False)
                self.__items[4].setEnabled(False)
                self.__items[5].setEnabled(False)
                self.__items[6].setEnabled(False)
                self.__items[7].setEnabled(False)
                self.__items[8].setEnabled(False)
        elif event.type() is QEvent.MouseButtonRelease:
            item: ColorPanelBar = watched
            index: int = self.__items.index(item)
            if index >= 6:
                self.__items[0].setEnabled(True)
                self.__items[1].setEnabled(True)
                self.__items[2].setEnabled(True)
                self.__items[3].setEnabled(True)
                self.__items[4].setEnabled(True)
                self.__items[5].setEnabled(True)
            elif index >= 3:
                self.__items[0].setEnabled(True)
                self.__items[1].setEnabled(True)
                self.__items[2].setEnabled(True)
                self.__items[6].setEnabled(True)
                self.__items[7].setEnabled(True)
                self.__items[8].setEnabled(True)
            elif index >= 0:
                self.__items[3].setEnabled(True)
                self.__items[4].setEnabled(True)
                self.__items[5].setEnabled(True)
                self.__items[6].setEnabled(True)
                self.__items[7].setEnabled(True)
                self.__items[8].setEnabled(True)

        return super(ColorPanelFader, self).eventFilter(watched, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter: QPainter = QPainter(self)
        painter.fillRect(self.rect(), self.__bgColor)

    def updateColor(self, color: QColor, value: float, percent: float) -> None:
        item: ColorPanelBar = self.sender()
        index: int = self.__items.index(item)

        if index is 0:
            # 获取当前HSB处的颜色值
            self.__items[1].topColor = color
            self.__items[2].topColor = color
            self.__items[1].borderColor = color
            self.__items[2].borderColor = color
        elif index is 1:
            self.__items[2].topColor = color
            self.__items[2].borderColor = color
        elif index is 2:
            self.__items[1].topColor = color
            self.__items[1].borderColor = color
        elif index == 3:
            self.__items[6].percent = 100 - percent
        elif index == 4:
            self.__items[7].percent = 100 - percent
        elif index == 5:
            self.__items[8].percent = 100 - percent
        elif index == 6:
            self.__items[3].percent = 100 - percent
        elif index == 7:
            self.__items[4].percent = 100 - percent
        elif index == 8:
            self.__items[5].percent = 100 - percent

        # 如果是HSB变化则CMY和RGB变化
        if index < 3:
            hue: float = self.__items[0].percent / 100
            sat: float = self.__items[1].percent / 100
            bright: float = self.__items[2].percent / 100

            # 组合HSB当前值,然后转为CMY和RGB计算百分比进行设置
            color: QColor = QColor.fromHsvF(hue, sat, bright)
            percentRed: float = color.redF() * 100
            percentGreen: float = color.greenF() * 100
            percentBlue: float = color.blueF() * 100

            self.__items[3].percent = 100 - percentRed
            self.__items[4].percent = 100 - percentGreen
            self.__items[5].percent = 100 - percentBlue
            self.__items[6].percent = percentRed
            self.__items[7].percent = percentGreen
            self.__items[8].percent = percentBlue

        # 根据百分比获取颜色值
        red: float = self.__items[6].percent / 100
        green: float = self.__items[7].percent / 100
        blue: float = self.__items[8].percent / 100
        currentColor: QColor = QColor.fromRgbF(red, green, blue)
        self.colorChanged.emit(currentColor,
                               self.__items[0].value,
                               self.__items[1].percent,
                               self.__items[2].percent)

        # 如果是CMY或者RGB变化则HSB变化
        if index >= 3:
            # hue活出现负数=白色,要矫正
            percentHue: float = currentColor.hueF() * 100
            if percentHue < 0:
                percentHue = 0

            percentSat: float = currentColor.saturationF() * 100
            percentBright: float = currentColor.lightnessF() * 100

            # 计算当前值所占百分比
            self.__items[0].percent = percentHue
            self.__items[1].percent = percentSat
            self.__items[2].percent = percentBright

            self.__items[1].topColor = currentColor
            self.__items[2].topColor = currentColor
            self.__items[1].borderColor = currentColor
            self.__items[2].borderColor = currentColor

    def sizeHint(self) -> QSize: return QSize(500, 350)

    def minimumSizeHint(self) -> QSize: return QSize(100, 60)

    @property
    def barSpace(self) -> int: return self.__barSpace

    @barSpace.setter
    def barSpace(self, bar_space: int) -> None:
        if self.__barSpace == bar_space: return
        self.__barSpace = bar_space
        self.__layout.setSpacing(bar_space)

    @property
    def groupSpace(self) -> int: return self.__groupSpace

    @groupSpace.setter
    def groupSpace(self, group_space: int) -> None:
        if self.__groupSpace == group_space: return
        self.__groupSpace = group_space
        self.__layout.setSpacing(self.__barSpace)
        self.__spacer1.changeSize(group_space, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.__spacer2.changeSize(group_space, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()


if __name__ == '__main__':
    import sys
    from PySide2.QtGui import QFont
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication, QLabel, QHBoxLayout

    class FrmColorPanelFader(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmColorPanelFader, self).__init__(parent)
            self.resize(650, 350)
            self.colorPanelFader = ColorPanelFader()
            self.labColor = QLabel()
            self.labColor.setMinimumWidth(50)
            self.labColor.setMaximumWidth(50)

            layout = QHBoxLayout()
            layout.addWidget(self.colorPanelFader)
            layout.addWidget(self.labColor)
            self.setLayout(layout)

            self.colorPanelFader.colorChanged.connect(self.colorChanged)
            self.colorChanged(QColor(255, 0, 0), 0, 100, 100)

        def colorChanged(self, color: QColor, hue: float, sat: float, bright: float) -> None:
            self.labColor.setStyleSheet("QLabel{background:%s;}" % color.name())

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmColorPanelFader()
    window.setWindowTitle("颜色滑块面板")
    window.show()
    sys.exit(app.exec_())
