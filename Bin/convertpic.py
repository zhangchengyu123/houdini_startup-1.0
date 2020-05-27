import subprocess
from pathlib import Path
import sys
from os import environ


hfs = Path("C:\\Program Files\\Side Effects Software\\Houdini 17.5.173")/"bin"/"houdinifx"

startup = Path(environ['CGSTARTUP'],"startup.py")


subprocess.call(" ".join([str(startup.resolve()),"convertpic"]), shell="ture")
#subprocess.Popen(str(hfs.as_posix()))


