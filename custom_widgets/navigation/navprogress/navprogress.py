from enum import Enum
from typing import List, AnyStr

from PySide2.QtCore import QEnum, QSize, Qt, QPoint, QRect
from PySide2.QtGui import QColor, QFont, QPaintEvent, QPainter, QFontDatabase, QPen, QPolygon
from PySide2.QtWidgets import QWidget

from custom_widgets.iconhelper.resource import *


class NavProgress(QWidget):

    """
    导航进度条控件
    作者:feiyangqingyun(QQ:517216493) 2016-11-29
    译者:sunchuquin(QQ:1715216365) 2021-06-28
    1. 可设置前景色/背景色/当前值前景色/当前值背景色
    2. 可设置最大步数及当前第几步
    3. 可设置导航标签队列文字信息
    4. 可设置三种风格样式 京东订单流程样式/淘宝订单流程样式/支付宝订单流程样式
    5. 文字自适应大小
    """

    @QEnum
    class NavStyle(Enum):
        NavStyle_JD = 0  # 京东订单流程样式
        NavStyle_TB = 1  # 淘宝订单流程样式
        NavStyle_ZFB = 2  # 支付宝订单流程样式

    def __init__(self, parent: QWidget = None):
        super(NavProgress, self).__init__(parent)
        self.__topInfo: List[AnyStr] = [
            "step1", "step2", "step3", "step4", "step5"
        ]  # 导航顶部标签数据
        self.__bottomInfo: List[AnyStr] = [
            "2016-11-24 20:57:58", "2016-11-24 21:55:56"
        ]  # 导航底部标签数据

        self.__maxStep: int = 5  # 最大步数
        self.__currentStep: int = 1  # 当前第几步
        self.__navStyle: NavProgress.NavStyle = NavProgress.NavStyle.NavStyle_JD  # 导航样式

        self.__background: QColor = QColor(100, 100, 100)  # 背景色
        self.__foreground: QColor = QColor(255, 255, 255)  # 前景色
        self.__currentBackground: QColor = QColor(100, 184, 255)  # 当前背景色
        self.__currentForeground: QColor = QColor(255, 255, 255)  # 当前前景色

        self.__iconFont: QFont = QFont()

        # 判断图形字体是否存在，不存在则加入
        fontDb: QFontDatabase = QFontDatabase()
        if not fontDb.families().__contains__("FontAwesome"):
            fontId: int = fontDb.addApplicationFont(":/image/fontawesome-webfont.ttf")
            fontName: List[str] = fontDb.applicationFontFamilies(fontId)
            if len(fontName) == 0:
                print("load fontawesome-webfont.ttf error")

        if fontDb.families().__contains__("FontAwesome"):
            self.__iconFont: QFont = QFont("FontAwesome")
            self.__iconFont.setHintingPreference(QFont.PreferNoHinting)  # if Qt version >= 4.8.0

    @property
    def topInfo(self) -> List[AnyStr]: return self.__topInfo

    @topInfo.setter
    def topInfo(self, top_info: List[AnyStr]) -> None:
        if self.__topInfo == top_info: return
        self.__topInfo = top_info
        self.update()

    @property
    def bottomInfo(self) -> List[AnyStr]: return self.__bottomInfo

    @bottomInfo.setter
    def bottomInfo(self, bottom_info: List[AnyStr]) -> None:
        if self.__bottomInfo == bottom_info: return
        self.__bottomInfo = bottom_info
        self.update()

    @property
    def maxStep(self) -> int: return self.__maxStep

    @maxStep.setter
    def maxStep(self, max_step: int) -> None:
        if self.__maxStep == max_step and max_step > self.topInfo.__len__(): return
        self.__maxStep = max_step
        self.update()

    @property
    def currentStep(self) -> int: return self.__currentStep

    @currentStep.setter
    def currentStep(self, current_step: int) -> None:
        if self.__currentStep == current_step and self.__maxStep < current_step <= 0: return
        self.__currentStep = current_step
        self.update()

    @property
    def navStyle(self) -> NavStyle: return self.__navStyle

    @navStyle.setter
    def navStyle(self, nav_style: NavStyle) -> None:
        if self.__navStyle == nav_style: return
        self.__navStyle = nav_style
        self.update()

    @property
    def background(self) -> QColor: return self.__background

    @background.setter
    def background(self, n_background: QColor) -> None:
        if self.__background == n_background: return
        self.__background = n_background
        self.update()

    @property
    def foreground(self) -> QColor: return self.__foreground

    @foreground.setter
    def foreground(self, n_foreground: QColor) -> None:
        if self.__foreground == n_foreground: return
        self.__foreground = n_foreground
        self.update()

    @property
    def currentBackground(self) -> QColor: return self.__currentBackground

    @currentBackground.setter
    def currentBackground(self, current_background: QColor) -> None:
        if self.__currentBackground == current_background: return
        self.__currentBackground = current_background
        self.update()

    @property
    def currentForeground(self) -> QColor: return self.__currentForeground

    @currentForeground.setter
    def currentForeground(self, current_foreground: QColor) -> None:
        if self.__currentForeground == current_foreground: return
        self.__currentForeground = current_foreground
        self.update()

    def sizeHint(self) -> QSize: return QSize(500, 80)

    def minimumSizeHint(self) -> QSize: return QSize(50, 20)

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 根据不一样的样式绘制
        if self.__navStyle == NavProgress.NavStyle.NavStyle_JD:
            # 绘制背景
            self.drawBg_JD(painter)
            # 绘制文字
            self.drawText_JD(painter)
            # 绘制当前背景
            self.drawCurrentBg_JD(painter)
            # 绘制当前文字
            self.drawCurrentText_JD(painter)
        elif self.__navStyle == NavProgress.NavStyle.NavStyle_TB:
            # 绘制背景
            self.drawBg_TB(painter)
            # 绘制文字
            self.drawText_TB(painter)
            # 绘制当前背景
            self.drawCurrentBg_TB(painter)
        elif self.__navStyle == NavProgress.NavStyle.NavStyle_ZFB:
            # 绘制背景
            self.drawBg_ZFB(painter)
            # 绘制文字
            self.drawText_ZFB(painter)
            # 绘制当前背景
            self.drawCurrentBg_ZFB(painter)

    def drawBg_JD(self, painter: QPainter) -> None:
        painter.save()

        # 圆半径为高度一定比例,计算宽度,将宽度等分
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 2
        radius: int = height // 2
        initX: int = width // 2
        initY: int = height // 2 + radius // 5

        # 逐个绘制连接线条
        pen: QPen = QPen()
        pen.setWidthF(radius / 4)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.__background)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__maxStep - 1):
            painter.drawLine(QPoint(initX, initY), QPoint(initX + width, initY))
            initX += width

        # 逐个绘制圆
        initX = width // 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__background)

        for i in range(self.__maxStep):
            painter.drawEllipse(QPoint(initX, initY), radius, radius)
            initX += width

        # 逐个绘制圆中的数字
        initX = width // 2
        font: QFont = QFont()
        font.setPixelSize(radius)
        painter.setFont(font)
        painter.setPen(self.__foreground)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__maxStep):
            textRect: QRect = QRect(initX - radius, initY - radius, radius * 2, radius * 2)
            painter.drawText(textRect, Qt.AlignCenter, str(i + 1))
            initX += width

        painter.restore()

    def drawText_JD(self, painter: QPainter) -> None:
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 2
        initX: int = 0
        initY: int = height

        painter.save()
        font: QFont = QFont()
        font.setPixelSize(height / 3)
        painter.setFont(font)
        painter.setPen(self.__background)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__maxStep):
            textRect: QRect = QRect(initX, initY, width, height)
            painter.drawText(textRect, Qt.AlignCenter, self.__topInfo[i])
            initX += width

        painter.restore()

    def drawCurrentBg_JD(self, painter: QPainter) -> None:
        painter.save()

        # 圆半径为高度一定比例,计算宽度,将宽度等分
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 2
        radius: int = height // 2
        initX: int = width // 2
        initY: int = height // 2 + radius // 5
        radius -= radius / 5

        # 逐个绘制连接线条
        pen: QPen = QPen()
        pen.setWidthF(radius / 7)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.__currentBackground)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__currentStep - 1):
            painter.drawLine(QPoint(initX, initY), QPoint(initX + width, initY))
            initX += width

        # 如果当前进度超过一个步数且小于最大步数则增加半个线条
        if 0 < self.__currentStep < self.__maxStep:
            painter.drawLine(QPoint(initX, initY), QPoint(initX + width // 2, initY))

        # 逐个绘制圆
        initX: int = width // 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__currentBackground)

        for i in range(self.__currentStep):
            painter.drawEllipse(QPoint(initX, initY), radius, radius)
            initX += width

        # 逐个绘制圆中的数字
        initX = width // 2
        font: QFont = QFont()
        font.setPixelSize(radius)
        painter.setFont(font)
        painter.setPen(self.__currentForeground)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__currentStep):
            textRect: QRect = QRect(initX - radius, initY - radius, radius * 2, radius * 2)
            painter.drawText(textRect, Qt.AlignCenter, str(i + 1))
            initX += width

        painter.restore()

    def drawCurrentText_JD(self, painter: QPainter) -> None:
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 2
        initX: int = 0
        initY: int = height

        painter.save()
        font: QFont = QFont()
        font.setPixelSize(height / 3)
        painter.setFont(font)
        painter.setPen(self.__currentBackground)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__currentStep):
            textRect: QRect = QRect(initX, initY, width, height)
            painter.drawText(textRect, Qt.AlignCenter, self.__topInfo[i])
            initX += width

        painter.restore()

    def drawBg_TB(self, painter: QPainter) -> None:
        painter.save()

        # 圆半径为高度一定比例,计算宽度,将宽度等分
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 3
        radius: int = height // 2
        initX: int = width // 2
        initY: int = self.height() // 2

        # 逐个绘制连接线条
        pen: QPen = QPen()
        pen.setWidthF(radius / 4)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.__background)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__maxStep - 1):
            painter.drawLine(QPoint(initX, initY), QPoint(initX + width, initY))
            initX += width

        # 逐个绘制圆
        initX: int = width // 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__background)

        for i in range(self.__maxStep):
            painter.drawEllipse(QPoint(initX, initY), radius, radius)
            initX += width

        # 逐个绘制圆中的数字
        initX = width // 2
        font: QFont = QFont()
        font.setPixelSize(radius)
        painter.setFont(font)
        painter.setPen(self.__foreground)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__maxStep):
            textRect: QRect = QRect(initX - radius, initY - radius, radius * 2, radius * 2)
            painter.drawText(textRect, Qt.AlignCenter, str(i + 1))
            initX += width

        painter.restore()

    def drawText_TB(self, painter: QPainter) -> None:
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 3
        initX: int = 0
        initY: int = 0

        painter.save()
        font: QFont = QFont()
        font.setPixelSize(height // 3)
        painter.setFont(font)
        painter.setPen(self.__background)
        painter.setBrush(Qt.NoBrush)

        # 绘制上部分文字
        for i in range(self.__maxStep):
            textRect: QRect = QRect(initX, initY, width, height)
            painter.drawText(textRect, Qt.AlignCenter, self.__topInfo[i])
            initX += width

        # 绘制下部分文字
        initX = 0
        initY: int = self.height() // 3 * 2

        for i in range(self.__currentStep):
            textRect: QRect = QRect(initX, initY, width, height)
            painter.drawText(textRect, Qt.AlignCenter, self.__bottomInfo[i])
            initX += width

        painter.restore()

    def drawCurrentBg_TB(self, painter: QPainter) -> None:
        painter.save()

        # 圆半径为高度一定比例,计算宽度,将宽度等分
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 3
        radius: int = height // 2
        initX: int = width // 2
        initY: int = self.height() // 2
        radius -= radius // 5

        # 逐个绘制连接线条
        pen: QPen = QPen()
        pen.setWidthF(radius / 7)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.__currentBackground)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__currentStep - 1):
            painter.drawLine(QPoint(initX, initY), QPoint(initX + width, initY))
            initX += width

        # 如果当前进度超过一个步数且小于最大步数则增加半个线条
        if 0 < self.__currentStep < self.__maxStep:
            painter.drawLine(QPoint(initX, initY), QPoint(initX + width // 2, initY))

        # 逐个绘制圆
        initX: int = width // 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__currentBackground)

        for i in range(self.__currentStep):
            painter.drawEllipse(QPoint(initX, initY), radius, radius)
            initX += width

        # 逐个绘制圆中的字符串
        initX: int = width // 2
        self.__iconFont.setPixelSize(radius)
        painter.setFont(self.__iconFont)
        painter.setPen(self.__currentForeground)
        painter.setBrush(Qt.NoBrush)

        # 完成字符,可以查看表格更换图形字符
        finshStr: str = chr(0xf00c)

        for i in range(self.__currentStep):
            textRect: QRect = QRect(initX - radius, initY - radius, radius * 2, radius * 2)
            painter.drawText(textRect, Qt.AlignCenter, finshStr)
            initX += width

        painter.restore()

    def drawBg_ZFB(self, painter: QPainter) -> None:
        painter.save()

        # 圆半径为高度一定比例,计算宽度,将宽度等分
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 3
        radius: int = height // 3
        initX: int = width // 2
        initY: int = self.height() // 2

        # 逐个绘制连接线条
        pen: QPen = QPen()
        pen.setWidthF(radius // 4)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.__background)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for i in range(self.__maxStep - 1):
            painter.drawLine(QPoint(initX, initY), QPoint(initX + width, initY))
            initX += width

        # 逐个绘制圆
        initX: int = width // 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__background)

        for i in range(self.__maxStep):
            painter.drawEllipse(QPoint(initX, initY), radius, radius)
            initX += width

        painter.restore()

    def drawText_ZFB(self, painter: QPainter) -> None:
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 3
        initX: int = 0
        initY: int = 0

        painter.save()
        font: QFont = QFont()
        font.setPixelSize(height / 3)
        painter.setFont(font)
        painter.setPen(self.__background)
        painter.setBrush(Qt.NoBrush)

        # 绘制上部分文字
        for i in range(self.__maxStep):
            textRect: QRect = QRect(initX, initY, width, height)
            painter.drawText(textRect, Qt.AlignCenter, self.__topInfo[i])
            initX += width

        # 绘制下部分文字
        initX: int = 0
        initY: int = self.height() // 3 * 2

        for i in range(self.__maxStep):
            textRect: QRect = QRect(initX, initY, width, height)

            if i is 0:
                painter.drawText(textRect, Qt.AlignCenter, self.__bottomInfo[0])
            elif i == self.__maxStep - 1:
                painter.drawText(textRect, Qt.AlignCenter, self.__bottomInfo[-1])

            initX += width

        painter.restore()

    def drawCurrentBg_ZFB(self, painter: QPainter) -> None:
        painter.save()

        # 圆半径为高度一定比例,计算宽度,将宽度等分
        width: int = self.width() // self.__maxStep
        height: int = self.height() // 3
        radius: int = height // 3
        initX: int = width // 2
        initY: int = self.height() // 2

        # 绘制当前圆
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__currentBackground)

        for i in range(self.__currentStep - 1):
            initX += width

        painter.drawEllipse(QPoint(initX, initY), radius, radius)

        initX = initX - width // 4
        initY = 0
        height = self.height() // 4

        # 绘制当前上部提示信息背景
        bgRect: QRect = QRect(initX, initY, width // 2, height)
        painter.setBrush(self.__currentBackground)
        painter.drawRoundedRect(bgRect, height / 2, height / 2)

        # 绘制当前上部提示信息
        font: QFont = QFont()
        font.setPixelSize(height / 1.9)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(self.__currentForeground)
        painter.drawText(bgRect, Qt.AlignCenter, self.__topInfo[self.__currentStep - 1])

        # 绘制倒三角
        centerX: int = initX + width // 4
        offset: int = 10
        pts: QPolygon = QPolygon()
        pts.append(QPoint(centerX - offset, height))
        pts.append(QPoint(centerX + offset, height))
        pts.append(QPoint(centerX, height + offset))

        painter.setPen(Qt.NoPen)
        painter.drawPolygon(pts)

        painter.restore()


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTimer, QTextCodec
    from PySide2.QtGui import QFont
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QSizePolicy

    class FrmNavProgress(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmNavProgress, self).__init__(parent)
            layout = QVBoxLayout()
            sizePolicy = QSizePolicy()
            sizePolicy.setVerticalStretch(2)
            sizePolicy.setVerticalPolicy(QSizePolicy.Preferred)
            sizePolicy.setHorizontalPolicy(QSizePolicy.Preferred)
            self.navProgress1 = NavProgress()
            self.navProgress1.setSizePolicy(sizePolicy)
            self.navProgress2 = NavProgress()
            self.navProgress2.setSizePolicy(sizePolicy)
            sizePolicy.setVerticalStretch(3)
            self.navProgress3 = NavProgress()
            self.navProgress3.setSizePolicy(sizePolicy)
            self.navProgress4 = NavProgress()
            self.navProgress4.setSizePolicy(sizePolicy)
            self.navProgress5 = NavProgress()
            self.navProgress5.setSizePolicy(sizePolicy)
            self.navProgress6 = NavProgress()
            self.navProgress6.setSizePolicy(sizePolicy)
            layout.addWidget(self.navProgress1)
            layout.addWidget(self.navProgress2)
            layout.addWidget(self.navProgress3)
            layout.addWidget(self.navProgress4)
            layout.addWidget(self.navProgress5)
            layout.addWidget(self.navProgress6)
            self.setLayout(layout)
            QTimer.singleShot(0, self.initForm)

        def initForm(self):
            topInfo: List[AnyStr] = [
                "创建订单", "审核订单", "生产", "配送", "签收"
            ]

            self.navProgress1.topInfo = topInfo
            self.navProgress1.maxStep = 5
            self.navProgress1.currentStep = 3

            self.navProgress2.topInfo = topInfo
            self.navProgress2.maxStep = 5
            self.navProgress2.currentStep = 5
            self.navProgress2.currentBackground = QColor(24,189,155)

            topInfo: List[AnyStr] = [
                "拍下商品", "付款到支付宝", "卖家发货", "确认收货", "评价"
            ]
            bottomInfo: List[AnyStr] = [
                "2016-11-24 20:58:59", "2016-11-24 21:25:26", "2016-11-25 10:25:26",
                "2016-11-25 15:26:58", "2016-11-25 20:36:39"
            ]

            self.navProgress3.topInfo = topInfo
            self.navProgress3.bottomInfo = bottomInfo
            self.navProgress3.maxStep = 5
            self.navProgress3.currentStep = 3
            self.navProgress3.navStyle = NavProgress.NavStyle.NavStyle_TB

            self.navProgress4.topInfo = topInfo
            self.navProgress4.bottomInfo = bottomInfo
            self.navProgress4.maxStep = 5
            self.navProgress4.currentStep = 5
            self.navProgress4.currentBackground = QColor(24,189,155)
            self.navProgress4.navStyle = NavProgress.NavStyle.NavStyle_TB

            topInfo: List[AnyStr] = [
                "已发货", "运输中", "派件中", "已签收", "已评价"
            ]
            bottomInfo: List[AnyStr] = [
                "深圳市", "上海市"
            ]

            self.navProgress5.topInfo = topInfo
            self.navProgress5.bottomInfo = bottomInfo
            self.navProgress5.maxStep = 5
            self.navProgress5.currentStep = 3
            self.navProgress5.navStyle = NavProgress.NavStyle.NavStyle_ZFB

            self.navProgress6.topInfo = topInfo
            self.navProgress6.bottomInfo = bottomInfo
            self.navProgress6.maxStep = 5
            self.navProgress6.currentStep = 5
            self.navProgress6.currentBackground = QColor(24, 189, 155)
            self.navProgress6.navStyle = NavProgress.NavStyle.NavStyle_ZFB

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmNavProgress()
    window.setWindowTitle('导航进度条')
    window.show()
    sys.exit(app.exec_())
