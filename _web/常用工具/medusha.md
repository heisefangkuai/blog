# Medusa v2.2 翻译和使用

## 语法

```linux
Medusa [-h host|-H file] [-u username|-U file] [-p password|-P file] [-C file] -M module [OPT]
```

## 选项

```linux
-h [TEXT]    : 目标主机名或IP地址
-H [FILE]    : 包含目标主机名或IP地址的文件
-u [TEXT]    : 用户名来测试
-U [FILE]    : 包含要测试的用户名的文件
-p [TEXT]    : 密码来测试
-P [FILE]    : 包含要测试的密码的文件
-C [FILE]    : 包含组合项的文件。更多信息请参见自述。
-O [FILE]    : 将日志信息附加到的文件
-e [n/s/ns]  : 附加密码检查 ([n] 无密码, [s] Password = Username)
-M [TEXT]    : 要执行的模块的名称 (没有.mod扩展名)
-m [TEXT]    : 传递给模块的参数。这可以用a多次传递，每次的参数不同，它们都会被发送到模块 (i.e. -m Param1 -m Param2, etc.)
-d           : 转储所有已知模块
-n [NUM]     : 用于非默认TCP端口号
-s           : 启用SSL
-g [NUM]     : 尝试连接数秒后放弃 (default 3)
-r [NUM]     : 重试之间的睡眠时间 (default 3)
-R [NUM]     : 尝试NUM重试后再放弃。尝试的总数将是NUM + 1。
-c [NUM]     : 在usec中等待验证套接字是否可用的时间 (default 500 usec).
-t [NUM]     : 同时测试的登录总数
-T [NUM]     : 同时测试的主机总数
-L           : 使用每个线程一个用户名并行化登录。默认值是在继续之前处理整个用户名。
-f           : 找到第一个有效的用户名/密码后，停止扫描主机。
-F           : 在任何主机上找到第一个有效的用户名/密码后停止审计。
-b           : 抑制启动横幅
-q           : 显示模块的使用信息
-v [NUM]     : 详细的级别 [0 - 6 (more)]
-w [NUM]     : 错误调试级别 [0 - 10 (more)]
-V           : 显示版本
-Z [TEXT]    : 基于先前扫描的地图进行恢复扫描
```

## 例子

```linux
1、指定用户名于密码于服务进行破解
medusa -M ssh -u root -p owaspbwa -h 192.168.72.142

2、指定文件进行破解
medusa -M ssh -u root -P passlist.txt -h 192.168.72.142

3、指定用户列表文件
medusa -M ssh -U userlist.txt -P passlist.txt -h 192.168.72.142

4、同时我们也可以将见用户改为文件，同时我们也将线程数调为5，
medusa -M ssh -U userlist.txt -P passlist.txt -H server.txt -t 5
```
