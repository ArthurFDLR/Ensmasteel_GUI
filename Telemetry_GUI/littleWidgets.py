from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore as Qt


class LabeledValue(Qtw.QFrame):
    def __init__(self,name,value,parent=None):
        super().__init__(parent)
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)
        self.myLayout=Qtw.QHBoxLayout(self)
        self.setLayout(self.myLayout)
        self.labelName=Qtw.QLabel(name,self)
        self.labelName.setAlignment(Qt.Qt.AlignCenter)
        self.labelName.setStyleSheet("QLabel {font-family : Segoe UI; font-size : 24px;}")
        self.myLayout.addWidget(self.labelName)
        self.labelValue=Qtw.QLabel(str(value),self)
        self.labelValue.setAlignment(Qt.Qt.AlignCenter)
        self.labelValue.setStyleSheet("QLabel {font-family : Segoe UI; font-size : 24px;}")
        self.myLayout.addWidget(self.labelValue)
    
    def setValue(self,value):
        self.labelValue.setText(value)