from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel

from custom_widgets.color.colorbutton import ColorButton
from custom_widgets.color.colorpanelbar import ColorPanelBar
from custom_widgets.color.colorpanelbtn import ColorPanelBtn
from custom_widgets.color.colorpanelfader import ColorPanelFader
from custom_widgets.color.colorpanelhsb import ColorPanelHSB


class ColorPanel(QWidget):
    """
    颜色面板柱状条
    作者:feiyangqingyun(QQ:517216493) 2017-11-21
    译者:sunchuquin(QQ:1715216365) 2021-07-04
    """

    def __init__(self, parent: QWidget = None):
        super(ColorPanel, self).__init__(parent)
        self.resize(650, 450)

        g_layout = QVBoxLayout()

        self.stackedWidget = QStackedWidget()
        self.pageFader = QWidget()
        layout = QVBoxLayout()
        self.colorPanelFader = ColorPanelFader()
        layout.addWidget(self.colorPanelFader)
        layout.setContentsMargins(0, 0, 0, 0)
        self.pageFader.setLayout(layout)
        self.pageHSB = QWidget()
        layout = QHBoxLayout()
        self.colorPanelHSB = ColorPanelHSB()
        self.colorPanelBar = ColorPanelBar()
        self.colorPanelBar.setMinimumWidth(60)
        self.colorPanelBar.setMaximumWidth(60)
        layout.addWidget(self.colorPanelHSB)
        layout.addWidget(self.colorPanelBar)
        layout.setContentsMargins(0, 0, 0, 0)
        self.pageHSB.setLayout(layout)
        self.pageBtn = QWidget()
        layout = QVBoxLayout()
        self.colorPanelBtn = ColorPanelBtn()
        layout.addWidget(self.colorPanelBtn)
        layout.setContentsMargins(0, 0, 0, 0)
        self.pageBtn.setLayout(layout)
        self.stackedWidget.addWidget(self.pageFader)
        self.stackedWidget.addWidget(self.pageHSB)
        self.stackedWidget.addWidget(self.pageBtn)
        g_layout.addWidget(self.stackedWidget)

        self.widgetColor = QWidget()
        self.btnHue = ColorButton()
        self.btnSat = ColorButton()
        self.btnBright = ColorButton()
        self.btnCyan = ColorButton()
        self.btnMagenta = ColorButton()
        self.btnYellow = ColorButton()
        self.btnRed = ColorButton()
        self.btnGreen = ColorButton()
        self.btnBlue = ColorButton()
        self.widgetColor.setMinimumHeight(45)
        self.widgetColor.setMaximumHeight(45)
        layout = QHBoxLayout()
        layout.addWidget(self.btnHue)
        layout.addWidget(self.btnSat)
        layout.addWidget(self.btnBright)
        layout.addWidget(self.btnCyan)
        layout.addWidget(self.btnMagenta)
        layout.addWidget(self.btnYellow)
        layout.addWidget(self.btnRed)
        layout.addWidget(self.btnGreen)
        layout.addWidget(self.btnBlue)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        self.widgetColor.setLayout(layout)
        g_layout.addWidget(self.widgetColor)

        self.widgetPanel = QWidget()
        layout = QHBoxLayout()
        self.btnPanelFader = ColorButton()
        self.btnPanelHSB = ColorButton()
        self.btnPanelBtn = ColorButton()
        self.labColor = QLabel()
        self.labColor.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.btnPanelFader)
        layout.addWidget(self.btnPanelHSB)
        layout.addWidget(self.btnPanelBtn)
        layout.addWidget(self.labColor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        self.widgetPanel.setLayout(layout)
        g_layout.addWidget(self.widgetPanel)
        self.setLayout(g_layout)

        self.initForm()

    def initForm(self) -> None:
        self.btnHue.borderColor = QColor(Qt.darkGray)
        self.btnSat.borderColor = QColor(Qt.darkGray)
        self.btnBright.borderColor = QColor(Qt.darkGray)
        self.btnHue.normalColor = QColor(Qt.darkGray).light(20)
        self.btnSat.normalColor = QColor(Qt.darkGray).light(20)
        self.btnBright.normalColor = QColor(Qt.darkGray).light(20)

        self.btnCyan.borderColor = QColor(Qt.cyan)
        self.btnMagenta.borderColor = QColor(Qt.magenta)
        self.btnYellow.borderColor = QColor(Qt.yellow)
        self.btnCyan.normalColor = QColor(Qt.cyan).light(50)
        self.btnMagenta.normalColor = QColor(Qt.magenta).light(50)
        self.btnYellow.normalColor = QColor(Qt.yellow).light(50)

        self.btnRed.borderColor = QColor(Qt.red)
        self.btnGreen.borderColor = QColor(Qt.green)
        self.btnBlue.borderColor = QColor(Qt.blue)
        self.btnRed.normalColor = QColor(Qt.red).light(50)
        self.btnGreen.normalColor = QColor(Qt.green).light(50)
        self.btnBlue.normalColor = QColor(Qt.blue).light(50)

        self.btnPanelFader.text = "颜色滑块面板"
        self.btnPanelHSB.text = "颜色选取面板"
        self.btnPanelBtn.text = "颜色按钮面板"

        self.btnPanelFader.normalColor = QColor("#16A085")
        self.btnPanelHSB.normalColor = QColor("#C0392B")
        self.btnPanelBtn.normalColor = QColor("#27AE60")

        font: QFont = QFont()
        font.setPixelSize(15)
        font.setBold(True)
        self.btnPanelFader.textFont = font
        self.btnPanelHSB.textFont = font
        self.btnPanelBtn.textFont = font

        self.colorPanelFader.colorChanged.connect(self.colorChangedFader)
        self.colorPanelHSB.colorChanged.connect(self.colorChangedHSB)
        self.colorPanelBar.colorChanged.connect(self.colorChangedBar)
        self.colorPanelBtn.colorChanged.connect(self.colorChangedBtn)

        self.widgetColor.setEnabled(False)
        self.stackedWidget.setCurrentIndex(0)
        self.colorPanelBar.staticMode = False
        self.colorChangedBar(QColor(Qt.red), 0, 100)

        self.btnPanelFader.clicked.connect(self.buttonClicked)
        self.btnPanelHSB.clicked.connect(self.buttonClicked)
        self.btnPanelBtn.clicked.connect(self.buttonClicked)

    def colorChangedFader(self, color: QColor, hue: float, sat: float, bright: float) -> None:
        self.btnHue.text = "Hue\n%0.1f" % round(hue, 1)
        self.btnSat.text = "Sat\n%0.1f" % round(sat, 1)
        self.btnBright.text = "Bright\n%0.1f" % round(bright, 1)

        self.setColor(color)

    def colorChangedHSB(self, color: QColor, hue: float, sat: float) -> None:
        self.colorPanelBar.topColor = color
        self.colorPanelBar.borderColor = color

        self.btnHue.text = "Hue\n%0.1f" % round(hue, 1)
        self.btnSat.text = "Sat\n%0.1f" % round(sat, 1)
        self.btnBright.text = "Bright\n%0.1f" % round(self.colorPanelBar.percent, 1)

        c: QColor = QColor.fromHsvF(hue / 360, sat / 100, self.colorPanelBar.percent / 100)
        self.setColor(c)

    def colorChangedBar(self, color: QColor, value: float, percent: float) -> None:
        if self.colorPanelHSB.isVisible():
            self.colorPanelHSB.percent = percent

        hue: float = color.hue()
        hue = 360 if hue < 0 else hue
        sat: float = color.saturationF() * 100

        if not self.colorPanelBar.isVisible():
            self.btnHue.text = "Hue\n%0.1f" % round(hue, 1)
            self.btnSat.text = "Sat\n%0.1f" % round(sat, 1)

        self.btnBright.text = "Bright\n%0.1f" % round(percent, 1)

        self.setColor(color)

    def colorChangedBtn(self, color: QColor) -> None:
        self.colorChangedBar(color, 0, 100)

    def setColor(self, color: QColor) -> None:
        # 根据背景色自动计算合适的前景色
        gray: float = (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
        textColor: QColor = QColor(Qt.black) if gray > 0.5 else QColor(Qt.white)
        self.labColor.setText(color.name().upper())
        self.labColor.setStyleSheet("QLabel{font:25px;color:%s;background:%s;}" % (textColor.name(), color.name()))

        percentRed: float = color.redF() * 100
        percentGreen: float = color.greenF() * 100
        percentBlue: float = color.blueF() * 100

        self.btnCyan.text = "Cyan\n%0.1f%%" % round(100 - percentRed, 1)
        self.btnMagenta.text = "Magenta\n%0.1f%%" % round(100 - percentGreen, 1)
        self.btnYellow.text = "Yellow\n%0.1f%%" % round(100 - percentBlue, 1)

        self.btnRed.text = "Red\n%0.1f%%" % round(percentRed, 1)
        self.btnGreen.text = "Green\n%0.1f%%" % round(percentGreen, 1)
        self.btnBlue.text = "Blue\n%0.1f%%" % round(percentBlue, 1)

    def buttonClicked(self) -> None:
        btn: ColorButton = self.sender()
        if btn == self.btnPanelFader:
            self.stackedWidget.setCurrentIndex(0)
        elif btn == self.btnPanelHSB:
            self.stackedWidget.setCurrentIndex(1)
        elif btn == self.btnPanelBtn:
            self.stackedWidget.setCurrentIndex(2)


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QTextCodec
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    app.setFont(QFont("Microsoft Yahei", 9))
    codec: QTextCodec = QTextCodec.codecForName(b"utf-8")
    QTextCodec.setCodecForLocale(codec)
    window = ColorPanel()
    window.setWindowTitle("颜色面板控件集合")
    window.show()
    sys.exit(app.exec_())
