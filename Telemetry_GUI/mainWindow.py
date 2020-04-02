from PyQt5 import QtWidgets as Qtw
from PyQt5.QtGui import QColor, QPixmap, QPainter, QBrush, QPen
from PyQt5 import QtCore as Qt
from littleWidgets import LabeledValue
from parseSerial import Parser
from parseSerial import MessageID
import map_generator

class CinetiqueW(Qtw.QFrame):
    def __init__(self,prefix):
        super().__init__()
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)
        self.myLayout=Qtw.QVBoxLayout(self)
        self.setLayout(self.myLayout)
        self.widgets={prefix+"x":LabeledValue("x",0,self) , prefix+"y":LabeledValue("y",0,self) , prefix+"Th":LabeledValue("theta",0,self) , prefix+"v":LabeledValue("v",0,self) , prefix+"w":LabeledValue("w",0,self)}
        if prefix=="R":
            self.label_robot=Qtw.QLabel("Robot:")
            self.label_robot.setAlignment(Qt.Qt.AlignCenter)
            self.label_robot.setStyleSheet("QLabel {color:#E0FFFF; font-size:48px; font-style:bold;}")
            self.myLayout.addWidget(self.label_robot)
        else:
            self.label_ghost = Qtw.QLabel("Ghost:")
            self.label_ghost.setAlignment(Qt.Qt.AlignCenter)
            self.label_ghost.setStyleSheet("QLabel {color:#E0FFFF; font-size:48px; font-style:bold;}")
            self.myLayout.addWidget(self.label_ghost)
        for w in self.widgets.values():
            self.myLayout.addWidget(w)
    
    def update(self,newData : dict):
        for k,v in newData.items():
            if k in self.widgets.keys():
                self.widgets[k].setValue(v)

class Sequence(Qtw.QFrame):
    def __init__(self):
        super().__init__()
        self.i="0"
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)

        self.mainLayout=Qtw.QHBoxLayout(self)

        self.insideWidget=Qtw.QWidget(self)
        self.insideWidgetLayout=Qtw.QHBoxLayout(self)

        self.actions={}
        for i in range(500):
            self.actions.update({"A"+str(i):Qtw.QLabel("",self.insideWidget)})
            self.insideWidgetLayout.addWidget(self.actions["A"+str(i)])
            self.actions["A" + str(i)].setStyleSheet("QLabel: {border : 2px solid #E0FFFF;}")
            self.actions["A"+str(i)].setVisible(False)

        self.insideWidget.setLayout(self.insideWidgetLayout)

        self.mainLayout.addWidget(self.insideWidget)
        self.setLayout(self.mainLayout)

    
    def update(self,newData : dict):
        if "i" in newData.keys():
            self.i=newData["i"]
        for k,v in newData.items():
            if k[0]=="A":
                self.actions[k].setText(v)
                self.actions[k].setAlignment(Qt.Qt.AlignCenter)
                self.actions[k].setVisible(True)
                self.actions[k].setStyleSheet("QLabel {border:2px solid #555555;"
                                              "color: #E0FFFF;}")

            if k[0]=="F":
                k_= "A"+k[1]
                if v=="1": #fail
                    self.actions[k_].setStyleSheet("QLabel {border:2px solid #FF0000;"
                                              "color: #FF0000;}")

        if self.actions["A"+self.i].isVisible():
            self.actions["A"+self.i].setStyleSheet("QLabel {border : 2px solid #2CF007;}")

