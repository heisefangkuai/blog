# linux

- [docker](./linux/docker.html)
- [vim编辑器](./linux/vim编辑器.html)
- [给linux增加虚拟内存](./linux/给linux增加虚拟内存.html)
- [远程连接linux图形界面](./linux/远程连接linux图形界面.html)
- [tcpdump](https://mp.weixin.qq.com/s/Txb6PeQzNest1lLNgIhdCQ)

## linux基本常用命令

```shell
service network restart   # 开启网络服务，vmware无法联网时常用

关闭防火墙限制
sudo setenforce 0

systemctl stop firewalld.service #停止firewall
systemctl disable firewalld.service #禁止firewall开机启动
firewall-cmd --state #查看默认防火墙状态（关闭后显示notrunning，开启后显示running）

清空防火墙：临时生效
iptables 　-F
iptables 　-L
```

## yum命令

```yum
# 安装指定软件
yum install software-name
# 卸载指定软件
yum remove software-name
# 升级指定软件
yum update software-name
# 清除yum 缓存
yum clean all

# 常用命令
# 通过关键字搜索需要安装的软件
yum search keyword
# 列出全部、安装的、最近的、软件更新
yum list (all、installed、recent、updates)
# 显示指定的软件信息
yum info packagename
# 查询哪个rpm软件包含了目标文件
yum whatprovides filename
```
