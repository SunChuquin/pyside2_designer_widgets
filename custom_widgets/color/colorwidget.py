from PySide2.QtCore import QObject, QTimer, Qt, QSize
from PySide2.QtGui import QClipboard, QMouseEvent, QFont, QCursor, QScreen, QPixmap, QImage, QColor
from PySide2.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QFrame, QApplication


class Singleton(type(QObject), type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ColorWidget(QWidget, metaclass=Singleton):
    """
    屏幕拾色器
    作者:feiyangqingyun(QQ:517216493) 2019-10-07
    译者:sunchuquin(QQ:1715216365) 2021-07-04
    """

    def __init__(self, parent: QWidget = None):
        super(ColorWidget, self).__init__(parent)
        self.cp: QClipboard = QClipboard()
        self.pressed: bool = False
        self.timer: QTimer = QTimer()

        self.gridLayout: QGridLayout = QGridLayout(self)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout: QVBoxLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)

        self.labColor: QLabel = QLabel()
        self.labColor.setText('+')
        self.labColor.setStyleSheet("background-color: rgb(255, 107, 107);color: rgb(250, 250, 250);")
        self.labColor.setAlignment(Qt.AlignCenter)
        font: QFont = QFont()
        font.setPixelSize(35)
        font.setBold(True)
        self.labColor.setFont(font)
        sizePolicy: QSizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labColor.sizePolicy().hasHeightForWidth())
        self.labColor.setSizePolicy(sizePolicy)
        self.labColor.setMinimumSize(QSize(80, 70))
        self.labColor.setMaximumSize(QSize(80, 70))
        self.labColor.setCursor(QCursor(Qt.CrossCursor))
        self.labColor.setFrameShape(QFrame.StyledPanel)
        self.labColor.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.labColor)

        self.label: QLabel = QLabel(self)
        self.label.setMinimumSize(QSize(0, 18))
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);color: rgb(200, 200, 200);")
        self.label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 3, 1)

        self.labWeb: QLabel = QLabel(self)
        self.gridLayout.addWidget(self.labWeb, 0, 1, 1, 1)

        self.txtWeb: QLineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.txtWeb, 0, 2, 1, 1)

        self.labRgb: QLabel = QLabel(self)
        self.gridLayout.addWidget(self.labRgb, 1, 1, 1, 1)

        self.txtRgb: QLineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.txtRgb, 1, 2, 1, 1)

        self.labPoint: QLabel = QLabel(self)
        self.gridLayout.addWidget(self.labPoint, 2, 1, 1, 1)

        self.txtPoint: QLineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.txtPoint, 2, 2, 1, 1)

        self.label.setText('当前颜色显示')
        self.labWeb.setText('web值: ')
        self.labRgb.setText('rgb值: ')
        self.labPoint.setText('坐标值: ')

        self.setLayout(self.gridLayout)
        self.setWindowTitle('屏幕拾色器')
        self.setFixedSize(270, 108)

        self.cp = QApplication.clipboard()
        self.pressed = False

        timer = QTimer(self)
        timer.setInterval(100)
        timer.timeout.connect(self.showColorValue)
        timer.start()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.labColor.rect().contains(event.pos()): return
        self.pressed = True

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.pressed = False

    def showColorValue(self) -> None:
        if not self.pressed: return

        x: int = QCursor.pos().x()
        y: int = QCursor.pos().y()
        self.txtPoint.setText("x:%d  y:%d" % (x, y))

        screen: QScreen = QApplication.primaryScreen()
        pixmap: QPixmap = screen.grabWindow(QApplication.desktop().winId(), x, y, 2, 2)

        red: int = 0
        green: int = 0
        blue: int = 0
        strDecimalValue: str = ''
        strHex: str = ''
        if not pixmap.isNull():
            image: QImage = pixmap.toImage()
            if not image.isNull():
                if image.valid(0, 0):
                    color: QColor = QColor(image.pixel(0, 0))
                    red = color.red()
                    green = color.green()
                    blue = color.blue()

                    strDecimalValue = "%d, %d, %d" % (red, green, blue)
                    strHex = "#%02X%02X%02X" % (red, green, blue)

        # 根据背景色自动计算合适的前景色
        color: QColor = QColor(red, green, blue)
        gray: float = (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
        textColor: QColor = QColor(Qt.black) if gray > 0.5 else QColor(Qt.white)

        value = "background:rgb(%s);color:%s" % (strDecimalValue, textColor.name())
        self.labColor.setStyleSheet(value)
        self.txtRgb.setText(strDecimalValue)
        self.txtWeb.setText(strHex)


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)

    window = ColorWidget()
    window.show()
    sys.exit(app.exec_())

