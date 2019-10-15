# -*- coding: utf-8 -*-
import json
import os
import uiautomator2 as u2
from flask import Flask, request
import time
from common.auto_adb import auto_adb
import publicFunction
import add
import login
import devices
import utils.detectionDevicesUtils as dDU
import utils.global_Param as gp
import utils.socket_client as sc

# 调度
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 30,
    'misfire_grace_time': 60 * 60  #100秒的任务超时容错
}
scheduler = BackgroundScheduler(executors=executors, timezone='MST', job_defaults=job_defaults)


app = Flask(__name__)

gp.init()
adb = auto_adb()
# 公用类
pf = publicFunction.PublicFuncation()
# 添加类
addClass = add.Add()
# 登陆等类
loginClass = login.Login()
# 设备入库类
devicesClass = devices.Devices()
# 检测设备
ddUtils = dDU.DetectionDevicesUtils()

"""
    检测设备是否连接
        返回一个字典数据(key: 设备号   value: d)
"""
phoneMap = adb.test_device_usb()

"""
    定时检测 设备
"""
def schedulerDetection():
    phoneSet = ddUtils.detectionDevices()
    dataInfo = {}
    # 移除 存在于 phoneSet 而不存在 phoneMap 中的设备信息
    for key in list(phoneMap.keys()):
        if key not in phoneSet:
            phoneMap.pop(key)
            # socket 推送消息
            dataInfo['type'] = 'removeDevice'
            sc.send_short_msg(bytes(json.dumps(pf.return_result(True, '', dataInfo)), encoding='utf-8'))

    for deviceNum in phoneSet:
        d = u2.connect_usb(deviceNum)
        # 检测屏幕状态
        if not d.info.get('screenOn'):
            # 打开屏幕
            d.screen_on()
            # 向上滑动
            d.swipe_ext('up', box=(200, 200, 200, 900))

        if deviceNum not in phoneMap.keys():
            # 新增设备
            # socket 推送消息
            dataInfo['type'] = 'insertDevice'
            phoneMap[deviceNum] = d
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
            sc.send_short_msg(bytes(json.dumps(pf.return_result(True, '', dataInfo)), encoding='utf-8'))


"""
    发送消息
"""
def send_Msg(d, params):
    d.implicitly_wait(10.0)
    # 检测是否存在 message app
    app_package = "com.facebook.orca"
    result = os.popen("adb shell pm path " + app_package).read()
    if result:
        # 启动messenger app
        d.app_start(app_package)
    else:
        apk_path = "http://domita-assets-02.oss-cn-beijing.aliyuncs.com/downloads/Messenger%20%E2%80%93%20Text%20and%20Video%20Chat%20for%20Free_v234.0.0.9.121_apkpure.com.apk"
        result = os.popen("adb -s {pid} install {apkPath}".format(pid='', apkPath=apk_path))
    print("发送消息:", params['msg'])


"""
    登陆
"""
@app.route('/login', methods=['POST'])
def web_login():
    data = request.get_data()
    data = json.loads(data.decode("UTF-8"))
    return loginClass.login(data)


"""
    登出
"""
@app.route('/logout', methods=['GET'])
def logout():
    return pf.return_result(True, '退出成功', '')


"""
    注册
"""
@app.route('/reg', methods=['POST'])
def reg():
    data = request.get_data()
    data = json.loads(data.decode("UTF-8"))
    return loginClass.reg(data)


"""
    获取设备信息
"""
@app.route('/find_PhoneInfo', methods=['GET'])
def find_phones():
    if phoneMap == {}:
        return pf.return_result(False, '朋友，未连接到任何手机', '')
    else:
        # 获取设备信息
        try:
            return pf.find_PhoneInfo(phoneMap)
        except:
            return pf.return_result(False, '朋友，未连接到任何手机', '')

