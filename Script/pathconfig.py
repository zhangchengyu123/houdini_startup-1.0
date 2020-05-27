from pathlib import Path
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def combine_Path(path):

    list = ["None"]
    for roots, dirs, files in os.walk(path):
        for dir in dirs:
            root = Path(roots) / Path(dir)
            if root.parent == Path(path) and dir!="Lib":
                list.append(dir)

    return list


def QcomboxConset(Qcombox,project_root,*folder):
        if len(folder)>0:
            text =folder[0]
        else:
            text=""
        context = Qcombox.currentText()
        try:
            root  = Path(os.path.join(project_root, context,text))
            items = combine_Path(root)
            #new_items=list(filter(lambda x : x !="Lib", [x for x in items]))

            return [context,root,items]
        except:
            if context=="None":
                return ["None","None","None"]



def set_Scrollbar(qbox,maxitems):
    listview = QListView()
    qbox.setModel(listview.model())
    qbox.setView(listview)
    qbox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    qbox.setMaxVisibleItems(maxitems)





def addText(str1,list1,qbox):
    if  str1 == "None" or len(list1) == 0:
        qbox.clear()
        qbox.addItem("None")
    elif len(list1) != 0:
        qbox.clear()
        qbox.addItems(list1)
        set_Scrollbar(qbox,5)






