from enum import Enum
from typing import List

from PySide2.QtCore import QEnum, Signal, QObject, QEvent, QPoint, Qt, QRect, QSize
from PySide2.QtGui import QColor, QFont, QPixmap, QMouseEvent, QPaintEvent, QPainter, QPen, QBrush, QLinearGradient
from PySide2.QtWidgets import QWidget


class ColorButton(QWidget):

    """
    多样式超级按钮控件
    作者:feiyangqingyun(QQ:517216493) 2017-9-24
    译者:sunchuquin(QQ:1715216365) 2021-06-29
    1. 可设置圆角角度,边框宽度
    2. 可设置角标和正文文字内容/字体/对齐方式/颜色
    3. 可设置边框颜色,正常颜色,按下颜色
    4. 可设置背景图片
    5. 可设置按钮颜色模式
    """

    clicked = Signal()

    @QEnum
    class ColorMode(Enum):
        ColorMode_Normal = 0  # 松开按下两种颜色
        ColorMode_Replace = 1  # 按下松开颜色上下交替
        ColorMode_Shade = 2  # 按下松开颜色渐变交替

    @QEnum
    class TextAlign(Enum):
        TextAlign_Top_Left = 0  # 顶部左侧
        TextAlign_Top_Center = 1  # 顶部居中
        TextAlign_Top_Right = 2  # 顶部右侧
        TextAlign_Center_Left = 3  # 中间左侧
        TextAlign_Center_Center = 4  # 中间居中
        TextAlign_Center_Right = 5  # 中间右侧
        TextAlign_Bottom_Left = 6  # 底部左侧
        TextAlign_Bottom_Center = 7  # 底部居中
        TextAlign_Bottom_Right = 8  # 底部右侧

    def __init__(self, parent: QWidget = None):
        super(ColorButton, self).__init__(parent)
        self.__borderRadius: int = 5  # 圆角半径
        self.__borderWidth: int = 2  # 边框宽度
        self.__borderColor: QColor = QColor(180, 180, 180)  # 边框颜色

        self.__showSuperText: bool = False  # 显示角标
        self.__superText: str = '1'  # 角标文字
        self.__superTextFont: QFont = self.font()  # 角标文字字体
        self.__superTextAlign: ColorButton.TextAlign = ColorButton.TextAlign.TextAlign_Top_Left  # 角标文字对齐方式
        self.__superTextColor: QColor = QColor(230, 230, 230)  # 角标文字颜色

        self.__text: str = ''  # 文字
        self.__textFont: QFont = self.font()  # 文字字体
        self.__textAlign: ColorButton.TextAlign = ColorButton.TextAlign.TextAlign_Center_Center  # 文字对齐方式
        self.__textColor: QColor = QColor(230, 230, 230)  # 文字颜色

        self.__normalColor: QColor = QColor(80, 80, 80)  # 正常颜色
        self.__pressedColor: QColor = QColor(30, 30, 30)  # 按下颜色

        self.__canMove: bool = False  # 是否能移动
        self.__bgImage: QPixmap = QPixmap()  # 背景图片
        self.__colorMode: ColorButton.ColorMode = ColorButton.ColorMode.ColorMode_Normal  # 背景色模式

        self.__isPressed: bool = False  # 是否按下

        self.__lastPoint: QPoint = QPoint()

        self.installEventFilter(self)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.isEnabled(): return
        self.clicked.emit()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if not self.isEnabled():
            return super(ColorButton, self).eventFilter(watched, event)

        if event.type() == QEvent.MouseButtonPress:
            e: QMouseEvent = event
            if self.rect().contains(e.pos()) and e.button() == Qt.LeftButton:
                self.__lastPoint = e.pos()
                self.__isPressed = True
                self.update()
        elif event.type() == QEvent.MouseMove and self.__isPressed and self.__canMove:
            e: QMouseEvent = event
            dx: int = e.pos().x() - self.__lastPoint.x()
            dy: int = e.pos().y() - self.__lastPoint.y()
            self.move(self.x() + dx, self.y() + dy)
            return True
        elif event.type() == QEvent.MouseButtonRelease and self.__isPressed:
            self.isPressed = False
            self.update()

        return super(ColorButton, self).eventFilter(watched, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景
        self.drawBg(painter)
        # 绘制文字
        self.drawText(painter)

    def drawBg(self, painter: QPainter) -> None:
        painter.save()

        # 设置边框颜色及宽度
        pen: QPen = QPen()
        pen.setColor(self.__borderColor)
        pen.setWidthF(self.__borderWidth)
        painter.setPen(pen)

        # 绘制区域要减去边框宽度
        rect: QRect = QRect()
        rect.setX(self.__borderWidth)
        rect.setY(self.__borderWidth)
        rect.setWidth(self.width() - self.__borderWidth * 2)
        rect.setHeight(self.height() - self.__borderWidth * 2)

        # 如果背景图片存在则显示背景图片,否则显示背景色
        if not self.__bgImage.isNull():
            # 等比例缩放绘制
            img: QPixmap = self.__bgImage.scaled(rect.width(), rect.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap((self.rect().width() - img.width()) / 2, (self.rect().height() - img.height()) / 2, img)
        else:
            if self.__colorMode == ColorButton.ColorMode.ColorMode_Normal:
                if self.__isPressed:
                    painter.setBrush(QBrush(self.__pressedColor))
                else:
                    painter.setBrush(QBrush(self.__normalColor))
            elif self.__colorMode == ColorButton.ColorMode.ColorMode_Replace:
                gradient: QLinearGradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))

                if self.__isPressed:
                    gradient.setColorAt(0.0, self.__pressedColor)
                    gradient.setColorAt(0.49, self.__pressedColor)
                    gradient.setColorAt(0.50, self.__normalColor)
                    gradient.setColorAt(1.0, self.__normalColor)
                else:
                    gradient.setColorAt(0.0, self.__normalColor)
                    gradient.setColorAt(0.49, self.__normalColor)
                    gradient.setColorAt(0.50, self.__pressedColor)
                    gradient.setColorAt(1.0, self.__pressedColor)

                painter.setBrush(gradient)
            elif self.__colorMode == ColorButton.ColorMode.ColorMode_Shade:
                gradient: QLinearGradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))

                if self.__isPressed:
                    gradient.setColorAt(0.0, self.__pressedColor)
                    gradient.setColorAt(1.0, self.__normalColor)
                else:
                    gradient.setColorAt(0.0, self.__normalColor)
                    gradient.setColorAt(1.0, self.__pressedColor)

                painter.setBrush(gradient)

            painter.drawRoundedRect(rect, self.__borderRadius, self.__borderRadius)

        painter.restore()

    def drawText(self, painter: QPainter) -> None:
        if not self.__bgImage.isNull(): return

        painter.save()

        # 如果要显示角标,则重新计算显示文字的区域
        if self.__showSuperText:
            offset: int = 3
            rect: QRect = QRect()
            rect.setX(self.__borderWidth * offset)
            rect.setY(self.__borderWidth)
            rect.setWidth(self.width() - self.__borderWidth * offset * 2)
            rect.setHeight(self.height() - self.__borderWidth * 2)

            alignment: Qt.Alignment = Qt.AlignCenter
            if self.__superTextAlign == ColorButton.TextAlign.TextAlign_Top_Left:
                alignment = Qt.AlignTop | Qt.AlignLeft
            elif self.__superTextAlign == ColorButton.TextAlign.TextAlign_Top_Center:
                alignment = Qt.AlignTop | Qt.AlignHCenter
            elif self.__superTextAlign == ColorButton.TextAlign.TextAlign_Top_Right:
                alignment = Qt.AlignTop | Qt.AlignRight
            elif self.__superTextAlign == ColorButton.TextAlign.TextAlign_Center_Left:
                alignment = Qt.AlignLeft | Qt.AlignVCenter
            elif self.__superTextAlign == ColorButton.TextAlign.TextAlign_Center_Center:
                alignment = Qt.AlignHCenter | Qt.AlignVCenter
            elif self.__superTextAlign == ColorButton.TextAlign.TextAlign_Center_Right:
                alignment = Qt.AlignRight | Qt.AlignVCenter
            elif self.__superTextAlign == ColorButton.TextAlign.TextAlign_Bottom_Left:
                alignment = Qt.AlignBottom | Qt.AlignLeft
            elif self.__superTextAlign == ColorButton.TextAlign.TextAlign_Bottom_Center:
                alignment = Qt.AlignBottom | Qt.AlignHCenter
            elif self.__superTextAlign == ColorButton.TextAlign.TextAlign_Bottom_Right:
                alignment = Qt.AlignBottom | Qt.AlignRight

            # 绘制角标
            painter.setPen(self.__superTextColor)
            painter.setFont(self.__superTextFont)
            painter.drawText(rect, alignment, self.__superText)

        offset: int = 5
        rect: QRect = QRect()
        rect.setX(self.__borderWidth * offset)
        rect.setY(self.__borderWidth)
        rect.setWidth(self.width() - self.__borderWidth * offset * 2)
        rect.setHeight(self.height() - self.__borderWidth * 2)

        alignment: Qt.Alignment = Qt.AlignCenter
        if self.__textAlign == ColorButton.TextAlign.TextAlign_Top_Left:
            alignment = Qt.AlignTop | Qt.AlignLeft
        elif self.__textAlign == ColorButton.TextAlign.TextAlign_Top_Center:
            alignment = Qt.AlignTop | Qt.AlignHCenter
        elif self.__textAlign == ColorButton.TextAlign.TextAlign_Top_Right:
            alignment = Qt.AlignTop | Qt.AlignRight
        elif self.__textAlign == ColorButton.TextAlign.TextAlign_Center_Left:
            alignment = Qt.AlignLeft | Qt.AlignVCenter
        elif self.__textAlign == ColorButton.TextAlign.TextAlign_Center_Center:
            alignment = Qt.AlignHCenter | Qt.AlignVCenter
        elif self.__textAlign == ColorButton.TextAlign.TextAlign_Center_Right:
            alignment = Qt.AlignRight | Qt.AlignVCenter
        elif self.__textAlign == ColorButton.TextAlign.TextAlign_Bottom_Left:
            alignment = Qt.AlignBottom | Qt.AlignLeft
        elif self.__textAlign == ColorButton.TextAlign.TextAlign_Bottom_Center:
            alignment = Qt.AlignBottom | Qt.AlignHCenter
        elif self.__textAlign == ColorButton.TextAlign.TextAlign_Bottom_Right:
            alignment = Qt.AlignBottom | Qt.AlignRight

        painter.setPen(self.__textColor)
        painter.setFont(self.__textFont)
        painter.drawText(rect, alignment, self.__text)

        painter.restore()

    @property
    def borderRadius(self) -> int: return self.__borderRadius

    @borderRadius.setter
    def borderRadius(self, border_radius: int) -> None:
        if self.__borderRadius == border_radius: return
        self.__borderRadius = border_radius
        self.update()

    @property
    def borderWidth(self) -> int: return self.__borderWidth

    @borderWidth.setter
    def borderWidth(self, border_width: int) -> None:
        if self.__borderWidth == border_width: return
        self.__borderWidth = border_width
        self.update()

    @property
    def borderColor(self) -> QColor: return self.__borderColor

    @borderColor.setter
    def borderColor(self, border_color: QColor) -> None:
        if self.__borderColor == border_color: return
        self.__borderColor = border_color
        self.update()

    @property
    def showSuperText(self) -> bool: return self.__showSuperText

    @showSuperText.setter
    def showSuperText(self, show_super_text: bool) -> None:
        if self.__showSuperText == show_super_text: return
        self.__showSuperText = show_super_text
        self.update()

    @property
    def superText(self) -> str: return self.__superText

    @superText.setter
    def superText(self, super_text: str) -> None:
        if self.__superText == super_text: return
        self.__superText = super_text
        self.update()

    @property
    def superTextFont(self) -> QFont: return self.__superTextFont

    @superTextFont.setter
    def superTextFont(self, super_text_font: QFont) -> None:
        if self.__superTextFont == super_text_font: return
        self.__superTextFont = super_text_font
        self.update()

    @property
    def superTextAlign(self) -> TextAlign: return self.__superTextAlign

    @superTextAlign.setter
    def superTextAlign(self, super_text_align: TextAlign) -> None:
        if self.__superTextAlign == super_text_align: return
        self.__superTextAlign = super_text_align
        self.update()

    @property
    def superTextColor(self) -> QColor: return self.__superTextColor

    @superTextColor.setter
    def superTextColor(self, super_text_color: QColor) -> None:
        if self.__superTextColor == super_text_color: return
        self.__superTextColor = super_text_color
        self.update()

    @property
    def text(self) -> str: return self.__text

    @text.setter
    def text(self, n_text: str) -> None:
        if self.__text == n_text: return
        self.__text = n_text
        self.update()

    @property
    def textFont(self) -> QFont: return self.__textFont

    @textFont.setter
    def textFont(self, text_font: QFont) -> None:
        if self.__textFont == text_font: return
        self.__textFont = text_font
        self.update()

    @property
    def textAlign(self) -> TextAlign: return self.__textAlign

    @textAlign.setter
    def textAlign(self, text_align: TextAlign) -> None:
        if self.__textAlign == text_align: return
        self.__textAlign = text_align
        self.update()

    @property
    def textColor(self) -> QColor: return self.__textColor

    @textColor.setter
    def textColor(self, text_color: QColor) -> None:
        if self.__textColor == text_color: return
        self.__textColor = text_color
        self.update()

    @property
    def normalColor(self) -> QColor: return self.__normalColor

    @normalColor.setter
    def normalColor(self, normal_color: QColor) -> None:
        if self.__normalColor == normal_color: return
        self.__normalColor = normal_color
        self.update()

    @property
    def pressedColor(self) -> QColor: return self.__pressedColor

    @pressedColor.setter
    def pressedColor(self, pressed_color: QColor) -> None:
        if self.__pressedColor == pressed_color: return
        self.__pressedColor = pressed_color
        self.update()

    @property
    def canMove(self) -> bool: return self.__canMove

    @canMove.setter
    def canMove(self, can_move: bool) -> None:
        if self.__canMove == can_move: return
        self.__canMove = can_move
        self.update()

    @property
    def bgImage(self) -> QPixmap: return self.__bgImage

    @bgImage.setter
    def bgImage(self, bg_image: QPixmap) -> None:
        if self.__bgImage == bg_image: return
        self.__bgImage = bg_image
        self.update()

    @property
    def colorMode(self) -> ColorMode: return self.__colorMode

    @colorMode.setter
    def colorMode(self, color_mode: ColorMode) -> None:
        if self.__colorMode == color_mode: return
        self.__colorMode = color_mode
        self.update()

    @property
    def isPressed(self) -> bool: return self.__isPressed

    @isPressed.setter
    def isPressed(self, is_pressed: bool) -> None:
        if self.__isPressed == is_pressed: return
        self.__isPressed = is_pressed

    def sizeHint(self) -> QSize: return QSize(100, 50)

    def minimumSizeHint(self) -> QSize: return QSize(30, 20)


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec
    from PySide2.QtGui import QFontDatabase
    from PySide2.QtWidgets import QApplication, QGridLayout
    from custom_widgets.iconhelper.resource import *

    class FrmColorButton(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmColorButton, self).__init__(parent)
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

            layout = QGridLayout()

            self.colorButton1 = ColorButton()
            self.colorButton2 = ColorButton()
            self.colorButton3 = ColorButton()
            self.colorButton4 = ColorButton()
            self.colorButton5 = ColorButton()
            layout.addWidget(self.colorButton1, 0, 0)
            layout.addWidget(self.colorButton2, 0, 1)
            layout.addWidget(self.colorButton3, 0, 2)
            layout.addWidget(self.colorButton4, 0, 3)
            layout.addWidget(self.colorButton5, 0, 4)

            self.colorButton6 = ColorButton()
            self.colorButton7 = ColorButton()
            self.colorButton8 = ColorButton()
            self.colorButton9 = ColorButton()
            self.colorButton10 = ColorButton()
            layout.addWidget(self.colorButton6, 1, 0)
            layout.addWidget(self.colorButton7, 1, 1)
            layout.addWidget(self.colorButton8, 1, 2)
            layout.addWidget(self.colorButton9, 1, 3)
            layout.addWidget(self.colorButton10, 1, 4)

            self.colorButton11 = ColorButton()
            self.colorButton12 = ColorButton()
            self.colorButton13 = ColorButton()
            self.colorButton14 = ColorButton()
            self.colorButton15 = ColorButton()
            layout.addWidget(self.colorButton11, 2, 0)
            layout.addWidget(self.colorButton12, 2, 1)
            layout.addWidget(self.colorButton13, 2, 2)
            layout.addWidget(self.colorButton14, 2, 3)
            layout.addWidget(self.colorButton15, 2, 4)

            self.colorButton16 = ColorButton()
            self.colorButton17 = ColorButton()
            self.colorButton18 = ColorButton()
            self.colorButton19 = ColorButton()
            self.colorButton20 = ColorButton()
            layout.addWidget(self.colorButton16, 3, 0)
            layout.addWidget(self.colorButton17, 3, 1)
            layout.addWidget(self.colorButton18, 3, 2)
            layout.addWidget(self.colorButton19, 3, 3)
            layout.addWidget(self.colorButton20, 3, 4)

            self.colorButton21 = ColorButton()
            self.colorButton22 = ColorButton()
            self.colorButton23 = ColorButton()
            self.colorButton24 = ColorButton()
            self.colorButton25 = ColorButton()
            layout.addWidget(self.colorButton21, 4, 0)
            layout.addWidget(self.colorButton22, 4, 1)
            layout.addWidget(self.colorButton23, 4, 2)
            layout.addWidget(self.colorButton24, 4, 3)
            layout.addWidget(self.colorButton25, 4, 4)

            self.setLayout(layout)
            self.initForm()

        def initForm(self):
            self.colorButton1.textAlign = ColorButton.TextAlign.TextAlign_Center_Center
            self.colorButton1.text = "Groups\nWorkspace"
            self.colorButton1.normalColor = QColor("#C62F2F")
            self.colorButton1.borderColor = QColor(255, 107, 107)

            self.colorButton2.text = "Groups\nWorkspace"
            self.colorButton2.colorMode = ColorButton.ColorMode.ColorMode_Replace
            self.colorButton2.borderColor = QColor(180, 180, 180)

            self.colorButton3.text = "Workspace"
            self.colorButton3.colorMode = ColorButton.ColorMode.ColorMode_Shade
            self.colorButton3.borderColor = QColor(180, 180, 180)
            self.colorButton3.normalColor = QColor("#2BB669")
            self.colorButton3.pressedColor = QColor("#159C77")
            self.colorButton3.borderColor = QColor("#1D9E74")

            self.colorButton4.text = "Workspace"
            self.colorButton4.colorMode = ColorButton.ColorMode.ColorMode_Shade
            self.colorButton4.borderColor = QColor(100, 100, 100)
            self.colorButton4.borderWidth = 2
            self.colorButton4.borderRadius = 5

            self.colorButton5.text = "Position"
            self.colorButton5.colorMode = ColorButton.ColorMode.ColorMode_Replace
            self.colorButton5.borderColor = QColor(200, 200, 200)
            self.colorButton5.normalColor = QColor("#2BB669")
            self.colorButton5.pressedColor = QColor("#159C77")
            self.colorButton5.borderColor = QColor("#1D9E74")
            self.colorButton5.showSuperText = True
            self.colorButton5.superText = "5"

            self.colorButton6.text = "Palete\n10"
            self.colorButton7.text = "Group\n17"
            self.colorButton8.text = "201"
            self.colorButton8.textAlign = ColorButton.TextAlign.TextAlign_Top_Center
            self.colorButton9.text = "202"
            self.colorButton9.textAlign= ColorButton.TextAlign.TextAlign_Bottom_Center
            self.colorButton10.text = "1/500"

            textFont: QFont = QFont()
            textFont.setPixelSize(25)
            textFont.setBold(True)
            self.colorButton10.textFont = textFont
            self.colorButton10.textAlign = ColorButton.TextAlign.TextAlign_Center_Center

            self.__iconFont.setPixelSize(45)

            self.colorButton11.textFont = self.__iconFont
            self.colorButton11.text = chr(0xf100)
            self.colorButton11.textColor = QColor("#F4B634")

            self.colorButton12.textFont = self.__iconFont
            self.colorButton12.text = chr(0xf101)
            self.colorButton12.textColor = QColor("#F4B634")

            self.colorButton13.textFont = self.__iconFont
            self.colorButton13.text = chr(0xf102)
            self.colorButton13.textColor = QColor("#F4B634")

            self.colorButton14.textFont = self.__iconFont
            self.colorButton14.text = chr(0xf103)
            self.colorButton14.textColor = QColor("#F4B634")

            self.colorButton15.textFont = self.__iconFont
            self.colorButton15.text = chr(0xf085)
            self.colorButton15.textColor = QColor("#F4B634")

            font1: QFont = QFont()
            font1.setPointSize(8)
            font2: QFont = QFont()
            font2.setPointSize(11)
            font2.setBold(True)

            self.colorButton16.superTextAlign = ColorButton.TextAlign.TextAlign_Top_Left
            self.colorButton16.showSuperText = True
            self.colorButton16.superTextFont = font1
            self.colorButton16.superText = "1"
            self.colorButton16.textFont = font2
            self.colorButton16.text = "演出秀1"

            self.colorButton17.superTextAlign = ColorButton.TextAlign.TextAlign_Top_Center
            self.colorButton17.showSuperText = True
            self.colorButton17.superTextFont = font1
            self.colorButton17.superText = "2"
            self.colorButton17.textFont = font2
            self.colorButton17.text = "演出秀2"

            self.colorButton18.superTextAlign = ColorButton.TextAlign.TextAlign_Top_Right
            self.colorButton18.showSuperText = True
            self.colorButton18.superTextFont = font1
            self.colorButton18.superText = "3"
            self.colorButton18.textFont = font2
            self.colorButton18.text = "演出秀3"

            self.colorButton19.superTextAlign = ColorButton.TextAlign.TextAlign_Bottom_Left
            self.colorButton19.showSuperText = True
            self.colorButton19.superTextFont = font1
            self.colorButton19.superText = "4"
            self.colorButton19.textFont = font2
            self.colorButton19.text = "演出秀4"

            self.colorButton20.superTextAlign = ColorButton.TextAlign.TextAlign_Bottom_Right
            self.colorButton20.showSuperText = True
            self.colorButton20.superTextFont = font1
            self.colorButton20.superText = "5"
            self.colorButton20.textFont = font2
            self.colorButton20.text = "演出秀5"

            self.colorButton21.normalColor = QColor("#16A085")
            self.colorButton21.borderColor = self.colorButton21.normalColor.light(90)
            self.colorButton22.normalColor = QColor("#2980B9")
            self.colorButton22.borderColor = self.colorButton22.normalColor.light(90)
            self.colorButton23.normalColor = QColor("#8E44AD")
            self.colorButton23.borderColor = self.colorButton23.normalColor.light(90)
            self.colorButton24.normalColor = QColor("#2C3E50")
            self.colorButton24.borderColor = self.colorButton24.normalColor.light(90)
            self.colorButton25.normalColor = QColor("#D35400")
            self.colorButton25.borderColor = self.colorButton25.normalColor.light(90)

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmColorButton()
    window.setWindowTitle("多样式超级按钮")
    window.show()
    sys.exit(app.exec_())
