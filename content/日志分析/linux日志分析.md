# linux 日志分析

Linux 系统拥有非常灵活和强大的日志功能，可以保存几乎所有的操作记录，并可以从中检索出我们需要的信息。

## 日志简介

查看日志配置情况：more /etc/rsyslog.conf
日志默认存放位置：/var/log/

    /var/log/messages — 记录 Linux 内核消息及各种应用程序的公共日志信息
    /var/log/dmesg — 记录 Linux 操作系统在引导过程中的各种事件信息。可以用dmesg查看它们。
    /var/log/auth.log — 包含系统授权信息，包括用户登录和使用的权限机制等。
    /var/log/boot.log — 包含系统启动时的日志。
    /var/log/daemon.log — 包含各种系统后台守护进程日志信息。
    /var/log/dpkg.log – 包括安装或dpkg命令清除软件包的日志。
    /var/log/kern.log – 包含内核产生的日志，有助于在定制内核时解决问题。
    /var/log/maillog /var/log/mail.log — 记录进入或发出系统的电子邮件活动
    /var/log/user.log — 记录所有等级用户信息的日志。
    /var/log/Xorg.x.log — 来自X的日志信息。
    /var/log/alternatives.log – 更新替代信息都记录在这个文件中。
    /var/log/cups — 涉及所有打印信息的日志。
    /var/log/anaconda.log — 在安装Linux时，所有安装信息都储存在这个文件中。
    /var/log/yum.log — 包含使用yum安装的软件包信息。
    /var/log/cron — 记录 crond 计划任务产生的事件信息
    /var/log/faillog – 包含用户登录失败信息。此外，错误登录命令也会记录在本文件中。

除了上述Log文件以外， /var/log还基于系统的具体应用包含以下一些子目录：
    /var/log/httpd/或/var/log/apache2 — 包含服务器access_log和error_log信息。
    /var/log/lighttpd/ — 包含light HTTPD的access_log和error_log。
    /var/log/mail/ –  这个子目录包含邮件服务器的额外日志。
    /var/log/prelink/ — 包含.so文件被prelink修改的信息。
    /var/log/audit/ — 包含被 Linux audit daemon储存的信息。
    /var/log/samba/ – 包含由samba存储的信息。
    /var/log/sa/ — 包含每日由sysstat软件包收集的sar文件。
    /var/log/sssd/ – 用于守护进程安全服务。

比较重要的几个日志：
    登录失败记录：/var/log/btmp     //lastb
    最后一次登录：/var/log/lastlog  //lastlog
    登录成功记录: /var/log/wtmp     //last
    登录日志记录：/var/log/secure
    目前登录用户信息：/var/run/utmp  //w、who、users
    历史命令记录：history
    仅清理当前用户：history -c

## 日志的优先级别

数字等级越小，优先级越高，消息越重要。
0->EMERG -> 紧急->会导致主机系统不可用的情况
1->ALERT -> 警告->必须马上采取措施解决的问题
2->CRIT  -> 严重->比较严重的情况
3->ERR   -> 错误->运行出现错误
4->WARNING->提醒->可能影响系统功能，需要提醒用户的重要事件
5->NOTICE-> 注意->不会影响正常功能，但是需要注意的事件
6->INFO  -> 信息->一般信息
7->DEBUG -> 调试->程序或系统调试信息等

## 日志分析技巧

- 常用的shell命令

Linux 下常用的 shell 命令如：find、grep 、egrep、awk、sed

小技巧：

1、find命令

```linux
//在目录 /etc 中查找文件 init
find /etc -name init

根目录下所有.jsp后缀文件
find / -name *.jsp

最近3天修改过的文件
find -type f -mtime -3

最近3天创建的文件
find -type f -ctime -3
```

2、Grep 命令

```linux
grep -rn "hello,world!"
*: 表示当前目录所有文件，也可以是某个文件名
-r 是递归查找
-n 是显示行号
-R查找所有文件包含子目录
-i 忽略大小写

grep显示前后几行信息, 标准 unix/linux 下的 grep 通过下面參数控制上下文
grep -C 5 foo file 显示 file 文件里匹配 foo 字串那行以及上下 5 行
grep -B 5 foo file 显示 foo 及前 5 行
grep -A 5 foo file 显示 foo 及后 5 行
查看 grep 版本号的方法是 grep -V

grep "user hoover" /var/log/auth.log
grep -B 3 -A 2 'Invalid user' /var/log/auth.log
grep 'Invalid user' | tail -f /var/log/auth.log
grep "authentication failure" /var/log/auth.log | cut -d '=' -f 8
awk '/sshd.*invalid user/ { print $9 }' /var/log/auth.log

过滤出不带有某个关键词的行并输出行号
grep -nv 'root' /etc/passwd

查看根目录下 含有root信息的文件，并标注行号
grep -nr root /

查看根目录下后缀为.jsp .jspx文件，并从大到小排列
grep -nr -v "404" ./ | grep -E "\.jsp | \.jspx" | more
```

3、如何显示一个文件的某几行：

```linux
从第 1000 行开始，显示 2000 行。即显示 1000~2999 行
cat input_file | tail -n +1000 | head -n 2000

显示文件前十行
head /etc/passwd

实时展示文件内容
tail -f 文件名
```

