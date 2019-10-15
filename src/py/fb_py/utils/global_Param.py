#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/11 0011 21:29
# @Author   :lyh
# @Desc     :

def init():
    global global_dict
    global_dict = {}


def set_value(key, value):
    global_dict[key] = value


def get_value(key):
    return global_dict[key]