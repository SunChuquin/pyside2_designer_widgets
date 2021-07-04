from enum import Enum
from typing import List

import shiboken2
from PySide2.QtCore import QEnum, QTimer, QSize, Qt, QRect
from PySide2.QtGui import QFont, QColor, QPaintEvent, QPainter, QPen
from PySide2.QtWidgets import QWidget


class PanelItem(QWidget):
    """
    面板区域控件
    作者:feiyangqingyun(QQ:517216493) 2017-10-21
    译者:sunchuquin(QQ:1715216365) 2021-07-04
    1. 可设置标题栏文字/高度/字体/对齐方式/颜色
    2. 可设置边框宽度/边框圆角角度/边框颜色
    3. 可设置报警颜色切换间隔/报警加深颜色/报警普通颜色
    4. 可设置启用状态和禁用状态时文字和边框颜色
    """
    @QEnum
    class Alignment(Enum):
        Alignment_Left = 0  # 左对齐
        Alignment_Center = 1  # 居中对齐
        Alignment_Right = 2  # 右对齐

    def __init__(self, parent: QWidget = None):
        super(PanelItem, self).__init__(parent)
        self.__titleHeight: int = 30  # 标题高度
        self.__titleText: str = ''  # 标题文字
        self.__titleFont: QFont = QFont(self.font().family(), 15)  # 标题字体
        self.__titleAlignment: PanelItem.Alignment = PanelItem.Alignment.Alignment_Center  # 标题对齐方式
        self.__titleColor: QColor = QColor(255, 255, 255)  # 标题颜色
        self.__titleDisableColor: QColor = QColor(230, 230, 230)  # 禁用状态下文字颜色

        self.__borderWidth: int = 3  # 边框宽度
        self.__borderRadius: int = 5  # 边框圆角角度
        self.__borderColor: QColor = QColor(21, 156, 119)  # 边框颜色
        self.__borderDisableColor: QColor = QColor(180, 180, 180)  # 禁用状态下边框颜色

        self.__alarmInterval: int = 500  # 报警切换间隔
        self.__alarmTextColor: QColor = QColor(250, 250, 250)  # 报警文字颜色
        self.__alarmDarkColor: QColor = QColor(205, 0, 0)  # 报警加深颜色
        self.__alarmNormalColor: QColor = QColor(80, 80, 80)  # 报警普通颜色

        self.__isAlarm: bool = False  # 是否报警
        self.__isEnable: bool = True  # 是否启用

        self.__isDark: bool = False  # 是否加深
        self.__tempColor: QColor = self.__borderColor  # 临时颜色
        self.__timer: QTimer = QTimer(self)  # 报警切换定时器
        self.__timer.timeout.connect(self.checkAlarm)
        self.__timer.setInterval(500)

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制边框
        self.drawBorder(painter)
        # 绘制标题
        self.drawTitle(painter)

    def drawBorder(self, painter: QPainter) -> None:
        if self.__borderWidth <= 0: return

        painter.save()

        pen: QPen = QPen()
        pen.setWidth(self.__borderWidth)
        pen.setColor(self.__tempColor)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        rect: QRect = QRect(self.__borderWidth // 2,
                            self.__borderWidth // 2,
                            self.width() - self.__borderWidth,
                            self.height() - self.__borderWidth)
        painter.drawRoundedRect(rect, self.__borderRadius, self.__borderRadius)

        painter.restore()

    def drawTitle(self, painter: QPainter) -> None:
        painter.save()

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__tempColor)

        offset: int = self.__borderWidth - self.__borderWidth // 3
        rect: QRect = QRect(offset, offset, self.width() - offset * 2, self.__titleHeight)
        painter.drawRect(rect)

        # 绘制标题文字
        if self.__isEnable:
            painter.setPen(self.__alarmTextColor if self.__isAlarm else self.__titleColor)
        else:
            painter.setPen(self.__titleDisableColor)

        painter.setFont(self.__titleFont)

        # 文字区域要重新计算
        offset = self.__borderWidth * 3
        textRect: QRect = QRect(offset, 0, self.width() - offset * 2, self.__titleHeight)

        align: Qt.Alignment = Qt.Alignment
        if self.__titleAlignment == PanelItem.Alignment.Alignment_Left:
            align = Qt.AlignLeft | Qt.AlignVCenter
        elif self.__titleAlignment == PanelItem.Alignment.Alignment_Center:
            align = Qt.AlignHCenter | Qt.AlignVCenter
        elif self.__titleAlignment == PanelItem.Alignment.Alignment_Right:
            align = Qt.AlignRight | Qt.AlignVCenter

        painter.drawText(textRect, align, self.__titleText)

        painter.restore()

    @property
    def titleHeight(self) -> int: return self.__titleHeight

    @titleHeight.setter
    def titleHeight(self, title_height: int) -> None:
        if self.__titleHeight == title_height: return
        self.__titleHeight = title_height
        self.update()

    @property
    def titleText(self) -> str: return self.__titleText

    @titleText.setter
    def titleText(self, title_text: str) -> None:
        if self.__titleText == title_text: return
        self.__titleText = title_text
        self.update()

    @property
    def titleFont(self) -> QFont: return self.__titleFont

    @titleFont.setter
    def titleFont(self, title_font: QFont) -> None:
        if self.__titleFont == title_font: return
        self.__titleFont = title_font
        self.update()

    @property
    def titleAlignment(self) -> Alignment: return self.__titleAlignment

    @titleAlignment.setter
    def titleAlignment(self, title_alignment: Alignment) -> None:
        if self.__titleAlignment == title_alignment: return
        self.__titleAlignment = title_alignment
        self.update()

    @property
    def titleColor(self) -> QColor: return self.__titleColor

    @titleColor.setter
    def titleColor(self, title_color: QColor) -> None:
        if self.__titleColor == title_color: return
        self.__titleColor = title_color
        self.update()

    @property
    def titleDisableColor(self) -> QColor: return self.__titleDisableColor

    @titleDisableColor.setter
    def titleDisableColor(self, title_disable_color: QColor) -> None:
        if self.__titleDisableColor == title_disable_color: return
        self.__titleDisableColor = title_disable_color
        self.update()

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
        self.isEnable = self.__isEnable
        self.update()

    @property
    def borderDisableColor(self) -> QColor: return self.__borderDisableColor

    @borderDisableColor.setter
    def borderDisableColor(self, border_disable_color: QColor) -> None:
        if self.__borderDisableColor == border_disable_color: return
        self.__borderDisableColor = border_disable_color
        self.setEnable(self.__isEnable)
        self.update()

    @property
    def alarmInterval(self) -> int: return self.__alarmInterval

    @alarmInterval.setter
    def alarmInterval(self, alarm_interval: int) -> None:
        if self.__alarmInterval == alarm_interval: return
        self.__alarmInterval = alarm_interval
        self.__timer.setInterval(alarm_interval)

    @property
    def alarmTextColor(self) -> QColor: return self.__alarmTextColor

    @alarmTextColor.setter
    def alarmTextColor(self, alarm_text_color: QColor) -> None:
        if self.__alarmTextColor == alarm_text_color: return
        self.__alarmTextColor = alarm_text_color
        self.update()

    @property
    def alarmDarkColor(self) -> QColor: return self.__alarmDarkColor

    @alarmDarkColor.setter
    def alarmDarkColor(self, alarm_dark_color: QColor) -> None:
        if self.__alarmDarkColor == alarm_dark_color: return
        self.__alarmDarkColor = alarm_dark_color
        self.isAlarm = self.__isAlarm
        self.update()

    @property
    def alarmNormalColor(self) -> QColor: return self.__alarmNormalColor

    @alarmNormalColor.setter
    def alarmNormalColor(self, alarm_normal_color: QColor) -> None:
        if self.__alarmNormalColor == alarm_normal_color: return
        self.__alarmNormalColor = alarm_normal_color
        self.isAlarm = self.__isAlarm
        self.update()

    @property
    def isAlarm(self) -> bool: return self.__isAlarm

    @isAlarm.setter
    def isAlarm(self, is_alarm: bool) -> None:
        if not self.__isEnable: return

        self.__isAlarm = is_alarm
        if is_alarm:
            if not self.__timer.isActive(): self.__timer.start()
            self.__isDark = True
            self.__tempColor = self.__alarmDarkColor
        else:
            if self.__timer.isActive(): self.__timer.stop()
            self.__isDark = False
            self.__tempColor = self.__borderColor
        self.update()

    @property
    def isEnable(self) -> bool: return self.__isEnable

    @isEnable.setter
    def isEnable(self, is_enable: bool) -> None:
        self.__isEnable = is_enable
        if self.__timer.isActive(): self.__timer.stop()

        if is_enable:
            self.__tempColor = self.__borderColor
        else:
            self.__tempColor = self.__borderDisableColor

        self.update()

        # 将对应的子元素设置启用禁用状态
        for w in self.findChildren(QWidget):
            w.setEnabled(is_enable)

    def sizeHint(self) -> QSize: return QSize(250, 200)

    def minimumSizeHint(self) -> QSize: return QSize(30, 20)

    def checkAlarm(self) -> None:
        if self.__isDark:
            self.__tempColor = self.__alarmNormalColor
        else:
            self.__tempColor = self.__alarmDarkColor

        self.__isDark = not self.__isDark
        self.update()


