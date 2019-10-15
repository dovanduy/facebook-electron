#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/8 0008 15:19
# @Author   :lyh
# @Desc     : 公共函数
import devices

class PublicFuncation:
    def __init__(self):
        self.devices = devices.Devices()

    """
        获取设备信息
    """
    def find_PhoneInfo(self, phoneMap):
        resultMap = {}
        for key in phoneMap.keys():
            d = phoneMap[key]
            # 设备详细信息 (字典数据)
            phoneInfo = d.device_info
            params = {}
            # 设备号
            params['device_id'] = key
            # 设备型号
            params['device_model'] = phoneInfo['model']
            # 设备备注
            params['device_remark'] = ''
            # 设备登陆fb账号的账号昵称
            params['fb_nickName'] = ''


            # 判断设备是否未新设备
            if not self.devices.isExistsDevice(key):
                # 不存在 将设备添加到数据库
                # 设备状态
                params['device_status'] = '空闲'
                self.devices.addDevice(params)
                # 设置添加好友数和小组数
                params['friendNum'] = 0
                params['treamNum'] = 0
            else:
                # 存在 获取 当前设备状态 当天添加好友数和小组数
                result = self.devices.findDevice(key)
                # 设备状态
                params['device_status'] = result[4]
                # 设备备注
                params['device_remark'] = result[3]
                # 设备登陆fb账号的账号昵称
                params['fb_nickName'] = result[5]
                result = self.devices.findNowDataAddNum(key)
                params['friendNum'] = 0
                params['treamNum'] = 0
                for tempResult in result:
                    # 添加类型（0---添加好友，1---添加小组）
                    if tempResult[0] == 1:
                        params['treamNum'] = int(tempResult[1])
                    else:
                        params['friendNum'] = int(tempResult[1])
            params['for_screen'] = 'http://' + d.wlan_ip + ':7912/remote'
            resultMap[key] = params
        return self.return_result(True, '', resultMap)

    """
        返回结果
            success：是否成功
            msg：错误/失败消息
            data：成功结果数据
    """
    def return_result(self, success, msg, data):
        result = {}
        result['success'] = success
        result['msg'] = msg
        result['data'] = data
        return result