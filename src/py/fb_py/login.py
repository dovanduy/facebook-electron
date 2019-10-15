#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/8 0008 15:34
# @Author   :lyh
# @Desc     :登陆
import utils.md5Utils as md5Utils
import utils.sqlUtils as sqlUtils
import publicFunction


class Login:
    def __init__(self):
        self.mysqlUtils = sqlUtils.SqlUtils()
        self.pf = publicFunction.PublicFuncation()
        self.md5 = md5Utils.MD5Utils()

    """
        登陆
            account : 账号
            pwd : 密码
    """
    def login(self, params={}):
        self.mysqlUtils.start()
        # 密码加密
        pwd = self.md5.encryption(params['pwd'])
        sql = "select * from user_info where account = '" + params['account'] + "' and pwd = '" + pwd + "'"
        result = self.mysqlUtils.selectSql(sql)
        if result == '' or len(result) == 0:
            self.mysqlUtils.close()
            return self.pf.return_result(False, '登陆失败', '')
        else:
            data = {}
            data['userId'] = result[0][0]
            data['userName'] = result[0][1]
            if not result[0][3]:
                print('普通员工（非管理员）')
                # 用户所在小组名称
                # data['treamName'] = self.mysqlUtils.selectSql("select * from tream_info where id = " + result[0][3])[0][1]
            self.mysqlUtils.close()
            return self.pf.return_result(True, '登陆成功', data)

    """
        注册
            account : 账号
            pwd : 密码
            tream_id ：小组id
   """
    def reg(self, params={}):
        self.mysqlUtils.start()
        # 查询账号是否存在
        sql = "select * from user_info where account = '" + params['account'] + "'"
        result = self.mysqlUtils.selectSql(sql)
        if result == '' or len(result) != 0:
            self.mysqlUtils.close()
            return self.pf.return_result(False, '注册失败(该：{account}账号已存在)'.format(account=params['account']), '')

        # 密码加密
        pwd = self.md5.encryption(params['pwd'])
        # 插入数据
        sql = "insert into user_info(account, pwd) values('" + params['account'] + "', '" + pwd +"')"
        #sql = "insert into user_info(account, pwd, tream_id) values('" + params['account'] + "', '" + pwd + "', " + params['tream_id'] + ")"
        result = self.mysqlUtils.cudSql(sql)
        self.mysqlUtils.close()
        if result:
            return self.pf.return_result(True, '注册成功', '')
        else:
            return self.pf.return_result(False, '注册失败', '')