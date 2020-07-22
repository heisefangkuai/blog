# a

## 1)获取远程主机的端口和OS检测的信息

nmap -sS -P0 -sV -O （target）

这里的 < target > 可以是单一 IP, 或主机名，或域名，或子网
-sS TCP SYN 扫描 (也称为半开放扫描或隐式扫描)
-P0 允许你关闭 ICMP pings.
-sV 系统版本检测
-O 识别主机测操作系统
其他选择:
-A 同时启用操作系统指纹识别和版本检测
-v 使用-v两次以增加冗长
nmap -sS -P0 -A -v < target >

## 2 获取打开特定端口的服务器列表

nmap -sT -p 80 -oG – 192.168.1.* | grep open

更改端口号的-p参数。有关指定地址范围的不同方法，请参阅“man nmap”。

## 3 查找网络中的所有活动IP地址

nmap -sP 192.168.0.*
或者也可用以下命令:
nmap -sP 192.168.0.0/24
指定 subnet

## 4)Ping 指定范围内的 IP 地址

nmap -sP 192.168.1.100-254

nmap接受多种寻址符号、多个目标/范围等。

## 5 在给定子网上查找未使用的ip

nmap -T4 -sP 192.168.2.0/24 && egrep "00:00:00:00:00:00" /proc/net/arp

## 6 在局域网上扫找 Conficker 蠕虫病毒

nmap -PN -T4 -p139,445 -n -v –script=smb-check-vulns –script-args safe=1 192.168.0.1-254

用要检查的IP替换192.168.0.1-256。

## 7 扫描网络上的恶意接入点 rogue APs

nmap -A -p1-85,113,443,8080-8100 -T4 –min-hostgroup 50 –max-rtt-timeout 2000 –initial-rtt-timeout 300 –max-retries 3 –host-timeout
20m –max-scan-delay 1000 -oA wapscan 10.0.0.0/8

我用这个扫描成功地在一个非常非常大的网络上找到了许多 rogue APs。

## 8)使用诱饵扫描方法来扫描主机端口,以避免被系统管理员捕获

sudo nmap -sS 192.168.0.10 -D 192.168.0.2

扫描目标设备/计算机上打开的端口(192.168.0.10)，同时设置诱饵地址(192.168.0.2)。这将在目标安全日志中显示诱饵ip地址，而不是您的ip。诱饵地址必须是活的。检查/var/log/secure上的目标安全日志，确保它工作正常。

## 9 列出子网的反向DNS记录列表

nmap -R -sL 209.85.229.99/27 | awk '{if($3=="not")print"("$2") no PTR";else print$3" is "$2}' | grep '('

## 10)显示网络上共有多少台 Linux 及 Win 设备

sudo nmap -F -O 192.168.1.1-255 | grep "Running: " > /tmp/os; echo "$(cat /tmp/os | grep Linux | wc -l) Linux device(s)"; echo "$(cat /tmp/os | grep Windows | wc -l) Window(s) devices"
