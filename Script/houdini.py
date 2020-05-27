import subprocess
import os
from pathlib import Path
import sutils
import projectparsing
from collections import defaultdict



os.environ["HOUDINI_BUFFEREDSAVE"] = "1"
os.environ["HOUDINI_DSO_ERROR"] = "2"

os.environ["PDG_IMAGEMAGICK"] = r"C:/Program Files/ImageMagick-7.0.9-Q16/magick.exe"
os.environ["PDG_FFMPEG"] = r"C:/ffmpeg/ffmpeg/bin/ffmpeg.exe"
#===============================================lutset======================================================


pwd = Path(os.environ["CGSTARTUP"])

#dso = r"E:/houdini_pip/v01/hdk"
#dso_path = [dso,"&"]

#dso = Path(";".join(dso_path)).as_posix()
#os.environ["HOUDINI_DSO_PATH"] = dso







aces = True

if aces:
    os.environ["OCIO"] = Path(os.path.join(pwd,"lib","luts","config.ocio")).as_posix()
    lut = Path(os.path.join("lib","luts","baked","houdini","Rec.709 for ACEScg Houdini.lut")).as_posix()
    os.environ["HOUDINI_IMAGE_DISPLAY_GAMMA"] = "1"
    os.environ["HOUDINI_IMAGE_DISPLAY_LUT"] = Path(pwd/lut).as_posix()

else:
    os.environ["HOUDINI_IMAGE_DISPLAY_OVERRIDE"] = "1"
    os.environ["HOUDINI_IMAGE_DISPLAY_GAMMA"] = "2.2"
    os.environ["HOUDINI_IMAGE_DISPLAY_LUT"] = ""






#----------------------------------------------------------------------------------------------------------------------
scripts =r'E:\houdini_pip\v01\houdini'
hou_path = [scripts, "&"]



local_file = Path(__file__).parent/Path("text.txt")

directory = Path(pwd)/"Software"/"houdini"

def getpath():
    result = list(map(lambda dir: Path.joinpath(directory,dir),os.listdir(directory)))
    return result

def filterotls(directory):
    otls_list =list()
    for root in directory:
        for rootpath,dirs,files in os.walk(str(root)):
            name=os.path.basename(rootpath)
            if name == "otls":
                otls_list.append(rootpath)
    return otls_list



#===============================================================================set baisc otl path=================================
otlist = getpath()
otldir = filterotls(otlist)

#========================================= set env_path for houdini========================================



#=========================================================CGRU config===============================================

dir  = os.environ["CGRU_LOCATION"]

data = sutils.getconfig(os.environ["CGSTARTUP"], "config.json")
cgru = data["cgru_variables"]

cgru_result = defaultdict(list)

for key, value in cgru.items():
    temp = dict()

    if isinstance(value[0],list):
        for v in value:
            temp[key] = Path(os.path.sep.join(v).replace("%CGRU_LOCATION", str(dir))).as_posix()

            cgru_result = sutils.megerDict(temp, cgru_result)

    else:
        temp[key] = Path(os.path.sep.join(value).replace("%CGRU_LOCATION", str(dir))).as_posix()
        cgru_result = sutils.megerDict(temp, cgru_result)

flatten = lambda l: sum(map(flatten,l),[])if isinstance(l,list) else [l]



scan_path = flatten(cgru_result["HOUDINI_OTLSCAN_PATH"])
otldir.append(scan_path[0])
otldir.append("&")
cgru_result.pop("HOUDINI_OTLSCAN_PATH")
cgru_result.pop("CGRU_LOCATION")



for k, v in cgru_result.items():
    v.append("&")
    cgru_result[k] = flatten(v)
    final_path = os.path.pathsep.join(cgru_result[k])
    os.environ[k]=final_path





os.environ["HOUDINI_OTLSCAN_PATH"] =Path(";".join(otldir)).as_posix()




os.environ["HOUDINI_PATH"] = Path(";".join(hou_path)).as_posix()

infor = os.environ["HOUDINI_PATH"]


sutils.softwareLocation()
sutils.splashLocation()
project = projectparsing.getItemRoot(os.getcwd(),"_test")
project_variables = defaultdict(list)

#===================================set variables for houdini=============================================

if project:
    sutils.softwareLocation(project,"test")
    sutils.splashLocation(project,"test")
    project_variables = projectparsing.makeprojectvariable(project)
    assetroot = projectparsing.getItemRoot(os.getcwd(), "_Assets")

    if assetroot:
        project_variables  = sutils.megerDict(projectparsing.makeassetsvariable(assetroot),project_variables)

    episodeRoot=projectparsing.getEpisodeRoot(os.getcwd())

    if episodeRoot[0] :
        project_variables = sutils.megerDict(projectparsing.makeEpisodeVariable(episodeRoot[0]),project_variables)
        if episodeRoot[1]:

            project_variables = sutils.megerDict(projectparsing.makeEpisodeVar(episodeRoot[0],episodeRoot[1]),project_variables)
            shotroot = projectparsing.getShotroot(episodeRoot[1])

            if shotroot:
                project_variables = sutils.megerDict(projectparsing.makeShotVariable(episodeRoot[0], episodeRoot[1]),project_variables)
                Taskroot = projectparsing.getTaskroot(episodeRoot[1],os.getcwd())


                if Taskroot:
                    project_variables = sutils.megerDict(projectparsing.makeTaskVariable(project_variables["SHOT"], Taskroot),project_variables)


inf ="HOUDINI_PATH:{}".format(infor)
data =""
if project_variables:
    project_variables.pop("HOUDINI_PATH")
    for k,v in project_variables.items():
        while isinstance(v[0],list):
             v[0]=v[0][0]

        os.environ[k]=v[0].as_posix()
        data ="{}:{}\n".format(k,os.environ[k])+data
    infor=data
    with open(local_file, "w") as f:
        f.write(infor)
        f.close()

else:
    with open(local_file, "w") as f:
        f.write("")
        f.close()




hfs=Path(os.environ["SOFTWAREROOT"])/"bin"/"houdinifx"


subprocess.Popen(hfs.as_posix())
