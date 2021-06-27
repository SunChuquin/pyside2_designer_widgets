from enum import Enum
from typing import AnyStr

from PySide2.QtCore import QEnum, QRect, QSize, Signal, Qt, QPoint
from PySide2.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QPolygon
from PySide2.QtWidgets import QLabel, QWidget


class NavLabel(QLabel):

    """
    导航标签控件
    作者:feiyangqingyun(QQ:517216493) 2016-11-28
    译者:sunchuquin(QQ:1715216365) 2021-06-27
    1. 可设置前景色和背景色
    2. 可设置箭头位置方向 左右上下
    3. 可设置箭头大小
    4. 可设置显示倒三角
    5. 可设置倒三角长度/位置/颜色
    """

    clicked = Signal()

    @QEnum
    class ArrowPosition(Enum):
        ArrowPosition_Left = 0  # 向左箭头
        ArrowPosition_Right = 1  # 向右箭头
        ArrowPosition_Top = 2  # 向上箭头
        ArrowPosition_Bottom = 3  # 向下箭头

    @QEnum
    class TrianglePosition(Enum):
        TrianglePosition_Left = 0  # 左侧
        TrianglePosition_Right = 1  # 右侧
        TrianglePosition_Top = 2  # 顶部
        TrianglePosition_Bottom = 3  # 底部

    def __init__(self, text: AnyStr, parent: QWidget = None):
        super(NavLabel, self).__init__(parent)
        self.__borderRadius: int = 5  # 边框圆角角度
        self.__background: QColor = QColor(100, 184, 255)  # 背景色
        self.__foreground: QColor = QColor(255, 255, 255)  # 前景色

        self.__showArrow: bool = True  # 显示箭头
        self.__arrowSize: int = 5  # 箭头大小
        self.__arrowPosition: NavLabel.ArrowPosition = NavLabel.ArrowPosition.ArrowPosition_Right  # 箭头位置

        self.__showTriangle: bool = False  # 显示倒三角
        self.__triangleLen: int = 5  # 倒三角边长
        self.__trianglePosition: NavLabel.TrianglePosition = NavLabel.TrianglePosition.TrianglePosition_Left  # 倒三角位置
        self.__triangleColor: QColor = QColor(255, 255, 255)  # 倒三角颜色

        self.__bgRect: QRect = self.geometry()  # 绘制区域

        self.setText(text)

    @property
    def borderRadius(self) -> int: return self.__borderRadius

    @borderRadius.setter
    def borderRadius(self, border_radius: int) -> None:
        if self.__borderRadius == border_radius: return
        self.__borderRadius = border_radius
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
    def showArrow(self) -> bool: return self.__showArrow

    @showArrow.setter
    def showArrow(self, show_arrow: bool) -> None:
        if self.__showArrow == show_arrow: return
        self.__showArrow = show_arrow
        self.update()

    @property
    def arrowSize(self) -> int: return self.__arrowSize

    @arrowSize.setter
    def arrowSize(self, arrow_size: int) -> None:
        if self.__arrowSize == arrow_size: return
        self.__arrowSize = arrow_size
        self.update()

    @property
    def arrowPosition(self) -> ArrowPosition: return self.__arrowPosition

    @arrowPosition.setter
    def arrowPosition(self, arrow_position: ArrowPosition) -> None:
        if self.__arrowPosition == arrow_position: return
        self.__arrowPosition = arrow_position
        self.update()

    @property
    def showTriangle(self) -> bool: return self.__showTriangle

    @showTriangle.setter
    def showTriangle(self, show_triangle: bool) -> None:
        if self.__showTriangle == show_triangle: return
        self.__showTriangle = show_triangle
        self.update()

    @property
    def triangleLen(self) -> int: return self.__triangleLen

    @triangleLen.setter
    def triangleLen(self, triangle_len: int) -> None:
        if self.__triangleLen == triangle_len: return
        self.__triangleLen = triangle_len
        self.update()

    @property
    def trianglePosition(self) -> TrianglePosition: return self.__trianglePosition

    @trianglePosition.setter
    def trianglePosition(self, triangle_position: TrianglePosition) -> None:
        if self.__trianglePosition == triangle_position: return
        self.__trianglePosition = triangle_position
        self.update()

    @property
    def triangleColor(self) -> QColor: return self.__triangleColor

    @triangleColor.setter
    def triangleColor(self, triangle_color: QColor) -> None:
        if self.__triangleColor == triangle_color: return
        self.__triangleColor = triangle_color
        self.update()

    def sizeHint(self) -> QSize: return QSize(100, 30)

    def minimumSizeHint(self) -> QSize: return QSize(20, 10)

    def mousePressEvent(self, event: QMouseEvent) -> None: self.clicked.emit()

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制准备工作,启用反锯齿
        painter: QPainter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 绘制背景
        self.drawBg(painter)
        # 绘制文字
        self.drawText(painter)
        # 绘制倒三角
        self.drawTriangle(painter)

    def drawBg(self, painter: QPainter) -> None:
        width: int = self.width()
        height: int = self.height()
        endX: int = width - self.__arrowSize
        endY: int = height - self.__arrowSize

        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__background)

        pts: QPolygon = QPolygon()
        if self.__arrowPosition == NavLabel.ArrowPosition.ArrowPosition_Right:
            self.__bgRect = QRect(0, 0, endX, height)
            pts.append(QPoint(endX, int(height / 2 - self.__arrowSize)))
            pts.append(QPoint(endX, int(height / 2 + self.__arrowSize)))
            pts.append(QPoint(width, int(height / 2)))
        elif self.__arrowPosition == NavLabel.ArrowPosition.ArrowPosition_Left:
            self.__bgRect = QRect(self.__arrowSize, 0, width - self.__arrowSize, height)
            pts.append(QPoint(self.__arrowSize, int(height / 2 - self.__arrowSize)))
            pts.append(QPoint(self.__arrowSize, int(height / 2 + self.__arrowSize)))
            pts.append(QPoint(0, int(height / 2)))
        elif self.__arrowPosition == NavLabel.ArrowPosition.ArrowPosition_Bottom:
            self.__bgRect = QRect(0, 0, width, endY)
            pts.append(QPoint(int(width / 2 - self.__arrowSize), endY))
            pts.append(QPoint(int(width / 2 + self.__arrowSize), endY))
            pts.append(QPoint(int(width / 2), height))
        elif self.__arrowPosition == NavLabel.ArrowPosition.ArrowPosition_Top:
            self.__bgRect = QRect(0, self.__arrowSize, width, height - self.__arrowSize)
            pts.append(QPoint(int(width / 2 - self.__arrowSize), self.__arrowSize))
            pts.append(QPoint(int(width / 2 + self.__arrowSize), self.__arrowSize))
            pts.append(QPoint(int(width / 2), 0))

        # 绘制圆角矩形和三角箭头
        if not self.__showArrow:
            bgRect = self.rect()
            painter.drawRoundedRect(self.__bgRect, self.__borderRadius, self.__borderRadius)
        else:
            painter.drawRoundedRect(self.__bgRect, self.__borderRadius, self.__borderRadius)
            painter.drawPolygon(pts)

        painter.restore()

    def drawText(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(self.__foreground)
        painter.setBrush(Qt.NoBrush)
        painter.drawText(self.__bgRect, Qt.AlignCenter, self.text())
        painter.restore()

    def drawTriangle(self, painter: QPainter) -> None:
        if not self.__showTriangle: return

        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__triangleColor)

        # 绘制在右侧中间,根据设定的倒三角的边长设定三个点位置
        width: int = self.width()
        height: int = self.height()
        midWidth: int = width // 2
        midHeight: int = height // 2

        pts: QPolygon = QPolygon()
        if self.__trianglePosition == NavLabel.TrianglePosition.TrianglePosition_Left:
            pts.append(QPoint(self.__triangleLen, midHeight))
            pts.append(QPoint(0, midHeight - self.__triangleLen))
            pts.append(QPoint(0, midHeight + self.__triangleLen))
        elif self.__trianglePosition == NavLabel.TrianglePosition.TrianglePosition_Right:
            pts.append(QPoint(width - self.__triangleLen, midHeight))
            pts.append(QPoint(width, midHeight - self.__triangleLen))
            pts.append(QPoint(width, midHeight + self.__triangleLen))
        elif self.__trianglePosition == NavLabel.TrianglePosition.TrianglePosition_Top:
            pts.append(QPoint(midWidth, self.__triangleLen))
            pts.append(QPoint(midWidth - self.__triangleLen, 0))
            pts.append(QPoint(midWidth + self.__triangleLen, 0))
        elif self.__trianglePosition == NavLabel.TrianglePosition.TrianglePosition_Bottom:
            pts.append(QPoint(midWidth, height - self.__triangleLen))
            pts.append(QPoint(midWidth - self.__triangleLen, height))
            pts.append(QPoint(midWidth + self.__triangleLen, height))

        painter.drawPolygon(pts)

        painter.restore()


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec
    from PySide2.QtGui import QFont
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy

    class FrmNavLabel(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmNavLabel, self).__init__(parent)

            widget = QWidget()
            layout = QHBoxLayout()
            self.navLabel51 = NavLabel('首页')
            self.navLabel52 = NavLabel('学生管理')
            self.navLabel53 = NavLabel('成绩查询')
            layout.addWidget(self.navLabel51)
            layout.addWidget(self.navLabel52)
            layout.addWidget(self.navLabel53)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            widget.setLayout(layout)
            widget.setMinimumSize(300, 30)
            widget.setMaximumSize(300, 30)

            widget1 = QWidget()
            layout = QGridLayout()
            self.navLabel11 = NavLabel('当前温度')
            self.navLabel12 = NavLabel('当前湿度')
            self.navLabel13 = NavLabel('当前压力')
            self.navLabel21 = NavLabel('温度告警值')
            self.navLabel22 = NavLabel('湿度告警值')
            self.navLabel23 = NavLabel('压力告警值')
            layout.addWidget(self.navLabel11, 0, 0)
            layout.addWidget(self.navLabel12, 1, 0)
            layout.addWidget(self.navLabel13, 2, 0)
            layout.addWidget(self.navLabel21, 0, 1)
            layout.addWidget(self.navLabel22, 1, 1)
            layout.addWidget(self.navLabel23, 2, 1)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setHorizontalSpacing(6)
            layout.setVerticalSpacing(6)
            widget1.setLayout(layout)
            widget1.setMinimumSize(220, 100)
            widget1.setMaximumSize(220, 100)
            widget1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

            widget2 = QWidget()
            layout = QHBoxLayout()
            self.navLabel31 = NavLabel('当\n前\n温\n度')
            self.navLabel32 = NavLabel('当\n前\n湿\n度')
            self.navLabel33 = NavLabel('当\n前\n压\n力')
            self.navLabel41 = NavLabel('当\n前\n温\n度')
            self.navLabel42 = NavLabel('当\n前\n湿\n度')
            self.navLabel43 = NavLabel('当\n前\n压\n力')
            layout.addWidget(self.navLabel31)
            layout.addWidget(self.navLabel32)
            layout.addWidget(self.navLabel33)
            layout.addWidget(self.navLabel41)
            layout.addWidget(self.navLabel42)
            layout.addWidget(self.navLabel43)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(6)
            widget2.setLayout(layout)
            widget2.setMinimumSize(220, 110)
            widget2.setMaximumSize(220, 16777215)
            widget2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

            widget_2 = QWidget(self)
            layout = QVBoxLayout()
            layout.addWidget(widget)
            layout.addWidget(widget1)
            layout.addWidget(widget2)
            widget_2.setLayout(layout)

            self.initForm()

        def initForm(self):
            self.navLabel11.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Left
            self.navLabel12.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Left
            self.navLabel13.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Left

            self.navLabel21.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Right
            self.navLabel22.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Right
            self.navLabel23.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Right

            self.navLabel31.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Top
            self.navLabel32.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Top
            self.navLabel33.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Top

            self.navLabel41.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Bottom
            self.navLabel42.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Bottom
            self.navLabel43.arrowPosition = NavLabel.ArrowPosition.ArrowPosition_Bottom

            self.navLabel12.background = QColor(255, 107, 107)
            self.navLabel13.background = QColor(24, 189, 155)
            self.navLabel21.background = QColor(225, 102, 255)
            self.navLabel22.background = QColor(45, 62, 80)
            self.navLabel23.background = QColor(210, 84, 0)

            self.navLabel32.background = QColor(255, 107, 107)
            self.navLabel33.background = QColor(24, 189, 155)
            self.navLabel41.background = QColor(225, 102, 255)
            self.navLabel42.background = QColor(45, 62, 80)
            self.navLabel43.background = QColor(210, 84, 0)

            self.navLabel51.borderRadius = 0
            self.navLabel52.borderRadius = 0
            self.navLabel53.borderRadius = 0
            self.navLabel51.background = QColor(80, 80, 80)
            self.navLabel52.background = QColor(80, 80, 80)
            self.navLabel53.background = QColor(80, 80, 80)
            self.navLabel52.showTriangle = True
            self.navLabel53.showTriangle = True
            self.navLabel53.showArrow = False

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmNavLabel()
    window.setWindowTitle('导航标签控件')
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec_())

