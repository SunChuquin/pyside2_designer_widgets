from typing import List

import custom_widgets.iconhelper.resource

import PySide2
from PySide2.QtCore import QObject, Qt, QSize, QEvent
from PySide2.QtGui import QFontDatabase, QFont, QPixmap, QPainter, QColor, QIcon
from PySide2.QtWidgets import QToolButton, QAbstractButton, QLabel, QWidget


class Singleton(type(QObject), type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class IconHelper(QObject, metaclass=Singleton):
    """
    图形字体处理类

    图型编号在线查询：https://www.fontawesomecheatsheet.com/
    """

    def __init__(self):
        super().__init__()

        self.icon_font: QFont = QFont()  # 图形字体
        self.btns: List[QToolButton] = []  # 按钮队列
        self.pix_normal: List[QPixmap] = []  # 正常图片队列
        self.pix_dark: List[QPixmap] = []  # 加深图片队列

        fontDb: QFontDatabase = QFontDatabase()
        if not fontDb.families().__contains__("FontAwesome"):
            fontId: int = fontDb.addApplicationFont(":/image/fontawesome-webfont.ttf")
            fontName: List[str] = fontDb.applicationFontFamilies(fontId)
            if len(fontName) == 0:
                print("load fontawesome-webfont.ttf error")

        if fontDb.families().__contains__("FontAwesome"):
            self.icon_font: QFont = QFont("FontAwesome")
            self.icon_font.setHintingPreference(QFont.PreferNoHinting)  # if QT_VERSION >= 4.8.0

    # __init__

    def setIconForQLabel(self, label: QLabel,
                         text: str,
                         font_size: int = 12):
        """ 设置 QLabel 的图标 """
        self.icon_font.setPixelSize(font_size)
        label.setFont(self.icon_font)
        label.setText(text)

    # setIconForQLabel

    def setIconForQAbstractButton(self, button: PySide2.QtWidgets.QAbstractButton,
                                  text: str,
                                  font_size: int = 12):
        """ 设置 QAbstractButton 的图标 """

        self.icon_font.setPixelSize(font_size)
        button.setFont(self.icon_font)
        button.setText(text)

    # setIconForQAbstractButton

    def getPixmap(self, color: QColor,
                  text: str,
                  font_size: int = 12,
                  pix_width: int = 15,
                  pix_height: int = 15,
                  flags=Qt.AlignCenter) -> QPixmap:
        """ 生成图标 """
        pix: QPixmap = QPixmap(pix_width, pix_height)
        pix.fill(Qt.transparent)

        painter: QPainter = QPainter()
        painter.begin(pix)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setPen(color)

        self.icon_font.setPixelSize(font_size)
        painter.setFont(self.icon_font)
        painter.drawText(pix.rect(), flags, text)
        painter.end()

        return pix

    # getPixmap

    def getPixmapForQToolButton(self, button: QAbstractButton,
                                normal: bool) -> QPixmap:
        """ 从 QToolButton 获取图标 """
        pix: QPixmap = QPixmap()
        index: int = self.btns.index(button)

        if index >= 0:
            if normal:
                pix = self.pix_normal[index]
            else:
                pix = self.pix_dark[index]
        return pix

    # getPixmapForQToolButton

    @staticmethod
    def setStyleForNavPaneNoIcon(widget: QWidget,
                                 text_location: str = "left",
                                 border_width: int = 3,
                                 border_color: str = "#029FEA",
                                 normal_bg_color: str = "#292F38",
                                 dark_bg_color: str = "#1D2025",
                                 normal_text_color: str = "#54626F",
                                 dark_text_color: str = "#FDFDFD"):
        """ 指定导航面板样式，不带图标 """
        strBorder: str = ""
        if text_location == "top":
            strBorder = "border-width:{0}px 0px 0px 0px;padding:{0}px {1}px {1}px {1}px;".format(border_width,
                                                                                                 border_width * 2)
        elif text_location == "right":
            strBorder = "border-width:0px {0}px 0px 0px;padding:{1}px {0}px {1}px {1}px;;".format(border_width,
                                                                                                  border_width * 2)
        elif text_location == "bottom":
            strBorder = "border-width:0px 0px {0}px 0px;padding:{1}px {1}px {0}px {1}px;".format(border_width,
                                                                                                 border_width * 2)
        elif text_location == "left":
            strBorder = "border-width:0px 0px 0px {0}px;padding:{1}px {1}px {1}px {0}px;".format(border_width,
                                                                                                 border_width * 2)

        qss: List[str] = [
            "QWidget[flag=\"{0}\"] QAbstractButton{border-style:none;border-radius:0px;padding:5px;color:{1};background:{2};}".format(
                text_location, normal_text_color, normal_bg_color),

            "QWidget[flag=\"{0}\"] QAbstractButton:hover,"
            "QWidget[flag=\"{0}\"] QAbstractButton:pressed,"
            "QWidget[flag=\"{0}\"] QAbstractButton:checked{"
            "border-style:solid;{1}border-color:{2};color:{3};background:{4};}".format(text_location, strBorder,
                                                                                       border_color, dark_text_color,
                                                                                       dark_bg_color)
        ]

        widget.setStyleSheet("".join(qss))

    # setStyleForNavPaneNoIcon

    def setStyleForNavPane(self,
                           widget: PySide2.QtWidgets.QWidget,
                           buttons: List[PySide2.QtWidgets.QToolButton],
                           pix_char: List[int],
                           icon_size: int = 12,
                           icon_width: int = 15,
                           icon_height: int = 15,
                           text_location: str = "left",
                           border_width: int = 3,
                           bordef_color: str = "#029FEA",
                           normal_bg_color: str = "#292F38",
                           dark_bg_color: str = "#1D2025",
                           normal_text_color: str = "#54626F",
                           dark_text_color: str = "#FDFDFD"):
        """ 指定导航面板样式，带图标和效果切换 """
        btnCount: int = len(buttons)
        charCount: int = len(pix_char)
        if btnCount <= 0 or charCount <= 0 or btnCount != charCount:
            return

        strBorder: str = ""
        if text_location == "top":
            strBorder = "border-width:{0}px 0px 0px 0px;padding:{0}px {1}px {1}px {1}px;".format(border_width,
                                                                                                 border_width * 2)
        elif text_location == "right":
            strBorder = "border-width:0px {0}px 0px 0px;padding:{1}px {0}px {1}px {1}px;".format(border_width,
                                                                                                 border_width * 2)
        elif text_location == "bottom":
            strBorder = "border-width:0px 0px {0}px 0px;padding:{1}px {1}px {0}px {1}px;".format(border_width,
                                                                                                 border_width * 2)
        elif text_location == "left":
            strBorder = "border-width:0px 0px 0px {0}px;padding:{1}px {1}px {1}px {0}px;".format(border_width,
                                                                                                 border_width * 2)

        # 如果图标是左侧显示则需要让没有选中的按钮左侧也有加深的边框，颜色为背景颜色
        qss: List[str] = []
        if buttons[0].toolButtonStyle() == Qt.ToolButtonTextBesideIcon:
            qss.append(
                "QWidget[flag=\"{0}\"] QAbstractButton{border-style:solid;border-radius:0px;{1}border-color:{2};color:{3};background:{2};}".format(
                    text_location, strBorder, normal_bg_color, normal_text_color))
        else:
            qss.append(
                "QWidget[flag=\"{0}\"] QAbstractButton{border-style:none;border-radius:0px;padding:5px;color:{1};background:{2};}".format(
                    text_location, normal_text_color, normal_bg_color))

        qss.append("QWidget[flag=\"{0}\"] QAbstractButton:hover,"
                   "QWidget[flag=\"{0}\"] QAbstractButton:pressed,"
                   "QWidget[flag=\"{0}\"] QAbstractButton:checked{"
                   "border-style:solid;{1}border-color:{2};color:{3};background:{4};}".format(
            text_location, strBorder, bordef_color, dark_text_color, dark_bg_color))

        qss.append("QWidget#{0}{background:{1};}".format(widget.objectName(), normal_bg_color))

        qss.append("QWidget>QToolButton{border-width:0px;}")
        qss.append("QWidget>QToolButton{background-color:{0};color:{1};}".format(normal_bg_color, normal_text_color))
        qss.append(
            "QWidget>QToolButton:hover,QWidget>QToolButton:pressed,QWidget>QToolButton:checked{background-color:{0};color:{1};}".format(
                dark_bg_color, dark_text_color))

        widget.setStyleSheet("".join(qss))

        for i in range(btnCount):
            # 存储对应按钮对象，方便鼠标移上去的时候切换图片
            pixNormal: PySide2.QtGui.QPixmap = self.getPixmap(QColor(normal_text_color), str(pix_char[i]), icon_size,
                                                              icon_width, icon_height)
            pixDark: PySide2.QtGui.QPixmap = self.getPixmap(QColor(dark_text_color), str(pix_char[i]), icon_size,
                                                            icon_width, icon_height)

            buttons[i].setIcon(QIcon(pixNormal))
            buttons[i].setIconSize(QSize(icon_width, icon_height))
            buttons[i].installEventFilter(self)

            self.btns.append(buttons[i])
            self.pix_normal.append(pixNormal)
            self.pix_dark.append(pixDark)

    # setStyleForNavPane

    def setStyleForNavButton(self, frame: PySide2.QtWidgets.QFrame,
                             buttons: List[PySide2.QtWidgets.QToolButton],
                             pix_char: List[int],
                             icon_size: int = 12,
                             icon_width: int = 15,
                             icon_height: int = 15,
                             normal_bg_color: str = "#2FC5A2",
                             dark_bg_color: str = "#3EA7E9",
                             normal_text_color: str = "EEEEEE",
                             dark_text_color: str = "FFFFFF"):
        """ 指定导航按钮样式，带图标和效果切换 """
        btnCount: int = len(buttons)
        charCount: int = len(pix_char)
        if btnCount <= 0 or charCount <= 0 or btnCount != charCount:
            return

        qss: List[str] = [
            "QFrame>QToolButton{border-style:none;border-width:0px;}",

            "QFrame>QToolButton{background-color:{0};color:{1};}".format(
                normal_bg_color, normal_text_color),

            "QFrame>QToolButton:hover,QFrame>QToolButton:pressed,QFrame>QToolButton:checked{background-color:{0};color:{1};}".format(
                dark_bg_color, dark_text_color)
        ]

        frame.setStyleSheet("".join(qss))

        for i in range(btnCount):
            # 存储对应按钮对象，方便鼠标移上去的时候切换图片
            pixNormal: QPixmap = self.getPixmap(QColor(normal_text_color), str(pix_char[i]), icon_size, icon_width, icon_height)
            pixDark: QPixmap = self.getPixmap(QColor(dark_text_color), str(pix_char[i]), icon_size, icon_width, icon_height)

            buttons[i].setIcon(QIcon(pixNormal))
            buttons[i].setIconSize(QSize(icon_width, icon_height))
            buttons[i].installEventFilter(self)

            self.btns.append(buttons[i])
            self.pix_normal.append(pixNormal)
            self.pix_dark.append(pixDark)

    # setStyleForNavButton

    def eventFilter(self, watched: PySide2.QtCore.QObject,
                    event: PySide2.QtCore.QEvent) -> bool:
        """ 事件过滤器 """
        if watched.inherits("QToolButton"):  # 这里会警告期望输入bytes实际输入str，应该是qt本身的问题，因为文档和实际运行都是str
            btn: QToolButton = watched
            index: int = self.btns.index(btn)
            if index >= 0:
                if event.type() == QEvent.Enter:
                    btn.setIcon(QIcon(self.pix_dark[index]))
                elif event.type() == QEvent.Leave:
                    if btn.isChecked():
                        btn.setIcon(QIcon(self.pix_dark[index]))
                    else:
                        btn.setIcon(QIcon(self.pix_normal[index]))
        return QObject.eventFilter(watched, event)

    # eventFilter


if __name__ == '__main__':
    def buttonClick1():
        print("hello world")

    import sys
    from PySide2.QtWidgets import QApplication
    app: QApplication = QApplication(sys.argv)
    A: IconHelper = IconHelper()
    B: IconHelper = IconHelper()
    print(id(A))
    print(id(B))
    b_icon_normal: QPixmap = A.getPixmap(QColor(100, 100, 100), '\uf061', 15, 15, 15)
    b_icon_hover: QPixmap = A.getPixmap(QColor(255, 255, 255), '\uf061', 15, 15, 15)
    b_icon_check: QPixmap = A.getPixmap(QColor(255, 255, 255), '\uf061', 15, 15, 15)

    from custom_widgets.navigation.navbutton.navbutton import NavButton
    b_btn: NavButton = NavButton()
    b_btn.setPaddingLeft(32)
    b_btn.setLineSpace(6)

    b_btn.setShowIcon(True)
    b_btn.setIconSpace(15)
    b_btn.setIconSize(QSize(15, 15))
    b_btn.setIconNormal(b_icon_normal)
    b_btn.setIconHover(b_icon_hover)
    b_btn.setIconCheck(b_icon_check)

    b_btn.setChecked(True)

    b_btn.clicked.connect(buttonClick1)
    b_btn.show()

    sys.exit(app.exec_())

