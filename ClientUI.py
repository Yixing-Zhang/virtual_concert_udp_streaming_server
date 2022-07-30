import sys
from PyQt5.QtWidgets import *
import RegistrationClient


class ClientUI(QDialog):
    def __init__(self, parent=None):
        super(ClientUI, self).__init__(parent)
        layout = QVBoxLayout()
        self.resize(500, 200)
        self.setWindowTitle("Registration Client")

        self.client = RegistrationClient.RegistrationClient()
        self.client.Start()

        self.btn1 = QPushButton("Terminate")
        self.btn1.clicked.connect(lambda: self.whichBtn(self.btn1))
        layout.addWidget(self.btn1)

        self.setLayout(layout)

    def whichBtn(self, btn):
        if btn.text() == 'Terminate':
            self.client.Terminate()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    btnDemo = ClientUI()
    btnDemo.show()
    sys.exit(app.exec_())
