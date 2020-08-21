# PowerView.ps1(信息收集)

```powershell
Get-NetDomain   : 获取当前用户所在域的名称
Get-NetUser     : 获取所有用户的详细信息
Get-NetUser -SPN  : 举域帐户的SPN
Get-NetDomainController : 获取所有域控制器的信息
Get-NetComputer : 获取域内所有机器的详细信息
Get-NetOU       : 获取域中的OU信息
Get-NetGroup    : 获取所有域内组和组成员信息
Get-NetFileServer   : 根据SPN获取当前域使用的文件服务器信息
Get-NetShare    : 获取当前域内所有网络共享信息
Get-NetSession  : 获取指定服务器的会话
Get-NetRDPSession   : 获取指定服务器的远程连接
Get-NetProcess  : 获取远程主机的进程
Get-UserEvent   : 获取指定用户的日志
Get-ADObiect    : 获取活动目录的对象
Get-NetGPO      : 获取域内所有的组策略对象
Get-DomainPolicy    : 获取域默认策略或域控制器策略
Invoke-UserHunter   : 获取域用户登录的计算机信息及该用户是否有本地管理员权限
Invoke-ProcessHunter    : 通过查询域内所有的机器进程找到特定用户
Invoke-UserEvenHunter   : 根据用户日志查询某域用户登录过哪些域机器。
Get-ObjectAcl   : 查询有DC Replication权限的用户
Invoke-ShareFinder  : 从共享文件中挖掘敏感信息
Invoke-FileFinder
Get-NetGroupMember DNSAdmins    :获取dns服务器
Find-LocalAdminAccess   : 有权限访问的机器

# 当前域基本信息枚举
Get-NetDomain   # 得到当前域
Get-NetDomain –Domain moneycorp.local   # 获取另一个域的对象
Get-DomainSID   # 获取当前域的域SID
Get-DomainPolicy    # 获取当前域的域策略
(Get-DomainPolicy –domain moneycorp.local)."system access"  # 获取另一个域的域策略
Get-NetDomainController     # 获取当前域的域控制器
Get-NetDomainController –Domain moneycorp.local     # 获取另一个域的域控制器

# 域内用户信息枚举
Get-NetUser     # 获取当前域中的用户列表
Get-NetUser –Username student1  # 获取指定用户
Get-UserProperty    # 获取当前域中用户的所有属性的列表
Get-UserProperty –Properties pwdlastset         # 获取域中所有用户的修改密码的时候
Get-UserProperty -Properties badpwdcount        # 获取用户的错误密码的次数
Get-UserProperty -Properties logoncount         # 获取用户的登陆次数
Find-UserField -SearchField Description -SearchTerm "built" # 在用户属性中搜索特定字符串

# 域内机器信息枚举
Get-NetComputer     # 获取域内机子信息
Get-NetComputer –OperatingSystem "*Server 2016*"    # 探测特定操作系统机子
Get-NetComputer -Ping   # ping探测存活主机
Get-NetComputer -FullData

# 域内组信息枚举
Get-NetGroup
Get-NetGroup –Domain <targetdomain>
Get-NetGroup –FullData
Get-NetGroup *admin*    # 获取组名中包含单词“admin”的所有组

Get-NetGroup –UserName "student1"   # 获取用户所属的组
Get-NetGroupMember -GroupName "Enterprise Admins" –Domain moneycorp.local   # 指定域
Get-NetGroupMember -GroupName "Domain Admins" -Recurse  # 获取域管理员组的所有成员 * -Recurse  是递归查询
Get-NetGroupMember -GroupName "Domain Admins" -Recurse | select MemberName # 获取域管理员的用户名

# 目标机子登录用户的信息(非dc机器上需要管理员权限):
Get-NetLocalGroup -ComputerName dcorpdc.dollarcorp.moneycorp.local -ListGroups
# 获取机器上所有本地组的成员(非dc机器上需要管理员权限)
Get-NetLocalGroup -ComputerName dcorpdc.dollarcorp.moneycorp.local -Recurse
# 获取计算机上积极登录的用户(需要目标上的本地管理权限)
Get-NetLoggedon –ComputerName <servername>
# 获取计算机上本地登录的用户(需要目标上的远程注册表——在服务器OS上默认启动)
Get-LoggedonLocal -ComputerName dcorpdc.dollarcorp.moneycorp.local
# 获取计算机上最后一个登录的用户(需要目标上的管理权限和远程注册表)
Get-LastLoggedOn -ComputerName <servername>

# 域内敏感文件枚举
# 查找当前域中主机上的共享。
Invoke-ShareFinder -Verbose
Invoke-ShareFinder -ExcludeStandard -ExcludePrint -ExcludeIPC –Verbose
# 在域中找到计算机上的敏感文件
Invoke-FileFinder -Verbose
# 获取域的所有文件服务器
Get-NetFileServer

# GPO & OUs
Get-NetGPO
Get-NetGPO | select displayname
Get-NetGPO -ComputerName dcorp-student41.dollarcorp.moneycorp.local # 获取当前计算机的权限(hostname+当前域)
Get-NetGPO -GPOname '{3E04167E-C2B6-4A9A-8FB7-C811158DC97C}'        # 获取指定计算机的权限(id是Get-NetOU -Fulldata中的gplink)
Get-NetGPOGroup  # 查找groups.xml中的用户
Get-NetGPOGroup -Verbose
Get-NetGroupMember -GroupName RDPUsers  # 查找组“RDPUsers”的成员
Get-NetOU -Fulldata     # 获取所有ou(域中OU指的是组织单位)的数据
Get-NetOU StudentMachines | %{Get-NetComputer -ADSPath $_}  # 列出所有的计算机在学生的机器
Find-GPOComputerAdmin –Computername  CASC-DC1.cascade.local   # 通过GPO查找目标机器有管理权限的用户
Find-GPOLocation -UserName arksvc   # 通过GPO查找xxxx用户在域内哪些机子有管理员权限
gpresult /R     # 获取当前用户的策略集合

# 列举适用于StudentMachines OU的GPO:
(Get-NetOU StudentMachines -FullData).gplink    # 获取的值下面用到
Get-NetGPO -ADSpath 'LDAP://cn={3E04167E-C2B6-4A9A-8FB7-C811158DC97C},cn=policies,cn=system,DC=dollarcorp,DC=moneycorp,DC=local'

# 获取与指定对象关联的acl
Get-ObjectAcl -SamAccountName student41 –ResolveGUIDs

# 获取与指定前缀关联的acl，以便用于搜索
Get-ObjectAcl -ADSprefix 'CN=Administrator,CN=Users' -Verbose

# 我们还可以使用ActiveDirectory模块枚举acl，但不需要解析guid
(Get-Acl 'AD:\CN=Administrator,CN=Users,DC=dollarcorp,DC=moneycorp,DC=local').Access

# 获取与要用于搜索的指定LDAP路径关联的acl
Get-ObjectAcl -ADSpath "LDAP://CN=Domain Admins,CN=Users,DC=dollarcorp,DC=moneycorp,DC=local" -ResolveGUIDs -Verbose

# 寻找有趣的ace(结果很多)
Invoke-ACLScanner -ResolveGUIDs

# 获取与指定路径关联的acl
Get-PathAcl -Path "\\dcorp-dc.dollarcorp.moneycorp.local\sysvol"

# 获取当前域的所有域信任的列表
Get-NetDomainTrust
Get-NetDomainTrust –Domain us.dollarcorp.moneycorp.local

# 获取当前林的详细信息
Get-NetForest
Get-NetForest –Forest eurocorp.local

# 获取当前林中的所有域
Get-NetForestDomain
Get-NetForestDomain –Forest eurocorp.local



# 获取当前目录林的所有全局目录
Get-NetForestCatalog
Get-NetForestCatalog –Forest eurocorp.local

# 绘制森林的信任图
Get-NetDomainTrust
Get-NetForestTrust
Get-NetForestTrust –Forest moneycorp.local
Get-NetForestDomain -Verbose | Get-NetDomainTrust   # 列出信任关系
Get-NetDomainTrust | ?{$_.TrustType -eq 'External'} # 只列出外部信托
Get-NetForestDomain -Verbose | Get-NetDomainTrust | ?{$_.TrustType -eq 'External'}  # 只列出外部信任的

# 获取指定域中的用户
Get-Netuser –Domain moneycorp.local

# 找到当前用户具有本地管理访问权限的当前域中的所有计算机
Find-LocalAdminAccess   # 存在就可以直接用Enter-Pssession命令去连接
Find-LocalAdminAccess -Verbose

# 查找计算机上域管理员(或指定的用户/组)的会话的
Invoke-UserHunter

# 查看域控制器上是否存在会话
Get-NetSession -Computername dcorp-dc.dollarcorp.moneycorp.local
```

