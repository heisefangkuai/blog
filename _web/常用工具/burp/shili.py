#coding=utf8
from burp import IBurpExtender
from burp import IHttpListener
from burp import IHttpRequestResponse
from burp import IResponseInfo
from burp import IRequestInfo
from burp import IHttpService
import re

# 类BurpExtender (Required)包含用于与Burp套件API交互的所有函数
print 'Thinking\'s find JSON callback Bui~'

class BurpExtender(IBurpExtender, IHttpListener):
   # define registerExtenderCallbacks: From IBurpExtender Interface 
   def registerExtenderCallbacks(self, callbacks):
       # keep a reference to our callbacks object (Burp Extensibility Feature)
       self._callbacks = callbacks
       # obtain an extension helpers object (Burp Extensibility Feature)
       # [http://portswigger.net/burp/extender/api/burp/IExtensionHelpers.html](http://portswigger.net/burp/extender/api/burp/IExtensionHelpers.html)
       self._helpers = callbacks.getHelpers()
       # set our extension name that will display in Extender Tab
       self._callbacks.setExtensionName("find JSON callback")
       # register ourselves as an HTTP listener
       callbacks.registerHttpListener(self)
   # define processHttpMessage: From IHttpListener Interface 
   def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
       # determine what tool we would like to pass though our extension:
       if toolFlag == 64 or toolFlag == 16 or toolFlag == 8 or toolFlag == 4: #if tool is Proxy Tab or repeater
           # determine if request or response:
           if not messageIsRequest:#only handle responses
               #获取响应包的数据
               response = messageInfo.getResponse()
               analyzedResponse = self._helpers.analyzeResponse(response) # returns IResponseInfo
               response_headers = analyzedResponse.getHeaders()
               response_bodys = response[analyzedResponse.getBodyOffset():].tostring()
               response_StatusCode = analyzedResponse.getStatusCode()
               #获取请求包的数据
               resquest = messageInfo.getRequest()
               analyzedRequest = self._helpers.analyzeResponse(resquest)
               request_header = analyzedRequest.getHeaders()
               request_bodys = resquest[analyzedRequest.getBodyOffset():].tostring()
               #获取服务信息
               httpService = messageInfo.getHttpService()
               port = httpService.getPort()
               host = httpService.getHost()
               #第一种情况：url中带有callback,且返回的是json数据。
               expressionA = r'.*(callback).*'
               expressionB = r'.*(application/json|application/javascript).*'
               expressionC = r'.*(text/html|application/javascript).*'
               for rqheader in request_header:
                   if rqheader.startswith("Host"):
                       rqhost = rqheader
                       break
               ishtml = 0        
               for rpheader in response_headers:
                   if rpheader.startswith("Content-Type:")  and re.match(expressionC,rpheader):
                       ishtml = 1
                   if rpheader.startswith("Content-Type:")  and  re.match(expressionB,rpheader):                            
                       if re.match(expressionA,request_header[0]):
                           print '='*10,'[success|有callback且返回json数据]','='*10,'\n\n[Host]',rqhost,port,'\n\n[URI]',request_header[0],'\n\n[ResponseBody]',response_bodys[0:30],'\n\n\n'
                           break
               #第二种情况：url中没有带callback,但是通过添加callback参数后，便返回了带方法名的json数据。
               if not re.match(expressionA,request_header[0]):
                   new_headers = request_header
                   if '?' in new_headers[0]:
                       new_headers[0] = new_headers[0].replace('?','?callback=BuiBui&')
                   else:
                       new_headers[0] = new_headers[0][:-9] +'?callback=BuiBui'
                   req = self._helpers.buildHttpMessage(new_headers, request_bodys) 
                   ishttps = False
                   if port == 443:
                       ishttps = True
                   if response_StatusCode == 200 and ishtml == 1:  
                       rep = self._callbacks.makeHttpRequest(host, port, ishttps, req)
                       #TODO 在某些情况下makeHttpRequest时候会出现一些bug,得到的结果但是取不到response,很奇怪(已经解决,404页面取不到正文返回包)
                       #新的请求请求包
                       analyzedreq = self._helpers.analyzeResponse(rep)
                       req_headers = analyzedreq.getHeaders()
                       req_bodys = rep[analyzedreq.getBodyOffset():].tostring()
                       #新的请求响应包
                       analyzedrep = self._helpers.analyzeResponse(rep)
                       rep_headers = analyzedrep.getHeaders()
                       rep_bodys = rep[analyzedrep.getBodyOffset():].tostring()
                       if 'BuiBui' in rep_bodys:
                           for repheader in rep_headers:
                               if repheader.startswith("Content-Type:")  and  re.match(expressionB,repheader):
                                   print '='*10,'[success|发现隐藏callback且返回json数据]','='*10,'\n\n[Host]',rqhost,port,'\n\n[URI]',req_headers[0],'\n\n[ResponseBody]',rep_bodys[0:30],'\n\n\n'
                                   break