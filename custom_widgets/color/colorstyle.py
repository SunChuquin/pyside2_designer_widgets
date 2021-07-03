from typing import List

from PySide2.QtCore import QEvent, QSize, Signal, Qt, QRect
from PySide2.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QFont, QFontDatabase, QPen
from PySide2.QtWidgets import QWidget

from custom_widgets.iconhelper.resource import *

class ColorStyle(QWidget):
    """
    颜色样式选择控件
    作者:feiyangqingyun(QQ:517216493) 2017-9-10
    译者:sunchuquin(QQ:1715216365) 2021-07-03
    1. 可设置背景颜色
    2. 可设置角标颜色
    3. 可设置角标大小
    """
    selected = Signal(QColor)  # bgColor

    def __init__(self, parent: QWidget = None):
        super(ColorStyle, self).__init__(parent)
        self.__bgColor: QColor = QColor("#26282C")  # 背景颜色
        self.__signColor: QColor = QColor("#CD2929")  # 选中符号颜色
        self.__signSize: int = 30  # 选中符号大小
        self.__checked: bool = False  # 是否选中
        self.__hovered: bool = False  # 是否永久悬停

        self.__iconFont: QFont = QFont()  # 图形字体
        self.__hover: bool = False  # 当前是否悬停

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

    def enterEvent(self, event: QEvent) -> None:
        self.__hover = True
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        self.__hover = False
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.checked = not self.__checked

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景
        self.drawBg(painter)
        # 绘制选中标记符号
        self.drawSign(painter)

    def drawBg(self, painter: QPainter) -> None:
        painter.save()

        # 如果悬停则绘制外边框和内边框
        if self.__hover or self.__hovered:
            painter.setBrush(Qt.NoBrush)

            pen: QPen = QPen()
            pen.setWidth(2)

            # 绘制外边框
            pen.setColor(self.__bgColor)
            painter.setPen(pen)
            painter.drawRect(5, 5, self.width() - 10, self.height() - 10)

            # 绘制里边框
            pen.setColor("#FFFFFF")
            painter.setPen(pen)
            painter.drawRect(7, 7, self.width() - 14, self.height() - 14)

        # 绘制里边背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.__bgColor))
        painter.drawRect(8, 8, self.width() - 16, self.height() - 16)

        painter.restore()

    def drawSign(self, painter: QPainter) -> None:
        painter.save()

        # 如果当前选中则绘制角标
        if self.__checked:
            # 计算角标区域
            rec: QRect = QRect(self.width() - self.__signSize,
                               self.height() - self.__signSize,
                               self.__signSize,
                               self.__signSize)

            # 绘制带边框背景
            pen: QPen = QPen()
            pen.setWidth(3)
            pen.setColor("#FFFFFF")

            painter.setPen(pen)
            painter.setBrush(QColor(self.__signColor))
            painter.drawEllipse(rec.x() + 3,
                                rec.y() + 3,
                                self.__signSize - 6,
                                self.__signSize - 6)

            # 绘制文字
            self.__iconFont.setPixelSize(16)
            painter.setFont(self.__iconFont)
            painter.drawText(rec, Qt.AlignCenter, chr(0xf00c))

        painter.restore()

    def sizeHint(self) -> QSize: return QSize(120, 120)

    def minimumSizeHint(self) -> QSize: return QSize(50, 50)

    @property
    def bgColor(self) -> QColor: return self.__bgColor

    @bgColor.setter
    def bgColor(self, bg_color: QColor) -> None:
        if self.__bgColor == bg_color: return
        self.__bgColor = bg_color
        self.update()

    @property
    def signColor(self) -> QColor: return self.__signColor

    @signColor.setter
    def signColor(self, sign_color: QColor) -> None:
        if self.__signColor == sign_color: return
        self.__signColor = sign_color
        self.update()

    @property
    def signSize(self) -> int: return self.__signSize

    @signSize.setter
    def signSize(self, sign_size: int) -> None:
        if self.__signSize == sign_size: return
        self.__signSize = sign_size
        self.update()

    @property
    def checked(self) -> bool: return self.__checked

    @checked.setter
    def checked(self, n_checked: bool) -> None:
        if self.__checked == n_checked: return
        self.__checked = n_checked
        self.update()
        if n_checked: self.selected.emit(self.__bgColor)

    @property
    def hovered(self) -> bool: return self.__hovered

    @hovered.setter
    def hovered(self, n_hovered: bool) -> None:
        if self.__hovered == n_hovered: return
        self.__hovered = n_hovered
        self.update()


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication, QGridLayout, QLabel, QSlider, QHBoxLayout, QVBoxLayout

    class FrmColorStyle(QWidget):

        changeStyle = Signal(str)  # color

        def __init__(self, parent: QWidget = None):
            super(FrmColorStyle, self).__init__(parent)

            self.resize(500, 300)

            self.labRed = QLabel('红色')
            self.sliderRed = QSlider()
            self.sliderRed.setMaximum(255)
            self.sliderRed.setOrientation(Qt.Horizontal)
            self.labGreen = QLabel('绿色')
            self.sliderGreen = QSlider()
            self.sliderGreen.setMaximum(255)
            self.sliderGreen.setOrientation(Qt.Horizontal)
            self.labBlue = QLabel('蓝色')
            self.sliderBlue = QSlider()
            self.sliderBlue.setMaximum(255)
            self.sliderBlue.setOrientation(Qt.Horizontal)
            layout = QGridLayout()
            layout.addWidget(self.labRed, 0, 0)
            layout.addWidget(self.sliderRed, 0, 1)
            layout.addWidget(self.labGreen, 1, 0)
            layout.addWidget(self.sliderGreen, 1, 1)
            layout.addWidget(self.labBlue, 2, 0)
            layout.addWidget(self.sliderBlue, 2, 1)

            self.colorStyle0 = ColorStyle()
            self.labValue = QLabel()
            layout2 = QHBoxLayout()
            layout2.addWidget(self.labValue)
            self.colorStyle0.setLayout(layout2)
            layout3 = QHBoxLayout()
            layout3.addWidget(self.colorStyle0)
            layout3.addLayout(layout)

            layout4 = QGridLayout()
            self.colorStyle1 = ColorStyle()
            layout4.addWidget(self.colorStyle1, 0, 0)
            self.colorStyle2 = ColorStyle()
            layout4.addWidget(self.colorStyle2, 0, 1)
            self.colorStyle3 = ColorStyle()
            layout4.addWidget(self.colorStyle3, 0, 2)
            self.colorStyle4 = ColorStyle()
            layout4.addWidget(self.colorStyle4, 0, 3)
            self.colorStyle5 = ColorStyle()
            layout4.addWidget(self.colorStyle5, 0, 4)
            self.colorStyle6 = ColorStyle()
            layout4.addWidget(self.colorStyle6, 1, 0)
            self.colorStyle7 = ColorStyle()
            layout4.addWidget(self.colorStyle7, 1, 1)
            self.colorStyle8 = ColorStyle()
            layout4.addWidget(self.colorStyle8, 1, 2)
            self.colorStyle9 = ColorStyle()
            layout4.addWidget(self.colorStyle9, 1, 3)
            self.colorStyle10 = ColorStyle()
            layout4.addWidget(self.colorStyle10, 1, 4)
            self.colorStyle11 = ColorStyle()
            layout4.addWidget(self.colorStyle11, 2, 0)
            self.colorStyle12 = ColorStyle()
            layout4.addWidget(self.colorStyle12, 2, 1)
            self.colorStyle13 = ColorStyle()
            layout4.addWidget(self.colorStyle13, 2, 2)
            self.colorStyle14 = ColorStyle()
            layout4.addWidget(self.colorStyle14, 2, 3)
            self.colorStyle15 = ColorStyle()
            layout4.addWidget(self.colorStyle15, 2, 4)

            layout5 = QVBoxLayout()
            layout5.addLayout(layout4)
            layout5.addLayout(layout3)
            self.setLayout(layout5)

            self.widgets: List[ColorStyle] = []
            self.initForm()

        def initForm(self):
            colors: List[str] = [
                "#26282C", "#C62F2F", "#FB79A5", "#4BACF8", "#159C77",
                "#FF5C8A", "#FF7A9E", "#FE76C8", "#717FF9", "#39AFEA",
                "#2BB669", "#6ACC19", "#E2AB12", "#FD726D", "#FD544E"
            ]

            self.widgets = [
                self.colorStyle1, self.colorStyle2, self.colorStyle3, self.colorStyle4, self.colorStyle5,
                self.colorStyle6, self.colorStyle7, self.colorStyle8, self.colorStyle9, self.colorStyle10,
                self.colorStyle11, self.colorStyle12, self.colorStyle13, self.colorStyle14, self.colorStyle15
            ]

            for i in range(len(self.widgets)):
                self.widgets[i].bgColor = colors[i]
                self.widgets[i].selected.connect(self.selected)

            self.sliderRed.sliderMoved.connect(self.sliderMoved)
            self.sliderGreen.sliderMoved.connect(self.sliderMoved)
            self.sliderBlue.sliderMoved.connect(self.sliderMoved)

            self.colorStyle1.checked = True
            self.colorStyle0.hovered = True

        def selected(self, color: QColor):
            w: ColorStyle = self.sender()
            for widget in self.widgets:
                if widget != w:
                    widget.checked = False

            self.sliderRed.setValue(color.red())
            self.sliderGreen.setValue(color.green())
            self.sliderBlue.setValue(color.blue())

            # 根据背景色自动计算合适的前景色
            gray: float = (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
            textColor: QColor = QColor(Qt.black) if gray > 0.5 else QColor(Qt.white)
            self.labValue.setStyleSheet("font:16px;color:%s;" % textColor.name())

            self.labValue.setText(color.name().upper())
            self.colorStyle0.bgColor = color
            self.colorStyle0.checked = False
            self.changeStyle.emit(color.name())

        def sliderMoved(self, value):
            for widget in self.widgets:
                widget.checked = False

            if value < 3:
                self.sender().setValue(0)
            elif value > 253:
                self.sender().setValue(255)

            color: QColor = QColor(self.sliderRed.value(),
                                   self.sliderGreen.value(),
                                   self.sliderBlue.value())

            # 根据背景色自动计算合适的前景色
            gray: float = (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
            textColor: QColor = QColor(Qt.black) if gray > 0.5 else QColor(Qt.white)
            self.labValue.setStyleSheet("font:16px;color:%s;" % textColor.name())

            self.labValue.setText(color.name().upper())
            self.colorStyle0.bgColor = color
            self.colorStyle0.checked = True
            self.changeStyle.emit(color.name())

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmColorStyle()
    window.setWindowTitle("颜色样式选择控件")
    window.show()
    sys.exit(app.exec_())
