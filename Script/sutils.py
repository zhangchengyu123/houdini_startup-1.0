import  startconfig
import os
from pathlib import Path
import platform
from  collections  import defaultdict
from itertools import chain




def getconfig(projectpath,filename):
    data =os.path.join(projectpath,filename)

    database=startconfig.makejsondata(data)

    return database



def megerDict(dict1,dict2):
    dict = defaultdict(list)
    for key, value in chain(dict1.items(),dict2.items()):
        dict[key].append(value)

    return dict


def softwareLocation(*projectlist,**kwargs):
    if len(projectlist)!=2 or not Path(projectlist[0]).exists():
        if len(projectlist)!=0:
            print(f"warning incorrect input data:{projectlist}")

        projectpath = Path(os.environ["CGSTARTUP"])
        filename="config.json"
        database=getconfig(projectpath,filename)

        oppath = database["location"][platform.system()]["houdini"]
        if "version" in kwargs:
            ver=kwargs["version"]
        else:
            ver = database["version"]["houdini"]

        os.environ["SOFTWAREROOT"] = Path("/".join(oppath).replace("%VER",ver)).as_posix()

    else:
        database = getconfig(projectlist[0],f"_{projectlist[1]}.conf")
        ver = database["version"]["houdini"]
        print(f"version is overrided by _{projectlist[1]}.conf,version is {ver}")
        softwareLocation(version=ver)


def splashLocation(*projectlist,**kwargs):
    if len(projectlist)!=2 or not Path(projectlist[0]).exists():
        if len(projectlist)!=0:
            print(f"warning incorrect input data:{projectlist}")
        else:
            return None

    else:
        database = getconfig(projectlist[0], f"_{projectlist[1]}.conf")
        splash = database["splash_file"]["pic"]
        os.environ["HOUDINI_SPLASH_FILE"] = Path("/".join(splash)).as_posix()


