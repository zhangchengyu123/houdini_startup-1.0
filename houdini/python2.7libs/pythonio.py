#coding=utf-8
def pythonIO():
    import  hou
    import  imp
    item =hou.ui.displayMessage("pythonIo the node ", buttons =("export","import","cancel"),severity=hou.severityType.Message)# pop up a small window

    if item == 0:

        filepath =hou.ui.selectFile("export node as python", title="pythonIo", pattern="*.py", default_value="nodewrite.py")#get choose file window to store file


        file=open(filepath,"w")

        file.write("import hou")
        file.write(hou.node("/").asCode(brief=False, recurse=True, save_creation_commands=True))# write code imformation as python store in file
        file.close()

    if item == 1:
        filepath = hou.ui.selectFile("export node as python", title="pythonIo", pattern="*.py",
                                     default_value="nodewrite.py")  # get *.py  file

        imp.load_source("writenode",filepath) # immediatly excute *.py   file








