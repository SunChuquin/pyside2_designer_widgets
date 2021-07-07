from typing import AnyStr

from PySide2.QtCore import QObject, QEvent, QTimer, QSize, QPoint, Qt, QRect
from PySide2.QtGui import QColor, QPaintEvent, QPainter, QMouseEvent, QFont, QLinearGradient, QPainterPath
from PySide2.QtWidgets import QWidget


class LightButton(QWidget):
    """
    高亮发光按钮控件
    作者:feiyangqingyun(QQ:517216493) 2016-10-16
    译者:sunchuquin(QQ:1715216365) 2021-07-04
    1. 可设置文本,居中显示
    2. 可设置文本颜色
    3. 可设置外边框渐变颜色
    4. 可设置里边框渐变颜色
    5. 可设置背景色
    6. 可直接调用内置的设置 绿色/红色/黄色/黑色/蓝色 等公有槽函数
    7. 可设置是否在容器中可移动,当成一个对象使用
    8. 可设置是否显示矩形
    9. 可设置报警颜色+非报警颜色
    10. 可控制启动报警和停止报警,报警时闪烁
    """

    def __init__(self, parent: QWidget = None):
        super(LightButton, self).__init__(parent)
        self.__text: AnyStr = ''  # 文本
        self.__textColor: QColor = QColor(255, 255, 255)  # 文字颜色
        self.__alarmColor: QColor = QColor(255, 107, 107)  # 报警颜色
        self.__normalColor: QColor = QColor(10, 10, 10)  # 正常颜色

        self.__borderOutColorStart: QColor = QColor(255, 255, 255)  # 外边框渐变开始颜色
        self.__borderOutColorEnd: QColor = QColor(166, 166, 166)  # 外边框渐变结束颜色
        self.__borderInColorStart: QColor = QColor(166, 166, 166)  # 里边框渐变开始颜色
        self.__borderInColorEnd: QColor = QColor(255, 255, 255)  # 里边框渐变结束颜色
        self.__bgColor: QColor = QColor(100, 184, 255)  # 背景颜色

        self.__showRect: bool = False  # 显示成矩形
        self.__canMove: bool = False  # 是否能够移动
        self.__showOverlay: bool = True  # 是否显示遮罩层
        self.__overlayColor: QColor = QColor(255, 255, 255)  # 遮罩层颜色

        self.__isAlarm: bool = False  # 是否报警
        self.__timerAlarm: QTimer = QTimer(self)  # 定时器切换颜色

        self.lastPoint: QPoint = QPoint()
        self.pressed: bool = False

        self.installEventFilter(self)
        self.__timerAlarm.timeout.connect(self.alarm)
        self.__timerAlarm.setInterval(500)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if self.__canMove:
            mouseEvent: QMouseEvent = event

            if mouseEvent.type() == QEvent.MouseButtonPress:
                if self.rect().contains(mouseEvent.pos()) and mouseEvent.button() is Qt.LeftButton:
                    self.lastPoint = mouseEvent.pos()
                    self.pressed = True
            elif mouseEvent.type() == QEvent.MouseMove and self.pressed:
                dx: int = mouseEvent.pos().x() - self.lastPoint.x()
                dy: int = mouseEvent.pos().y() - self.lastPoint.y()
                self.move(self.x() + dx, self.y() + dy)
            elif mouseEvent.type() == QEvent.MouseButtonRelease and self.pressed:
                self.pressed = False

        return super(LightButton, self).eventFilter(watched, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        width: int = self.width()
        height: int = self.height()
        side: int = min(width, height)

        # 绘制准备工作,启用反锯齿,平移坐标轴中心,等比例缩放
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        if self.__showRect:
            # 绘制矩形区域
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.__bgColor)
            painter.drawRoundedRect(self.rect(), 5, 5)

            # 绘制文字
            if not self.__text.isEmpty():
                font: QFont = QFont()
                font.setPixelSize(side - 20)
                painter.setFont(font)
                painter.setPen(self.__textColor)
                painter.drawText(self.rect(), Qt.AlignCenter, self.__text)
        else:
            painter.translate(width / 2, height / 2)
            painter.scale(side / 200.0, side / 200.0)

            # 绘制外边框
            self.drawBorderOut(painter)
            # 绘制内边框
            self.drawBorderIn(painter)
            # 绘制内部指示颜色
            self.drawBg(painter)
            # 绘制居中文字
            self.drawText(painter)
            # 绘制遮罩层
            self.drawOverlay(painter)

    def drawBorderOut(self, painter: QPainter) -> None:
        radius: int = 99
        painter.save()
        painter.setPen(Qt.NoPen)
        borderGradient: QLinearGradient = QLinearGradient(0, -radius, 0, radius)
        borderGradient.setColorAt(0, self.__borderOutColorStart)
        borderGradient.setColorAt(1, self.__borderOutColorEnd)
        painter.setBrush(borderGradient)
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        painter.restore()

    def drawBorderIn(self, painter: QPainter) -> None:
        radius: int = 90
        painter.save()
        painter.setPen(Qt.NoPen)
        borderGradient: QLinearGradient = QLinearGradient(0, -radius, 0, radius)
        borderGradient.setColorAt(0, self.__borderInColorStart)
        borderGradient.setColorAt(1, self.__borderInColorEnd)
        painter.setBrush(borderGradient)
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        painter.restore()

    def drawBg(self, painter: QPainter) -> None:
        radius: int = 80
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__bgColor)
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        painter.restore()

    def drawText(self, painter: QPainter) -> None:
        if self.__text == '': return

        radius: int = 100
        painter.save()

        font: QFont = QFont()
        font.setPixelSize(85)
        painter.setFont(font)
        painter.setPen(self.__textColor)
        rect: QRect = QRect(-radius, -radius, radius * 2, radius * 2)
        painter.drawText(rect, Qt.AlignCenter, self.__text)
        painter.restore()

    def drawOverlay(self, painter: QPainter) -> None:
        if not self.__showOverlay: return

        radius: int = 80
        painter.save()
        painter.setPen(Qt.NoPen)

        smallCircle: QPainterPath = QPainterPath()
        bigCircle: QPainterPath = QPainterPath()
        radius -= 1
        smallCircle.addEllipse(-radius, -radius, radius * 2, radius * 2)
        radius *= 2
        bigCircle.addEllipse(-radius, -radius + 140, radius * 2, radius * 2)

        # 高光的形状为小圆扣掉大圆的部分
        highlight: QPainterPath = smallCircle - bigCircle

        linearGradient: QLinearGradient = QLinearGradient(0, -radius / 2, 0, 0)
        self.__overlayColor.setAlpha(100)
        linearGradient.setColorAt(0.0, self.__overlayColor)
        self.__overlayColor.setAlpha(30)
        linearGradient.setColorAt(1.0, self.__overlayColor)
        painter.setBrush(linearGradient)
        painter.rotate(-20)
        painter.drawPath(highlight)

        painter.restore()

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
    def alarmColor(self) -> QColor: return self.__alarmColor

    @alarmColor.setter
    def alarmColor(self, alarm_color: QColor) -> None:
        if self.__alarmColor == alarm_color: return
        self.__alarmColor = alarm_color
        self.update()

    @property
    def normalColor(self) -> QColor: return self.__normalColor

    @normalColor.setter
    def normalColor(self, normal_color: QColor) -> None:
        if self.__normalColor == normal_color: return
        self.__normalColor = normal_color
        self.update()

    @property
    def borderOutColorStart(self) -> QColor: return self.__borderOutColorStart

    @borderOutColorStart.setter
    def borderOutColorStart(self, border_out_color_start: QColor) -> None:
        if self.__borderOutColorStart == border_out_color_start: return
        self.__borderOutColorStart = border_out_color_start
        self.update()

    @property
    def borderOutColorEnd(self) -> QColor: return self.__borderOutColorEnd

    @borderOutColorEnd.setter
    def borderOutColorEnd(self, border_out_color_end: QColor) -> None:
        if self.__borderOutColorEnd == border_out_color_end: return
        self.__borderOutColorEnd = border_out_color_end
        self.update()

    @property
    def borderInColorStart(self) -> QColor: return self.__borderInColorStart

    @borderInColorStart.setter
    def borderInColorStart(self, border_in_color_start: QColor) -> None:
        if self.__borderInColorStart == border_in_color_start: return
        self.__borderInColorStart = border_in_color_start
        self.update()

    @property
    def borderInColorEnd(self) -> QColor: return self.__borderInColorEnd

    @borderInColorEnd.setter
    def borderInColorEnd(self, border_in_color_end: QColor) -> None:
        if self.__borderInColorEnd == border_in_color_end: return
        self.__borderInColorEnd = border_in_color_end
        self.update()

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def canMove(self) -> bool: return self.__canMove

    @canMove.setter
    def canMove(self, can_move: bool) -> None:
        if self.__canMove == can_move: return
        self.__canMove = can_move
        self.update()

    @property
    def showRect(self) -> bool: return self.__showRect

    @showRect.setter
    def showRect(self, show_rect: bool) -> None:
        if self.__showRect == show_rect: return
        self.__showRect = show_rect
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

    def sizeHint(self) -> QSize: return QSize(100, 100)

    def minimumSizeHint(self) -> QSize: return QSize(10, 10)

    def setGreen(self) -> None:
        """ 设置为绿色 """
        self.__textColor = QColor(255, 255, 255)
        self.bgColor = QColor(0, 166, 0)

    def setRed(self) -> None:
        """ 设置为红色 """
        self.__textColor = QColor(255, 255, 255)
        self.bgColor = QColor(255, 0, 0)

    def setYellow(self) -> None:
        """ 设置为黄色 """
        self.__textColor = QColor(25, 50, 7)
        self.bgColor = QColor(238, 238, 0)

    def setBlack(self) -> None:
        """ 设置为黑色 """
        self.__textColor = QColor(255, 255, 255)
        self.bgColor = QColor(10, 10, 10)

    def setGray(self) -> None:
        """ 设置为灰色 """
        self.__textColor = QColor(255, 255, 255)
        self.bgColor = QColor(129, 129, 129)

    def setBlue(self) -> None:
        """ 设置为蓝色 """
        self.__textColor = QColor(255, 255, 255)
        self.bgColor = QColor(0, 0, 166)

    def setLightBlue(self) -> None:
        """ 设置为淡蓝色 """
        self.__textColor = QColor(255, 255, 255)
        self.bgColor = QColor(100, 184, 255)

    def setLightRed(self) -> None:
        """ 设置为淡红色 """
        self.__textColor = QColor(255, 255, 255)
        self.bgColor = QColor(255, 107, 107)

    def setLightGreen(self) -> None:
        """ 设置为淡绿色 """
        self.__textColor = QColor(255, 255, 255)
        self.bgColor = QColor(24, 189, 155)

    def startAlarm(self) -> None:
        """ 开始报警闪烁 """
        if self.__timerAlarm.isActive(): return
        self.__timerAlarm.start()

    def stopAlarm(self) -> None:
        """ 停止报警闪烁 """
        if not self.__timerAlarm.isActive(): return
        self.__timerAlarm.stop()

    def alarm(self) -> None:
        """ 设置闪烁颜色 """
        if self.__isAlarm:
            self.__textColor = QColor(255, 255, 255)
            self.__bgColor = self.__normalColor
        else:
            self.__textColor = QColor(255, 255, 255)
            self.__bgColor = self.__alarmColor

        self.update()
        self.__isAlarm = not self.__isAlarm


