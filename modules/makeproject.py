import os
import shutil
from pathlib import Path
import  sys

def copytree(src,dst,symLinks=False,ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src,item)
        d = os.path.join(src,item)
        if os.path.isdir(s):
            shutil.copytree(s,d,symLinks,ignore)
folder = str(sys.argv[2])
src = Path("E:\\houdini_pip\\v01\\Template")
dst = Path(os.getcwd())

dst = dst/folder
src = src/folder


os.mkdirs(str(dst))

copytree(src,dst)