---

- Get-NetDomain : 获取当前用户所在域的名称

```powershell
PS C:\AD\Tools> Get-NetDomain

Forest                  : moneycorp.local
DomainControllers       : {dcorp-dc.dollarcorp.moneycorp.local}
Children                : {us.dollarcorp.moneycorp.local}
DomainMode              : Unknown
DomainModeLevel         : 7
Parent                  : moneycorp.local
PdcRoleOwner            : dcorp-dc.dollarcorp.moneycorp.local
RidRoleOwner            : dcorp-dc.dollarcorp.moneycorp.local
InfrastructureRoleOwner : dcorp-dc.dollarcorp.moneycorp.local
Name                    : dollarcorp.moneycorp.local
---------------

powershell相同的命令：
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
[System.DirectoryServices.ActiveDirectory.Domain]::GetComputerDomain()
```

- Get-NetUser : 获取所有用户的详细信息

```powershell
PS C:\AD\Tools> Get-NetUser

logoncount             : 14032
badpasswordtime        : 6/25/2020 3:08:52 AM
description            : Built-in account for administering the computer/domain
distinguishedname      : CN=Administrator,CN=Users,DC=dollarcorp,DC=moneycorp,DC=local
objectclass            : {top, person, organizationalPerson, user}
lastlogontimestamp     : 7/7/2020 2:02:00 PM
name                   : Administrator
objectsid              : S-1-5-21-1874506631-3219952063-538504511-500
samaccountname         : Administrator
admincount             : 1
codepage               : 0
samaccounttype         : 805306368
whenchanged            : 7/7/2020 9:02:00 PM
accountexpires         : 9223372036854775807
countrycode            : 0
adspath                : LDAP://CN=Administrator,CN=Users,DC=dollarcorp,DC=moneycorp,DC=local
instancetype           : 4
objectguid             : e88d11d3-3e60-4a68-b46a-94ff32b7c8cf
lastlogon              : 7/7/2020 7:11:00 PM
lastlogoff             : 12/31/1600 4:00:00 PM
objectcategory         : CN=Person,CN=Schema,CN=Configuration,DC=moneycorp,DC=local
dscorepropagationdata  : {2/21/2019 12:17:00 PM, 2/19/2019 1:04:02 PM, 2/19/2019 12:55:49 PM, 2/17/2019 7:16:56 AM...}
memberof               : {CN=Group Policy Creator Owners,CN=Users,DC=dollarcorp,DC=moneycorp,DC=local, CN=Domain
                         Admins,CN=Users,DC=dollarcorp,DC=moneycorp,DC=local,
                         CN=Administrators,CN=Builtin,DC=dollarcorp,DC=moneycorp,DC=local}
whencreated            : 2/17/2019 7:00:16 AM
iscriticalsystemobject : True
badpwdcount            : 0
cn                     : Administrator
useraccountcontrol     : 66048
usncreated             : 8196
primarygroupid         : 513
pwdlastset             : 2/16/2019 9:14:11 PM
usnchanged             : 293710
等等。。。
```

