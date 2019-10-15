#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/10 0010 15:52
# @Author   :lyh
# @Desc     : 每个 5s 检测设备
import subprocess

class DetectionDevicesUtils:
    """
        检测设备
            返回已存在的设备号
    """
    def detectionDevices(self):
        command_list = ['adb', 'devices']
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        each = process.communicate()[0]
        phoneSet = set()
        each = str(each.decode('utf8'))
        # 设备集合
        devicesList = each[each.find("\n"): each.rfind("\r")]
        devicesList = devicesList[1: devicesList.rfind("\r")]
        if devicesList == '':
            return phoneSet
        devicesList = devicesList.split('\r\n')
        for deviceTemp in devicesList:
            phoneSet.add(deviceTemp[0: deviceTemp.find('\t')])
        return phoneSet