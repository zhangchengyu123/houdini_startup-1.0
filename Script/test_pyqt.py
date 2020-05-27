#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import getpass
from pathlib import Path
import subprocess
import pathconfig
import glob
import PyQt5.sip








scriptRoot = sys.path[0]
project_root = Path(r"E:\houdini_pip\Project").as_posix()
cmd = Path(r"E:\houdini_pip\v01\Enviroment\run_houdini").as_posix()


version ="1.0"

sec=0
class WorkThread(QThread):
    timer = pyqtSignal()
    end = pyqtSignal()

    def run(self):
        while True:
            self.sleep(1)
            if sec == 2:
                self.end.emit()
                break

            self.timer.emit()



class MainWindow(QMainWindow):


    def __init__(self):
        ## INIT ##
        super(MainWindow,self).__init__()
        self.initUI()
        self.TrayIcon()
        self.loadSetting()




    def TrayIcon(self):
        self.tp = QSystemTrayIcon(self)
        icon = QIcon(r"E:\ns_startup-master\Icons\octaneIcon.png")
        self.tp.setIcon(icon)
        main_Menu = QMenu()
        addction = QAction("Cancel", self.tp, triggered=self.close)
        main_Menu.addAction(addction)
        self.tp.setContextMenu(main_Menu)
        self.tp.activated.connect(self.trayclick)
        self.tp.setToolTip("landy_startup")
        self.tp.show()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)




    def trayclick(self,reason):
        if reason in (QSystemTrayIcon.Trigger,QSystemTrayIcon.DoubleClick):
            self.showNormal()



    def storeSetting(self):
        settings = QSettings("../template.ini", QSettings.IniFormat)
        if settings  is not None:
            settings.clear()
        i=0
        for qbox in self.qboxcount:
            i+=1
            name="qbox"+str(i)
            settings.setValue(f"{name}",qbox.currentText())

    def loadSetting(self):
        settings = QSettings("../template.ini", QSettings.IniFormat)
        i=0
        for qbox in self.qboxcount:
            i+=1
            name="qbox"+str(i)
            result = settings.value(f"{name}",qbox.currentText())
            qbox.setCurrentText(result)


    def initUI(self):
        cell_Widget=QWidget()
        self.setWindowTitle("Landy_Startup " + version)
        img=QPixmap(r"E:\ns_startup-master\Icons\a.png").scaled(int(20),int(20))
        self.setWindowIcon(QIcon(img))
        self.resolution = QDesktopWidget().screenGeometry()
        self.move(self.resolution.width() - 473, self.resolution.height() - 980)

        palette1 = QPalette()
        palette1.setColor(palette1.Background,QColor(80,80,80))
        self.setPalette(palette1)
        #============================================================================================================



        self.ComboBox()
        title = QLabel("Project:")
        episodes = QLabel("Episodes:")
        shot = QLabel("Shot:")
        Dept= QLabel("Dept:")
        Element = QLabel("Element:")


        self.grp_box = QGroupBox("start_up", self)
        layout  = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout3 = QHBoxLayout()





        hlayout.addWidget(title)
        hlayout.addWidget(self.cb,Qt.AlignJustify)
        hlayout.addWidget(episodes)
        hlayout.addWidget(self.cb2,Qt.AlignJustify)
        hlayout.addWidget(shot)
        hlayout.addWidget(self.cb3,Qt.AlignJustify)
        hlayout.addWidget(Dept)
        hlayout.addWidget(self.cb4,Qt.AlignJustify)
        hlayout.addWidget(Element)
        hlayout.addWidget(self.cb5,Qt.AlignJustify)


        self.grp_box.setLayout(hlayout)
        layout.addWidget(self.grp_box)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(1)
        self.textEdit.setPlaceholderText("Here display the information for houdini environment")
        self.textEdit.setFontWeight(300)
        self.textEdit.setFont(QFont("Microsoft YaHei"))
        #self.scrollbar = QScrollBar()
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.textEdit.setMaximumHeight(200)


        #self.scrollbar.setMaximum(3)


        hlayout2.addWidget(self.textEdit)




        qss ='''QTextEdit{
        background:rgba(60,60,60,255);
        border-radius:4px;
        color:white       
        }'''
        self.textEdit.setStyleSheet(qss)

        button  = QPushButton("Open Houdini")
        preset_bnt  = QPushButton("set_template")
        dir_bnt   = QPushButton("openFile")

        hlayout3.addStretch(1)
        hlayout3.addWidget(button)
        hlayout3.addWidget(preset_bnt)
        hlayout3.addWidget(dir_bnt)
        cell_Widget.setStyleSheet("""
        QPushButton{
        color: rgb(255 ,255 ,255);
        background-color: rgb(50, 50, 50);
        border-radius: 3px;
        border: 1px solid rgb(40, 40, 40);
        padding:5px 20px
        }

        QPushButton:hover {
        background-color: rgb(155, 155, 155);
        }

        QPushButton:pressed {
        background-color: rgb(80, 80, 80);
        }
        
        QComboBox{
        color: rgb(180 ,180 ,180);
        background-color: rgb(50, 50, 50);
        border: 1px solid rgb(40, 40, 40);
        padding:1px 20px
        }
        
        QComboBox QAbstractItemView
        {
             border: 1px solid rgb(161,161,161);
             background-color: rgb(50, 50, 50);
        }
         
        QComboBox QAbstractItemView::item
        {
            height: 15px;
        }
         
        QComboBox QAbstractItemView::item:selected
        {	
            background-color: rgba(54, 98, 180);
        }
        
        QComboBox QScrollBar::vertical{
            background-color: rgb(50, 50, 50);
         }
        
        

        """)












        layout.addLayout(hlayout2)
        layout.addLayout(hlayout3)



        cell_Widget.setLayout(layout)
        self.local_file = Path(__file__).parent / Path("text.txt")


        self.setCentralWidget(cell_Widget)
        self.worker = WorkThread()

