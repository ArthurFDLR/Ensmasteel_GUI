from mainWindow import MainWindow
from PyQt5 import QtCore,QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
mainWin = QtWidgets.QMainWindow()
mainWin.setStyleSheet("QMainWindow {background-color : #333333; border : 5px solid #555555}") # css applique directement sur la fenetre
mainWid = MainWindow()
mainWin.setCentralWidget(mainWid)
mainWin.showMaximized() # Mettre l'application en plein écran (tout en conservant l'accès à la fermeture windows)
mainWin.show()
sys.exit(app.exec_())