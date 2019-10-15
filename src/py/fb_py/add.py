#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/8 0008 15:16
# @Author   :lyh
# @Desc     : 添加好友/小组
import time
import json
import utils.sqlUtils as sqlUtils
import publicFunction
import devices
import utils.socket_client as sc


class Add:
    def __init__(self):
        self.mysqlUtil = sqlUtils.SqlUtils()
        self.pf = publicFunction.PublicFuncation()
        self.devices = devices.Devices()

    """
        添加--公共函数
            msg : 所有条件
    """
    def add_public(self, d, msg=None):
        d.implicitly_wait(10.0)
        try:
            # 第一次运行fb
            d(resourceId="com.facebook.katana:id/(name removed)", description="好友，第2/6个选项卡").click()
        except:
            # 第 1+n 次运行使用
            d.xpath('//android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/'
                    'android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                    'android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/'
                    'android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/'
                    'android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/'
                    'android.widget.FrameLayout[2]').click()
        # 点击搜索
        d(description="搜索").click()
        # 输入搜索内容
        d.send_keys(msg, clear=True)
        d(description="查看" + str(msg).lower() + "的搜索结果").click()


    """
        添加---返回主页
    """
    def returnHomePage(self, d):
        # 退回到 选择添加的用户还是小组页面
        d(resourceId="com.facebook.katana:id/(name removed)", description="返回").click()
        # 退回到 输入搜索信息页面
        d(resourceId="com.facebook.katana:id/(name removed)", description="返回").click()
        # 选择页面
        d(resourceId="com.facebook.katana:id/(name removed)", description="返回").click()
        # 退回到首页
        try:
            # 第一次运行fb
            d(resourceId="com.facebook.katana:id/(name removed)", description="动态消息，第1/6个选项卡").click()
        except:
            d.xpath('//android.widget.FrameLayout[3]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/'
                    'android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/'
                    'android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/'
                    'android.widget.LinearLayout[1]/android.widget.FrameLayout[1]').click()

    """
        添加好友
            参数（集合）：
            [{  
                msg : 搜索条件
                num : 添加好友个数
                sleepTime : 每次添加好友间隔时间（s）
                city ：城市
                school ： 学校
                work ：工作
                foaf ：好友的好友（True/False）},{。。。} ]
    """
    def add_friends(self, d, params=None):
        result_dict = {}
        result_dict['type'] = 'add_friends'
        result_dict['equipments'] = d.serial
        sc.send_short_msg(bytes(json.dumps(self.pf.return_result(True, 'The task will be executed in 2 minutes', result_dict)), encoding='utf-8'))
        time.sleep(120)
        listMap = params['param']
        temp = listMap[0]
        temp['userId'] = params['userId']
        result_dict['num'] = self.add_one_friend(d, temp)
        sc.send_short_msg(bytes(json.dumps(self.pf.return_result(True, '', result_dict)), encoding='utf-8'))
        listMap.pop(0)
        if len(listMap) == 0:
            params['scheduler'].shutdown()

    """
        添加单个好友
        必传：
            msg : 搜索条件
            num : 添加好友个数
            sleepTime : 每次添加好友间隔时间（s）
        可选：
            city ：城市
            school ： 学校
            work ：工作
            foaf ：好友的好友（True/False）
    """
    def add_one_friend(self, d, params={}):
        self.mysqlUtil.start()
        self.devices.updateDeviceStatus(d.serial, '工作中')

        userId = params['userId']
        msg = params['msg']
        num = int(params['num'])
        self.add_public(d, msg)

        d.implicitly_wait(10.0)
        d(description="用户").click()
        time.sleep(5)
        # 设置筛选条件
        d(description="筛选条件").click()
        time.sleep(.5)
        # 城市
        if 'city' in params.keys() and params['city']:
            d(description="城市, 任何地点").click()
            d(text="搜索城市").click()
            d.send_keys(params['city'], clear=True)
            time.sleep(2)
            d.xpath('//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]').click()
            # 不存在搜索结果
            if not d(description="重置").exists():
                time.sleep(2)
                d(description="返回").click()
                d(description="返回").click()

        # 学校
        if 'school' in params.keys() and params['school']:
            d(description="学校, 任何学校").click()
            d(text="搜索学校").click()
            d.send_keys(params['school'], clear=True)
            time.sleep(2)
            d.xpath('//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]').click()
            # 不存在搜索结果
            if not d(description="重置").exists():
                d(description="返回").click()
                d(description="返回").click()

        # 工作
        if 'work' in params.keys() and params['work']:
            d(description="工作, 任何公司").click()
            d(text="搜索公司").click()
            time.sleep(2)
            d.send_keys(params['work'], clear=True)
            # 不存在搜索结果
            if not d(description="重置").exists():
                d(description="返回").click()
                d(description="返回").click()

        # 好友的好友
        if 'foaf' in params.keys():
            if params['foaf']:
                d.xpath('//*[@resource-id="android:id/content"]/android.view.ViewGroup[1]/android.view.ViewGroup[6]').click()
        time.sleep(1)
        d(description="显示结果").click()
        time.sleep(2)

        index = 0
        while index < num:
            # 添加好友列表
            try:
                d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/'
                        'android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/'
                        'android.view.ViewGroup[1]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView[1]/'
                        'android.view.ViewGroup[' + str(index + 1) + ']/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
            except:
                continue
            index += 1
            time.sleep(float(params['sleepTime']))

        # 返回主页
        self.returnHomePage(d)
        self.mysqlUtil.cudSql("insert into add_info(add_type, add_key, add_num, user_id, device_id) values (0, '" + msg + "', " + str(index) + ", " + str(userId) + ", '"+d.serial+"')")
        # 修改设备到当前状态
        self.devices.updateDeviceStatus(d.serial, '空闲')
        self.mysqlUtil.close()
        return index

    """
        添加公开小组
        参数（集合）：
            [{  
            必传：
                msg : 搜索条件（集合）
                num : 添加小组个数
                sleepTime : 每次添加好友间隔时间（s）
            可选：
                city ：城市
                school ： 学校
            }, {...}, {...}]
    """
    def add_tream(self, d, params=None):
        result_dict = {}
        result_dict['type'] = 'add_friends'
        sc.send_short_msg(bytes(json.dumps(self.pf.return_result(True, 'The task will be executed in 2 minutes', result_dict)), encoding='utf-8'))
        time.sleep(120)
        listMap = params['param']
        temp = listMap[0]
        temp['userId'] = params['userId']
        result_dict['num'] = self.add_one_tream(d, temp)
        sc.send_short_msg(bytes(json.dumps(self.pf.return_result(True, '', result_dict)), encoding='utf-8'))
        listMap.pop(0)
        if len(listMap) == 0:
            params['scheduler'].shutdown()

    """
        添加当个公开小组
            必传：
                msg : 搜索条件（集合）
                num : 添加小组个数
                sleepTime : 每次添加好友间隔时间（s）
            可选：
                city ：城市
                school ： 学校
    """
    def add_one_tream(self, d, params={}):
        self.mysqlUtil.start()
        self.devices.updateDeviceStatus(d.serial, '工作中')

        userId = params['userId']
        msg = params['msg']
        num = int(params['num'])
        self.add_public(d, msg)

        d.implicitly_wait(10.0)
        d(description="小组").click()
        time.sleep(5)
        d(description="筛选条件").click()
        time.sleep(.5)
        # 城市
        if 'city' in params.keys() and params['city']:
            d(description="城市, 任何地点").click()
            d(text="搜索城市").click()
            d.send_keys(params['city'], clear=True)
            time.sleep(2)
            d.xpath('//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]').click()
            # 不存在搜索结果
            if not d(description="重置").exists():
                time.sleep(2)
                d(description="返回").click()
                d(description="返回").click()

        # 选择 公开小组
        d.xpath(
            '//*[@resource-id="android:id/content"]/android.view.ViewGroup[1]/android.view.ViewGroup[4]').click()
        time.sleep(1)
        d(description="显示结果").click()
        time.sleep(2)

        index = 0
        while index < num:
            try:
                d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/'
                        'android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/'
                        'android.view.ViewGroup[1]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView[1]/'
                        'android.view.ViewGroup[' + str(
                    index + 1) + ']/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
                d(description="加入小组").click()
            except:
                continue
            index += 1
            time.sleep(float(params['sleepTime']))

        # 返回主页
        self.returnHomePage(d)
        self.mysqlUtil.cudSql("insert into add_info(add_type, add_key, add_num, user_id, device_id) values (1, '" + msg + "', " + str(index) + ", " + str(userId) + ", '" + d.serial + "')")
        # 修改设备到当前状态
        self.devices.updateDeviceStatus(d.serial, '空闲')
        self.mysqlUtil.close()
        return index