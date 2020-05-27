import hou
import os
import itertools

root = r'E:\houdini_pip\vexlib'

def setPerset():
    f = hou.ui.displayMessage("Save the current code to disk?", buttons=("current_series", "new_series","No"))
    menu_list = hou.pwd().parm("type").menuItems()


    if f == 0:
       floder = hou.ui.selectFromList(menu_list, default_choices=(), exclusive=False,column_header="select the type",clear_on_cancel=False)
       if len(floder) != 0:
         text = hou.ui.readInput("fill the file name ", buttons=('OK',"Cancel"),
                                 severity=hou.severityType.Message,
                                 close_choice = 1
                                 )
         dirpath = root + "\\" + menu_list[floder[0]] + "\\"
         files = os.listdir(dirpath)
         filedir = dirpath + text[1] + ".txt"


         if text[0] == 0 :

             if text[1] + ".txt" in files:
                 r = hou.ui.displayMessage("detect the same name", severity=hou.severityType.Error,title="Error")

             else:
                 context = hou.pwd().parm("snippet").eval()

                 fo = open(filedir, "w")

                 fo.write(context)

                 fo.close()



    if f == 1:
        newFloder = hou.ui.readInput("fill the series name ", buttons=('OK', "Cancel"),
                                severity=hou.severityType.Message,
                                close_choice = 1
                                )
        folders = os.listdir(root)


        if newFloder[0] == 0:
            if newFloder[1] in folders:
                hou.ui.displayMessage("detect the same folder", severity=hou.severityType.Error, title="Error")
            else:
                filename = hou.ui.readInput("fill the file name ", buttons=('OK', "Cancel"),
                                             severity=hou.severityType.Message,
                                             close_choice = 1
                                             )
                seriesName = newFloder[1]


                if filename[0] == 0:
                   seriesdir = root + "//" + seriesName+"//"

                   os.mkdir(seriesdir)
                   file_path = seriesdir+filename[1]+".txt"
                   context = hou.pwd().parm("snippet").eval()
                   fo = open(file_path,"w")
                   fo.write(context)
                   fo.close()


def setText():

    folder = hou.pwd().parm("type").evalAsString()
    file  = hou.pwd().parm("file").evalAsString()
    file = file+".txt"
    roots = "/".join([root,folder,file])
    try:
        f = open(roots,"r")
        n = f.readlines()
        f.close()
    except hou.LoadWarning:
        hou.NodeError("don't exist the file")
    ctx = ""
    for nn in n:
        ctx +=nn
    result = hou.pwd().parm("snippet").eval()
    if result!="":
        ctx = result+"\n"+ctx
        hou.pwd().parm("snippet").set(ctx,follow_parm_reference=True)
    else:
        hou.pwd().parm("snippet").set(ctx,follow_parm_reference=True)


def menuItem():
    import sys
    sys.path.append(r"E:\\houdini_pip\\v01\\houdini\\scripts\\sop\\")
    folders = os.listdir(root)
    if len(folders) == 0:
        folders = ["None"]
        result = list(itertools.chain(*zip(folders, folders)))

        return result
    else:
        result = list(itertools.chain(*zip(folders, folders)))

        return result

def menuItem1():
    import sys
    sys.path.append(r"E:\\houdini_pip\\v01\\houdini\\scripts\\sop\\")
    default = hou.pwd().parm("type").evalAsString()
    dirpath = "/".join([root,default])
    fileList = os.listdir(dirpath)
    newList = []
    folders = os.listdir(root)
    for file in fileList:
        f = file.split(".")[0]
        newList.append(f)
        if len(fileList) == 0 or len(folders) == 0:
            newList = ["None"]
            result = list(itertools.chain(*zip(newList, newList)))
            return result
        else:
            result = list(itertools.chain(*zip(newList, newList)))
            return result

def fileSet():
    default = hou.pwd().parm("type").evalAsString()
    dirpath = "/".join([root,default])
    if os.path.exists(dirpath) is True:
        fileList = os.listdir(dirpath)
    else:
        fileList = []
    newList = []
    for file in fileList:
        f = file.split(".")[0]
        newList.append(f)
    folders = os.listdir(root)

    if len(fileList) == 0 or len(folders) == 0:
        newList = ["None"]
        result = list(itertools.chain(*zip(newList, newList)))
        return result
    else:
        result = list(itertools.chain(*zip(newList, newList)))
        return result

