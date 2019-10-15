#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/8 0008 16:49
# @Author   :lyh
# @Desc     :md5 加密
import hashlib


class MD5Utils:
    """
        加密
    """

    def encryption(self, content):
        # 盐
        salt = b'domita'
        md5 = hashlib.md5(salt)
        md5.update(str(content).encode('utf-8'))
        return md5.hexdigest()
