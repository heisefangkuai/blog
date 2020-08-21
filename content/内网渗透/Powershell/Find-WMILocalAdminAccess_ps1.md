# Find-WMILocalAdminAccess

此命令会产生大量了流量

```powershell
# 1.查找计算机列表
Get-NetComputer

# 2.讲计算机列表保存为1.txt文件
# 3.引入
import-module ./Find-WMILocalAdminAccess.ps1

# 执行
Find-WMILocalAdminAccess -ComputerFile .\111.txt -Verbose
```

(这条命令向域控发出Get-NetComputer获取机器列表，然后在每台机器上执行Invoke-CheckLocalAdminAcess)
Find-LocalAdminAccess不能执行，可用WMI和powershell Remoting等远程管理工具代替探测，（Find-WMILocalAdminAccess.ps1）

App.UserLic.FirstUseOn=1589448794
App.UserLic.FirstUseOn=1589448794