- Get-NetDomainController : 获取所有域控制器的信息

```powershell
PS C:\AD\Tools> Get-NetDomainController

Forest                     : moneycorp.local
CurrentTime                : 7/8/2020 2:16:10 AM
HighestCommittedUsn        : 667990
OSVersion                  : Windows Server 2016 Standard
Roles                      : {PdcRole, RidRole, InfrastructureRole}
Domain                     : dollarcorp.moneycorp.local
IPAddress                  : 172.16.2.1
SiteName                   : Default-First-Site-Name
SyncFromAllServersCallback :
InboundConnections         : {a10dec78-e40a-4c4f-afad-c506692af93f, e3b5934c-0fbb-4de1-a5ee-33a0183442b4}
OutboundConnections        : {92a12922-5f6f-4133-b29c-eefaf42dd608, 2f7dd237-61c1-4146-b0af-3befac8c9b19}
Name                       : dcorp-dc.dollarcorp.moneycorp.local
Partitions                 : {CN=Configuration,DC=moneycorp,DC=local, CN=Schema,CN=Configuration,DC=moneycorp,DC=local, DC=ForestDnsZones,DC=moneycorp,DC=local,DC=dollarcorp,DC=moneycorp,DC=local...}
```

- Get-NetComputer : 获取域内所有机器的详细信息

