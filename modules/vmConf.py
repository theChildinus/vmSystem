#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# VmConf类
# 用户配置的信息


"""
@author:    chenkuan
@license:   GNU General Public License 2.0
@contact:   chen1511@foxmail.com
@version:   1.0-2016-07-18
"""

import json
import vmState

class VmConf(object):
    """
    This is the class that save the vm information from the GUI
    """
    def __init__(self):
        self.clearConf()

    def clearConf(self):
        self.name = ""
        self.systype = ""

        self.processes = {}  # 监控级别应放在process属性里, str:int，进程名：处理等级
        self.ports = {}  # 监控级别应放在port属性里

        self.checkRootkit = False
        #self.ssdt = []

    def getConf(self):
        """
        从类对象中获得全部属性
        :return:
        """
        return [var for var in vars(self).values()]

    def setConf(self, **kwargs):
        """
        将Conf的各属性存入类对象
        :param kwargs:
        :return:
        """

    def getConfFromFile(self):
        """
        # 从文件中读取json数据，读出来是dict
        # 将类对象中所有属性更新
        :return:
        """
        self.clearConf()
        try:
            with open(self.name + ".json", "r") as f:
                attr_dict = json.load(f)
                #将attr_dict中的所有属性分配到当前类中
                for key, value in attr_dict:
                    if hasattr(self, key):
                        setattr(self, key, value)
                    else:
                        #类中没有此属性？？？不可能
                        pass
        except IOError, e:
            #没有此文件的话不管它，直接清空Conf
            pass


    def setConfToFile(self):
        """
        # 将类所有属性序列化到json文件中
        :return:
        """
        with open(self.name + ".json", "w") as f:
            json.dump(vars(self), f)