if __name__ == '__main__':
    import sys
    from typing import List
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication, QGridLayout, QPushButton, QComboBox, QFrame, QTextEdit, \
        QSpacerItem, QSizePolicy, QHBoxLayout

    class FrmPanelItem(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmPanelItem, self).__init__(parent)
            self.items: List[PanelItem] = []

            layout = QGridLayout()
            self.panelItem1 = PanelItem()
            self.panelItem2 = PanelItem()
            self.panelItem3 = PanelItem()
            self.panelItem4 = PanelItem()
            layout.addWidget(self.panelItem1, 0, 0)
            layout.addWidget(self.panelItem2, 0, 1)
            layout.addWidget(self.panelItem3, 1, 0)
            layout.addWidget(self.panelItem4, 1, 1)

            layout2 = QHBoxLayout()
            self.cboxAlignment = QComboBox()
            self.cboxAlignment.clear()
            self.cboxAlignment.addItems(['左对齐', '居中对齐', '右对齐'])
            self.cboxColor = QComboBox()
            self.cboxColor.clear()
            self.cboxColor.addItems(['绿色', '蓝色', '水红色', '黑色'])
            self.btnDisable = QPushButton('禁用')
            layout2.addWidget(self.cboxAlignment)
            layout2.addWidget(self.cboxColor)
            layout2.addWidget(self.btnDisable)
            layout3 = QHBoxLayout()
            self.btnEnable = QPushButton('启用')
            self.btnAlarm = QPushButton('报警')
            self.btnNormal = QPushButton('正常')
            layout3.addWidget(self.btnEnable)
            layout3.addWidget(self.btnAlarm)
            layout3.addWidget(self.btnNormal)

            layout.addLayout(layout2, 2, 0)
            layout.addLayout(layout3, 2, 1)
            self.setLayout(layout)
            self.initForm()

            self.btnDisable.clicked.connect(self.on_btnDisable_clicked)
            self.btnEnable.clicked.connect(self.on_btnEnable_clicked)
            self.btnAlarm.clicked.connect(self.on_btnAlarm_clicked)
            self.btnNormal.clicked.connect(self.on_btnNormal_clicked)
            self.cboxAlignment.activated.connect(self.on_cboxAlignment_activated)
            self.cboxColor.activated.connect(self.on_cboxColor_activated)

        def initForm(self) -> None:
            self.items.append(self.panelItem1)
            self.items.append(self.panelItem2)
            self.items.append(self.panelItem3)
            self.items.append(self.panelItem4)

            self.cboxAlignment.setCurrentIndex(1)

            for i in range(len(self.items)):
                self.items[i].titleText = "标题%d" % (i + 1)

        def on_btnDisable_clicked(self) -> None:
            for item in self.items:
                item.isEnable = False

        def on_btnEnable_clicked(self) -> None:
            for item in self.items:
                item.isEnable = True

        def on_btnAlarm_clicked(self) -> None:
            for item in self.items:
                item.isAlarm = True

        def on_btnNormal_clicked(self) -> None:
            for item in self.items:
                item.isAlarm = False

        def on_cboxAlignment_activated(self, index: int) -> None:
            for item in self.items:
                item.titleAlignment = PanelItem.Alignment(index)

        def on_cboxColor_activated(self, index: int) -> None:
            colors: List[QColor] = [
                QColor("#16A085"),
                QColor("#2980B9"),
                QColor("#8E44AD"),
                QColor("#2C3E50")
            ]

            for item in self.items:
                item.borderColor = colors[index]

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmPanelItem()
    window.resize(500, 300)
    window.setWindowTitle("面板区域")
    window.show()
    sys.exit(app.exec_())
