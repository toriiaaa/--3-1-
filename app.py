import sys

from PyQt6.QtWidgets import QApplication, QWidget

from window.main import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
app.aboutToQuit.connect(window.push_exit)