```powershell
PS C:\AD\Tools> Get-NetComputer

dcorp-dc.dollarcorp.moneycorp.local
dcorp-mgmt.dollarcorp.moneycorp.local
dcorp-ci.dollarcorp.moneycorp.local
dcorp-mssql.dollarcorp.moneycorp.local
dcorp-adminsrv.dollarcorp.moneycorp.local
dcorp-appsrv.dollarcorp.moneycorp.local
dcorp-sql1.dollarcorp.moneycorp.local
dcorp-studAdmin.dollarcorp.moneycorp.local
dcorp-student35.dollarcorp.moneycorp.local
dcorp-student36.dollarcorp.moneycorp.local
dcorp-student37.dollarcorp.moneycorp.local
dcorp-student38.dollarcorp.moneycorp.local
dcorp-student39.dollarcorp.moneycorp.local
dcorp-student40.dollarcorp.moneycorp.local
dcorp-student41.dollarcorp.moneycorp.local
dcorp-student42.dollarcorp.moneycorp.local
dcorp-student43.dollarcorp.moneycorp.local
dcorp-student45.dollarcorp.moneycorp.local
dcorp-student46.dollarcorp.moneycorp.local
dcorp-student44.dollarcorp.moneycorp.local
dcorp-std41.dollarcorp.moneycorp.local
dcorp-std43.dollarcorp.moneycorp.local
```

- Get-NetOU : 获取域中的OU信息

```powershell
PS C:\AD\Tools> Get-NetOU

LDAP://OU=Domain Controllers,DC=dollarcorp,DC=moneycorp,DC=local
LDAP://OU=Applocked,DC=dollarcorp,DC=moneycorp,DC=local
LDAP://OU=Servers,DC=dollarcorp,DC=moneycorp,DC=local
LDAP://OU=StudentMachines,DC=dollarcorp,DC=moneycorp,DC=local
```

- Get-NetGroup    : 获取所有域内组和组成员信息

```powershell
PS C:\AD\Tools> Get-NetGroup

Administrators
Users
Guests
Print Operators
Backup Operators
Replicator
Remote Desktop Users
Network Configuration Operators
Performance Monitor Users
Performance Log Users
Distributed COM Users
IIS_IUSRS
Cryptographic Operators
Event Log Readers
Certificate Service DCOM Access
RDS Remote Access Servers
RDS Endpoint Servers
RDS Management Servers
Hyper-V Administrators
Access Control Assistance Operators
Remote Management Users
System Managed Accounts Group
Storage Replica Administrators
Domain Computers
Domain Controllers
Cert Publishers
Domain Admins
Domain Users
Domain Guests
Group Policy Creator Owners
RAS and IAS Servers
Server Operators
Account Operators
Pre-Windows 2000 Compatible Access
Windows Authorization Access Group
Terminal Server License Servers
Allowed RODC Password Replication Group
Denied RODC Password Replication Group
Read-only Domain Controllers
Cloneable Domain Controllers
Protected Users
Key Admins
DnsAdmins
DnsUpdateProxy
RDPUsers
```