"""
    修改设备 备注、fb账号昵称
        参数：
            params:{
                "device_id": 设备号
                "remark": 设备备注
                "fbNick":fb账号昵称
                }
"""
@app.route('/updateDevice', methods=['POST'])
def updateDevice():
    data = request.get_data()
    data = json.loads(data.decode("UTF-8"))
    result = devicesClass.updateRemarkAndfbNick(data['device_id'], data['remark'], data['fbNick'])
    return pf.return_result(result, '', '')


"""
    锁屏
        参数：
            device_id : 设备id
"""
@app.route('/lock', methods=['POST'])
def lock():
    data = request.get_data()
    data = json.loads(data.decode("UTF-8"))
    d = u2.connect_usb(data['device_id'])
    d.screen_off()
    return pf.return_result(True, '', '')


"""
    解屏
        参数：
            device_id : 设备id
"""
@app.route('/unlock', methods=['POST'])
def unlock():
    data = request.get_data()
    data = json.loads(data.decode("UTF-8"))
    d = u2.connect_usb(data['device_id'])
    # 打开屏幕
    d.screen_on()
    # 向上滑动
    d.swipe_ext('up', box=(200, 200, 200, 900))
    return pf.return_result(True, '', '')


"""
    退出系统
"""
@app.route('/exit', methods=['GET'])
def exit_System():
    adb.run('kill-server')
    return pf.return_result(True, '', '拜拜')


"""
    添加好友/小组
    json数据格式：
        必传：
            type: 函数名
            minutesNum : 间隔分钟数
            userId : 用户id
            params : 其他参数 {{"":"","":""}, {}...}
        非必传：
            equipments : 设备号
"""
@app.route("/choose_method", methods=['POST'])
def choose_method():
    result_dict = {}
    data = request.get_data()
    data = json.loads(data.decode("UTF-8"))
    userId = data['userId']
    # 用户id是否为 ''
    if userId == 0:
        return pf.return_result(False, '朋友，请先登陆', '')
    type = data['type']

    params = {}
    # 其他参数集合
    otherParamList = None
    if 'params' in data.keys():
        otherParamList = data['params']
    params['userId'] = userId
    params['scheduler'] = scheduler

    isScheduler = False
    minutes = float(data['minutesNum']) - 2
    result_dict['type'] = type
    try:
        temp = otherParamList[0]
        temp['userId'] = userId
        # 移除
        otherParamList.pop(0)

        # 设备号
        result_dict['equipments'] = data['equipments']
        if 'add_friends' == type:
            # 首次执行
            num = addClass.add_one_friend(phoneMap[data['equipments']], temp)
            if len(otherParamList) == 0:
                result_dict['num'] = num
                sc.send_short_msg(bytes(json.dumps(pf.return_result(True, '', result_dict)), encoding='utf-8'))
                return pf.return_result(True, '', '')
            params['param'] = otherParamList
            scheduler.add_job(addClass.add_friends, 'interval', (phoneMap[data['equipments']], params), minutes=minutes)
            isScheduler = True
        else:
            num = addClass.add_one_tream(phoneMap[data['equipments']], temp)
            if len(otherParamList) == 0:
                result_dict['num'] = num
                sc.send_short_msg(bytes(json.dumps(pf.return_result(True, '', result_dict)), encoding='utf-8'))
                return pf.return_result(True, '', '')
            params['param'] = otherParamList
            scheduler.add_job(addClass.add_tream, 'interval', (phoneMap[data['equipments']], params), minutes=minutes)
            isScheduler = True

        # 给需要定时执行的任务 开启一个独立线程
        scheduler.start()
    except Exception as e:
        if isScheduler:
            return pf.return_result(True, '', '')
        print(e)
        sc.send_short_msg(bytes(json.dumps(pf.return_result(False, 'Exception error', '')), encoding='utf-8'))
        return pf.return_result(False, '朋友，发生未知错误', '')


if __name__ == "__main__":
    scheduler.add_job(schedulerDetection, 'interval', seconds=5)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
