#coding=utf-8
import hou
import os
import tempfile

data = [
    "Geometry",
    "particles",
    "flip_mesh",
    "flip_sim",
    "volume",
    "VDB",
    "pyro_sim"
]

type = [
    ".bgeo.sc",
    ".pc",
    ".bgeo.gz"
]



def openFile(node):
        parms_path = node.parm("sopoutput").eval()

        path=os.path.split(parms_path)[0]
        if os.path.exists(hou.expandString(path)) is True:
            os.startfile(hou.expandString(path))
        else:
            raise(hou.Error("can't find file path"))

def eval_node_parms(node):
    geo_type = node.parm("Geometry_Type").evalAsString()

    format_type = node.parm("Format_Type").evalAsString()

    cache_name = node.parm("Cache_name").eval()
    version    = node.parm("version").evalAsString()
    text       =      node.parm("command").eval()
    tempdir    =os.environ.get("HOUDINI_TEMP_DIR")


    data ={}
    data["geotype"] = geo_type
    data["format"]  = format_type
    data["cachedir"]= r"$CACHE"
    data["cachename"] = cache_name
    data["ver"]   = version
    data["description"] = text
    path ="/".join([data["cachedir"],geo_type,data["cachename"],str(data["ver"])])
    data["path"]=path
    data["tempdir"] =tempdir

    if len(data["cachename"]) != 0:

        filename = data["cachename"]+"."+"$F4"+data["format"]
        basename = data["path"]
        data["fullpath"] = "/".join([basename,filename])

        node.parm("sopoutput").set(data["fullpath"])

    else:
        data["fullpath"] = "$HIP/geo/$HIPNAME.$OS.$F.bgeo.sc"
        abs_path = hou.expandString(data["fullpath"])
        node.parm("sopoutput").set(abs_path)



    return data



def change_version(node):
    data = eval_node_parms(node)
    result =node.userData(data["fullpath"])
    node.parm("description").set(result)


def execute(node):
    data = eval_node_parms(node)
    filepath = hou.hipFile.path()

    filename = hou.hipFile.basename()


    dir_path =os.path.splitext(data["cachedir"])[0].rsplit("/",1)[0]


    if os.path.exists(hou.expandString(data["path"])) is False:
        os.makedirs(hou.expandString(data["path"]))
    dirs = os.listdir(hou.expandString(data["path"]))


    node.parm("description").set(data["description"])
    node.setUserData(data["fullpath"],data["description"])

    if dir_path  not in  data["tempdir"] :
        if len(dirs) != 0 :
            hou.ui.displayMessage("Detected the existence of files, replace them ?",
                                  buttons=("yes","no"),
                                  severity=hou.severityType.Message
                                  )
            hou.hipFile.saveAsBackup()

            node.node("rop_geometry1").parm("execute").pressButton()
        else:
            hou.hipFile.saveAsBackup()

            node.node("rop_geometry1").parm("execute").pressButton()

    else :
        raise(hou.Error("This is tempfile, please set correct path"))




