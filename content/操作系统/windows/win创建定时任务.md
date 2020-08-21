# 定时任务

## 一、win在任务计划程序中创建

## 二、win使用schtasks命令

描述: 允许管理员创建、删除、查询、更改、运行和中止本地或远程系统上的计划任务。

参数列表:
    /Create         创建新计划任务。
    /Delete         删除计划任务。
    /Query          显示所有计划任务。
    /Change         更改计划任务属性。
    /Run            按需运行计划任务。
    /End            中止当前正在运行的计划任务。
    /ShowSid        显示与计划的任务名称相应的安全标识符。
    /?              显示此帮助消息。

以管理员身份运行：

```schtasks
# 每天晚上 03:30 定时执行
schtasks /create /tn "TimedTask1" /tr C:\Users\Administrator\Desktop\TimedTask\Run.bat /sc DAILY /st 22:22

# 查询创建的任务
schtasks /query /tn TimedTask1 /v

# 立即运行创建的任务
schtasks /run /tn TimedTask1

# 删除任务
schtasks /delete /tn TimedTask1
```

## linux定时任务

```crond
# 查看任务是否启动命令
service crond status

# crond任务命令
service crond start|stop|restart

# 查看现在已经有的定时任务
crontab -l

# 查看root下的定时任务
crontab -u root -l

# 编辑定时任务
crontab -e

编辑的是/var/spool/cron下对应用户的cron文件,也可以直接修改/etc/crontab文件
# .---------------- 分 (0 - 59)
# |  .------------- 时 (0 - 23)
# |  |  .---------- 天 (1 - 31)
# |  |  |  .------- 月 (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- 星期 (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
# *号表示“每”的意思，减号表示一个时间范围，逗号表示指定时间，*/n 每隔n久

*/1 * * * * echo 123456 >> /root/11111.ss


问题：
当使用命令：service crond start 后 crond任务任然处于未启动状态
需要先通过命令：pkill cron 来强杀干扰crond任务启动的所有进程，然后再执行命令：service crond start
```