if __name__ == '__main__':
    import sys
    from typing import List
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication, QGridLayout, QPushButton, QCheckBox, QFrame, QTextEdit,\
        QSpacerItem, QSizePolicy, QHBoxLayout

    class FrmPanelMoveWidget(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmPanelMoveWidget, self).__init__(parent)
            self.btns: List[LightButton] = []

            layout = QGridLayout()
            self.btnClear = QPushButton('清除')
            self.btnClear.setMinimumWidth(120)
            self.btnShow = QPushButton('显示子元素坐标')
            self.btnShow.setMinimumWidth(120)
            self.checkBox = QCheckBox('可移动')
            self.frame = QFrame()
            self.frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            self.frame.setMinimumHeight(100)
            self.frame.setFrameShape(QFrame.StyledPanel)
            self.frame.setFrameShadow(QFrame.Sunken)
            self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.textEdit = QTextEdit()
            self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.textEdit.setReadOnly(True)

            layout.addWidget(self.frame, 0, 0)
            layout.addWidget(self.textEdit, 1, 0)
            layout2 = QHBoxLayout()
            layout2.addItem(self.horizontalSpacer)
            layout2.addWidget(self.checkBox)
            layout2.addWidget(self.btnShow)
            layout2.addWidget(self.btnClear)

            layout.addLayout(layout2, 2, 0)
            self.setLayout(layout)

            self.initForm()
            self.checkBox.stateChanged.connect(self.on_checkBox_stateChanged)
            self.btnShow.clicked.connect(self.on_btnShow_clicked)
            self.btnClear.clicked.connect(self.on_btnClear_clicked)

        def initForm(self) -> None:
            colors: List[QColor] = [
                QColor(100, 184, 255),
                QColor(255, 107, 107),
                QColor(24, 189, 155),
                QColor(1, 174, 103),
                QColor(52, 73, 94)
            ]

            x: int = 5
            y: int = 5
            radius: int = 50

            for i in range(5):
                btn: LightButton = LightButton(self.frame)

                btn.setGeometry(x, y, radius, radius)
                x = x + radius
                btn.text = "0%d" % (i + 1)
                btn.canMove = False
                btn.showOverlay = False
                btn.bgColor = colors[i]
                self.btns.append(btn)

        def on_checkBox_stateChanged(self, arg1: int) -> None:
            canMove: bool = arg1 != 0

            for btn in self.btns:
                btn.canMove = canMove

        def on_btnShow_clicked(self) -> None:
            for btn in self.btns:
                text: str = btn.text
                x: int = btn.x()
                y: int = btn.y()
                self.textEdit.append("名称:%s\tx:%d\ty:%d" % (text, x, y))

        def on_btnClear_clicked(self) -> None:
            self.textEdit.clear()

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmPanelMoveWidget()
    window.resize(500, 300)
    window.setWindowTitle("移动元素")
    window.show()
    sys.exit(app.exec_())


