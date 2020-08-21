# JAWS—另一个Windows遍历脚本

JAWS也是一个powershell脚本，目的是为了帮助渗透测试员和CTF选手快速识别Windows主机上的提权向量。该脚本是用powershell2.0编写的，所以在win7之后的主机上都可以运行。当前功能

- 网络信息收集(接口,arp,netstat)
- 防火墙状态和规则
- 运行的进程
- 具有完全控制权限的文件和文件夹
- 映射驱动器
- 引人注意的异常文件
- 不带引号的服务路径
- 近期使用的文档
- 系统安装文件
- AlwaysInstallElevted注册表项检查
- 存储的凭证
- 安装的应用
- 潜在的漏洞服务
- MuiCache文件
- 计划任务

## 用法

```powershell
从CMD Shell中运行并写出到文件中。
CMD C:\temp> powershell.exe -ExecutionPolicy Bypass -File .\jaws-enum.ps1 -OutputFilename JAWS-Enum.txt

从CMD Shell中运行并写到屏幕。
CMD C:\temp> powershell.exe -ExecutionPolicy Bypass -File .\jaws-enum.ps1

从PS Shell中运行并写出到文件。
PS C:\temp> .\jaws-enum.ps1 -OutputFileName Jaws-Enum.txt
```
