from typing import List

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QResizeEvent, QMouseEvent, QPaintEvent, QPainter, QColor, QFont, QFontDatabase
from PySide2.QtCore import QEvent, QRect, QSize, Signal, QPoint, Qt

from custom_widgets.iconhelper.resource import *

class NavTitle(QWidget):
    """
    导航标题栏控件
    作者:feiyangqingyun(QQ:517216493) 2019-3-28
    译者:sunchuquin(QQ:1715216365) 2020-12-23
    1. 可设置标题文字
    2. 可设置左侧图标和右侧五个图标
    3. 可设置图标的正常颜色+悬停颜色+按下颜色
    4. 可识别各图标按下信号+松开信号,用索引标识
    5. 可以自行拓展图标大小
    6. 可设置标题是否居中
    """

    mousePressed: Signal = Signal(int)

    mouseReleased: Signal = Signal(int)

    def __init__(self):
        super().__init__()

        self.__leftIcon: int = 0xf0e8  # 左侧图标
        self.__rightIcon1: int = 0  # 右侧图标1
        self.__rightIcon2: int = 0  # 右侧图标2
        self.__rightIcon3: int = 0  # 右侧图标3
        self.__rightIcon4: int = 0  # 右侧图标4
        self.__rightIcon5: int = 0xf00d  # 右侧图标5

        self.__padding: int = 8  # 左侧右侧间距
        self.__iconSize: int = 20  # 图标大小
        self.__textCenter: bool = False  # 文字居中
        self.__text: str = ""  # 标题文字

        self.__bgColor: QColor = QColor("#40444D")  # 背景颜色
        self.__textColor: QColor = QColor("#FAF6F7")  # 文本颜色
        self.__borderColor: QColor = QColor("#32363F")  # 边框颜色

        self.__iconNormalColor: QColor = QColor("#FAF6F7")  # 图标正常颜色
        self.__iconHoverColor: QColor = QColor("#22A3A9")  # 图标悬停颜色
        self.__iconPressColor: QColor = QColor("#0E99A0")  # 图标按下颜色

        self.__pressed: bool = False  # 鼠标是否按下
        self.__lastPoint: QPoint = QPoint(0, 0)   # 鼠标按下处的鼠标
        self.__leftIconState: bool = True  # 左侧图标是否根据鼠标信号变色

        self.__iconFont: QFont = QFont()  # 图形字体
        self.__leftRect: QRect = QRect()  # 左侧图标区域
        self.__rightRect1: QRect = QRect()  # 右侧图标1区域
        self.__rightRect2: QRect = QRect()  # 右侧图标2区域
        self.__rightRect3: QRect = QRect()  # 右侧图标3区域
        self.__rightRect4: QRect = QRect()  # 右侧图标4区域
        self.__rightRect5: QRect = QRect()  # 右侧图标5区域

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

        self.setMouseTracking(True)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """ 当窗口小部件调整大小时，将事件发送到该小部件 """
        self.__leftRect: QRect = QRect(self.__padding, 0, self.__iconSize, self.height())
        self.__rightRect1: QRect = QRect(self.width() - (self.__iconSize * 5) - self.__padding, 0, self.__iconSize,
                                         self.height())
        self.__rightRect2: QRect = QRect(self.width() - (self.__iconSize * 4) - self.__padding, 0, self.__iconSize,
                                         self.height())
        self.__rightRect3: QRect = QRect(self.width() - (self.__iconSize * 3) - self.__padding, 0, self.__iconSize,
                                         self.height())
        self.__rightRect4: QRect = QRect(self.width() - (self.__iconSize * 2) - self.__padding, 0, self.__iconSize,
                                         self.height())
        self.__rightRect5: QRect = QRect(self.width() - (self.__iconSize * 1) - self.__padding, 0, self.__iconSize,
                                         self.height())

    def leaveEvent(self, event: QEvent) -> None:
        """ 当鼠标光标离开小部件时，将事件发送到该小部件 """
        self.__pressed = False
        self.__lastPoint = QPoint(-1, -1)
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """ 接收小部件的鼠标按下事件 """
        self.__pressed = True
        self.__lastPoint = event.pos()
        self.update()

        if self.__leftRect.contains(self.__lastPoint):
            self.mousePressed.emit(1)
        elif self.__rightRect1.contains(self.__lastPoint):
            self.mousePressed.emit(2)
        elif self.__rightRect2.contains(self.__lastPoint):
            self.mousePressed.emit(3)
        elif self.__rightRect3.contains(self.__lastPoint):
            self.mousePressed.emit(4)
        elif self.__rightRect4.contains(self.__lastPoint):
            self.mousePressed.emit(5)
        elif self.__rightRect5.contains(self.__lastPoint):
            self.mousePressed.emit(6)
        else:
            self.mousePressed.emit(0)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """ 接收该小部件的鼠标移动事件 """
        self.__lastPoint = event.pos()
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """ 接收该小部件的鼠标释放事件 """
        self.__pressed = False
        self.update()

        if self.__leftRect.contains(self.__lastPoint):
            self.mouseReleased.emit(1)
        elif self.__rightRect1.contains(self.__lastPoint):
            self.mouseReleased.emit(2)
        elif self.__rightRect2.contains(self.__lastPoint):
            self.mouseReleased.emit(3)
        elif self.__rightRect3.contains(self.__lastPoint):
            self.mouseReleased.emit(4)
        elif self.__rightRect4.contains(self.__lastPoint):
            self.mouseReleased.emit(5)
        elif self.__rightRect5.contains(self.__lastPoint):
            self.mouseReleased.emit(6)
        else:
            self.mouseReleased.emit(0)

    def paintEvent(self, event: QPaintEvent) -> None:
        """ 接收绘画事件 """
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景 + 边框
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__bgColor)
        painter.drawRect(self.rect())

        font: QFont = QFont()
        font.setPixelSize(15)
        painter.setFont(font)

        # 绘制文字
        if len(self.__text):
            painter.setPen(self.__textColor)
            textRect: QRect = QRect(int(self.__iconSize + self.__padding * 1.5), 0, self.width(), self.height())
            if self.__textCenter:
                painter.drawText(self.rect(), Qt.AlignHCenter | Qt.AlignVCenter, self.__text)
            else:
                painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, self.__text)

        font = self.__iconFont
        font.setPixelSize(self.__iconSize - 5)
        painter.setFont(font)

        # 绘制左侧图标
        if self.__leftIcon != 0:
            if self.__leftIconState:
                self.drawIcon(painter, self.__leftRect, self.__leftIcon)
            else:
                painter.drawText(self.__leftRect, Qt.AlignHCenter | Qt.AlignVCenter, chr(int(self.__leftIcon)))

        # 绘制右侧图标1
        self.drawIcon(painter, self.__rightRect1, self.__rightIcon1)
        # 绘制右侧图标2
        self.drawIcon(painter, self.__rightRect2, self.__rightIcon2)
        # 绘制右侧图标3
        self.drawIcon(painter, self.__rightRect3, self.__rightIcon3)
        # 绘制右侧图标4
        self.drawIcon(painter, self.__rightRect4, self.__rightIcon4)
        # 绘制右侧图标5
        self.drawIcon(painter, self.__rightRect5, self.__rightIcon5)

    def drawIcon(self, painter: QPainter, rect: QRect, icon: int) -> None:
        """  """
        if icon != 0:
            if rect.contains(self.__lastPoint):
                painter.setPen(self.__iconPressColor if self.__pressed else self.__iconHoverColor)
            else:
                painter.setPen(self.__iconNormalColor)

            painter.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, chr(int(icon)))

    def getLeftIcon(self) -> int:
        """ 读取左侧图标 """
        return self.__leftIcon

    def getRightIcon1(self) -> int:
        """ 读取右侧图标1 """
        return self.__rightIcon1

    def getRightIcon2(self) -> int:
        """ 读取右侧图标2 """
        return self.__rightIcon2

    def getRightIcon3(self) -> int:
        """ 读取右侧图标3 """
        return self.__rightIcon3

    def getRightIcon4(self) -> int:
        """ 读取右侧图标4 """
        return self.__rightIcon4

    def getRightIcon5(self) -> int:
        """ 读取右侧图标5 """
        return self.__rightIcon5

    def getPadding(self) -> int:
        """ 读取左侧右侧间距 """
        return self.__padding

    def getIconSize(self) -> int:
        """ 读取图标大小 """
        return self.__iconSize

    def getTextCenter(self) -> bool:
        """ 读取文字居中 """
        return self.__textCenter

    def getText(self) -> str:
        """ 读取标题文字 """
        return self.__text

    def getBgColor(self) -> QColor:
        """ 读取背景颜色 """
        return self.__bgColor

    def getTextColor(self) -> QColor:
        """ 读取文本颜色 """
        return self.textColor

    def getBorderColor(self) -> QColor:
        """ 读取边框颜色 """
        return self.__borderColor

    def getIconNormalColor(self) -> QColor:
        """ 读取图标正常颜色 """
        return self.__iconNormalColor

    def getIconHoverColor(self) -> QColor:
        """ 读取图标悬停颜色 """
        return self.__iconHoverColor

    def getIconPressColor(self) -> QColor:
        """ 读取图标按下颜色 """
        return self.__iconPressColor

    def getLeftIconState(self) -> bool:
        """ 左侧图标是否根据鼠标信号变色 """
        return self.__leftIconState

    def sizeHint(self) -> QSize:
        """  """
        return QSize(100, 25)

    def minimumSizeHint(self) -> QSize:
        """  """
        return QSize(50, 15)

    def setLeftIcon(self, left_icon: int) -> None:
        """ 设置左侧图标 """
        if self.__leftIcon != left_icon:
            self.__leftIcon = left_icon
            self.update()

    def setRightIcon1(self, right_icon: int) -> None:
        """ 设置右侧图标1 """
        if self.__rightIcon1 != right_icon:
            self.__rightIcon1 = right_icon
            self.update()

    def setRightIcon2(self, right_icon: int) -> None:
        """ 设置右侧图标2 """
        if self.__rightIcon2 != right_icon:
            self.__rightIcon2 = right_icon
            self.update()

    def setRightIcon3(self, right_icon: int) -> None:
        """ 设置右侧图标3 """
        if self.__rightIcon3 != right_icon:
            self.__rightIcon3 = right_icon
            self.update()

    def setRightIcon4(self, right_icon: int) -> None:
        """ 设置右侧图标4 """
        if self.__rightIcon4 != right_icon:
            self.__rightIcon4 = right_icon
            self.update()

    def setRightIcon5(self, right_icon: int) -> None:
        """ 设置右侧图标5 """
        if self.__rightIcon5 != right_icon:
            self.__rightIcon5 = right_icon
            self.update()

    def setPadding(self, padding: int) -> None:
        """ 设置左侧右侧间距 """
        if self.__padding != padding:
            self.__padding = padding
            self.update()

    def setIconSize(self, icon_size: int) -> None:
        """ 设置图标大小 """
        if self.__iconSize != icon_size:
            self.__iconSize = icon_size
            self.update()

    def setTextCenter(self, text_center: bool) -> None:
        """ 设置文字居中 """
        if self.__textCenter != text_center:
            self.__textCenter = text_center
            self.update()

    def setText(self, text: str) -> None:
        """ 设置标题文字 """
        if self.__text != text:
            self.__text = text
            self.update()

    def setBgColor(self, bg_color: QColor) -> None:
        """ 设置背景颜色 """
        if self.__bgColor != bg_color:
            self.__bgColor = bg_color
            self.update()

    def setTextColor(self, text_color: QColor) -> None:
        """ 设置文本颜色 """
        if self.__textColor != text_color:
            self.__textColor = text_color
            self.update()

    def setBorderColor(self, border_color: QColor) -> None:
        """ 设置边框颜色 """
        if self.__borderColor != border_color:
            self.__borderColor = border_color
            self.update()

    def setIconNormalColor(self, icon_normal_color: QColor) -> None:
        """ 设置图标正常颜色 """
        if self.__iconNormalColor != icon_normal_color:
            self.__iconNormalColor = icon_normal_color
            self.update()

    def setIconHoverColor(self, icon_hover_color: QColor) -> None:
        """ 设置图标悬停颜色 """
        if self.__iconHoverColor != icon_hover_color:
            self.__iconHoverColor = icon_hover_color
            self.update()

    def setIconPressColor(self, icon_press_color) -> None:
        """ 设置图标按下颜色 """
        if self.__iconPressColor != icon_press_color:
            self.__iconPressColor = icon_press_color
            self.update()

    def setLeftIconState(self, state) -> None:
        """ 左侧图标是否根据鼠标信号变色 """
        if self.__leftIconState != state:
            self.__leftIconState = state
            self.update()

    leftIcon: int = property(fget=getLeftIcon, fset=setLeftIcon, fdel=None, doc="左侧图标")
    rightIcon1: int = property(fget=getRightIcon1, fset=setRightIcon1, fdel=None, doc="右侧图标1")
    rightIcon2: int = property(fget=getRightIcon2, fset=setRightIcon2, fdel=None, doc="右侧图标2")
    rightIcon3: int = property(fget=getRightIcon3, fset=setRightIcon3, fdel=None, doc="右侧图标3")
    rightIcon4: int = property(fget=getRightIcon4, fset=setRightIcon4, fdel=None, doc="右侧图标4")
    rightIcon5: int = property(fget=getRightIcon5, fset=setRightIcon5, fdel=None, doc="右侧图标5")

    padding: int = property(fget=getPadding, fset=setPadding, fdel=None, doc="左侧右侧间距")
    iconSize: int = property(fget=getIconSize, fset=setIconSize, fdel=None, doc="图标大小")
    textCenter: bool = property(fget=getTextCenter, fset=setTextCenter, fdel=None, doc="文字居中")
    text: str = property(fget=getText, fset=setText, fdel=None, doc="标题文字")

    bgColor: QColor = property(fget=getBgColor, fset=setBgColor, fdel=None, doc="背景颜色")
    textColor: QColor = property(fget=getTextColor, fset=setTextColor, fdel=None, doc="文本颜色")
    borderColor: QColor = property(fget=getBorderColor, fset=setBorderColor, fdel=None, doc="边框颜色")

    iconNormalColor: QColor = property(fget=getIconNormalColor, fset=setIconNormalColor, fdel=None, doc="图标正常颜色")
    iconHoverColor: QColor = property(fget=getIconHoverColor, fset=setIconHoverColor, fdel=None, doc="图标悬停颜色")
    iconPressColor: QColor = property(fget=getIconPressColor, fset=setIconPressColor, fdel=None, doc="图标按下颜色")

    leftIconState: bool = property(fget=getLeftIconState, fset=setLeftIconState, fdel=None, doc="左侧图标是否根据鼠标信号变色")


if __name__ == '__main__':
    def mousePressed(value: int) -> None:
        print('mousePressed: ', value)

    def mouseReleased(value: int) -> None:
        print('mouseReleased: ', value)

    import sys
    from PySide2.QtWidgets import QGridLayout

    app: QApplication = QApplication(sys.argv)
    a = QWidget()
    b = QGridLayout()

    window: NavTitle = NavTitle()
    window.setMinimumSize(237, 30)
    window.setLeftIconState(True)
    # window.setLeftIconState(False)
    window.setText("设备列表")
    window.setRightIcon1(0xf067)
    window.setRightIcon2(0xf068)
    window.setRightIcon3(0xf0C7)
    window.setRightIcon4(0xf013)
    window.mousePressed.connect(mousePressed)
    window.mouseReleased.connect(mouseReleased)

    b.addWidget(window)
    a.setLayout(b)
    a.show()

    sys.exit(app.exec_())
