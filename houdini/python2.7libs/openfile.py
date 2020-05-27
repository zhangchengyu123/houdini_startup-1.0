#coding=utf-8
def openFile():
    import  hou
    import  os
    dict={
        "file" : "file",
        "filecache" : "file",
        "ifd" : "vm_picture"

    }


    node = hou.selectedNodes()[0]
    type = node.type().nameComponents()[2]
    if type in dict.keys():
        parm=node.evalParm(dict[type])
        path=os.path.split(parm)[0]
        if os.path.exists(path) is True:
            os.startfile(path)
        else:
            raise(hou.PermissionError("can't find file path"))







