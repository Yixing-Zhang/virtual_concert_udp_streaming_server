import sys
from PyQt5.QtWidgets import *
import ForwardServer


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        layout = QVBoxLayout()
        self.resize(500, 200)
        self.setWindowTitle("Sever")

        self.server = ForwardServer.ForwardServer()
        self.server.Start()

        self.btn1 = QPushButton("Terminate")
        self.btn1.clicked.connect(lambda: self.whichBtn(self.btn1))
        layout.addWidget(self.btn1)

        self.setLayout(layout)

    def whichBtn(self, btn):
        if btn.text() == 'Terminate':
            self.server.Terminate()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    btnDemo = Form()
    btnDemo.show()
    sys.exit(app.exec_())
