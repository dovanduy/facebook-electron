#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/9 0009 16:05
# @Author   :lyh
# @Desc     :设备信息
import utils.sqlUtils as sqlUtils


class Devices:
    def __init__(self):
        self.mysqlUtils = sqlUtils.SqlUtils()

    """
       获取单个设备 
    """
    def findDevice(self, device_id):
        self.mysqlUtils.start()
        result = self.mysqlUtils.selectSql("select * from devices_info where device_id = '" + device_id + "'")[0]
        self.mysqlUtils.close()
        return result

    """
        获取设备当天添加的人
    """
    def findNowDataAddNum(self, device_id):
        self.mysqlUtils.start()
        result = self.mysqlUtils.selectSql("select add_type, sum(add_num) from add_info where date(create_time) = CURDATE() and device_id = '"+device_id+"' GROUP BY add_type ")
        self.mysqlUtils.close()
        return result

    """
        判断是否存在该设备
    """
    def isExistsDevice(self, device_id):
        self.mysqlUtils.start()
        result = self.mysqlUtils.selectSql("select * from devices_info where device_id = '" + device_id + "'")
        self.mysqlUtils.close()
        if result == '' or len(result) == 0:
            result = False
        else:
            result = True
        return result

    """
        添加设备
    """
    def addDevice(self, params={}):
        self.mysqlUtils.start()
        result = self.mysqlUtils.cudSql("insert into devices_info(device_id, device_model, device_remark, device_status, fb_nickName) values ('"+params['device_id']+"', '"+params['device_model']+"', '"+params['device_remark']+"', '"+params['device_status']+"', '"+params['fb_nickName']+"')")
        self.mysqlUtils.close()
        return result

    """
        修改设备 备注、fb账号昵称
    """
    def updateRemarkAndfbNick(self, device_id, remark, fbNick):
        self.mysqlUtils.start()
        result = self.mysqlUtils.cudSql("update devices_info set device_remark='"+remark+"', fb_nickName='"+fbNick+"' where device_id='"+device_id+"'")
        self.mysqlUtils.close()
        return result

    """
        修改设备状态
    """
    def updateDeviceStatus(self, device_id, device_status):
        self.mysqlUtils.start()
        result = self.mysqlUtils.cudSql("update devices_info set device_status='"+device_status+"' where device_id='"+device_id+"'")
        self.mysqlUtils.close()
        return result