4、只是显示 /etc/passwd 的账户

```linux
cat /etc/passwd |awk -F ':' '{print $1}'
awk -F 指定域分隔符为 ':'，将记录按指定的域分隔符划分域，填充域，$0则表示所有域, $1 表示第一个域, $n表示第 n 个域。
```

5、删除历史操作记录，只保留前 153 行

```linux
sed -i '153,$d' ~/.bash_history
```

awk、sort、uniq

```liux
awk的F参数是指定分隔符，print $1意思是打印第一列，sort命令是用来排序的，uniq命令是用来把相邻的重复数据聚合到一起，加个c参数意思就是把重复次数统计出来，为什么先要用sort聚合一次呢，就是因为uniq命令只会聚合相邻的重复数据，最后那个sort命令刚才说了是用于排序的，他的n参数是以数字排序，r参数是倒叙排序
awk -F " " '{print $1}' access.log| sort|uniq -c|sort -nr
```

- 日志分析技巧

/var/log/secure

```linux
1、定位有多少 IP 在爆破主机的 root 帐号：
grep "Failed password for root" /var/log/secure | awk '{print $11}' | sort | uniq -c | sort -nr | more

定位有哪些IP在爆破：
grep "Failed password" /var/log/secure|grep -E -o "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"|uniq -c

爆破用户名字典是什么？
grep "Failed password" /var/log/secure|perl -e 'while($_=<>){ /for(.*?) from/; print "$1\n";}'|uniq -c|sort -nr

2、登录成功的 IP 有哪些：
grep "Accepted " /var/log/secure | awk '{print $11}' | sort | uniq -c | sort -nr | more

登录成功的日期、用户名、IP：
grep "Accepted " /var/log/secure | awk '{print $1,$2,$3,$9,$11}'

3、增加一个用户kali日志：
grep "useradd" /var/log/secure

4、删除用户 kali 日志：
grep "userdel" /var/log/secure

5、su 切换用户：sudo授权执行:

软件安装升级卸载日志
more /var/log/yum.log

```

`users`命令只是简单地输出当前登录的用户名称，每个显示的用户名对应一个登录会话
`who`命令用于报告当前登录到系统中的每个用户的信息
`w`命令用于显示当前系统中的每个用户及其所运行的进程信息，比users、who命令的输出内容要丰富一些。
`last`命令用于查询成功登录到系统的用户记录，最近的登录情况将显示在最前面。
`lastb`命令用于查询登录失败的用户记录，如登录的用户名错误、密码不正确等情况都将记录在案

## 系统状态命令

1、lsof

查看某个用户启动了什么进程
lsof -u root

某个端口是哪个进程打开的
lsof -i:8080

2、last、lastb、lastlog

登录失败记录：/var/log/btmp
lastb

最后一次登录：/var/log/lastlog  
lastlog

登录成功记录: /var/log/wtmp
last

3、crontab

查看计划任务是否有恶意脚本或者恶意命令
crontab -l

4、netstat

a参数是列出所有连接，n是不要解析机器名，p列出进程名
netstat -anp

5、ps

查看进程信息
ps -ef
ps -aux

6、top

查看进程cpu占比（动态任务，可实时查看最高cpu占有率）
top

7、stat

查看某个文件是否被修改过
stat

8、last和lastb（对应日志wtmp/btmp）

last查看成功登陆的IP（用于查看登陆成功信息）
登陆用户---连接方式---时间

lastb查看连接失败的IP（可用于查看爆破信息）
登陆用户---登陆方式---登陆IP---时间

## 日志分析

1、安全日志 /var/log/secure
作用：安全日志secure包含验证和授权方面信息
分析：是否有IP爆破成功

2、用户信息 /etc/passwd
内容含义：注册名、口令、用户标识号、组标识号、用户名、用户主目录、命令解释程序  
分析：是否存在攻击者创建的恶意用户

3、命令执行记录 ~/.bash_history
作用：命令执行记录 ~/.bash_history
分析：是否有账户执行过恶意操作系统命令

4、root邮箱 /var/spool/mail/root
作用：root邮箱 /var/spool/mail/root
分析：root邮箱的一个文件，在该文件中包含大量信息，当日志被删除可查询本文件

5、中间件日志(Web日志access_log)
nginx、apache、tomcat、jboss、weblogic、websphere

作用：记录访问信息
分析：请求次数过大，访问敏感路径的IP
位置：/var/log下 access.log文件（apache默认位置）
位置：/var/log/nginx下 access名称日志（nginx日志位置）
位置：tomcat、weblogic等日志均存放在安装路径下logs文件下
访问日志结构：访问IP---时间---请求方式---请求路径---请求协议----请求状态---字节数

6.登陆日志（可直接使用命令调取该信息，对应命令last/lastb）
位置：/var/log/wtmp #成功连接的IP信息
位置：/var/log/btmp #连接失败的IP信息

7.cron(定制任务日志)日志
位置：/var/log/cron
作用：查看历史计划任务（对该文件进行分析调取恶意病毒执行的计划任务，获取准确时间）

8、history日志
位置：~/.bash_history
作用：操作命令记录，可筛查攻击者执行命令信息

9、其他日志
redis、sql server、mysql、oracle等
作用：记录访问信息
分析：敏感操作
