#coding=utf-8
import os
import sutils
from pathlib import Path
import subprocess
import itertools

sutils.softwareLocation()

iconvert=Path(os.environ["SOFTWAREROOT"])/"bin"/ "iconvert"

suppose_format=["tiff", "exr" , "jpg", "png", "hdr"]
########==============================================================================================================
commands =list()
for root,dir,names in os.walk("."):
    for filename in names:
        if Path(filename).suffix[1:] in suppose_format:
            name=filename.split(".")[0]

            command=[
                iconvert.as_posix(),
                (Path(root).resolve()/filename).as_posix(),
                (Path(root).resolve()/Path(filename)).as_posix()+".rat"
            ]
            commands.append(command)

max_workers = 16
processes   = (subprocess.Popen(cmd,shell=True) for cmd in commands) ##利用一个列表生成式 返回一个生成器

running_processes = list(itertools.islice(processes,max_workers)) ##利用迭代器工具去迭代Popen返回的值 迭代次数由 max_workers决定并返回一个列表

print (running_processes)
while running_processes: ##通过while 执行多任务进程
   for i,process in enumerate(running_processes):
        if process.poll()is not None:   ##Popen类中的poll方法返回监控对象进程是否完成终止 None为任务还在进行中
           running_processes[i]=next(processes) ##如果检测完成 则读取添加生成器中下一个类 进行运行操作


           if running_processes[i] is None: ##如果未完成任务
                del running_processes[i] ##删除列表内的变量并且终止循环
                break

            #subprocess.call(command)