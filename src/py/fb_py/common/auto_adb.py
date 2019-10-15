# -*- coding: utf-8 -*-
import os
import subprocess
import platform
import uiautomator2 as u2
import time

class auto_adb():
    def __init__(self):
        try:
            adb_path = 'adb'
            subprocess.Popen([adb_path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            self.adb_path = adb_path
        except OSError:
            if platform.system() == 'Windows':
                adb_path = os.path.join('Tools', "adb", 'adb.exe')
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.adb_path = adb_path
                except OSError:
                    pass
            else:
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except OSError:
                    pass
            print('请安装 ADB 及驱动并配置环境变量')
            exit(1)

    def run(self, raw_command):
        command = '{} {}'.format(self.adb_path, raw_command)
        process = os.popen(command)
        output = process.read()
        return output

    """
        通过usb连接检测是否存在设备
            :return --> 返回一个字典数据
                            key: 设备号   value: d
    """
    def test_device_usb(self):
        print('检查设备是否连接...')
        phoneMap = {}
        command_list = [self.adb_path, 'devices']
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        each = process.communicate()[0]
        each = str(each.decode('utf8'))
        """output = process.communicate()[0]

        for each in output:
            each = str(each.decode('utf8'))
            if "device" in each:"""

        # 设备
        devicesList = each[each.find("\n"): each.rfind("\r")]
        devicesList = devicesList[1: devicesList.rfind("\r")]
        if devicesList == '':
            return phoneMap
        devicesList = devicesList.split('\r\n')
        for deviceTemp in devicesList:
            deviceTemp = deviceTemp[0: deviceTemp.find('\t')]
            # usb 连接
            d = u2.connect_usb(deviceTemp)
            phoneMap[deviceTemp] = d
            # 检测屏幕状态
            if not d.info.get('screenOn'):
                # 打开屏幕
                d.screen_on()
                # 向上滑动
                d.swipe_ext('up', box=(200, 200, 200, 900))

            # 启动应用
            # 检测运行的软件
            app_runningList = d.app_list_running()
            if 'in.zhaoj.shadowsocksr' not in app_runningList:
                # 第一 启动ssr
                d.app_start("in.zhaoj.shadowsocksr")
                time.sleep(0.5)
                d(resourceId="in.zhaoj.shadowsocksr:id/fab").click()
                d.press('home')

            if 'com.github.uiautomator' not in app_runningList:
                # 第二 启动 atx
                d.app_start("com.github.uiautomator")
                d.press('home')

            # 第三 启动 fb
            d.app_start("com.facebook.katana")

            """time.sleep(10)
            if d(text='继续使用美式英语').exists():
                d(text='继续使用美式英语').click()"""
        return phoneMap


    """
        通过 ip 连接检测是否存在设备
            :return --> 返回一个字典数据
                            key: 设备号   value: d
    """
    def test_device_ip(self, devicesIps):
        phoneMap = {}
        for ip in devicesIps:
            # wifi
            d = u2.connect(ip)
            # 检测屏幕状态
            if not d.info.get('screenOn'):
                # 打开屏幕
                d.screen_on()
                # 解锁
                # d.unlock()
                # 向上滑动
                d.swipe_ext('up', box=(200, 200, 200, 800))

            # 启动应用
            # 检测运行的软件
            app_runningList = d.app_list_running()
            if 'in.zhaoj.shadowsocksr' not in app_runningList:
                # 第一 启动ssr
                d.app_start("in.zhaoj.shadowsocksr")
                d(resourceId="in.zhaoj.shadowsocksr:id/fab").click()
                time.sleep(2)
                d.press('home')

            if 'com.github.uiautomator' not in app_runningList:
                # 第二 启动 atx
                d.app_start("com.github.uiautomator")
                d.press('home')

            # 第三 启动 fb
            d.app_start("com.facebook.katana")
            time.sleep(10)
            if d(text='继续使用美式英语').exists():
                d(text='继续使用美式英语').click()
            phoneMap[d.device_info['serial']] = d
        return phoneMap