from typing import List, AnyStr

from PySide2.QtCore import QDate, QEvent, QSize, Qt, QPointF, QRectF
from PySide2.QtGui import QMouseEvent, QPaintEvent, QColor, QPainter, QCursor, QRadialGradient, QPen
from PySide2.QtWidgets import QWidget


class ShadowCalendar(QWidget):
    """
    光晕日历控件
    作者:雨田哥(QQ:3246214072)
    整理:feiyangqingyun(QQ:517216493) 2019-10-07
    译者:sunchuquin(QQ:1715216365) 2021-06-27
    1. 可设置背景颜色
    2. 可设置光晕颜色
    3. 可设置文字颜色
    4. 可设置选中日期背景
    5. 光晕跟随鼠标移动
    """

    class DateItem:
        def __init__(self):
            self.year: int = -1
            self.month: int = -1
            self.day: int = -1

    def __init__(self, parent: QWidget = None):
        super(ShadowCalendar, self).__init__(parent)
        self.__bgColor: QColor = QColor("#212425")  # 背景颜色
        self.__textColor: QColor = QColor("#FFFFFF")  # 文字颜色
        self.__shadowColor: QColor = QColor("#FFFFFF")  # 光晕颜色
        self.__selectColor: QColor = QColor("#0078D7")  # 选中颜色

        self.__selectDate: QDate = QDate()  # 今天日期
        self.__dateItem: List[List[ShadowCalendar.DateItem], ]
        self.__dateItem = [[ShadowCalendar.DateItem() for column in range(7)] for row in range(6)]  # 日期数组 [6][7]

        # 首次主动设置日期
        self.updateCalendar(QDate.currentDate())

        # 开启鼠标追踪
        self.setMouseTracking(True)

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def textColor(self) -> QColor: return self.__textColor

    @textColor.setter
    def textColor(self, text_color: QColor) -> None:
        if self.__textColor == text_color: return
        self.__textColor = text_color
        self.update()

    @property
    def shadowColor(self) -> QColor: return self.__shadowColor

    @shadowColor.setter
    def shadowColor(self, shadow_color: QColor) -> None:
        if self.__shadowColor == shadow_color: return
        self.__shadowColor = shadow_color
        self.update()

    @property
    def selectColor(self) -> QColor: return self.__selectColor

    @selectColor.setter
    def selectColor(self, select_color: QColor) -> None:
        if self.__selectColor == select_color: return
        self.__selectColor = select_color
        self.update()

    def sizeHint(self) -> QSize: return QSize(370, 355)

    def minimumSizeHint(self) -> QSize: return QSize(100, 85)

    def updateCalendar(self, select_date: QDate) -> None:
        if self.__selectDate == select_date: return
        row: int = 0
        dateItem: List[List[ShadowCalendar.DateItem], ] = \
            [[ShadowCalendar.DateItem() for column in range(7)] for row in range(6)]
        date: QDate = QDate(select_date.year(), select_date.month(), 1)
        while date.month() == select_date.month():
            weekDay: int = date.dayOfWeek()
            dateItem[row][weekDay - 1].year = date.year()
            dateItem[row][weekDay - 1].month = date.month()
            dateItem[row][weekDay - 1].day = date.day()
            date = date.addDays(1)
            if weekDay is 7 and date.month() is date.month():
                row += 1

        # 重新赋值
        for i in range(6):
            for j in range(7):
                self.__dateItem[i][j] = dateItem[i][j]

        self.__selectDate = select_date
        self.update()

    def leaveEvent(self, event: QEvent) -> None: self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None: self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        sw: int = 336
        sh: int = 336
        scaleX: float = self.width() * 1.0 / sw
        scaleY: float = self.height() * 1.0 / sh

        painter.scale(scaleX, scaleY)
        painter.setPen(Qt.NoPen)
        painter.fillRect(0, 0, sw, sh, self.__bgColor)

        iw: float = sw / 7.0
        ih: float = sh / 7.0

        # mask
        globalpoint: QPointF = self.mapFromGlobal(QCursor.pos())
        point: QPointF = QPointF(globalpoint.x() / scaleX, globalpoint.y() / scaleY)

        # 绘制光晕背景
        if self.underMouse():
            effectradius: int = 58
            painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
            radialGrad: QRadialGradient = QRadialGradient(point, effectradius)
            radialGrad.setColorAt(0, QColor(0, 0, 0, 120))
            radialGrad.setColorAt(1, QColor(0, 0, 0, 255))
            painter.setBrush(radialGrad)
            painter.drawEllipse(point, effectradius, effectradius)

            painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
            painter.setBrush(Qt.NoBrush)

            for row in range(6):
                for column in range(7):
                    rect: QRectF = QRectF(column * iw, (row + 1) * ih, iw, ih).adjusted(3, 3, -3, -3)
                    if rect.contains(point):
                        painter.save()
                        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
                        painter.setPen(QPen(QColor(220, 220, 220, 160), 2))
                        painter.drawRoundedRect(rect, 2, 2)
                        painter.restore()
                        continue
                    else:
                        painter.setPen(QPen(self.__shadowColor, 2))

                    painter.drawRoundedRect(rect, 2, 2)

            # 绘制圆形的光晕底层背景
            painter.fillRect(0, 0, sw, sh, QColor(200, 200, 200, 50))

        # 绘制头部中文数字,先设置图像叠加模式为源在上面
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.setPen(self.__textColor)
        listHead: List[AnyStr] = ["一", "二", "三", "四", "五", "六", "日"]
        for i in range(7):
            painter.drawText(i * iw, 0, iw, ih, Qt.AlignCenter, listHead[i])

        # 绘制日期
        for row in range(6):
            for column in range(7):
                if self.__dateItem[row][column].day > 0:
                    rect: QRectF = QRectF(column * iw, (row + 1) * ih, iw, ih).adjusted(3, 3, -3, -3)

                    # 如果是选中的日期则突出绘制背景
                    if QDate.currentDate() == QDate(self.__dateItem[row][column].year,
                                                    self.__dateItem[row][column].month,
                                                    self.__dateItem[row][column].day):
                        painter.setPen(QPen(self.__selectColor, 2))
                        painter.setBrush(Qt.NoBrush)

                        # 如果和光晕效果重叠则边框高亮
                        if rect.contains(point):
                            painter.setPen(QPen(self.__selectColor.lighter(), 2))

                        # 绘制圆角边框
                        painter.drawRoundedRect(rect, 2, 2)

                        # 绘制里边背景
                        painter.setPen(Qt.NoPen)
                        painter.setBrush(self.__selectColor)
                        painter.drawRoundedRect(rect.adjusted(4, 4, -4, -4), 2, 2)

                    painter.setPen(self.__textColor)
                    painter.drawText(rect, Qt.AlignCenter, str(self.__dateItem[row][column].day))


