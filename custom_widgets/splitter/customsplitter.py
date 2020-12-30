from PySide2.QtWidgets import QApplication, QWidget, QSplitter, QTextEdit, QVBoxLayout, QToolButton
from PySide2.QtCore import Qt

class CustomSplitter(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.splitter = QSplitter(self)
        self.splitter.addWidget(QTextEdit(self))
        self.splitter.addWidget(QTextEdit(self))
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)
        handle = self.splitter.handle(1)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        button = QToolButton(handle)
        button.setArrowType(Qt.LeftArrow)
        button.clicked.connect(
            lambda: self.handleSplitterButton(True))
        layout.addWidget(button)
        button = QToolButton(handle)
        button.setArrowType(Qt.RightArrow)
        button.clicked.connect(
            lambda: self.handleSplitterButton(False))
        layout.addWidget(button)
        handle.setLayout(layout)

    def handleSplitterButton(self, left=True):
        if not all(self.splitter.sizes()):
            self.splitter.setSizes([1, 1])
        elif left:
            self.splitter.setSizes([0, 1])
        else:
            self.splitter.setSizes([1, 0])


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = CustomSplitter()
    window.setGeometry(500, 300, 300, 300)
    window.show()
    sys.exit(app.exec_())
