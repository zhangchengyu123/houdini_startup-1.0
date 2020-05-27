#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from  multiprocessing import  pool,Manager
import time
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class aaa:
    def worker(self,i,q):
        time.sleep(1)
        q.put(i)
    def main(self):
        p=pool.Pool(5)
        q=Manager().Queue()

        for i in range(20):
            p.apply_async(self.worker,(i,q))
        num = 0
        a=0
        while True:
            result =q.get()
            num+=1
            a= num/20

            if a ==1:
                break
        return a
        p.close()
        p.join()


if __name__=="__main__":
    b =aaa().main()
    print(b)




