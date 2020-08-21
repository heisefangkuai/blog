# 给linux增加虚拟内存

准备在一个独立的文件系统中添加一个swap交换文件
创建（设置）交换空间，使用命令mkswap 。
启动新增加的1G的交换空间，使用命令swapon
修改/etc/fstab文件，使得新加的1G交换空间在系统重新启动后自动生效

free -m 查看虚拟内存情况

```linux
free -m
dd if=/dev/zero of=/var/swap bs=1M count=1024
chmod -R 600 /var/swap
mkswap /var/swap
swapon /var/swap
free -m
swapon -s
在文件最后加入：
echo '/var/swap swap swap defaults  0 0' >> /etc/fstab
注：ubuntu 不支持barrier，所以正确写法是：
echo '/var/swap swap swap defaults barrier=0  0  0' >> /etc/fstab
```
