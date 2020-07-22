# Shodan和ZoomEyE语法

## Shodan语法

- 使用搜索过滤

```linux
hostname：搜索指定的主机或域名，例如 hostname:"google"
port：搜索指定的端口或服务，例如 port:"21"
country：搜索指定的国家，例如 country:"CN"
city：搜索指定的城市，例如 city:"Hefei"
org：搜索指定的组织或公司，例如 org:"google"
isp：搜索指定的ISP供应商，例如 isp:"China Telecom"
product：搜索指定的操作系统/软件/平台，例如 product:"Apache httpd"
version：搜索指定的软件版本，例如 version:"1.6.2"
geo：搜索指定的地理位置，参数为经纬度，例如 geo:"31.8639, 117.2808"
before/after：搜索指定收录时间前后的数据，格式为 dd-mm-yy，例如 before:"11-11-15"
net：搜索指定的IP地址或子网，例如 net:"210.45.240.0/24"
```

- 搜索实例

查找位于合肥的 Apache 服务器：
apache city:"Hefei"

查找位于国内的 Nginx 服务器：
nginx country:"CN"

查找 GWS(Google Web Server) 服务器：
"Server: gws" hostname:"google"

查找指定网段的华为设备：
huawei net:"61.191.146.0/24"

- Shodan 是由官方提供的 Python 库

安装命令：

```linux
git clone https://github.com/achillean/shodan-python.git && cd shodan-python
python setup.py install
```

## ZoomEyE语法

显示帮助 shift+/
隐藏该帮助 ESC
回到首页 shift
高级搜索 Shift +s
聚焦搜索框 s

左侧部分：给出了本次搜索结果的搜索类型（网站、设备数量）、年份、所处国家、WEB应用、WEB容器、组件、服务、设备、端口信息
中间部分：给出了搜素结果的IP地址、使用的协议、开放的端口服务、所处的国家、城市、搜索时间
右侧部分：给出了使用HTTP协议版本信息、使用的组件名称、版本、以及服务器的类型、主机的系统信息
上方：“搜索结果”显示按照搜索条件查询之后所获得的结果信息
             “相关漏洞”给出各大组件、服务器系统等存在的历史性漏洞的描述文档，

ZoomEye搜索技巧
指定搜索的组件以及版本
app：组件名称
ver：组件版本
例如：搜索 apache组件    版本2.4
app:apache ver:2.4

指定搜索的端口
port:端口号
port:22

指定搜索的操作系统
OS:操作系统名称

指定搜索的服务
Service：SSH

指定搜索的地理位置范
country：国家名
city：城市名

搜索指定的CIDR网段
CIDR:网段区域
CIDR：192.168.158.12/24

搜索指定的网站域名
Site:网站域名

搜索指定的主机名
Hostname:主机名

搜索指定的设备名
Device：设备名
device:router

搜索具有特定首页关键词的主机
Keyword：关键词