- Get-NetShare : 获取当前域内所有网络共享信息

```powershell
PS C:\AD\Tools> Get-NetShare

shi1_netname  shi1_type shi1_remark   ComputerName
------------  --------- -----------   ------------
ADMIN$       2147483648 Remote Admin  localhost
C$           2147483648 Default share localhost
IPC$         2147483651 Remote IPC    localhost
shared                0               localhost
```

- Get-NetSession  : 获取指定服务器的会话

```powershell
PS C:\AD\Tools> Get-NetSession

sesi10_cname     : \\172.16.100.213
sesi10_username  : student41
sesi10_time      : 315308
sesi10_idle_time : 1465
ComputerName     : localhost

sesi10_cname     : \\[::1]
sesi10_username  : student41
sesi10_time      : 0
sesi10_idle_time : 0
ComputerName     : localhost
```

- Get-NetRDPSession : 获取指定服务器的远程连接

```powershell
PS C:\AD\Tools> Get-NetRDPSession


ComputerName : localhost
SessionName  : Services
UserName     :
ID           : 0
State        : Disconnected
SourceIP     :

ComputerName : localhost
SessionName  : Console
UserName     :
ID           : 1
State        : Connected
SourceIP     :

ComputerName : localhost
SessionName  :
UserName     : DCORP-STUDENT41\Administrator
ID           : 2
State        : Disconnected
SourceIP     :

ComputerName : localhost
SessionName  : RDP-Tcp#67
UserName     : dcorp\student41
ID           : 3
State        : Active
SourceIP     : 172.16.99.41
```

- Get-NetProcess  : 获取远程主机的进程

```powershell
PS C:\AD\Tools> Get-NetProcess

ComputerName : dcorp-student41
ProcessName  : System Idle Process
ProcessID    : 0
Domain       :
User         :

ComputerName : dcorp-student41
ProcessName  : System
ProcessID    : 4
Domain       :
User         :

ComputerName : dcorp-student41
ProcessName  : smss.exe
ProcessID    : 288
Domain       :
User         :
```

- Get-NetGPO : 获取域内所有的组策略对象

```powershell
PS C:\AD\Tools> Get-NetGPO

usncreated               : 8016
systemflags              : -1946157056
displayname              : Default Domain Policy
gpcmachineextensionnames : [{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}][{827D319E-6EAC-11D2-A4EA-00C04F79F83A}{803E14A0-B4FB-11D0-A0D0-00A0C90
                           72-6EAC-11D2-A4EA-00C04F79F83A}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}]
whenchanged              : 2/17/2019 7:14:30 AM
objectclass              : {top, container, groupPolicyContainer}
gpcfunctionalityversion  : 2
showinadvancedviewonly   : True
usnchanged               : 13009
dscorepropagationdata    : {2/21/2019 12:17:00 PM, 2/19/2019 1:04:02 PM, 2/19/2019 12:55:49 PM, 2/17/2019 7:01:46 AM...}
name                     : {31B2F340-016D-11D2-945F-00C04FB984F9}
adspath                  : LDAP://CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=dollarcorp,DC=moneycorp,DC=local
flags                    : 0
cn                       : {31B2F340-016D-11D2-945F-00C04FB984F9}
iscriticalsystemobject   : True
gpcfilesyspath           : \\dollarcorp.moneycorp.local\sysvol\dollarcorp.moneycorp.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}
distinguishedname        : CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=dollarcorp,DC=moneycorp,DC=local
whencreated              : 2/17/2019 7:00:13 AM
versionnumber            : 3
instancetype             : 4
objectguid               : cd0c7024-e03a-4369-958b-9c93fbd25649
objectcategory           : CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=moneycorp,DC=local

```

- Get-DomainPolicy    : 获取域默认策略或域控制器策略