class map(Qtw.QFrame): # Pour  affichage de la carte
    def __init__(self):
        super().__init__()
        self.X_R = 0.0
        self.Y_R = 0.0
        self.Th_R = 0.0
        self.X_G = 0.0
        self.Y_G = 0.0
        self.Th_G = 0.0
        self.State = 0
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)
        self.myLayout = Qtw.QHBoxLayout(self)
        self.label_map = Qtw.QLabel()
        self.myLayout.addWidget(self.label_map)
        self.setLayout(self.myLayout)
        pixmap = QPixmap("map_generated.png")
        self.label_map.setPixmap(pixmap)
        self.label_map.setAlignment(Qt.Qt.AlignCenter)

    def update(self, newData: dict): # Ce qui marche probablement pas (Mais je suis sur que tu maurais donne plus de temps jaurais reussi CONNARD)
        for k, v in newData.items():
            if k[0]=="R":
                if k[1]=="x":
                    self.X_R = float(v)
                    print(self.X_R)
                if k[1]=="y":
                    self.Y_R = float(v)
                    print(self.Y_R)
                if k[1]=="T":
                    self.Th_R = float(v)
                    print(self.Th_R)
            if k[0]=="G":
                if k[1] == "x":
                    self.X_G = float(v)
                if k[1] == "y":
                    self.Y_G = float(v)
                if k[1] == "T":
                    self.Th_G = float(v)
        map_generator.gen_map(self.X_R,self.Y_R,self.Th_R,self.X_G,self.Y_G,self.Th_G,self.State)
        pixmap = QPixmap("map_generated.png")
        self.label_map.setPixmap(pixmap)
        self.label_map.setAlignment(Qt.Qt.AlignCenter)

class MySwitch_R_G(Qtw.QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)

    def paintEvent(self, event):
        label = "R" if self.isChecked() else "G"
        bg_color = Qt.Qt.green if self.isChecked() else Qt.Qt.cyan

        radius = 10
        width = 32
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(170,170,170))

        pen = QPen(Qt.Qt.white)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(Qt.QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QBrush(bg_color))
        sw_rect = Qt.QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.Qt.AlignCenter, label)

class MySwitch_2(Qtw.QPushButton):
    def __init__(self):
        super().__init__()
        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)

    def paintEvent(self, event):
        label = "2" if self.isChecked() else "1"
        bg_color = Qt.Qt.green if self.isChecked() else Qt.Qt.cyan

        radius = 10
        width = 32
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(170,170,170))

        pen = QPen(Qt.Qt.white)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(Qt.QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QBrush(bg_color))
        sw_rect = Qt.QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.Qt.AlignCenter, label)

class State_settings(Qtw.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)
        self.myLayout = Qtw.QHBoxLayout(self)
        self.check_one_two = MySwitch_2()
        self.myLayout.addWidget(self.check_one_two)
        self.check_robot_ghost = MySwitch_R_G()
        self.myLayout.addWidget(self.check_robot_ghost)

        self.check_one_two.clicked.connect(self.statebutton)
        self.check_robot_ghost.clicked.connect(self.statebutton)

    def statebutton(self):
        if self.check_one_two.isChecked():
            self.State=2
        else:
            if self.check_robot_ghost.isChecked():
                self.State=1
            else:
                self.State=0


class Comm(Qtw.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)
        self.myLayout=Qtw.QHBoxLayout(self)
        self.lab=Qtw.QLabel("Last Message ID : ")
        self.lab.setAlignment(Qt.Qt.AlignCenter)
        self.lab.setStyleSheet("QLabel {border : 2px solid #2CF007;}")
        self.myLayout.addWidget(self.lab, 1)
        self.mess=Qtw.QLabel("")
        self.mess.setAlignment(Qt.Qt.AlignCenter)
        self.mess.setStyleSheet("QLabel {border : 2px solid #E0FFFF;}")
        self.myLayout.addWidget(self.mess, 3)

    def update(self,newData : dict):
        for k,v in newData.items():
            if k=="mess":
                self.mess.setText(v)

class PidUnit(Qtw.QFrame):
    def __init__(self,translation,which,mainWindowMessageSignal):
        super().__init__()
        self.translation=translation
        self.which=which
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)

        self.myLayout=Qtw.QVBoxLayout(self)
        self.setLayout(self.myLayout)
        self.btnUp=Qtw.QPushButton("++")
        self.lab=Qtw.QLabel("P")
        if which==1:
            self.lab=Qtw.QLabel("I")
        elif which==2:
            self.lab=Qtw.QLabel("D")

        self.btnDown=Qtw.QPushButton("--")
        self.myLayout.addWidget(self.btnUp)
        self.myLayout.addWidget(self.lab)
        self.myLayout.addWidget(self.btnDown)
        self.btnUp.clicked.connect(lambda : mainWindowMessageSignal.emit(MessageID.PID_tweak_M,1,translation,which,0))
        self.btnDown.clicked.connect(lambda : mainWindowMessageSignal.emit(MessageID.PID_tweak_M,0,translation,which,0))