if __name__ == '__main__':
    import sys
    from PySide2.QtGui import QFont, QFontDatabase, QPalette
    from PySide2.QtCore import QDateTime, QRect, QTextCodec
    from PySide2.QtWidgets import QApplication, QFrame, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
    from custom_widgets.iconhelper.resource import *
    from custom_widgets.line.line import Line

    class FrmShadowCalendar(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmShadowCalendar, self).__init__(parent)

            self.__iconFont: QFont = QFont()
            self.currentDate: QDateTime = QDateTime()

            self.shadowCalendar: ShadowCalendar = ShadowCalendar()
            self.widgetTop: QWidget = QWidget()
            self.btnDown: QPushButton = QPushButton()
            self.btnDown.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
            self.btnDown.setMinimumWidth(40)
            self.btnUp: QPushButton = QPushButton()
            self.btnUp.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
            self.btnUp.setMinimumWidth(40)
            self.labInfo: QLabel = QLabel()
            self.labInfo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.line = Line(shape=QFrame.HLine, color=QColor("#888888"))

            layout: QHBoxLayout = QHBoxLayout()
            layout.addWidget(self.labInfo)
            layout.addWidget(self.btnUp)
            layout.addWidget(self.btnDown)
            layout.setGeometry(QRect(0, 9, 0, 9))
            layout.setSpacing(6)
            self.widgetTop.setLayout(layout)

            layout: QVBoxLayout = QVBoxLayout()
            layout.addWidget(self.widgetTop)
            layout.addWidget(self.line)
            layout.addWidget(self.shadowCalendar)
            self.setLayout(layout)

            self.initForm()
            self.btnUp.clicked.connect(self.on_btnUp_clicked)
            self.btnDown.clicked.connect(self.on_btnDown_clicked)

        def initForm(self):
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

            # 设置图形字体
            self.__iconFont.setPixelSize(30)
            self.btnUp.setFont(self.__iconFont)
            self.btnDown.setFont(self.__iconFont)
            self.btnUp.setText(chr(0xf106))
            self.btnDown.setText(chr(0xf107))

            # 设置样式表
            self.btnDown.setStyleSheet("QPushButton{color:#FFFFFF;background:rgba(0,0,0,0);padding:0px;}"
                                       "QPushButton:hover{color:#43C1FB;}")
            self.btnUp.setStyleSheet("QPushButton{color:#FFFFFF;background:rgba(0,0,0,0);padding:0px;}"
                                     "QPushButton:hover{color:#43C1FB;}")
            self.labInfo.setStyleSheet("QLabel{font:18px;color:#43C1FB;}")

            palette: QPalette = self.palette()
            palette.setBrush(QPalette.Background, QColor("#212425"))
            self.setPalette(palette)
            self.setAutoFillBackground(True)

            self.currentDate = QDateTime.currentDateTime()
            self.updateInfo()

        def updateInfo(self):
            self.labInfo.setText(self.currentDate.toString("yyyy年MM月dd日  ddd"))

        def on_btnUp_clicked(self):
            self.currentDate = self.currentDate.addMonths(-1)
            self.shadowCalendar.updateCalendar(self.currentDate.date())
            self.updateInfo()

        def on_btnDown_clicked(self):
            self.currentDate = self.currentDate.addMonths(1)
            self.shadowCalendar.updateCalendar(self.currentDate.date())
            self.updateInfo()

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 10))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmShadowCalendar()
    window.setWindowTitle("光晕日历控件")
    window.show()
    sys.exit(app.exec_())
