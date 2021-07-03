from typing import List, AnyStr

import shiboken2
from PySide2.QtCore import Signal, QSize
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy


class ColorPanelBtn(QWidget):
    """
    颜色按钮面板
    作者:feiyangqingyun(QQ:517216493) 2017-11-17
    译者:sunchuquin(QQ:1715216365) 2021-07-03
    1. 可设置颜色集合
    2. 可设置按钮圆角角度
    3. 可设置列数
    4. 可设置按钮边框宽度和边框颜色
    """

    colorChanged = Signal(QColor)  # color

    def __init__(self, parent: QWidget = None):
        super(ColorPanelBtn, self).__init__(parent)
        self.__space: int = 2  # 按钮之间的间隔
        self.__columnCount: int = 11  # 按钮列数
        self.__borderRadius: int = 0  # 边框圆角
        self.__borderWidth: int = 2  # 边框宽度
        self.__borderColor: QColor = QColor("#C0392B")  # 边框颜色

        self.__gridLayout: QGridLayout = QGridLayout()
        self.__gridLayout.setSpacing(self.__space)
        self.__gridLayout.setMargin(0)
        self.__btns: List[QPushButton] = []
        self.__colors: List[AnyStr] = [
            "#FEFEFE", "#EEEEEF", "#DCDDDD", "#C9CACA", "#B6B6B7", "#A1A1A1", "#8B8B8C",
            "#757475", "#5F5D5D", "#474443", "#303030", "#00A2E9", "#009B4C", "#FFF000",
            "#E62129", "#E40082", "#B04B87", "#F08519", "#F4B3B3", "#897870", "#D2CDE6",
            "#A79CCB", "#758FC8", "#7C6FB0", "#9288B1", "#566892", "#5E5872", "#7789A4",
            "#008FD7", "#A0D9F6", "#B8CEDA", "#98AAB4", "#75838A", "#50585D", "#5B7877",
            "#4B8D7F", "#769C9B", "#5BA997", "#5FA776", "#62C3D0", "#56AAB7", "#B9CCBC",
            "#D5EAD8", "#A6D4AE", "#99A99C", "#9AA780", "#BCC774", "#BBC99A", "#ACCE22",
            "#D9E483", "#5F5C50", "#8B8979", "#B6B49E", "#B6B281", "#DED572", "#FFF582",
            "#FFF9B1", "#FFFCDB", "#B39B77", "#D59961", "#DAB96B", "#EF8641", "#F6AE45",
            "#F5B06E", "#FDD100", "#FBD7A3", "#89765B", "#AC6249", "#D0753B", "#EF8762",
            "#F5B193", "#FADAC9", "#AF8283", "#CF7771", "#FF696B", "#CF788A", "#E61D4C",
            "#EF8781", "#E95A6F", "#D49D9E", "#876474", "#AC6484", "#F4B5D0", "#D49EB6",
            "#B39FA8", "#D8C0CB", "#B3719D", "#CA5599", "#CD81B3", "#B593B3", "#D0A9CD",
            "#745E73", "#977B95", "#A878B1", "#A72185", "#934787", "#804E9A", "#7B5882",
            "#714588"
        ]
        self.setLayout(self.__gridLayout)
        self.initStyle()
        self.initBtn()

    def initStyle(self) -> None:
        qss: str = "QPushButton{border:none;border-radius:%dpx;" % self.__borderRadius
        qss += "QPushButton:hover{border:%dpx solid %s;}" % (self.__borderWidth, self.__borderColor.name())
        self.setStyleSheet(qss)

    def initBtn(self) -> None:
        for btn in self.__btns: shiboken2.delete(btn)
        self.__btns.clear()

        count: int = len(self.__colors)
        row: int = 0
        column: int = 0
        index: int = 0
        for i in range(count):
            btn: QPushButton = QPushButton()
            btn.pressed.connect(self.btnClicked)
            btn.setObjectName("btn" + self.__colors[i])
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("QPushButton{background:%s;}" % self.__colors[i])

            self.__gridLayout.addWidget(btn, row, column)
            column += 1
            index += 1

            if index % self.__columnCount == 0:
                row += 1
                column = 0

            self.__btns.append(btn)

    def btnClicked(self) -> None:
        btn: QPushButton = self.sender()
        objName: str = btn.objectName()
        self.colorChanged.emit(QColor(objName[-7:]))

    @property
    def space(self) -> int: return self.__space

    @space.setter
    def space(self, n_space: int) -> None:
        if self.__space == n_space: return
        self.__space = n_space
        self.__gridLayout.setSpacing(n_space)

    @property
    def columnCount(self) -> int: return self.__columnCount

    @columnCount.setter
    def columnCount(self, column_count: int) -> None:
        if self.__columnCount == column_count: return
        self.__columnCount = column_count
        self.initBtn()

    @property
    def borderRadius(self) -> int: return self.__borderRadius

    @borderRadius.setter
    def borderRadius(self, border_radius: int) -> None:
        if self.__borderRadius == border_radius: return
        self.__borderRadius = border_radius
        self.initStyle()

    @property
    def borderWidth(self) -> int: return self.__borderWidth

    @borderWidth.setter
    def borderWidth(self, border_width: int) -> None:
        if self.__borderWidth == border_width: return
        self.__borderWidth = border_width
        self.initStyle()

    @property
    def borderColor(self) -> QColor: return self.__borderColor

    @borderColor.setter
    def borderColor(self, border_color: QColor) -> None:
        if self.__borderColor == border_color: return
        self.__borderColor = border_color
        self.initStyle()

    @property
    def colors(self) -> List[AnyStr]: return self.__colors

    @colors.setter
    def colors(self, n_colors: List[AnyStr]) -> None:
        if self.__colors == n_colors: return
        self.__colors = n_colors
        self.initBtn()

    def sizeHint(self) -> QSize: return QSize(400, 300)

    def minimumSizeHint(self) -> QSize: return QSize(40, 30)


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec, Qt
    from PySide2.QtGui import QFont
    from PySide2.QtWidgets import QApplication, QLabel, QHBoxLayout

    class FrmColorPanelBtn(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmColorPanelBtn, self).__init__(parent)
            self.resize(500, 300)

            self.colorPanelBtn = ColorPanelBtn()
            self.labColor = QLabel()
            self.labColor.setMinimumWidth(30)

            layout = QHBoxLayout()
            layout.addWidget(self.colorPanelBtn)
            layout.addWidget(self.labColor)
            self.setLayout(layout)

            self.colorPanelBtn.colorChanged.connect(self.colorChanged)
            self.colorChanged(QColor(255, 0, 0))

        def colorChanged(self, color: QColor) -> None:
            self.labColor.setStyleSheet(str("QLabel{background:%s;}" % color.name()))

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = FrmColorPanelBtn()
    window.setWindowTitle("颜色按钮面板")
    window.show()
    sys.exit(app.exec_())

