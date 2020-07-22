# -*- coding:utf-8 -*-

from burp import IBurpExtender
from burp import IHttpListener
from java.io import PrintWriter

class BurpExtender(IBurpExtender, IHttpListener):

    def registerExtenderCallbacks(self, callbacks):
        self._cb = callbacks
        print 'aaaaaaahello burp!'
        # 将自己注册为HTTP侦听器
        callbacks.registerHttpListener(self)
        # 获取我们的输出流
        self._stdout = PrintWriter(callbacks.getStdout(), True)


    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        print( messageInfo.getResponse())