#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from  multiprocessing import pool,Manager
import time
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time









num=0
sec=0
class WorkThread(QThread):
    timer = pyqtSignal()
    end = pyqtSignal()

    def run(self):
        while True:
            self.sleep(1)
            if sec == 100:
                self.end.emit()
                break

            self.timer.emit()


class Process:
    def worker(self,i,q):
        q.put(i)

    def main(self):
        p=pool.Pool(15)
        q=Manager().Queue()

        for i in range(100):
            p.apply_async(self.worker,(i,q))

        while True:
            q.get()
            global num
            num+=1
            print(num)

            result=num/100
            if result ==1:
                break

        p.close()
        p.join()

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.Init_UI()

    def Init_UI(self):
        self.setGeometry(80,80,150,150)
        self.worker = WorkThread()
        btn = QPushButton("Open Houdini",self)
        btn.move(50, 50)
        btn.clicked.connect(self.showdialog)
        self.process


    def showdialog(self):


        self.worker.start()
        self.worker.timer.connect(self.add)

        self.dialog = QDialog()
        self.dialog.setWindowFlags(Qt.WindowMinMaxButtonsHint|Qt.WindowCloseButtonHint)

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        btn = QPushButton("Cancel")
        btn2 = QPushButton("Pause")
        hlayout.addWidget(btn)

        hlayout.addStretch(1)
        hlayout.addWidget(btn2)



        self.progressbar = QProgressBar()

        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.progressbar.setFormat("converting")


        self.progressbar.setStyleSheet(
            '''QProgressBar{
        border: none;
        color: white;
        text-align: center;
        background: rgb(68, 69, 73);
        border-radius: 3px;
        }
        QProgressBar::chunk {
        border: none;
        background: rgb(0, 160, 230);
        }'''
        )
        vlayout.addWidget(self.progressbar)
        vlayout.addStretch(1)
        vlayout.addLayout(hlayout)



        self.dialog.setGeometry(200,200,400,80)
        self.dialog.setLayout(vlayout)






        self.dialog.setStyleSheet("""
        QPushButton{
        color: rgb(255 ,255 ,255);
        background-color: rgb(50, 50, 50);
        border-radius: 3px;
        border: 1px solid rgb(40, 40, 40);
        padding:5px 20px
        }

        QPushButton:hover {
        background-color: rgb(155, 155, 155);
        }ssf

        QPushButton:pressed {
        background-color: rgb(80, 80, 80);
        }
        """
        )
        self.dialog.setModal(True)
        self.dialog.show()






        btn.clicked.connect(self.quit)


    def quit(self):
        self.dialog.close()
    def add(self):
        global sec
        sec+=1
        #Process().main()
        #print(result)
        self.progressbar.setValue(sec)
        if sec==30:
            self.quit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = Widget()
    windows.show()
    sys.exit(app.exec_())