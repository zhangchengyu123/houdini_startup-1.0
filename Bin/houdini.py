import subprocess
from pathlib import Path

from os import environ


hfs = Path("C:\\Program Files\\Side Effects Software\\Houdini 18.0.416")/"bin"/"houdinifx.exe"

startup = Path(environ['CGSTARTUP'],"startup.py")

print ("start path is: ",startup)

subprocess.call(" ".join([str(startup.resolve()),"houdini"]), shell="ture")
#subprocess.Popen(str(hfs.as_posix()))