```powershell
PS C:\AD\Tools> Get-DomainPolicy

Name                           Value
----                           -----
Kerberos Policy                {MaxTicketAge, MaxServiceAge, MaxClockSkew, MaxRenewAge...}
System Access                  {MinimumPasswordAge, MaximumPasswordAge, LockoutBadCount, PasswordComplexity...}
Version                        {Revision, signature}
Registry Values                {MACHINE\System\CurrentControlSet\Control\Lsa\NoLMHash}
Unicode                        {Unicode}
```

- Invoke-UserHunter : 获取域用户登录的计算机信息及该用户是否有本地管理员权限

```powershell
PS C:\AD\Tools> Invoke-UserHunter

UserDomain      : dollarcorp.moneycorp.local
UserName        : Administrator
ComputerName    : dcorp-appsrv.dollarcorp.moneycorp.local
IPAddress       : 172.16.4.217
SessionFrom     : 172.16.2.1
SessionFromName :
LocalAdmin      :

UserDomain      : dollarcorp.moneycorp.local
UserName        : Administrator
ComputerName    : dcorp-appsrv.dollarcorp.moneycorp.local
IPAddress       : 172.16.4.217
SessionFrom     : 172.16.2.1
SessionFromName :
LocalAdmin      :
```

- Get-ObjectAcl 查询有DC Replication权限的用户

```powershell
PS C:\AD\Tools> Get-ObjectAcl

ObjectDN              : DC=dollarcorp,DC=moneycorp,DC=local
ObjectSID             : S-1-5-21-1874506631-3219952063-538504511
ActiveDirectoryRights : DeleteChild
InheritanceType       : None
ObjectType            : 00000000-0000-0000-0000-000000000000
InheritedObjectType   : 00000000-0000-0000-0000-000000000000
ObjectFlags           : None
AccessControlType     : Deny
IdentityReference     : Everyone
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
```

- Invoke-ShareFinder

从共享文件中挖掘敏感信息是红队非常常用的收集信息手法，从中或许可以找到密码本、员工目录、薪酬信息、网络架构等信息，这些大多是由于共享文件权限设置不合理导致的。

```powershell
PS C:\AD\Tools> Invoke-ShareFinder

\\dcorp-mgmt.dollarcorp.moneycorp.local\ADMIN$  - Remote Admin
\\dcorp-mgmt.dollarcorp.moneycorp.local\C$      - Default share
\\dcorp-mgmt.dollarcorp.moneycorp.local\IPC$    - Remote IPC
\\dcorp-appsrv.dollarcorp.moneycorp.local\ADMIN$        - Remote Admin
等等。。。
```

- Invoke-FileFinder

```powershell
PS C:\AD\Tools> Invoke-FileFinder

FullName       : \\dcorp-dc.dollarcorp.moneycorp.local\SYSVOL\dollarcorp.moneycorp.local
Owner          : BUILTIN\Administrators
LastAccessTime : 2/16/2019 11:00:05 PM
LastWriteTime  : 2/16/2019 11:00:05 PM
CreationTime   : 2/16/2019 11:00:05 PM
Length         :

FullName       : \\dcorp-dc.dollarcorp.moneycorp.local\SYSVOL\dollarcorp.moneycorp.local\DfsrPrivate
Owner          : NT AUTHORITY\SYSTEM
LastAccessTime : 2/16/2019 11:07:26 PM
LastWriteTime  : 2/16/2019 11:07:26 PM
CreationTime   : 2/16/2019 11:07:26 PM
Length         :
等等。。。
```


## 获取与指定对象关联的acl

```powershell
Get-ObjectAcl -SamAccountName student41 –ResolveGUIDs

InheritedObjectType   : All
ObjectDN              : CN=student41,CN=Users,DC=dollarcorp,DC=moneycorp,DC=local
ObjectType            : All
IdentityReference(身份引用)     : BUILTIN\Administrators
IsInherited           : True
ActiveDirectoryRights : CreateChild, Self, WriteProperty, ExtendedRight, Delete, GenericRead, WriteDacl, WriteOwner
PropagationFlags      : None
ObjectFlags           : None
InheritanceFlags      : ContainerInherit
InheritanceType       : All
AccessControlType     : Allow
ObjectSID             : S-1-5-21-1874506631-3219952063-538504511-31155
```
