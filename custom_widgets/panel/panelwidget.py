from typing import List

from PySide2.QtCore import QRect, QSize
from PySide2.QtGui import QResizeEvent
from PySide2.QtWidgets import QWidget, QScrollArea, QFrame, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy


class PanelWidget(QWidget):
    """
    面板容器控件
    作者:feiyangqingyun(QQ:517216493) 2016-11-20
    译者:sunchuquin(QQ:1715216365) 2021-07-07
    1. 支持所有widget子类对象,自动产生滚动条
    2. 支持自动拉伸自动填充
    3. 提供接口获取容器内的所有对象的指针
    4. 可设置是否自动拉伸宽度高度
    5. 可设置设备面板之间的间距和边距
    """
    def __init__(self, parent: QWidget = None):
        super(PanelWidget, self).__init__(parent)
        self.__scrollArea: QScrollArea = QScrollArea(self)  # 滚动区域
        self.__scrollArea.setObjectName('scrollAreaMain')
        self.__scrollArea.setWidgetResizable(True)

        self.__scrollAreaWidgetContents: QWidget = QWidget()  # 滚动区域载体
        self.__scrollAreaWidgetContents.setGeometry(QRect(0, 0, 100, 100))

        self.__frame: QFrame = QFrame(self.__scrollAreaWidgetContents)  # 放置设备的框架,自动变宽变高
        self.__frame.setObjectName('frameMain')

        self.__verticalLayout: QVBoxLayout = QVBoxLayout(self.__scrollAreaWidgetContents)  # 设备面板总布局
        self.__verticalLayout.setSpacing(0)
        self.__verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.__gridLayout: QGridLayout = QGridLayout(self.__frame)  # 设备表格布局
        self.__gridLayout.setSpacing(0)
        self.__gridLayout.setContentsMargins(0, 0, 0, 0)

        self.__margin: int = 0  # 边距
        self.__space: int = 0  # 设备之间的间隔
        self.__autoWidth: bool = False  # 宽度自动拉伸
        self.__autoHeight: bool = False  # 高度自动拉伸

        self.__widgets: List[QWidget] = []  # 设备面板对象集合
        self.__columnCount: int = 0  # 面板列数

        self.__verticalLayout.addWidget(self.__frame)
        self.__scrollArea.setWidget(self.__scrollAreaWidgetContents)
        self.__frame.setStyleSheet("QFrame#frameMain{border-width:0px;}")

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__scrollArea.resize(self.size())

    def getColumnCount(self) -> int: return self.__columnCount

    @property
    def widgets(self) -> List[QWidget]: return self.__widgets

    @widgets.setter
    def widgets(self, *args) -> None:
        self.__widgets = args[0][0]
        self.__columnCount = args[0][1]

        row: int = 0
        column: int = 0
        index: int = 0

        # 先把之前的所有移除并不可见
        for widget in self.__widgets:
            self.__gridLayout.removeWidget(widget)
            widget.setVisible(False)

        # 重新添加到布局中并可见
        for widget in self.__widgets:
            self.__gridLayout.addWidget(widget, row, column)
            widget.setVisible(True)

            column += 1
            index += 1
            if index % args[0][1] is 0:
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

    @property
    def margin(self) -> int: return self.__margin

    @margin.setter
    def margin(self, *args) -> None:
        self.__gridLayout.setContentsMargins(args[0][0], args[0][1], args[0][2], args[0][3])

    @property
    def space(self) -> int: return self.__space

    @space.setter
    def space(self, n_space: int) -> None:
        if self.__space == n_space: return
        self.__gridLayout.setSpacing(n_space)

    @property
    def autoWidth(self) -> bool: return self.__autoWidth

    @autoWidth.setter
    def autoWidth(self, auto_width: bool) -> None:
        if self.__autoWidth == auto_width: return
        self.__autoWidth = auto_width

    @property
    def autoHeight(self) -> bool: return self.__autoHeight

    @autoHeight.setter
    def autoHeight(self, auto_height: bool) -> None:
        if self.__autoHeight == auto_height: return
        self.__autoHeight = auto_height

    def sizeHint(self) -> QSize: return QSize(300, 200)

    def minimumSizeHint(self) -> QSize: return QSize(20, 20)


