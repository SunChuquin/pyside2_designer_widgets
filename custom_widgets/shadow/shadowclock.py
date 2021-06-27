from typing import List, AnyStr

from PySide2.QtCore import QPropertyAnimation, QDateTime, QTime, Qt, QPointF, QSize
from PySide2.QtGui import QPaintEvent, QPainter, QColor, QRadialGradient, QFont, QFontMetricsF, QPainterPath, QPen, \
    QBrush
from PySide2.QtWidgets import QWidget


class ShadowClock(QWidget):
    """
    光晕时钟控件
    作者:雨田哥(QQ:3246214072)
    整理:feiyangqingyun(QQ:517216493) 2019-10-07
    译者:sunchuquin(QQ:1715216365) 2021-06-27
    1. 可设置圆弧半径宽度
    2. 可设置光晕宽度
    3. 可设置光晕颜色
    4. 可设置文本颜色
    5. 可分辨设置时钟/分钟/秒钟的颜色
    6. 采用动画机制平滑进度展示时间
    """
    def __init__(self, parent: QWidget = None):
        super(ShadowClock, self).__init__(parent)
        self.__radiusWidth: int = 6  # 半径宽度
        self.__shadowWidth: int = 4  # 光晕宽度

        self.__textColor: QColor = QColor("#22A3A9")  # 文本颜色
        self.__shadowColor: QColor = QColor("#22A3A9")  # 光晕颜色
        self.__hourColor: QColor = QColor("#22A3A9")  # 时钟颜色
        self.__minuteColor: QColor = QColor("#22A3A9")  # 分钟颜色
        self.__secondColor: QColor = QColor("#22A3A9")  # 秒钟颜色

        # 采用动画机制,产生过渡效果
        self.animation: QPropertyAnimation = QPropertyAnimation(self, b'')
        self.animation.valueChanged.connect(self.update)
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(20)
        self.animation.setLoopCount(-1)
        self.animation.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        width: int = self.width()
        height: int = self.height()
        side: int = min(width, height)

        # 绘制准备工作,启用反锯齿,平移坐标轴中心,等比例缩放
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.translate(width / 2.0, height / 2.0)
        painter.scale(side / 200.0, side / 200.0)

        # 绘制时圆弧
        n_now: QDateTime = QDateTime.currentDateTime()
        n_time: QTime = n_now.time()
        n_hour: int = n_time.hour() - 12 if n_time.hour() >= 12 else n_time.hour()
        n_min: int = n_time.minute()
        n_sec: int = n_time.second()
        n_msec: int = n_time.msec()

        n_dsec: float = n_sec + n_msec / 1000.0
        n_dmin: float = n_min + n_dsec / 60.0
        n_dhour: float = n_hour + n_dmin / 60.0

        # 绘制时圆弧
        self.drawArc(painter, 94, n_dhour * 30, self.__hourColor)
        # 绘制分圆弧
        self.drawArc(painter, 81, n_dmin * 6, self.__minuteColor)
        # 绘制秒圆弧
        self.drawArc(painter, 68, n_dsec * 6, self.__secondColor)
        # 绘制时间文本
        self.drawText(painter)

    def drawArc(self, painter: QPainter, radius: int, angle: float, arc_color: QColor) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)

        smallradius: int = radius - self.__radiusWidth
        maxRaidus: int = radius + self.__shadowWidth
        minRadius: int = smallradius - self.__shadowWidth

        # 采用圆形渐变,形成光晕效果
        radialGradient: QRadialGradient = QRadialGradient(QPointF(0, 0), maxRaidus)
        color: QColor = arc_color
        lightColor: QColor = arc_color.name()

        color.setAlphaF(0)
        radialGradient.setColorAt(0, color)
        radialGradient.setColorAt(minRadius * 1.0 / maxRaidus, color)
        color.setAlphaF(0.5)
        radialGradient.setColorAt(smallradius * 1.0 / maxRaidus, color)

        radialGradient.setColorAt((smallradius + 1) * 1.0 / maxRaidus, lightColor)
        radialGradient.setColorAt((radius - 1) * 1.0 / maxRaidus, lightColor)
        radialGradient.setColorAt(radius * 1.0 / maxRaidus, color)
        color.setAlphaF(0)
        radialGradient.setColorAt(1, color)

        painter.setBrush(QBrush(radialGradient))
        painter.drawPie(-maxRaidus, -maxRaidus, maxRaidus * 2, maxRaidus * 2, 90 * 16, int(-angle * 16))
        painter.restore()

    def drawText(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(Qt.NoPen)

        font: QFont = QFont()
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)

        now: QDateTime = QDateTime.currentDateTime()
        fm: QFontMetricsF = QFontMetricsF(font)
        textList: List[AnyStr] = [now.toString("MM月dd日yyyy"), now.toString("hh:mm:ss.zzz")]

        # 绘制文本路径
        textPath: QPainterPath = QPainterPath()
        textPath.addText(-fm.width(textList[0]) / 2.0, -fm.lineSpacing() / 2.0, font, textList[0])
        textPath.addText(-fm.width(textList[1]) / 2.0, fm.lineSpacing() / 2.0, font, textList[1])

        strokeColor: QColor = self.__textColor.light(80)
        strokeColor.setAlphaF(0.2)
        painter.strokePath(textPath, QPen(strokeColor, self.__shadowWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(self.__textColor)
        painter.drawPath(textPath)

        painter.restore()

    @property
    def radiusWidth(self) -> int: return self.__radiusWidth

    @radiusWidth.setter
    def radiusWidth(self, radius_width: int) -> None:
        if self.__radiusWidth == radius_width: return
        self.__radiusWidth = radius_width
        self.update()

    @property
    def shadowWidth(self) -> int: return self.__shadowWidth

    @shadowWidth.setter
    def shadowWidth(self, shadow_width: int) -> None:
        if self.__shadowWidth == shadow_width: return
        self.__shadowWidth = shadow_width
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
        self.__hourColor = shadow_color
        self.__minuteColor = shadow_color
        self.__secondColor = shadow_color
        self.update()

    @property
    def hourColor(self) -> QColor: return self.__hourColor

    @hourColor.setter
    def hourColor(self, hour_color: QColor) -> None:
        if self.__hourColor == hour_color: return
        self.__hourColor = hour_color
        self.update()

    @property
    def minuteColor(self) -> QColor: return self.__minuteColor

    @minuteColor.setter
    def minuteColor(self, minute_color: QColor) -> None:
        if self.__minuteColor == minute_color: return
        self.__minuteColor = minute_color
        self.update()

    @property
    def secondColor(self) -> QColor: return self.__secondColor

    @secondColor.setter
    def secondColor(self, second_color: QColor) -> None:
        if self.__secondColor == second_color: return
        self.__secondColor = second_color
        self.update()

    def sizeHint(self) -> QSize: return QSize(200, 200)

    def minimumSizeHint(self) -> QSize: return QSize(20, 20)


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec
    from PySide2.QtGui import QPalette
    from PySide2.QtWidgets import QApplication, QGridLayout

    class FrmShadowClock(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmShadowClock, self).__init__(parent)
            self.shadowClock1 = ShadowClock()
            self.shadowClock2 = ShadowClock()
            self.shadowClock3 = ShadowClock()
            self.shadowClock4 = ShadowClock()
            self.shadowClock5 = ShadowClock()
            self.shadowClock6 = ShadowClock()
            self.initForm()

            layout = QGridLayout()
            layout.addWidget(self.shadowClock1, 0, 0)
            layout.addWidget(self.shadowClock2, 0, 1)
            layout.addWidget(self.shadowClock3, 0, 2)
            layout.addWidget(self.shadowClock4, 1, 0)
            layout.addWidget(self.shadowClock5, 1, 1)
            layout.addWidget(self.shadowClock6, 1, 2)
            self.setLayout(layout)

        def initForm(self):
            palette: QPalette = self.palette()
            palette.setBrush(QPalette.Background, QColor("#2C3E50"))
            self.setPalette(palette)
            self.setAutoFillBackground(True)

            self.shadowClock1.textColor = QColor("#00FFFF")
            self.shadowClock2.textColor = QColor("#FDC150")
            self.shadowClock3.textColor = QColor("#FDA356")
            self.shadowClock4.textColor = QColor("#EB766E")
            self.shadowClock5.textColor = QColor("#A3DAD7")
            self.shadowClock6.textColor = QColor("#9DBCFF")

            self.shadowClock1.shadowColor = QColor("#00FFFF")
            self.shadowClock2.shadowColor = QColor("#FDC150")
            self.shadowClock3.shadowColor = QColor("#FDA356")
            self.shadowClock4.shadowColor = QColor("#EB766E")
            self.shadowClock5.shadowColor = QColor("#A3DAD7")
            self.shadowClock6.shadowColor = QColor("#9DBCFF")

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmShadowClock()
    window.setWindowTitle("光晕时钟控件")
    window.show()
    sys.exit(app.exec_())
