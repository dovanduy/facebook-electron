#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/8 0008 15:30
# @Author   :lyh
# @Desc     : 线程
import threading


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def getResult(self):
        try:
            return self.result
        except:
            return None