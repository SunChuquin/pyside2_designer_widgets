
from enum import Enum
from PySide2.QtGui import QPainter, QColor, QPixmap, QPen, QPolygon
from PySide2.QtCore import QEnum, QSize, Qt, QRect, QPoint
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

        # 文字左侧间隔
        self.__paddingLeft = 20  # int
        # 文字右侧间隔
        self.__paddingRight = 5  # int
        # 文字顶部间隔
        self.__paddingTop = 5  # int
        # 文字底部间隔
        self.__paddingBottom = 5  # int
        # 文字对齐
        self.__textAlign = NavButton.TextAlign.TEXTALIGN_LEFT  # typing.enum[TextAlign]

        # 显示倒三角
        self.__showTriangle = False  # bool
        # 倒三角边长
        self.__triangleLen = 5  # int
        # 倒三角位置
        self.__trianglePosition = NavButton.TrianglePosition.TRIANGLEPOSITION_RIGHT  # typing.enum[TrianglePosition]
        # 倒三角颜色
        self.__triangleColor = QColor(255, 255, 255)  # PySide2.QtGui.QColor

        # 显示图标
        self.__showIcon = True  # bool
        # 图标间隔
        self.__iconSpace = 10  # int
        # 图标尺寸
        self.__iconSize = QSize(16, 16)  # PySide2.QtCore.QSize
        # 正常图标
        self.__iconNormal = QPixmap(0, 0)  # PySide2.QtGui.QPixmap
        # 悬停图标
        self.__iconHover = QPixmap(0, 0)  # PySide2.QtGui.QPixmap
        # 选中图标
        self.__iconCheck = QPixmap(0, 0)  # PySide2.QtGui.QPixmap

        # 显示线条
        self.__showLine = True  # bool
        # 线条间隔
        self.__lineSpace = 0  # int
        # 线条宽度
        self.__lineWidth = 5  # int
        # 线条位置
        self.__linePosition = NavButton.LinePosition.LINEPOSITION_LEFT  # typing.enum[LinePosition]
        # 线条颜色
        self.__lineColor = QColor(0, 187, 158)  # PySide2.QtGui.QColor

        # 正常背景颜色
        self.__normalBgColor = QColor(230, 230, 230)  # PySide2.QtGui.QColor
        # 悬停背景颜色
        self.__hoverBgColor = QColor(130, 130, 130)  # PySide2.QtGui.QColor
        # 选中背景颜色
        self.__checkBgColor = QColor(80, 80, 80)  # PySide2.QtGui.QColor
        # 正常文字颜色
        self.__normalTextColor = QColor(100, 100, 100)  # PySide2.QtGui.QColor
        # 悬停文字颜色
        self.__hoverTextColor = QColor(255, 255, 255)  # PySide2.QtGui.QColor
        # 选中文字颜色
        self.__checkTextColor = QColor(255, 255, 255)  # PySide2.QtGui.QColor

        # 正常背景画刷
        self.__normalBgBrush = Qt.NoBrush  # PySide2.QtGui.QBrush
        # 悬停背景画刷
        self.__hoverBgBrush = Qt.NoBrush  # PySide2.QtGui.QBrush
        # 选中背景画刷
        self.__checkBgBrush = Qt.NoBrush  # PySide2.QtGui.QBrush

        # 悬停标志位
        self.__hover = False  # bool

        self.setCheckable(True)
        self.setText("导航按钮")

    def __del__(self):
        pass

    def enterEvent(self, event):  # enterEvent(self, event: PySide2.QtCore.QEvent)
        """  """
        self.__hover = True
        self.update()
    # enterEvent

    def leaveEvent(self, event):  # leaveEvent(self, event: PySide2.QtCore.QEvent)
        """  """
        self.__hover = False
        self.update()
    # leaveEvent

    def paintEvent(self, event):  # paintEvent(self, event: PySide2.QtCore.QEvent)
        """  """
        # 绘制准备工作，启用反锯齿
        painter = QPainter(self)
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
    # paintEvent

    def drawBg(self, painter):  # drawBg(self, painter: PySide2.QtGui.QPainter)
        """  """
        painter.save()
        painter.setPen(Qt.NoPen)

        width = self.width()  # int
        height = self.height()  # int

        bgRect = QRect()
        if self.__linePosition == NavButton.LinePosition.LINEPOSITION_LEFT:
            bgRect = QRect(self.lineSpace, 0, width - self.__lineSpace, height)  # PySide2.QtCore.QRect
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_RIGHT:
            bgRect = QRect(0, 0, width - self.__lineSpace, height)  # PySide2.QtCore.QRect
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_TOP:
            bgRect = QRect(0, self.lineSpace, width, height - self.__lineSpace)  # PySide2.QtCore.QRect
        elif self.__linePosition == NavButton.LinePosition.LINEPOSITION_BOTTOM:
            bgRect = QRect(0, 0, width, height - self.__lineSpace)  # PySide2.QtCore.QRect

        # 如果画刷存在则取画刷
        if self.isChecked():
            bgBrush = self.__checkBgBrush
        elif self.__hover:
            bgBrush = self.__hoverBgBrush
        else:
            bgBrush = self.__normalBgBrush

        if bgBrush != Qt.NoBrush:
            painter.setBrush(bgBrush)
        else:
            # 根据当前状态选择对应颜色
            if self.isChecked():
                bgColor = self.__checkBgColor  # PySide2.QtGui.QColor
            elif self.__hover:
                bgColor = self.__hoverBgColor  # PySide2.QtGui.QColor
            else:
                bgColor = self.__normalBgColor  # PySide2.QtGui.QColor

            painter.setBrush(bgColor)

        painter.drawRect(bgRect)

        painter.restore()
    # drawBg

    def drawText(self, painter):  # drawText(self, painter: PySide2.QtGui.QPainter)
        """  """
        painter.save()
        painter.setBrush(Qt.NoBrush)

        # 根据当前状态选择对应颜色
        if self.isChecked():
            textColor = self.__checkTextColor
        elif self.__hover:
            textColor = self.__hoverTextColor
        else:
            textColor = self.__normalTextColor

        textRect = QRect(self.__paddingLeft,
                         self.__paddingTop,
                         self.width() - self.__paddingLeft - self.__paddingRight,
                         self.height() - self.__paddingTop - self.__paddingBottom)
        painter.setPen(textColor)

        painter.drawText(textRect, self.__textAlign.value | Qt.AlignVCenter, self.text())

        painter.restore()
    # drawText

    def drawIcon(self, painter):  # drawIcon(self, painter: PySide2.QtGui.QPainter)
        """  """
        if not self.__showIcon:
            return

        painter.save()

        if self.isChecked():
            pix = self.__iconCheck
        elif self.__hover:
            pix = self.__iconHover
        else:
            pix = self.__iconNormal

        if not pix.isNull():
            # 等比例平滑缩放图标
            pix = pix.scaled(self.__iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawpixmap(self.__iconSpace, (self.height() - self.__iconSize.height()) / 2, pix)

        painter.restore()
    # drawIcon

    def drawLine(self, painter):  # drawLine(self, painter: PySide2.QtGui.QPainter)
        """  """
        if not self.__showLine:
            return

        if not self.isChecked():
            return

        painter.save()

        pen = QPen()
        pen.setWidth(self.__lineWidth)
        pen.setColor(self.__lineColor)
        painter.setPen(pen)

        # 根据线条位置设置线条坐标
        pointStart = QPoint()
        pointEnd = QPoint()
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
    # drawLine

    def drawTriangle(self, painter):  # drawTriangle(self, painter: PySide2.QtGui.QPainter)
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
        width = self.width()  # int
        height = self.height()  # int
        midWidth = width // 2
        midHeight = height // 2

        pts = QPolygon()
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
    # drawTriangle

    def getPaddingLeft(self):  # getPaddingLeft(self) -> int
        """ 读取文字左侧间隔 """
        return self.__paddingLeft
    # getPaddingLeft

    def getPaddingRight(self):  # getPaddingRight(self) -> int
        """ 读取文字右侧间隔 """
        return self.__paddingRight
    # getPaddingRight

    def getPaddingTop(self):  # getPaddingTop(self) -> int
        """ 读取文字顶部间隔 """
        return self.__paddingTop
    # getPaddingTop

    def getPaddingBottom(self):  # getPaddingBottom(self) -> int
        """ 读取文字底部间隔 """
        return self.__paddingBottom
    # getPaddingBottom

    def getTextAlign(self):  # getTextAlign(self) -> typing.enum[TextAlign]
        """ 读取文字对齐方式 """
        return self.__textAlign
    # getTextAlign

    def getShowTriangle(self):  # getShowTriangle(self) -> bool
        """ 读取是否显示倒三角 """
        return self.__showTriangle
    # getShowTriangle

    def getTriangleLen(self):  # getTriangleLen(self) -> int
        """ 读取倒三角边长 """
        return self.__triangleLen
    # getTriangleLen

    def getTrianglePosition(self):  # getTrianglePosition(self) -> typing.enum[TrianglePosition]
        """ 读取倒三角位置 """
        return self.__trianglePosition
    # getTrianglePosition

    def getTriangleColor(self):  # getTriangleColor(self) -> PySide2.QtGui.QColor
        """ 读取倒三角颜色 """
        return self.__triangleColor
    # getTriangleColor

    def getShowIcon(self):  # getShowIcon(self) -> bool
        """ 读取是否显示图标 """
        return self.__showIcon
    # getShowIcon

    def getIconSpace(self):  # getIconSpace(self) -> int
        """ 读取图标间隔 """
        return self.__iconSpace
    # getIconSpace

    def getIconSize(self):  # getIconSize(self) -> PySide2.QtCore.QSize
        """ 读取图标尺寸 """
        return self.__iconSize
    # getIconSize

    def getIconNormal(self):  # getIconNormal(self) -> PySide2.QtGui.QPixmap
        """ 读取正常图标 """
        return self.__iconNormal
    # getIconNormal

    def getIconHover(self):  # getIconHover(self) -> PySide2.QtGui.QPixmap
        """ 读取悬停图标 """
        return self.__iconHover
    # getIconHover

    def getIconCheck(self):  # getIconCheck(self) -> PySide2.QtGui.QPixmap
        """ 读取选中图标 """
        return self.__iconCheck
    # getIconCheck

    def getShowLine(self):  # getShowLine(self) -> bool
        """ 读取是否显示线条 """
        return self.__showLine
    # getShowLine

    def getLineSpace(self):  # getLineSpace(self) -> int
        """ 读取线条间隔 """
        return self.__lineSpace
    # getLineSpace

    def getLineWidth(self):  # getLineWidth(self) -> int
        """ 读取线条宽度 """
        return self.__lineWidth
    # getLineWidth

    def getLinePosition(self):  # getLinePosition(self) -> typing.enum[LinePosition]
        """ 读取线条位置 """
        return self.__linePosition
    # getLinePosition

    def getLineColor(self):  # getLineColor(self) -> PySide2.QtGui.QColor
        """ 读取线条颜色 """
        return self.__lineColor
    # getLineColor

    def getNormalBgColor(self):  # getNormalBgColor(self) -> PySide2.QtGui.QColor
        """ 读取正常背景颜色 """
        return self.__normalBgColor
    # getNormalBgColor

    def getHoverBgColor(self):  # getHoverBgColor(self) -> PySide2.QtGui.QColor
        """ 读取悬停背景颜色 """
        return self.__hoverBgColor
    # getHoverBgColor

    def getCheckBgColor(self):  # getCheckBgColor(self) -> PySide2.QtGui.QColor
        """ 读取选中背景颜色 """
        return self.__checkBgColor
    # getCheckBgColor

    def getNormalTextColor(self):  # getNormalTextColor(self) -> PySide2.QtGui.QColor
        """ 读取正常文字颜色 """
        return self.__normalTextColor
    # getNormalTextColor

    def getHoverTextColor(self):  # getHoverTextColor(self) -> PySide2.QtGui.QColor
        """ 读取悬停文字颜色 """
        return self.__hoverTextColor
    # getHoverTextColor

    def getCheckTextColor(self):  # getCheckTextColor(self) -> PySide2.QtGui.QColor
        """ 读取选中文字颜色 """
        return self.__checkTextColor
    # getCheckTextColor

    def sizeHint(self):  # sizeHint(self) -> PySide2.QtCore.QSize
        """  """
        return QSize(100, 30)
    # sizeHint

    def minimumSizeHint(self):  # minimumSizeHint(self) -> PySide2.QtCore.QSize
        """  """
        return QSize(20, 10)
    # minimumSizeHint

    def setPaddingLeft(self, padding_left):  # setPaddingLeft(self, padding_left: int)
        """ 设置文字左侧间隔 """
        if self.__paddingLeft != padding_left:
            self.__paddingLeft = padding_left
            self.update()
    # setPaddingLeft

    def setPaddingRight(self, padding_right):  # setPaddingRight(self, padding_right: int)
        """ 设置文字右侧间隔 """
        if self.__paddingRight != padding_right:
            self.__paddingRight = padding_right
            self.update()
    # setPaddingLeft

    def setPaddingTop(self, padding_top):  # setPaddingTop(self, padding_top: int)
        """ 设置文字顶部间隔 """
        if self.__paddingTop != padding_top:
            self.__paddingTop = padding_top
            self.update()
    # setPaddingTop

    def setPaddingBottom(self, padding_bottom):  # setPaddingBottom(self, padding_bottom: int)
        """ 设置文字底部间隔 """
        if self.__paddingBottom != padding_bottom:
            self.__paddingBottom = padding_bottom
            self.update()
    # setPaddingBottom

    def setPadding(self, padding_left, padding_right, padding_top, padding_bottom):  # setPadding(self, padding_left, padding_right, padding_top, padding_bottom):
        """ 设置文字间隔 """
        self.__paddingLeft = padding_left
        self.__paddingRight = padding_right
        self.__paddingTop = padding_top
        self.__paddingBottom = padding_bottom
        self.update()
    # setPadding

    def setTextAlign(self, text_align):  # setTextAlign(self, text_align: typing.enum[TextAlign])
        """ 设置文字对齐 """
        if self.__textAlign != text_align:
            self.__textAlign = text_align
            self.update()
    # setTextAlign

    def setShowTriangle(self, show_triangle):  # setShowTriangle(self, show_triangle: bool)
        """ 设置是否显示倒三角 """
        if self.__showTriangle != show_triangle:
            self.__showTriangle = show_triangle
            self.update()
    # setShowTriangle

    def setTriangleLen(self, triangle_len):  # setTriangleLen(self, triangle_len: int)
        """ 设置倒三角边长 """
        if self.__triangleLen != triangle_len:
            self.__triangleLen = triangle_len
            self.update()
    # setTriangleLen

    def setTrianglePosition(self, triangle_position):  # setTrianglePosition(self, triangle_position: typing.enum[TrianglePosition])
        """ 设置倒三角位置 """
        if self.__trianglePosition != triangle_position:
            self.__trianglePosition = triangle_position
            self.update()
    # setTrianglePosition

    def setTriangleColor(self, triangle_color):  # setTriangleColor(self, triangle_color: PySide2.QtGui.QColor)
        """ 设置倒三角颜色 """
        if self.__triangleColor != triangle_color:
            self.__triangleColor = triangle_color
            self.update()
    # setTriangleColor

    def setShowIcon(self, show_icon):  # setShowIcon(self, show_icon: bool)
        """ 设置是否显示图标 """
        if self.__showIcon != show_icon:
            self.__showIcon = show_icon
            self.update()
    # setShowIcon

    def setIconSpace(self, icon_space):  # setIconSpace(self, icon_space: int)
        """ 设置图标间隔 """
        if self.__iconSpace != icon_space:
            self.__iconSpace = icon_space
            self.update()
    # setIconSpace

    def setIconSize(self, icon_size):  # setIconSize(self, icon_size: PySide2.QtCore.QSize)
        """ 设置图标尺寸 """
        if self.__iconSize != icon_size:
            self.__iconSize = icon_size
            self.update()
    # setIconSize

    def setIconNormal(self, icon_normal):  # setIconNormal(self, icon_normal: PySide2.QtGui.QPixmap)
        """ 设置正常图标 """
        self.__iconNormal = icon_normal
        self.update()
    # setIconNormal

    def setIconHover(self, icon_hover):  # setIconHover(self, icon_hover: PySide2.QtGui.QPixmap)
        """ 设置悬停图标 """
        self.__iconHover = icon_hover
        self.update()
    # setIconHover

    def setIconCheck(self, icon_check):  # setIconCheck(self, icon_check: PySide2.QtGui.QPixmap)
        """ 设置按下图标 """
        self.__iconCheck = icon_check
        self.update()
    # setIconCheck

    def setShowLine(self, show_line):  # setShowLine(self, show_line: bool)
        """ 设置是否显示线条 """
        if self.__showLine != show_line:
            self.__showLine = show_line
            self.update()
    # setShowLine

    def setLineSpace(self, line_space):  # setLineSpace(self, line_space: int)
        """ 设置线条间隔 """
        if self.__lineSpace != line_space:
            self.__lineSpace = line_space
            self.update()
    # setLineSpace

    def setLineWidth(self, line_width):  # setLineWidth(self, line_width: int)
        """ 设置线条宽度 """
        if self.__lineWidth != line_width:
            self.__lineWidth = line_width
            self.update()
    # setLineWidth

    def setLinePosition(self, line_position):  # setLinePosition(self, line_position: typing.enum[LinePosition])
        """ 设置线条位置 """
        if self.__linePosition != line_position:
            self.__linePosition = line_position
            self.update()
    # setLinePosition

    def setLineColor(self, line_color):  # setLineColor(self, line_color: PySide2.QtGui.QColor)
        """ 设置线条颜色 """
        if self.__lineColor != line_color:
            self.__lineColor = line_color
            self.update()
    # setLineColor

    def setNormalBgColor(self, normal_bg_color):  # setNormalBgColor(self, normal_bg_color: PySide2.QtGui.QColor)
        """ 设置正常背景颜色 """
        if self.__normalBgColor != normal_bg_color:
            self.__normalBgColor = normal_bg_color
            self.update()
    # setNormalBgColor

    def setHoverBgColor(self, hover_bg_color):  # setHoverBgColor(self, hover_bg_color: PySide2.QtGui.QColor)
        """ 设置悬停背景颜色 """
        if self.__hoverBgColor != hover_bg_color:
            self.__hoverBgColor = hover_bg_color
            self.update()
    # setHoverBgColor

    def setCheckBgColor(self, check_bg_color):  # setCheckBgColor(self, check_bg_color: PySide2.QtGui.QColor)
        """ 设置选中背景颜色 """
        if self.__checkBgColor != check_bg_color:
            self.__checkBgColor = check_bg_color
            self.update()
    # setCheckBgColor

    def setNormalTextColor(self, normal_text_color):  # setNormalTextColor(self, normal_text_color: PySide2.QtGui.QColor)
        """ 设置正常文字颜色 """
        if self.__normalTextColor != normal_text_color:
            self.__normalTextColor = normal_text_color
            self.update()
    # setNormalTextColor

    def setHoverTextColor(self, hover_text_color):  # setHoverTextColor(self, hover_text_color: PySide2.QtGui.QColor)
        """ 设置悬停文字颜色 """
        if self.__hoverTextColor != hover_text_color:
            self.__hoverTextColor = hover_text_color
            self.update()
    # setHoverTextColor

    def setCheckTextColor(self, check_text_color):  # setCheckTextColor(self, check_text_color: PySide2.QtGui.QColor)
        """ 设置选中文字颜色 """
        if self.__checkTextColor != check_text_color:
            self.__checkTextColor = check_text_color
            self.update()
    # setCheckTextColor

    def setNormalBgBrush(self, normal_bg_brush):  # setNormalBgBrush(self, normal_bg_brush: PySide2.QtGui.QBrush)
        """ 设置正常背景画刷 """
        if self.__normalBgBrush != normal_bg_brush:
            self.__normalBgBrush = normal_bg_brush
            self.update()
    # setNormalBgBrush

    def setHoverBgBrush(self, hover_bg_brush):  # setHoverBgBrush(self, hover_bg_brush: PySide2.QtGui.QBrush)
        """ 设置悬停背景画刷 """
        if self.__hoverBgBrush != hover_bg_brush:
            self.__hoverBgBrush = hover_bg_brush
            self.update()
    # setHoverBgBrush

    def setCheckBgBrush(self, check_bg_brush):  # setCheckBgBrush(self, check_bg_brush: PySide2.QtGui.QBrush)
        """ 设置选中背景画刷 """
        if self.__checkBgBrush != check_bg_brush:
            self.__checkBgBrush = check_bg_brush
            self.update()
    # setCheckBgBrush

    paddingLeft = property(fget=getPaddingLeft, fset=setPaddingLeft, fdel=None, doc="")  # int
    paddingRight = property(fget=getPaddingRight, fset=setPaddingRight, fdel=None, doc="")  # int
    paddingTop = property(fget=getPaddingTop, fset=setPaddingTop, fdel=None, doc="")  # int
    paddingBottom = property(fget=getPaddingBottom, fset=setPaddingBottom, fdel=None, doc="")  # int
    textAlign = property(fget=getTextAlign, fset=setTextAlign, fdel=None, doc="")  # typing.enum[TextAlign]

    showTriangle = property(fget=getShowTriangle, fset=setShowTriangle, fdel=None, doc="")  # bool
    triangleLen = property(fget=getTriangleLen, fset=setTriangleLen, fdel=None, doc="")  # int
    trianglePosition = property(fget=getTrianglePosition, fset=setTrianglePosition, fdel=None, doc="")  # typing.enum[TrianglePosition]
    triangleColor = property(fget=getTriangleColor, fset=setTriangleColor, fdel=None, doc="")  # PySide2.QtGui.QColor

    showIcon = property(fget=getShowIcon, fset=setShowIcon, fdel=None, doc="")  # bool
    iconSpace = property(fget=getIconSpace, fset=setIconSpace, fdel=None, doc="")  # int
    iconSize = property(fget=getIconSize, fset=setIconSize, fdel=None, doc="")  # PySide2.QtCore.QSize
    iconNormal = property(fget=getIconNormal, fset=setIconNormal, fdel=None, doc="")  # PySide2.QtGui.QPixmap
    iconHover = property(fget=getIconHover, fset=setIconHover, fdel=None, doc="")  # PySide2.QtGui.QPixmap
    iconCheck = property(fget=getIconCheck, fset=setIconCheck, fdel=None, doc="")  # PySide2.QtGui.QPixmap

    showLine = property(fget=getShowLine, fset=setShowLine, fdel=None, doc="")  # bool
    lineSpace = property(fget=getLineSpace, fset=setLineSpace, fdel=None, doc="")  # int
    lineWidth = property(fget=getLineWidth, fset=setLineWidth, fdel=None, doc="")  # int
    linePosition = property(fget=getLinePosition, fset=setLinePosition, fdel=None, doc="")  # typing.enum[LinePosition]
    lineColor = property(fget=getLineColor, fset=setLineColor, fdel=None, doc="")  # PySide2.QtGui.QColor

    normalBgColor = property(fget=getNormalBgColor, fset=setNormalBgColor, fdel=None, doc="")  # PySide2.QtGui.QColor
    hoverBgColor = property(fget=getHoverBgColor, fset=setHoverBgColor, fdel=None, doc="")  # PySide2.QtGui.QColor
    checkBgColor = property(fget=getCheckBgColor, fset=setCheckBgColor, fdel=None, doc="")  # PySide2.QtGui.QColor
    normalTextColor = property(fget=getNormalTextColor, fset=setNormalTextColor, fdel=None, doc="")  # PySide2.QtGui.QColor
    hoverTextColor = property(fget=getHoverTextColor, fset=setHoverTextColor, fdel=None, doc="")  # PySide2.QtGui.QColor
    checkTextColor = property(fget=getCheckTextColor, fset=setCheckTextColor, fdel=None, doc="")  # PySide2.QtGui.QColor


if __name__ == '__main__':
    import sys

    def buttonClick(is_clicked):  # bool
        print(is_clicked)

    app = QApplication(sys.argv)

    button = NavButton()
    button.clicked.connect(buttonClick)
    button.show()

    sys.exit(app.exec_())
