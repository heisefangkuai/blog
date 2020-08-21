# kali

## 源文件位置

```Linux
cp /etc/apt/sources.list /etc/apt/sources.list.bak
vi /etc/apt/sources.list
leafpad /etc/apt/sources.list

apt-get update 命令即可更新源
apt-get upgrade 更新软件
```

## 安装vmtools

```shell
apt-get update && apt-get dist-upgrade
sudo apt-get install open-vm-tools-desktop fuse -y
```

## VM创建共享文件

```bash
创建共享文件目录
sudo mkdir /mnt/hgfs

查看你共享文件名
vmware-hgfsclient

将文件挂载到kali的/mnt/hgfs目录
sudo vmhgfs-fuse .host:/Baidu /mnt/hgfs

如果每次重启之后想让系统自动挂载 #vi /etc/fstab:
在最后添加一行：
.host:/VM_Shared /mnt/hgfs fuse.vmhgfs-fuse allow_other 0 0

当你修改了/etc/fstab后，一定要重新引导系统才会有效
```

## kali显示管理器

```shell
GDM，gnome系列的图形管理器
sudo apt-get install gdm3

KDM,SDDM是KDE系列的图形管理器
sudo apt-get install kali-defaults kali-root-login desktop-base kde-plasma-desktop
sudo apt-get install sddm

LightDM是轻量级的Ubuntu默认。
sudo apt-get install lightdm

配置和切换
sudo dpkg-reconfigure gdm3

切换登录管理器
sudo apt-get install kali-defaults kali-root-login desktop-base kde-plasma-desktop
sudo dpkg-reconfigure gdm
sudo dpkg --configure sddm
sudo dpkg-reconfigure lightdm
```

## 汉化

```shell
apt-get update && apt-get upgrade && apt-get clean

选择中文：
dpkg-reconfigure locales
选中en_US.UTF-8 UTF-8和zh_CN.UTF-8 UTF-8（空格是选择，tab是切换，*是选中）并将en_US.UTF-8选为默认。


安装google输入法
apt-get install fcitx
apt-get install fcitx-googlepinyin
```

在kali的工具菜单中添加工具

```shell
开始菜单中存放的位置在：/usr/share/applications
想要添加或者删除，可以在这个文件中添加一个或删除一个.desktop 的文件
创建一个.sh文件无法运行的时候使用chmod 777 *.sh给文件权限

[Desktop Entry]
Name=nn  # 文件的名字
Encoding=UTF-8
Exec=sh -c "/root/nn.sh;${SHELL:-bash}"   # 启动程序的位置
Icon=kali-menu.png  # 图标
StartupNotify=false
Terminal=true
Type=Application
Categories=03-04-web-crawlers;  # 存放哪个菜单下
X-Kali-Package=wfuzz
```

## [Aircrack-ng破解WiFi密码](./kali/Aircrack-ng.html)

