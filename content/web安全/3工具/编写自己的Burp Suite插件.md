# 编写自己的Burp Suite插件

Burp Suite的强大除了自身提供了丰富的可供测试人员使用的功能外，其提供的支持第三方拓展插件的功能也极大地方便使用者编写自己的自定义插件。

Burp Suite支持的插件类型有Java、Python、Ruby三种。无论哪种语言的实现，开发者只要选择自己熟悉的语言，按照接口规范去实现想要的功能即可。

github插件搜索：<https://github.com/search?l=Python&q=IBurpExtender&type=Code>

## API介绍

1. 插件入口和帮助接口类**4**
    IBurpExtender               # Burp插件的入口，所有Burp的插件均需要实现此接口
    IBurpExtenderCallbacks      # IBurpExtender接口的实现类
    IExtensionHelpers           # 帮助接口
    IExtensionStateListener     # 管理操作接口

2. UI相关接口类**6**：主要是定义Burp插件的UI显示和动作的处理事件，主要是软件交互中使用
    IContextMenuFactory
    IContextMenuInvocation
    ITab
    ITextEditor
    IMessageEditor
    IMenuItemHandler

3. Burp工具组件接口类**13**：Burp Suite工具组件接口类
    IInterceptedProxyMessage
    IIntruderAttack
    IIntruderPayloadGenerator
    IIntruderPayloadGeneratorFactory
    IIntruderPayloadProcessor
    IProxyListener
    IScanIssue
    IScannerCheck
    IScannerInsertionPoint
    IScannerInsertionPointProvider
    IScannerListener
    IScanQueueItem
    IScopeChangeListener

4. http消息处理接口类**9**：处理Cookie、Request、Response、Parameter等消息头接口类
    ICookie
    IHttpListener
    IHttpRequestResponse
    IHttpRequestResponsePersisted
    IHttpRequestResponseWithMarkers
    IHttpService
    IRequestInfo
    IParameter
    IResponseInfo

5. 不知道是啥的**9**
    IBurpCollaboratorClientContext
    IBurpCollaboratorInteraction
    IMessageEditorController
    IMessageEditorTab
    IMessageEditorTabFactory
    IResponseKeywords
    IResponseVariations
    ISessionHandlingAction
    ITempFile

通过对Burp插件 API的功能划分，对API的接口有一个初步的认知，知道在使用某个功能时，可以去哪个接口类中寻找相应的接口定义来做自己的实现。例如。我们想显示一个Tab页界面，那么肯定是要实现ITab接口；如果需要对消息进行编辑修改，则需要实现IMessageEditor接口；需要使用payload生成器，则需要实现IIntruderPayloadGenerator接口。通过接口分类后再找具体的接口定义的方法，可以帮助我们在不太熟悉Burp 插件API的情况下，更快地开发出自己需要的插件。

官方给出了简单的插件示例，包括java，python，ruby版本
<https://portswigger.net/burp/extender#SampleExtensions>

## 接口类

### IBurpExtender

所有插件必须实现这个接口，类名字必须为“BurpExtender”，并且必须提供一个默认构造器”。
IBurpExtender用来在burp上面注册扩展，IBurpExtender里面还有一个registerExtenderCallbakcs类方法需要实现：

例如设置插件名称

```python
class BurpExtender(IBurpExtender,IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self,callbacks):
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("插件名称")
        print 'aaaaaaahello burp!'  # 输出
```

## 接口类方法

### registerExtenderCallbacks

该类中有个registerExtenderCallbacks方法，该方法在插件被加载后会被调用，在所有扩展插件中必须实现这个接口。

python的调用方法，python需要对这个方法传入的参数进行处理，处理的是为了更加方便的调用基本接口的方法，这里就列出了一些方法，其他的可以参考IBurpExtenderCallbacks的内容。

```python
def registerExtenderCallbacks(self, callbacks):
       # 保留对回调对象的引用(Burp扩展特性)
       self._callbacks = callbacks
       # 获取一个扩展助手对象(Burp扩展特性)
       # [http://portswigger.net/burp/extender/api/burp/IExtensionHelpers.html](http://portswigger.net/burp/extender/api/burp/IExtensionHelpers.html)
       self._helpers = callbacks.getHelpers()
       # 设置将显示在Extender选项卡中的扩展名
       self._callbacks.setExtensionName("find JSON callback")
       # 将自己注册为HTTP侦听器
       callbacks.registerHttpListener(self)
```