class PidGroup(Qtw.QFrame):
    def __init__(self,translation,mainWindowMessageSignal):
        super().__init__()
        self.translation=translation
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)
        self.myLayout=Qtw.QVBoxLayout(self)
        self.setLayout(self.myLayout)
        if translation:
            self.label=Qtw.QLabel("TRANSLATION")
        else:
            self.label=Qtw.QLabel("ROTATION")
        self.myLayout.addWidget(self.label)

        self.group=Qtw.QWidget(self)
        self.layoutGroup=Qtw.QHBoxLayout(self.group)
        self.group.setLayout(self.layoutGroup)
        self.pWidget=PidUnit(translation,0,mainWindowMessageSignal)
        self.layoutGroup.addWidget(self.pWidget)
        self.iWidget=PidUnit(translation,1,mainWindowMessageSignal)
        self.layoutGroup.addWidget(self.iWidget)
        self.dWidget=PidUnit(translation,2,mainWindowMessageSignal)
        self.layoutGroup.addWidget(self.dWidget)
        self.myLayout.addWidget(self.group)

class PidPanel(Qtw.QFrame):
    def __init__(self,mainWindowMessageSignal):
        super().__init__()
        self.setFrameShadow(Qtw.QFrame.Plain)
        self.setFrameShape(Qtw.QFrame.StyledPanel)
        self.myLayout=Qtw.QHBoxLayout(self)
        self.setLayout(self.myLayout)
        self.translationGroup=PidGroup(True,mainWindowMessageSignal)
        self.myLayout.addWidget(self.translationGroup)
        self.rotationGroup=PidGroup(False,mainWindowMessageSignal)
        self.myLayout.addWidget(self.rotationGroup)



class MainWindow(Qtw.QWidget):
    sendMessage=Qt.pyqtSignal(MessageID,int,int,int,int)
    def __init__(self):
        super().__init__()
        self.setStyleSheet(open("./design_GUI.css").read())
        self.mainLayout=Qtw.QGridLayout(self)
        self.setLayout(self.mainLayout)

        self.label_title=Qtw.QLabel("ENSMASTEEL INTERFACE")
        self.label_title.setStyleSheet("QLabel {color : #E0FFFF;"
                                       "font-family : Segoe UI; font-size: 78px;"
                                       "text-align : center;}")
        self.label_title.setAlignment(Qt.Qt.AlignCenter)

        self.buttonTirette = Qtw.QPushButton('START SIMULATION', self)
        self.buttonTirette.clicked.connect(lambda : self.sendMessage.emit(MessageID.Tirette,0,0,0,0))

        self.mapWidget=map()
        self.cinetiqueR=CinetiqueW("R")
        self.cinetiqueR.setObjectName('cinetiqueR') # Pour utilisation dans le css
        self.cinetiqueG=CinetiqueW("G")
        self.cinetiqueG.setObjectName('cinetiqueG') # Idem
        self.sequenceWidget=Sequence()
        self.commWidget=Comm()
        self.pidPanel=PidPanel(self.sendMessage)
        self.stateSetting=State_settings()

        self.mainLayout.addWidget(self.label_title,1,0,1,6)
        self.mainLayout.addWidget(self.buttonTirette,2,0,1,3)
        self.mainLayout.addWidget(self.stateSetting,2,3,1,1)
        self.mainLayout.addWidget(self.mapWidget,3,0,4,4)
        self.mainLayout.addWidget(self.cinetiqueR,2,4,5,1)
        self.mainLayout.addWidget(self.cinetiqueG,2,5,5,1)
        self.mainLayout.addWidget(self.sequenceWidget,8,0,1,6)
        self.mainLayout.addWidget(self.commWidget,9,0,1,6)

        self.parserThread=Parser(self)
        self.parserThread.newTelem.connect(self.cinetiqueR.update)
        self.parserThread.newTelem.connect(self.cinetiqueG.update)
        self.parserThread.newTelem.connect(self.mapWidget.update)
        self.parserThread.newTelem.connect(self.sequenceWidget.update)
        self.parserThread.newTelem.connect(self.commWidget.update)
        self.parserThread.newInfo.connect(print)
        self.parserThread.newDebug.connect(print)
        
        self.parserThread.start()
