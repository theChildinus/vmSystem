#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# UserInterfaceController类
# 接受界面响应消息
# 对其管理的各个虚拟机调用方法生成相应线程进行处理



"""
@author:    chenkuan
@license:   GNU General Public License 2.0
@contact:   chen1511@foxmail.com
@version:   1.0-2016-07-21
"""

import sys
import json
import threading
import logging
logger = logging.getLogger()

#from PyQt4 import QtGui
#from view.vmGuiAction import VmGuiAction
from vmController import VmController

from modules.vmConf import VmConf
from modules.vmState import VmState


class UserInterfaceController(object):

    def __init__(self):
        #self.vms = []
        self.getVms()
        self.vmsConfs = {}
        self.vmsStates = {}
        for vm in self.vms:
            self.vmsConfs[vm] = VmConf(vm)
            #.vmsStates[vm] = VmState(vm)

        # 创建local对象，用来管理各个虚拟机
        self.localVm = threading.local()
        # 保存各线程的列表
        self.threadsVm = []
        # 保存各线程名称的列表
        self.threadsName = []

    def getVms(self):
        """
        #从libvmi中获取virt-manager中实际添加的虚拟机列表
        :return: list:
        """
        self.vms = ["win1", "win2", "win3"]
        #self.vms = []
        return self.vms

    def getVmtypes(self):
        """
        # 从volatility中获取可用的虚拟机类型
        :return:
        """
        self.vmtypes = ["CentOS65x64", "WinXPSP3x86", "Win7SP1x64"]
        return self.vmtypes

    def getVmsConfs(self, vmname):
        """
        #从文件中读取某个虚拟机配置信息
        #然后返回其所有属性值
        :return: tuple:
        """
        self.vmsConfs[vmname].getConfFromFile()
        return self.vmsConfs[vmname].getConf()

    def setVmsConfs(self, vmname, **kwargs):
        """
        #当界面更新配置时调用此方法
        #利用关键字参数传入所有configure属性
        :return:
        """
        # 将配置信息更新
        self.vmsConfs[vmname].setConf(kwargs)
        #将配置保存到文件
        self.vmsConfs[vmname].setConfToFile()

    def startMonitorVm(self, vmname):
        """
        #当界面开始监控某虚拟机时调用此方法
        #新开线程运行
        :return:
        """
        if str(vmname) not in self.threadsName:
            self.threadsVm.append(threading.Thread(target=self.generateSingleController, args=(vmname,), name="Thread-"+str(vmname)))
            self.threadsName.append(vmname)
            self.threadsVm[-1].start()
            logger.info(u"开始监控虚拟机" + unicode(vmname))
        else:
            logger.warning(u"虚拟机" + unicode(vmname) + u"已经处于监控状态")
        logger.debug(u"已有虚拟机监控列表：名称:" + unicode(self.threadsName) + u" 线程:" + unicode(self.threadsVm))


    def generateSingleController(self, vmname):
        """
        # 此方法用于生成单个控制器，将一系列参数传入,然后调用类方法开始监控
        :param vmname:
        :return:
        """
        #各个controller存在于各个线程内，互不干扰
        self.localVm.name = vmname
        self.localVm.controller = VmController(vmname, self.vmsConfs[vmname])
        #启动该线程对应的控制器
        #self.localVm.controller.startMonitor()