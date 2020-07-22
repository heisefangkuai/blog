# Nmap脚本使用

Nmap提供了强大的脚本引擎（NSE），以支持通过Lua编程来扩展Nmap的功能。

NSE（Nmap Scripting Engine）是Nmap最为强大、最为灵活的功能之一。

NSE主要分为两大部分：内嵌Lua解释器与NSE library。

解释器：Nmap采用嵌入的Lua解释器来支持Lua脚本语言。Lua语言小巧简单而且扩展灵活，能够很好地与Nmap自身的C/C++语言融合。

NSE library：为Lua脚本与Nmap提供了连接，负责完成基本初始化及提供脚本调度、并发执行、IO框架及异常处理，并且提供了默认的实用的脚本程序。

## 脚本参数

```nmap
SCRIPT SCAN:
  -sC: equivalent to --script=default
  --script=<Lua scripts>: <Lua scripts> is a comma separated list of directories, script-files or script-categories
  --script-args=<n1=v1,[n2=v2,...]>: provide arguments to scripts
  --script-args-file=filename: provide NSE script args in a file
  --script-trace: Show all data sent and received
  --script-updatedb: Update the script database.
  --script-help=<Lua scripts>: Show help about scripts. <Lua scripts> is a comma-separated list of script-files or script-categories.
```

参数说明：

-sC 是指的是采用默认配置扫描，与--script=default参数等价

--script=脚本名称，脚本一般都在Nmap的安装目录下的scripts目录中

--script-args=key1=value1,key2=value2... 该参数是用来传递脚本里面的参数的，key1是参数名，该参数对应value1这个值，那么有更多的参数，使用逗号连接
例如：nmap --script=http-enum --script-args 'http-enum.basepath=admin'

–script-args-file=filename，使用文件来为脚本提供参数。 

--script-trace 如果设置该参数，则所有的脚本收发请求过程。

--script-updatedb 在Nmap的scripts目录里有一个script.db，该文件中保存了当前Nmap可用的脚本，类似于一个小型数据库，如果我们开启nmap并且调用了此参数，则nmap会自行扫描scripts目录中的扩展脚本，进行数据库更新。

--script-help=脚本名称，调用该参数后，Nmap会输出该脚本名称对应的脚本使用参数，以及详细介绍信息。

## Nmap扩展脚本分类

- auth          处理身份验证
- broadcast     网络广播
- brute         暴力猜解
- default       默认
- discovery     服务发现
- dos           拒绝服务
- exploit       漏洞利用
- external      外部扩展
- fuzzer        模糊测试
- intrusive     扫描可能造成不良后果
- malware       检测后门
- safe          扫描危害较小
- version       版本识别
- vuln          漏洞检测

## nmap 扩展

### mysql相关扩展

检查mysql空密码
nmap -p 3306 --script=mysql-empty-password.nse ip

暴力破解mysql
nmap -p 3306 --script=mysql-brute.nse ip

知道了用户名与密码，可以枚举数据库中的用户
nmap -p 3306 --script=mysql-users.nse --script-args=mysqluser=root ip

枚举mysql用户信息
nmap -p 3306 --script=mysql-enum.nse ip

扫描已知口令
nmap -sV --script=mysql-databases --script-args dbuser=root,dbpass=11111111 ip

### ssh项目

知道账号密码执行linux命令
nmap -p 22  --script=ssh-run --script-args="ssh-run.cmd=ls /, ssh-run.username=root, ssh-run.password=密码" ip


## 扩展执行流程

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

## 扩展脚本执行规则

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

## 扩展脚本 action函数

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

## lua的基本参数

description = [[
description字段应包含描述脚本功能的段落或更多段落
]]
