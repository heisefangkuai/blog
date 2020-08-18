# Nmap

Nmap具体功能：端口扫描，协议扫描，漏洞扫描，绕过防护，漏洞利用等。

## 端口状态

- 公认端口：0--1024
- 注册端口：1025--49151。
- 动态和/或私有端口：49152--65535。

- Open：端口开启，有程序监听此端口
- Closed：端口关闭，数据能到达主机，但是没有程序监听此端口
- Filtered：数据未能到达主机
- Unfiltered：数据能到达主机，但是Nmap无法判断端口开启还是关闭
- Open | filtered：端口没返回值，主要出现在UDP，IP，FIN，NULL和Xmas扫描
- Closed | filtered：只出现在IP ID idle 扫描

## 扫描方法

- 单个扫描：nmap 192.168.1.1
- 多个扫描：nmap 192.168.1.1 192.168.1.2
- 网段扫描：nmap 192.168.2.1-192.168.2.100
- C段扫描： Nmap  192.168.0.1/24
- 导入扫描：nmap -iL [test.txt]
- 排除扫描：Nmap 192.168.0.0/24 --exclude 192.168.0.2
- 随机扫描：Nmap -sn -iR 3

## 主机发现技术

- -sn：不对目标的端口和其他信息进行扫描
- -PR：ARP协议的主机发现
- -PE：ICMP协议的主机发现，这个过程实质上和ping是一样的
- -PP：ICMP协议的时间戳主机发现
- -PM：ICMP协议的地址掩码主机发现
- -PU：UDP协议的主机发现，可靠性不高
- -PS：TCP SYN扫描，三次握手实现
- -PA：TCP ACK扫描，三次握手实现
- -PY：SCTP协议的主机发现，4次握手的机制实现的
- -PO：IP协议进行主机地址发现
- -PN：不进行Ping扫描
- -R：无论是否是活跃主机所对应的域名都列出来
- -n：取消对域名的转换
- --data-length：添加随机数据的数据包
- --dns-servers：不在自己的DNS服务器留下查询的记录
- --packet-trace：观察Nmap发出了哪些数据包，收到了哪些数据包

## 端口扫描

-sS：TCP SYN扫描，没有完成三次握手（匿名扫描，默认不加类型，需要root权限，扫描速度快）
-sT：Connect扫描，完成了TCP的三次握手（不需要root权限，TCP扫描的默认模式，端口状态和SYN相同，耗时长）
-sU：UDP扫描，速度慢
-sF：TCP FIN扫描
-sN：TCP NULL扫描，向目标端口发送一个不包含任何标志的数据包
-sX：TCP Xmas Tree扫描，向目标端口发送一个含有FIN、URG和PUSH标志的数据包
-sI：idle扫描，伪装成 “第三方” 使自己不被发现
-sV：指定nmap进行版本探测
-O：nmap进行OS探测
-F：扫描常见的100个端口
-p：指定某一个端口(-p 80/–p http/-p *)

## nmap常用的扫描命令

```nmap
查找网络中的所有活动IP地址
nmap -sP 192.168.0.*

获取远程主机的端口和OS检测的信息
nmap -sS -P0 -sV -O ip

获取打开特定端口的服务器列表
nmap -sT -p 80 -oG – 192.168.1.* | grep open
```

## nmap脚本分类

Nmap提供了强大的脚本引擎（NSE），以支持通过Lua编程来扩展Nmap的功能。

- auth          处理身份验证
- broadcast     网络广播
- brute         暴力猜解
- default       默认
- discovery     服务发现
- dos           拒绝服务
- exploit       漏洞利用
- external      外部扩展
- fuzzer        模糊测试
- intrusive     入侵检测,扫描可能造成不良后果
- malware       检测后门
- safe          扫描危害较小
- version       版本识别
- vuln          漏洞检测

参数说明：

- -sC 是指的是采用默认配置扫描，与--script=default参数等价
- --script=脚本名称：脚本一般都在Nmap的安装目录下的scripts目录中
- --script-args=key1=value1,key2=value2...：来传递脚本需要的参数，key1名=value1值，例如：nmap --script=http-enum --script-args 'http-enum.basepath=admin'
- –script-args-file=filename，使用文件来为脚本提供参数。
- --script-trace 如果设置该参数，则所有的脚本收发请求过程。
- --script-updatedb：更新scripts目录中的扩展脚本
- --script-help=脚本名称：输出该脚本的使用参数，以及详细介绍信息。

