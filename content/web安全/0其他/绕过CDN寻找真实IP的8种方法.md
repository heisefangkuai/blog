# 绕过CDN寻找真实IP的8种方法

一、DNS历史解析记录

查询域名的历史解析记录，可能会找到网站使用CDN前的解析记录，从而获取真实ip，相关查询的网站有：

```l
iphistory：https://viewdns.info/iphistory/
DNS查询：（https://dnsdb.io/zh-cn/）
微步在线：（https://x.threatbook.cn/）
域名查询：（https://site.ip138.com/）
DNS历史查询：（https://securitytrails.com/）
Netcraft：https://sitereport.netcraft.com/?url=github.com
```

二、查找子域名

很多时候，一些重要的站点会做CDN，而一些子域名站点并没有加入CDN，而且跟主站在同一个C段内，这时候，就可以通过查找子域名来查找网站的真实IP。

常用的子域名查找方法和工具：

1、搜索引擎查询：如Google、baidu、Bing等传统搜索引擎，site:baidu.com inurl:baidu.com，搜target.com|公司名字。

2、一些在线查询工具，如：

```l
http://tool.chinaz.com/subdomain/
http://i.links.cn/subdomain/
http://subdomain.chaxun.la/
http://searchdns.netcraft.com/
https://www.virustotal.com/
```

3、 子域名爆破工具

```l
Layer子域名挖掘机
wydomain：https://github.com/ring04h/wydomain
subDomainsBrute:https://github.com/lijiejie/
Sublist3r:https://github.com/aboul3la/Sublist3r
```

三、网站邮件头信息

比如说，邮箱注册，邮箱找回密码、RSS邮件订阅等功能场景，通过网站给自己发送邮件，从而让目标主动暴露他们的真实的IP，查看邮件头信息，获取到网站的真实IP。

四、网络空间安全引擎搜索

通过关键字或网站域名，就可以找出被收录的IP，很多时候获取到的就是网站的真实IP。

```l
钟馗之眼：https://www.zoomeye.org
Shodan：https://www.shodan.io
Fofa：https://fofa.so
```

五、利用SSL证书寻找真实IP

证书颁发机构(CA)必须将他们发布的每个SSL/TLS证书发布到公共日志中，SSL/TLS证书通常包含域名、子域名和电子邮件地址。因此SSL/TLS证书成为了攻击者的切入点。

```l
SSL证书搜索引擎：https://censys.io/ipv4?q=github.com
```

六、国外主机解析域名

大部分 CDN 厂商因为各种原因只做了国内的线路，而针对国外的线路可能几乎没有，此时我们使用国外的DNS查询，很可能获取到真实IP。

```l
国外多PING测试工具：
https://asm.ca.com/zh_cn/ping.php
http://host-tracker.com/
http://www.webpagetest.org/
https://dnscheck.pingdom.com/
```

七、扫描全网

通过Zmap、masscan等工具对整个互联网发起扫描，针对扫描结果进行关键字查找，获取网站真实IP。

1、ZMap号称是最快的互联网扫描工具，能够在45分钟扫遍全网。
https://github.com/zmap/zmap

2、Masscan号称是最快的互联网端口扫描器，最快可以在六分钟内扫遍互联网。
https://github.com/robertdavidgraham/masscan

八、配置不当导致绕过

在配置CDN的时候，需要指定域名、端口等信息，有时候小小的配置细节就容易导致CDN防护被绕过。
案例1：为了方便用户访问，我们常常将www.test.com 和 test.com 解析到同一个站点，而CDN只配置了www.test.com，通过访问test.com，就可以绕过 CDN 了。
案例2：站点同时支持http和https访问，CDN只配置 https协议，那么这时访问http就可以轻易绕过。
