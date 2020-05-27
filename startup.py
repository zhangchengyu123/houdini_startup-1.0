import sys
from pathlib import Path
import importlib.util

scripts = Path(sys.argv[0]).parent / "Script"
sys.path.append(scripts.as_posix())

modules = Path(sys.argv[0]).parent / "Modules"
sys.path.append(modules.as_posix())

software=sys.argv[1]

doc = importlib.util.find_spec(software)
print(doc)

if "Script" in Path(doc.origin).parts:
    print("script - ", software,"- exit")

elif "Modules" in Path(doc.origin).parts:
    print("modules - ", software,"- exit")
else:
    print("not exit modules")



__import__(software)