if __name__ == '__main__':
    import sys, random
    from PySide2.QtCore import QTimer
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout, QPushButton, QSizePolicy
    from lightbutton import LightButton
    from custom_widgets.progressbar.gaugeprogress import GaugeProgress

    class FrmPanelWidgetX(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmPanelWidgetX, self).__init__(parent)
            self.resize(206, 107)
            self.frame = QFrame()
            layout = QHBoxLayout()
            layout1 = QVBoxLayout()
            self.lab1 = QLabel('温度状态')
            self.lab2 = QLabel('湿度状态')
            self.lab3 = QLabel('压力状态')
            layout1.addWidget(self.lab1)
            layout1.addWidget(self.lab2)
            layout1.addWidget(self.lab3)
            layout1.setContentsMargins(0, 0, 0, 0)
            layout.addLayout(layout1)
            layout1 = QVBoxLayout()
            self.widget1 = LightButton()
            self.widget1.setMinimumSize(25, 25)
            self.widget1.setMaximumSize(25, 25)
            self.widget2 = LightButton()
            self.widget2.setMinimumSize(25, 25)
            self.widget2.setMaximumSize(25, 25)
            self.widget3 = LightButton()
            self.widget3.setMinimumSize(25, 25)
            self.widget3.setMaximumSize(25, 25)
            layout1.addWidget(self.widget1)
            layout1.addWidget(self.widget2)
            layout1.addWidget(self.widget3)
            layout1.setContentsMargins(0, 0, 0, 0)
            layout.addLayout(layout1)
            self.gaugeProgress = GaugeProgress()
            layout.addWidget(self.gaugeProgress)
            self.setLayout(layout)

            self.type = 0
            self.initForm()

        def initForm(self):
            timer: QTimer = QTimer(self)
            timer.setInterval(2000)
            timer.timeout.connect(self.updateValue)
            timer.start()
            self.updateValue()

        def updateValue(self):
            if self.type == 0:
                self.widget1.setLightGreen()
                self.widget2.setLightRed()
                self.widget3.setLightBlue()
                self.type = 1
            elif self.type == 1:
                self.widget1.setLightBlue()
                self.widget2.setLightGreen()
                self.widget3.setLightRed()
                self.type = 2
            elif self.type == 2:
                self.widget1.setLightRed()
                self.widget2.setLightBlue()
                self.widget3.setLightGreen()
                self.type = 0
            rand = random.randint(0, 100) % 100
            self.gaugeProgress.setValue(rand)

    class FrmPanelWidget(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmPanelWidget, self).__init__(parent)
            layout = QVBoxLayout()
            self.tabWidget = QTabWidget()
            layout.addWidget(self.tabWidget)
            self.widget1 = PanelWidget()
            self.widget2 = PanelWidget()
            self.tabWidget.addTab(self.widget1, '简单容器')
            self.tabWidget.addTab(self.widget2, '复杂容器')
            self.setLayout(layout)

            self.initForm()

        def initForm(self):
            widgets1: List[QWidget] = []
            columnCount1: int = 10

            for i in range(1, 101):
                btn: QPushButton = QPushButton()
                btn.setText(str(i))
                btn.setFixedHeight(100)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                widgets1.append(btn)

            self.widget1.widgets = widgets1, columnCount1
            self.widget1.margin = 3, 3, 3, 3

            widgets2: List[QWidget] = []
            columnCount2: int = 6

            for i in range(1, 51):
                frm: FrmPanelWidgetX = FrmPanelWidgetX()
                frm.setFixedHeight(105)
                frm.setMinimumWidth(200)
                frm.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                widgets2.append(frm)

            self.widget2.widgets = widgets2, columnCount2
            self.widget2.margin = 3, 3, 3, 3

    app = QApplication()
    window = FrmPanelWidget()
    window.show()
    sys.exit(app.exec_())

