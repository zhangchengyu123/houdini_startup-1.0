from pathlib import Path
import sutils
import os
from collections import defaultdict
import re



def getItemRoot(path,filename):
    file_name ="{}.conf".format(filename)
    while True:

        parent_dir = Path(path).parent
        if(Path(path)/file_name).exists():
            result = path
            return  result
            break
        elif path == parent_dir:
            result = None
            return  result
            break
        else:
            path = parent_dir

    return result


def makeprojectvariable(projectpath):
    data = sutils.getconfig(os.environ["CGSTARTUP"],"config.json")
    path = data["projectvariables"]

    result = defaultdict(list)


    for key,value in path.items():
        result[key] = Path(os.path.sep.join(value).replace("%PRJ",str(projectpath)))

    return result


def makeassetsvariable(assetspath):
    data = sutils.getconfig(os.environ["CGSTARTUP"],"config.json")
    path = data["assetvariables"]

    result = defaultdict(list)


    for key,value in path.items():
        result[key] = Path(os.path.sep.join(value).replace(r"%ASSET",str(assetspath)))


    return result


def getEpisodeRoot(episodepath):
    path  = re.search(r"Episodes",episodepath)
    if path:
        episode_path = episodepath[:path.span()[1]]
        episode = episodepath[path.span()[1]:]
        return [episode_path,episode]
    else:
        return None


def makeEpisodeVariable(episodepath):
    data = sutils.getconfig(os.environ["CGSTARTUP"],"config.json")
    path = data["episodevariables"]

    result = defaultdict(list)


    for key,value in path.items():
        result[key] = Path(os.path.sep.join(value).replace(r"%EPISODE",str(episodepath)))



    return result

def makeEpisodeVar(episodepath,epis_span):
    data = sutils.getconfig(os.environ["CGSTARTUP"],"config.json")
    path = data["episodevar"]
    episodepath=Path(episodepath)/Path(epis_span).parts[1]


    result = defaultdict(list)


    for key,value in path.items():
        result[key] = Path(os.path.sep.join(value).replace(r"%EPISODES",str(episodepath)))



    return result


def getShotroot(epis_span):
    if len(Path(epis_span).parts)>2:
        return True
    else:
        return None

def makeShotVariable(episodepath,episode_span):
    data = sutils.getconfig(os.environ["CGSTARTUP"],"config.json")

    path = data["shotVariables"]

    shot_path = Path(episodepath) / Path(episode_span).parts[1] / Path(episode_span).parts[2]

    shot_name = Path(episode_span).parts[2]

    result = defaultdict(list)
    for key, value in path.items():
        result[key] = Path(os.path.sep.join(value).replace(r"%SHOT", str(shot_path)).replace(r"%SNAME",str(shot_name)))

    return result

def getTaskroot(epis_span,pwd):

    if len(Path(epis_span).parts)>=4:
        path = re.search(r"work", pwd)

        if path:
            task_path = pwd[:path.span()[1]]
            task = pwd[path.span()[1]:]

            return [task_path, task]
        return True
    else:
        return None


def makeTaskVariable(shotpath,task_list):
    data = sutils.getconfig(os.environ["CGSTARTUP"],"config.json")
    path = data["taskVariables"]
    result = defaultdict(list)
    for key, value in path.items():

        result[key] = Path(os.path.sep.join(value).replace(r"%SHOT", str(shotpath[0])).replace(r"%TASKNAME",str(task_list[-1])))


    return result
