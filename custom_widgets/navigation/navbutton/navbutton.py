
from enum import Enum
from PySide2.QtGui import QPainter, QColor, QPixmap, QPen, QPolygon, QBrush
from PySide2.QtCore import QEnum, QSize, Qt, QRect, QPoint, QEvent
from PySide2.QtWidgets import QApplication, QPushButton


class NavButton(QPushButton):
    """
    导航按钮控件
    作者:feiyangqingyun(QQ:517216493) 2017-12-19
    译者:sunchuquin(QQ:1715216365) 2020-12-17
    1. 可设置文字的左侧+右侧+顶部+底部间隔
    2. 可设置文字对齐方式
    3. 可设置显示倒三角/倒三角边长/倒三角位置/倒三角颜色
    4. 可设置显示图标/图标间隔/图标尺寸/正常状态图标/悬停状态图标/选中状态图标
    5. 可设置显示边框线条/线条宽度/线条间隔/线条位置/线条颜色
    6. 可设置正常背景颜色/悬停背景颜色/选中背景颜色
    7. 可设置正常文字颜色/悬停文字颜色/选中文字颜色
    8. 可设置背景颜色为画刷颜色
    """

    # 文本对齐方式
    @QEnum
    class TextAlign(Enum):
        TEXTALIGN_LEFT = 0x0001  # 左侧对齐
        TEXTALIGN_RIGHT = 0x0002  # 右侧对齐
        TEXTALIGN_TOP = 0x0020  # 顶部对齐
        TEXTALIGN_BOTTOM = 0x0040  # 底部对齐
        TEXTALIGN_CENTER = 0x0004  # 居中对齐

    # 三角形的位置
    @QEnum
    class TrianglePosition(Enum):
        TRIANGLEPOSITION_LEFT = 0  # 左侧
        TRIANGLEPOSITION_RIGHT = 1  # 右侧
        TRIANGLEPOSITION_TOP = 2  # 顶部
        TRIANGLEPOSITION_BOTTOM = 3  # 底部

    # 线的位置
    @QEnum
    class LinePosition(Enum):
        LINEPOSITION_LEFT = 0  # 左侧
        LINEPOSITION_RIGHT = 1  # 右侧
        LINEPOSITION_TOP = 2  # 顶部
        LINEPOSITION_BOTTOM = 3  # 底部

    # 图标的位置
    @QEnum
    class IconPosition(Enum):
        ICONPOSITION_LEFT = 0  # 左侧
        ICONPOSITION_RIGHT = 1  # 右侧
        ICONPOSITION_TOP = 2  # 顶部
        ICONPOSITION_BOTTOM = 3  # 底部

    def __init__(self, parent=None):
        super(NavButton, self).__init__(parent=parent)

        self.__paddingLeft: int = 20  # 文字左侧间隔
        self.__paddingRight: int = 5  # 文字右侧间隔
        self.__paddingTop: int = 5  # 文字顶部间隔
        self.__paddingBottom: int = 5  # 文字底部间隔
        self.__textAlign: NavButton.TextAlign = NavButton.TextAlign.TEXTALIGN_LEFT  # 文字对齐

        self.__showTriangle: bool = False  # 显示倒三角
        self.__triangleLen: int = 5  # 倒三角边长
        self.__trianglePosition: NavButton.TrianglePosition = NavButton.TrianglePosition.TRIANGLEPOSITION_RIGHT  # 倒三角位置
        self.__triangleColor: QColor = QColor(255, 255, 255)  # 倒三角颜色

        self.__showIcon: bool = True  # 显示图标
        self.__iconSpace: int = 10  # 图标间隔
        self.__iconSize: QSize = QSize(16, 16)  # 图标尺寸
        self.__iconNormal: QPixmap = QPixmap(0, 0)  # 正常图标
        self.__iconHover: QPixmap = QPixmap(0, 0)  # 悬停图标
        self.__iconCheck: QPixmap = QPixmap(0, 0)  # 选中图标

        self.__showLine: bool = True  # 显示线条
        self.__lineSpace: int = 0  # 线条间隔
        self.__lineWidth: int = 5  # 线条宽度
        self.__linePosition: NavButton.LinePosition = NavButton.LinePosition.LINEPOSITION_LEFT  # 线条位置
        self.__lineColor: QColor = QColor(0, 187, 158)  # 线条颜色

        self.__normalBgColor: QColor = QColor(230, 230, 230)  # 正常背景颜色
        self.__hoverBgColor: QColor = QColor(130, 130, 130)  # 悬停背景颜色
        self.__checkBgColor: QColor = QColor(80, 80, 80)  # 选中背景颜色
        self.__normalTextColor: QColor = QColor(100, 100, 100)  # 正常文字颜色
        self.__hoverTextColor: QColor = QColor(255, 255, 255)  # 悬停文字颜色
        self.__checkTextColor: QColor = QColor(255, 255, 255)  # 选中文字颜色

        self.__normalBgBrush: QBrush = Qt.NoBrush  # 正常背景画刷
        self.__hoverBgBrush: QBrush = Qt.NoBrush  # 悬停背景画刷
        self.__checkBgBrush: QBrush = Qt.NoBrush  # 选中背景画刷

        self.__hover: bool = False  # 悬停标志位

        self.setCheckable(True)
        self.setText("导航按钮")

    def enterEvent(self, event: QEvent) -> None:
        """  """
        self.__hover = True
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        """  """
        self.__hover = False
        self.update()

    def paintEvent(self, event: QEvent) -> None:
        """  """
        # 绘制准备工作，启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景
        self.drawBg(painter)
        # 绘制文字
        self.drawText(painter)
        # 绘制图标
        self.drawIcon(painter)
        # 绘制边框线条
        self.drawLine(painter)
        # 绘制倒三角
        self.drawTriangle(painter)

    def drawBg(self, painter: QPainter) -> None:
        """  """
        painter.save()
        painter.setPen(Qt.NoPen)

        width: int = self.width()
        height: int = self.height()

        bgRect: QRect = QRect()
        if self.__linePosition == NavButton.LinePosition.LINEPOSITION_LEFT:
            bgRect = QRect(self.lineSpace, 0, width - self.__lineSpace, height)
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_RIGHT:
            bgRect = QRect(0, 0, width - self.__lineSpace, height)
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_TOP:
            bgRect = QRect(0, self.lineSpace, width, height - self.__lineSpace)
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_BOTTOM:
            bgRect = QRect(0, 0, width, height - self.__lineSpace)

        # 如果画刷存在则取画刷
        if self.isChecked():
            bgBrush: QBrush = self.__checkBgBrush
        elif self.__hover:
            bgBrush: QBrush = self.__hoverBgBrush
        else:
            bgBrush: QBrush = self.__normalBgBrush

        if bgBrush != Qt.NoBrush:
            painter.setBrush(bgBrush)
        else:
            # 根据当前状态选择对应颜色
            if self.isChecked():
                bgColor: QColor = self.__checkBgColor
            elif self.__hover:
                bgColor: QColor = self.__hoverBgColor
            else:
                bgColor: QColor = self.__normalBgColor

            painter.setBrush(bgColor)

        painter.drawRect(bgRect)

        painter.restore()

    def drawText(self, painter: QPainter) -> None:
        """  """
        painter.save()
        painter.setBrush(Qt.NoBrush)

        # 根据当前状态选择对应颜色
        if self.isChecked():
            textColor: QColor = self.__checkTextColor
        elif self.__hover:
            textColor: QColor = self.__hoverTextColor
        else:
            textColor: QColor = self.__normalTextColor

        textRect = QRect(self.__paddingLeft,
                         self.__paddingTop,
                         self.width() - self.__paddingLeft - self.__paddingRight,
                         self.height() - self.__paddingTop - self.__paddingBottom)
        painter.setPen(textColor)

        painter.drawText(textRect, self.__textAlign.value | Qt.AlignVCenter, self.text())

        painter.restore()

    def drawIcon(self, painter: QPainter) -> None:
        """  """
        if not self.__showIcon:
            return

        painter.save()

        if self.isChecked():
            pix: QPixmap = self.__iconCheck
        elif self.__hover:
            pix: QPixmap = self.__iconHover
        else:
            pix: QPixmap = self.__iconNormal

        if not pix.isNull():
            # 等比例平滑缩放图标
            pix: QPixmap = pix.scaled(self.__iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(self.__iconSpace, int((self.height() - self.__iconSize.height()) / 2), pix)

        painter.restore()

    def drawLine(self, painter: QPainter) -> None:
        """  """
        if not self.__showLine:
            return

        if not self.isChecked():
            return

        painter.save()

        pen: QPen = QPen()
        pen.setWidth(self.__lineWidth)
        pen.setColor(self.__lineColor)
        painter.setPen(pen)

        # 根据线条位置设置线条坐标
        pointStart: QPoint = QPoint()
        pointEnd: QPoint = QPoint()
        if self.__linePosition == NavButton.LinePosition.LINEPOSITION_LEFT:
            pointStart = QPoint(0, 0)
            pointEnd = QPoint(0, self.height())
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_RIGHT:
            pointStart = QPoint(self.width(), 0)
            pointEnd = QPoint(self.width(), self.height())
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_TOP:
            pointStart = QPoint(0, 0)
            pointEnd = QPoint(self.width(), 0)
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_BOTTOM:
            pointStart = QPoint(0, self.height())
            pointEnd = QPoint(self.width(), self.height())

        painter.drawLine(pointStart, pointEnd)

        painter.restore()

    def drawTriangle(self, painter: QPainter) -> None:
        """  """
        if not self.__showTriangle:
            return

        # 选中或者悬停显示
        if (not self.__hover) and (not self.isChecked()):
            return

        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__triangleColor)

        # 绘制在右侧中间，根据设定的倒三角的边长设定三个点位置
        width: int = self.width()
        height: int = self.height()
        midWidth: int = width // 2
        midHeight: int = height // 2

        pts: QPolygon = QPolygon()
        if self.__trianglePosition == NavButton.TrianglePosition.TRIANGLEPOSITION_LEFT:
            pts.setPoints(3,
                          self.__triangleLen, midHeight,
                          0, midHeight - self.__triangleLen,
                          0, midHeight + self.__triangleLen)
        elif self.__trianglePosition == NavButton.TrianglePosition.TRIANGLEPOSITION_RIGHT:
            pts.setPoints(3,
                          width - self.__triangleLen, midHeight,
                          width, midHeight - self.__triangleLen,
                          width, midHeight + self.__triangleLen)
        elif self.__trianglePosition == NavButton.TrianglePosition.TRIANGLEPOSITION_TOP:
            pts.setPoints(3,
                          midWidth, self.__triangleLen,
                          midWidth - self.__triangleLen, 0,
                          midWidth + self.__triangleLen, 0)
        elif self.__trianglePosition == NavButton.TrianglePosition.TRIANGLEPOSITION_BOTTOM:
            pts.setPoints(3,
                          midWidth, height - self.__triangleLen,
                          midWidth - self.__triangleLen, height,
                          midWidth + self.__triangleLen, height)

        painter.drawPolygon(pts)

        painter.restore()

    def getPaddingLeft(self) -> int:
        """ 读取文字左侧间隔 """
        return self.__paddingLeft

    def getPaddingRight(self) -> int:
        """ 读取文字右侧间隔 """
        return self.__paddingRight

    def getPaddingTop(self) -> int:
        """ 读取文字顶部间隔 """
        return self.__paddingTop

    def getPaddingBottom(self) -> int:
        """ 读取文字底部间隔 """
        return self.__paddingBottom

    def getTextAlign(self) -> TextAlign:
        """ 读取文字对齐方式 """
        return self.__textAlign

    def getShowTriangle(self) -> bool:
        """ 读取是否显示倒三角 """
        return self.__showTriangle

    def getTriangleLen(self) -> int:
        """ 读取倒三角边长 """
        return self.__triangleLen

    def getTrianglePosition(self) -> TrianglePosition:
        """ 读取倒三角位置 """
        return self.__trianglePosition

    def getTriangleColor(self) -> QColor:
        """ 读取倒三角颜色 """
        return self.__triangleColor

    def getShowIcon(self) -> bool:
        """ 读取是否显示图标 """
        return self.__showIcon

    def getIconSpace(self) -> int:
        """ 读取图标间隔 """
        return self.__iconSpace

    def getIconSize(self) -> QSize:
        """ 读取图标尺寸 """
        return self.__iconSize

    def getIconNormal(self) -> QPixmap:
        """ 读取正常图标 """
        return self.__iconNormal

    def getIconHover(self) -> QPixmap:
        """ 读取悬停图标 """
        return self.__iconHover

    def getIconCheck(self) -> QPixmap:
        """ 读取选中图标 """
        return self.__iconCheck

    def getShowLine(self) -> bool:
        """ 读取是否显示线条 """
        return self.__showLine

    def getLineSpace(self) -> int:
        """ 读取线条间隔 """
        return self.__lineSpace

    def getLineWidth(self) -> int:
        """ 读取线条宽度 """
        return self.__lineWidth

    def getLinePosition(self) -> LinePosition:
        """ 读取线条位置 """
        return self.__linePosition

    def getLineColor(self) -> QColor:
        """ 读取线条颜色 """
        return self.__lineColor

    def getNormalBgColor(self) -> QColor:
        """ 读取正常背景颜色 """
        return self.__normalBgColor

    def getHoverBgColor(self) -> QColor:
        """ 读取悬停背景颜色 """
        return self.__hoverBgColor

    def getCheckBgColor(self) -> QColor:
        """ 读取选中背景颜色 """
        return self.__checkBgColor

    def getNormalTextColor(self) -> QColor:
        """ 读取正常文字颜色 """
        return self.__normalTextColor

    def getHoverTextColor(self) -> QColor:
        """ 读取悬停文字颜色 """
        return self.__hoverTextColor

    def getCheckTextColor(self) -> QColor:
        """ 读取选中文字颜色 """
        return self.__checkTextColor

    def sizeHint(self) -> QSize:
        """  """
        return QSize(100, 30)

    def minimumSizeHint(self) -> QSize:
        """  """
        return QSize(20, 10)

    def setPaddingLeft(self, padding_left: int) -> None:
        """ 设置文字左侧间隔 """
        if self.__paddingLeft != padding_left:
            self.__paddingLeft = padding_left
            self.update()

    def setPaddingRight(self, padding_right: int) -> None:
        """ 设置文字右侧间隔 """
        if self.__paddingRight != padding_right:
            self.__paddingRight = padding_right
            self.update()

    def setPaddingTop(self, padding_top: int) -> None:
        """ 设置文字顶部间隔 """
        if self.__paddingTop != padding_top:
            self.__paddingTop = padding_top
            self.update()

    def setPaddingBottom(self, padding_bottom: int) -> None:
        """ 设置文字底部间隔 """
        if self.__paddingBottom != padding_bottom:
            self.__paddingBottom = padding_bottom
            self.update()

    def setPadding(self, padding_left: int, padding_right: int, padding_top: int, padding_bottom: int) -> None:
        """ 设置文字间隔 """
        self.__paddingLeft = padding_left
        self.__paddingRight = padding_right
        self.__paddingTop = padding_top
        self.__paddingBottom = padding_bottom
        self.update()

    def setTextAlign(self, text_align: TextAlign) -> None:
        """ 设置文字对齐 """
        if self.__textAlign != text_align:
            self.__textAlign = text_align
            self.update()

    def setShowTriangle(self, show_triangle: bool) -> None:
        """ 设置是否显示倒三角 """
        if self.__showTriangle != show_triangle:
            self.__showTriangle = show_triangle
            self.update()

    def setTriangleLen(self, triangle_len: int) -> None:
        """ 设置倒三角边长 """
        if self.__triangleLen != triangle_len:
            self.__triangleLen = triangle_len
            self.update()

    def setTrianglePosition(self, triangle_position: TrianglePosition) -> None:
        """ 设置倒三角位置 """
        if self.__trianglePosition != triangle_position:
            self.__trianglePosition = triangle_position
            self.update()

    def setTriangleColor(self, triangle_color: QColor) -> None:
        """ 设置倒三角颜色 """
        if self.__triangleColor != triangle_color:
            self.__triangleColor = triangle_color
            self.update()

    def setShowIcon(self, show_icon: bool) -> None:
        """ 设置是否显示图标 """
        if self.__showIcon != show_icon:
            self.__showIcon = show_icon
            self.update()

    def setIconSpace(self, icon_space: int) -> None:
        """ 设置图标间隔 """
        if self.__iconSpace != icon_space:
            self.__iconSpace = icon_space
            self.update()

    def setIconSize(self, icon_size: QSize) -> None:
        """ 设置图标尺寸 """
        if self.__iconSize != icon_size:
            self.__iconSize = icon_size
            self.update()

    def setIconNormal(self, icon_normal: QPixmap) -> None:
        """ 设置正常图标 """
        self.__iconNormal = icon_normal
        self.update()

    def setIconHover(self, icon_hover: QPixmap) -> None:
        """ 设置悬停图标 """
        self.__iconHover = icon_hover
        self.update()

    def setIconCheck(self, icon_check: QPixmap) -> None:
        """ 设置按下图标 """
        self.__iconCheck = icon_check
        self.update()

    def setShowLine(self, show_line: bool) -> None:
        """ 设置是否显示线条 """
        if self.__showLine != show_line:
            self.__showLine = show_line
            self.update()

    def setLineSpace(self, line_space: int) -> None:
        """ 设置线条间隔 """
        if self.__lineSpace != line_space:
            self.__lineSpace = line_space
            self.update()

    def setLineWidth(self, line_width: int) -> None:
        """ 设置线条宽度 """
        if self.__lineWidth != line_width:
            self.__lineWidth = line_width
            self.update()

    def setLinePosition(self, line_position: LinePosition) -> None:
        """ 设置线条位置 """
        if self.__linePosition != line_position:
            self.__linePosition = line_position
            self.update()

    def setLineColor(self, line_color: QColor) -> None:
        """ 设置线条颜色 """
        if self.__lineColor != line_color:
            self.__lineColor = line_color
            self.update()

    def setNormalBgColor(self, normal_bg_color: QColor) -> None:
        """ 设置正常背景颜色 """
        if self.__normalBgColor != normal_bg_color:
            self.__normalBgColor = normal_bg_color
            self.update()

    def setHoverBgColor(self, hover_bg_color: QColor) -> None:
        """ 设置悬停背景颜色 """
        if self.__hoverBgColor != hover_bg_color:
            self.__hoverBgColor = hover_bg_color
            self.update()

    def setCheckBgColor(self, check_bg_color: QColor) -> None:
        """ 设置选中背景颜色 """
        if self.__checkBgColor != check_bg_color:
            self.__checkBgColor = check_bg_color
            self.update()

    def setNormalTextColor(self, normal_text_color: QColor) -> None:
        """ 设置正常文字颜色 """
        if self.__normalTextColor != normal_text_color:
            self.__normalTextColor = normal_text_color
            self.update()

    def setHoverTextColor(self, hover_text_color: QColor) -> None:
        """ 设置悬停文字颜色 """
        if self.__hoverTextColor != hover_text_color:
            self.__hoverTextColor = hover_text_color
            self.update()

    def setCheckTextColor(self, check_text_color: QColor) -> None:
        """ 设置选中文字颜色 """
        if self.__checkTextColor != check_text_color:
            self.__checkTextColor = check_text_color
            self.update()

    def setNormalBgBrush(self, normal_bg_brush: QBrush) -> None:
        """ 设置正常背景画刷 """
        if self.__normalBgBrush != normal_bg_brush:
            self.__normalBgBrush = normal_bg_brush
            self.update()

    def setHoverBgBrush(self, hover_bg_brush: QBrush) -> None:
        """ 设置悬停背景画刷 """
        if self.__hoverBgBrush != hover_bg_brush:
            self.__hoverBgBrush = hover_bg_brush
            self.update()

    def setCheckBgBrush(self, check_bg_brush: QBrush) -> None:
        """ 设置选中背景画刷 """
        if self.__checkBgBrush != check_bg_brush:
            self.__checkBgBrush = check_bg_brush
            self.update()

    paddingLeft: int = property(fget=getPaddingLeft, fset=setPaddingLeft, fdel=None, doc="")
    paddingRight: int = property(fget=getPaddingRight, fset=setPaddingRight, fdel=None, doc="")
    paddingTop: int = property(fget=getPaddingTop, fset=setPaddingTop, fdel=None, doc="")
    paddingBottom: int = property(fget=getPaddingBottom, fset=setPaddingBottom, fdel=None, doc="")
    textAlign: TextAlign = property(fget=getTextAlign, fset=setTextAlign, fdel=None, doc="")

    showTriangle: bool = property(fget=getShowTriangle, fset=setShowTriangle, fdel=None, doc="")
    triangleLen: int = property(fget=getTriangleLen, fset=setTriangleLen, fdel=None, doc="")
    trianglePosition: TrianglePosition = property(fget=getTrianglePosition, fset=setTrianglePosition, fdel=None, doc="")
    triangleColor: QColor = property(fget=getTriangleColor, fset=setTriangleColor, fdel=None, doc="")

    showIcon: bool = property(fget=getShowIcon, fset=setShowIcon, fdel=None, doc="")
    iconSpace: int = property(fget=getIconSpace, fset=setIconSpace, fdel=None, doc="")
    iconSize: QSize = property(fget=getIconSize, fset=setIconSize, fdel=None, doc="")
    iconNormal: QPixmap = property(fget=getIconNormal, fset=setIconNormal, fdel=None, doc="")
    iconHover: QPixmap = property(fget=getIconHover, fset=setIconHover, fdel=None, doc="")
    iconCheck: QPixmap = property(fget=getIconCheck, fset=setIconCheck, fdel=None, doc="")

    showLine: bool = property(fget=getShowLine, fset=setShowLine, fdel=None, doc="")
    lineSpace: int = property(fget=getLineSpace, fset=setLineSpace, fdel=None, doc="")
    lineWidth: int = property(fget=getLineWidth, fset=setLineWidth, fdel=None, doc="")
    linePosition: LinePosition = property(fget=getLinePosition, fset=setLinePosition, fdel=None, doc="")
    lineColor: QColor = property(fget=getLineColor, fset=setLineColor, fdel=None, doc="")

    normalBgColor: QColor = property(fget=getNormalBgColor, fset=setNormalBgColor, fdel=None, doc="")
    hoverBgColor: QColor = property(fget=getHoverBgColor, fset=setHoverBgColor, fdel=None, doc="")
    checkBgColor: QColor = property(fget=getCheckBgColor, fset=setCheckBgColor, fdel=None, doc="")
    normalTextColor: QColor = property(fget=getNormalTextColor, fset=setNormalTextColor, fdel=None, doc="")
    hoverTextColor: QColor = property(fget=getHoverTextColor, fset=setHoverTextColor, fdel=None, doc="")
    checkTextColor: QColor = property(fget=getCheckTextColor, fset=setCheckTextColor, fdel=None, doc="")


if __name__ == '__main__':
    import sys

    def buttonClick(is_clicked: bool) -> None:
        print(is_clicked)

    app: QApplication = QApplication(sys.argv)

    button: NavButton = NavButton()
    button.clicked.connect(buttonClick)
    button.show()

    sys.exit(app.exec_())