#====================================================================================================================
        preset_bnt.clicked.connect(self.storeSetting)
        button.clicked.connect(self.start)
        dir_bnt.clicked.connect(self.openFile)


        self.worker.timer.connect(self.add)
        self.worker.end.connect(self.set_variable)


    def openFile(self):
        root = Path(project_root)/Path(self.context)

        path = "{}/Episodes/{}/{}/work/{}/{}".format(root, self.context1, self.context2, self.context3, self.context4)

        while True:
            if Path(path).exists():
                os.startfile(path)
                break
            else:
                path = Path(path).parent



            #message=QMessageBox()
            #message.information(self,"error","sorry current dir is not exist",QMessageBox.Cancel)

    def start(self):
        self.worker.start()

    def add(self):
        global  sec
        sec += 1
        if sec <2:
            root = Path(project_root)/Path(self.context)
            path = "{}/Episodes/{}/{}/work/{}/{}".format(root,self.context1,self.context2,self.context3,self.context4)
            while True:
                parent_dir = Path(path).parent
                if Path(path).exists():
                    result = Path(path)
                    break
                else:
                    path = parent_dir

            if self.local_file.exists:
                if not Path(result).exists():
                    subprocess.Popen(cmd,shell=True)
                else:
                    os.chdir(Path(result))
                    subprocess.Popen(cmd,shell=True)


    def set_variable(self):
        if self.textEdit.isReadOnly() is True:
            self.textEdit.setReadOnly(0)

        with open(self.local_file,"r") as r:
            infor = r.read()
            r.close()
            self.textEdit.setPlainText(infor)
        global sec
        sec = 0
        self.textEdit.setReadOnly(1)



#===================================================== QComboBox widget and signal===================================
    def ComboBox(self):

        files = os.listdir(project_root)
        list =["None"]
        for file in files:
            if os.path.isdir(Path(project_root)/Path(file)) is True and file != "Lib":
                list.append(file)

        self.cb  = QComboBox()
        self.cb2 = QComboBox()
        self.cb3 = QComboBox()
        self.cb4 = QComboBox()
        self.cb5 = QComboBox()


        self.qboxcount = [
            self.cb,
            self.cb2,
            self.cb3,
            self.cb4,
            self.cb5
            ]

        self.cb.addItems(list)
        self.cb2.addItem("None")
        self.cb3.addItem("None")
        self.cb4.addItem("None")
        self.cb5.addItem("None")
        pathconfig.set_Scrollbar(self.cb,5)









#====================================================================================

        self.cb.currentIndexChanged.connect(self.episode_text)
        self.cb2.currentIndexChanged.connect(self.shot_text)
        self.cb3.currentTextChanged.connect(self.dept_text)
        self.cb4.currentTextChanged.connect(self.element_text)
        self.cb5.currentTextChanged.connect(self.final_text)






    def episode_text(self):
        list=pathconfig.QcomboxConset(self.cb,project_root,"Episodes")
        self.root = list[1]
        self.context = self.cb.currentText()

        pathconfig.addText(list[0], list[2], self.cb2)
    def shot_text(self):
        list=pathconfig.QcomboxConset(self.cb2,self.root)
        self.root1 = list[1]
        self.context1 = self.cb2.currentText()
        pathconfig.addText(list[0], list[2], self.cb3)

    def dept_text(self):
        list=pathconfig.QcomboxConset(self.cb3,self.root1,"work")
        self.root2 = list[1]
        self.context2=self.cb3.currentText()
        pathconfig.addText(list[0], list[2], self.cb4)

    def element_text(self):
        list=pathconfig.QcomboxConset(self.cb4,self.root2)
        self.root3 = list[1]
        self.context3 = self.cb4.currentText()
        pathconfig.addText(list[0], list[2], self.cb5)

    def final_text(self):
        self.context4 = self.cb5.currentText()
        self.final_root = Path(os.path.join(self.root2,self.context4))






        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

