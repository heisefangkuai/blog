# windows

## [常用软件](./windows/常用软件.html)

## cmd获取所有连接过的wifi 密码

```cmd
for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do  @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear
```

## cmd查看进程并杀死进程

```cmd
# 查看所有端口
netstat  -aon
# 查看你要关闭的端口
netstat  -aon|findstr "7777"
# 通过进程id查看使用该端口的程序
tasklist|findstr "6020"
# 杀死占用端口的程序
taskkill /f /t /im ssh

其他方法：

方法二
Taskkill /pid [进程码] -t(结束该进程) -f(强制结束该进程以及所有子进程)
taskkill /pid 9396 -t 回车

方法三
tskill pid
tskill 6528
```