```nmap
默认脚本扫描
nmap --script=default ip

检查常见漏洞
nmap --script=vuln ip

暴力破解数据库、smb、snmp等
nmap --script=brute ip

特定FTP协议进行密码爆破
nmap --script=ftp-brute.nse ip

利用第三方的数据库或资源
nmap --script=external ip
```

### 扩展执行流程

调用任何一个扩展脚本会首先执行 /nmap/nse_main.lua ，该脚本主要做了以下几件事：

- 加载一些Nmap的核心库（nselib文件夹中）
- 定义多线程函数
- 定义输出结果处理函数
- 读取、加载扩展脚本
- 定义扩展脚本函数接口
- 执行扩展脚本
- ……

在第一行添加：

print("[*] nse_main.lua first excute ... \n")

保存后，使用一个脚本观察效果。

### 扩展脚本执行规则

在nse_main.lua的64行左右，定义了一些规则：

```nmap
-- Table of different supported rules.
local NSE_SCRIPT_RULES = {
  prerule = "prerule",      # prerule 在扫描任何主机之前运行一次
  hostrule = "hostrule",    # hostrule 在扫描一个主机后运行一次
  portrule = "portrule",    # portrule 在扫描一个主机的端口后运行一次
  postrule = "postrule",    # postrule 在全部扫描完毕以后运行一次
};
```

验证结论，写了一个测试脚本 /nmap/scripts/test.nse ，内容如下：

```nmap
prerule=function()
    print("prerule()")
end
hostrule=function(host)
    print("hostrule()")
end
portrule=function(host,port)
    print("portrule()")
end
action=function()
    print("action()")
end
postrule=function()
    print("postrule()")
end
```

nmap扫描调用这个脚本看看执行效果：

```nmap
C:\Users\Administrator>nmap --script=1test www.fake-blog.com
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 14:04 ?D1ú±ê×?ê±??
prerule()
portrule()
hostrule()
portrule()
portrule()
portrule()
Nmap scan report for www.fake-blog.com (139.129.149.54)
Host is up (0.034s latency).
Not shown: 995 filtered ports
PORT     STATE  SERVICE
21/tcp   open   ftp
80/tcp   open   http
443/tcp  open   https
1433/tcp closed ms-sql-s    # 这个端口不是开发的，所有没有执行portrule()
3306/tcp open   mysql

postrule()
Nmap done: 1 IP address (1 host up) scanned in 15.85 seconds
```

也就是说，prerule和postrule是在开始和结束运行，并且只运行一次，hostrule是扫描一个主机就运行一次，有N个主机就会运行N次，portrule是扫描到一个端口就运行一次，有N个端口就运行N次。

### 扩展脚本 action函数

action函数，它的主要作用是用于在portrule或hostrule返回true之后自动执行的函数。

测试脚本：

```nmap
local stdnse = require "stdnse"
prerule=function()
end
hostrule=function(host)
    return true
end
portrule=function(host,port)
    return true
end
action = function()
    print("[*]action ...")
end
postrule=function()
end
```

nmap扫描调用这个脚本看看执行效果：

```nmap
C:\Users\Administrator>nmap --script=1test www.fake-blog.com
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 14:23 ?D1ú±ê×?ê±??
[*]action ...
[*]action ...
[*]action ...
[*]action ...
[*]action ...
Nmap scan report for www.fake-blog.com (139.129.149.54)
Host is up (0.036s latency).
Not shown: 995 filtered ports
PORT     STATE  SERVICE
21/tcp   open   ftp
80/tcp   open   http
443/tcp  open   https
1433/tcp closed ms-sql-s
3306/tcp open   mysql

Nmap done: 1 IP address (1 host up) scanned in 17.10 seconds
```

可以看出有一个端口没有开启，不会执行，所以一个主机加四个端口，正好执行的五次

### lua的基本参数

description = [[
description字段应包含描述脚本功能的段落或更多段落
]]