### IHttpListener

该类是用来注册HTTP监听器，然后对获取到的请求或响应包进行处理，有个processHttpMessage的方法用于对请求和响应的数据包进行自定义操作，该方法在发送请求之前和接收响应之后会被调用。

```python
def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        # toolFlag  用于burp tool判断是否发出请求的flag
        # messageIsRequest  判断区分请求还是响应的flag
        # messageInfo   http包的具体细节，可以从中取得请求或者响应包的二进制流
       # 确定我们希望通过我们的扩展传递什么工具:
       # 如果工具是代理标签或中继器
       if toolFlag == 64 or toolFlag == 16 or toolFlag == 8 or toolFlag == 4:
           # 确定请求或响应:
           # 只处理响应
           if not messageIsRequest:
               #获取响应包的数据
               response = messageInfo.getResponse()
               analyzedResponse = self._helpers.analyzeResponse(response) # returns IResponseInfo
               response_headers = analyzedResponse.getHeaders()
               response_bodys = response[analyzedResponse.getBodyOffset():].tostring()
               #获取请求包的数据
               resquest = messageInfo.getRequest()
               analyzedRequest = self._helpers.analyzeResponse(resquest)
               request_header = analyzedRequest.getHeaders()
               request_bodys = resquest[analyzedResponse.getBodyOffset():].tostring()
```

### IHttpRequestResponse

该接口用来获取HTTP中请求和响应的HTTP信息，如果是响应包的HTTP信息，需要在请求被发送后才能获取到。
该接口有getComment(),getHighlight(),getHttpService(),getRequest(),getResponse(),setComment(java.lang.String comment),setHighlight(java.lang.String color),setHttpService(IHttpService httpService),setRequest(byte[] message),setResponse(byte[] message)
这些方法。可以直接在官方接口文档中查看。
其中getHttpService()方法会返回IHttpService的对象。如果需要获取协议，主机，端口信息的，就需要对IHttpService对象里相应的方法进行调用。

```python
httpService = messageInfo.getHttpService()
port = httpService.getPort()
host = httpService.getHost()
```

### IHttpService

该接口用来获取可以被发送的请求包的详细内容，有getHost(),getPort(),getProtocol这个三个方法。

```python
httpService = messageInfo.getHttpService()
port = httpService.getPort()
host = httpService.getHost()
```

### IResponseInfo

该接口是用来获取响应包的详细内容的，通过IExtensionHelpers.analyzeResponse()的方法调用该对象中的方法。

该接口有getBodyOffset(),getCookies(),getHeaders(),getInferredMimeType(),getStatedMimeType(),getStatusCode()的方法。

```python
response = messageInfo.getResponse()
analyzedResponse = self._helpers.analyzeResponse(response) # 返回 IResponseInfo
response_headers = analyzedResponse.getHeaders()
response_bodys = response[analyzedResponse.getBodyOffset():].tostring()
```

### IRequestInfo

该接口是用来获取请求包的详细内容的，通过IExtensionHelpers.analyzeRequest()的方法调用该对象中的方法。

该接口有getBodyOffset(),getContentType(),getHeaders(),getMethod(),getParameters(),getUrl()的方法。

```python
resquest = messageInfo.getRequest()
analyzedRequest = self._helpers.analyzeRequest(resquest)
request_header = analyzedRequest.getHeaders()
request_bodys = resquest[analyzedRequest.getBodyOffset():].tostring()
```

## 代码示例

一个Tab页的代码

```python
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
        # ITab名称
        return 'fake'

    def getUiComponent(self):
        return self.mainPanel
```

鼠标右键

```python
from burp import IBurpExtender
from burp import IContextMenuFactory
from javax.swing import JMenuItem
import threading

class BurpExtender(IBurpExtender,IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("Shodan Scan")
        self.callbacks.registerContextMenuFactory(self)
        return

    def createMenuItems(self,invocation):
        menu_list = []
        menu_list.append(JMenuItem("Scan with Shodan",None,actionPerformed= lambda x, inv=invocation:self.startThreaded(self.start_scan,inv)))
        return menu_list

    def startThreaded(self,func,*args):
        th = threading.Thread(target=func,args=args)
        th.start()

    def start_scan(self,invocation):
        print('aaaa')
```

接收响应数据包

```python
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
```






