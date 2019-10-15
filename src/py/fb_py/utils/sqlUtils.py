#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/8 0008 16:25
# @Author   :lyh
# @Desc     :连接数据
import pymysql


class SqlUtils:

    def start(self):
        self.db = pymysql.connect('127.0.0.1', 'root', '123456', 'py_fb')
        # self.db = pymysql.connect('rm-m5el4jn44c6ntnu18wo.mysql.rds.aliyuncs.com', 'smis_dev', 'Domita@2020', 'py_fb')
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()

    """
        查询
    """
    def selectSql(self, sql=''):
        try:
            self.cursor.execute(sql)
            # 获取结果列表
            result = self.cursor.fetchall()
            return result
        except:
            return ''

    """
        添加/修改/删除
    """
    def cudSql(self, sql=''):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except:
            # 回滚
            self.db.rollback()
            return False