# 远程连接linux图形界面

## ubuntu安装xrdp

```linux
1. 先更新ubuntu19源
2.安装xrdp
sudo apt-get install xrdp
3.安装xubuntu-desktop
sudo apt-get install xubuntu-desktop
4.向xsession中写入xfce4-session
echo "xfce4-session" >~/.xsession
5.启动xrdp
sudo service xrdp start

不行在安装vnc4server
sudo apt-get install vnc4server

关闭vncserver
vncserver -kill 1
查看端口：
netstat  -tnl
查看 3350 3389 5910 这三个端口处于LISTEN

使用下面命令可以查看当前ubuntu的桌面环境是KED 或者是GNOME
echo $DESKTOP_SESSION
```

## 购买服务器配置步骤

```ll
1. 添加EPEL源，要不然无法安装很多软件
[yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm](https://fedoraproject.org/wiki/EPEL/zh-cn)

2. 安装ifconfig命令
sudo yum install net-tools

3. 安装桌面系统
yum upgrade
yum -y groupinstall "X Window System"
yum -y groupinstall "GNOME Desktop"
startx

4. 安装xrdp
yum -y install xrdp

5. 启动xrdp
systemctl start xrdp
systemctl enable xrdp
netstat -tnlp | grep xrdp

以上不行在用下面的

配置包含xrdp软件的源
yum install epel* -y

安装xrdp
yum --enablerepo=epel -y install xrdp

```

## 在安装bb啊，安装完成需要重启

```pp
1. 下载并安装
wget --no-check-certificate https://github.com/teddysun/across/raw/master/bbr.sh && chmod +x bbr.sh && ./bbr.sh

2. 验证一下是否成功安装最新内核并开启，查看内核版本，显示为最新版就表示 OK 了
uname -r

3.
sysctl net.ipv4.tcp_available_congestion_control
返回值一般为：
net.ipv4.tcp_available_congestion_control = bbr cubic reno
或者为：
net.ipv4.tcp_available_congestion_control = reno cubic bbr

4.
sysctl net.ipv4.tcp_congestion_control
返回值一般为：
net.ipv4.tcp_congestion_control = bbr

5.
sysctl net.core.default_qdisc
返回值一般为：
net.core.default_qdisc = fq

6.
lsmod | grep bbr
返回值有 tcp_bbr 模块即说明 bbr 已启动。
```

- 安装软件无法安装依赖

```linux
更好源
```

- 3389端口没有开启

```linux
重启
```

- 远程连接显示“内部错误”

```linux
将下面两行参数设置追加到/etc/xrdp/sesman.ini的[Xvnc]配置中，最新版的没有8和9
param8=-SecurityTypes
param9=None
```

- ubuntu 13.10 及以后版本 无背景

```linux
感谢评论中的童鞋提出的方案:
xrdp支持不了13.10的gnome了，解决办法是装个xfce界面
sudo apt-get install xubuntu-desktop
然后
echo xfce4-session >~/.xsession
```

- 用到的源

```linux
修改源文件
sudo vi /etc/apt/sources.list
跟新源
sudo apt-get update

sudo apt-get upgrade

sudo apt-get -f install

deb http://mirrors.aliyun.com/ubuntu/ disco main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ disco-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ disco-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ disco-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco-backports main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ disco-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ disco-proposed main restricted universe multiverse
```
