#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 导入 burp 接口
from burp import IBurpExtender, ITab

# 导入 Java 库
from javax.swing import JPanel
from javax.swing import JButton

class BurpExtender(IBurpExtender, ITab):

    def registerExtenderCallbacks(self, callbacks):
        self._cb = callbacks
        self._hp = callbacks.getHelpers()
        self._cb.setExtensionName('fake')
        print 'hello burp!'
        self.mainPanel = JPanel()
        # # 初始化一个 JButton 并绑定单击事件
        # self.testBtn = JButton('Click Me!', actionPerformed=self.testBtn_onClick)
        # self.mainPanel.add(self.testBtn)
        self._cb.customizeUiComponent(self.mainPanel)
        self._cb.addSuiteTab(self)

    # 实现 ITab 接口的 getTabCaption() 方法
    def getTabCaption(self):
        return 'ssss'

    def getUiComponent(self):
        return self.mainPanel