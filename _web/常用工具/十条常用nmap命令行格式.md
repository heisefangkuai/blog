# a

## 1)获取远程主机的系统类型及开放端口

Get info about remote host ports and OS detection
nmap -sS -P0 -sV -O <target>

这里的 < target > 可以是单一 IP, 或主机名，或域名，或子网
-sS TCP SYN 扫描 (又称半开放,或隐身扫描)
-P0 允许你关闭 ICMP pings.
-sV 打开系统版本检测
-O 尝试识别远程操作系统
-sS TCP SYN scanning (also known as half-open, or stealth scanning)
-P0 option allows you to switch off ICMP pings.
-sV option enables version detection
-O flag attempt to identify the remote operating system
Other option:
-A 同时启用操作系统指纹识别和版本检测
-A option enables both OS fingerprinting and version detection
-v use -v twice for more verbosity.
nmap -sS -P0 -A -v < target >

## 2)列出开放了指定端口的主机列表

Get list of servers with a specific port open
nmap -sT -p 80 -oG – 192.168.1.* | grep open
Change the -p argument for the port number. See “man nmap” for
different ways to specify address ranges.

## 3)在网络寻找所有在线主机

Find all active IP addresses in a network
nmap -sP 192.168.0.*
或者也可用以下命令:
nmap -sP 192.168.0.0/24
指定 subnet

## 4)Ping 指定范围内的 IP 地址

Ping a range of IP addresses
nmap -sP 192.168.1.100-254
nmap accepts a wide variety of addressing notation, multiple
targets/ranges, etc.

## 5)在某段子网上查找未占用的 IP

Find unused IPs on a given subnet
nmap -T4 -sP 192.168.2.0/24 && egrep "00:00:00:00:00:00" /proc/net/arp

## 6)在局域网上扫找 Conficker 蠕虫病毒

Scan for the Conficker virus on your LAN ect.
nmap -PN -T4 -p139,445 -n -v –script=smb-check-vulns –script-args
safe=1 192.168.0.1-254
replace 192.168.0.1-256 with the IP’s you want to check.

## 7)扫描网络上的恶意接入点 rogue APs

Scan Network for Rogue APs.
nmap -A -p1-85,113,443,8080-8100 -T4 –min-hostgroup 50 –max-rtt-
timeout 2000 –initial-rtt-timeout 300 –max-retries 3 –host-timeout
20m –max-scan-delay 1000 -oA wapscan 10.0.0.0/8
I’ve used this scan to successfully find many rogue APs on a very,
very large network.

## 8)使用诱饵扫描方法来扫描主机端口

Use a decoy while scanning ports to avoid getting caught by the sys
admin
sudo nmap -sS 192.168.0.10 -D 192.168.0.2 
Scan for open ports on the target device/computer (192.168.0.10) while
setting up a decoy address (192.168.0.2). This will show the decoy ip
address instead of your ip in targets security logs. Decoy address
needs to be alive. Check the targets security log at /var/log/secure
to make sure it worked.

## 9)为一个子网列出反向 DNS 记录

List of reverse DNS records for a subnet
nmap -R -sL 209.85.229.99/27 | awk '{if($3=="not")print"("$2") no
PTR";else print$3" is "$2}' | grep '('

## 10)显示网络上共有多少台 Linux 及 Win 设备

How Many Linux And Windows Devices Are On Your Network?

sudo nmap -F -O 192.168.1.1-255 | grep "Running: " > /tmp/os; echo "$(cat /tmp/os | grep Linux | wc -l) Linux device(s)"; echo "$(cat /tmp/os | grep Windows | wc -l) Window(s) devices"