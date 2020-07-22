# Wireshark过滤器

过滤器分为抓包过滤器和显示过滤器，抓包过滤器会将不满足过滤条件的包丢弃，只保留满足条件的包，而显示过滤器则是对已抓取的包做过滤，过滤出满足条件的包。

显示过滤器可以保留全部的报数据，方便后期做流量分析，而抓包过滤器保留的数据有限，后期分析有局限性。

## Wireshark抓包过滤器

- 语法说明：
  - BPF语法：基于libpcap/wincap库
  - 类型：host（主机）、net（网段）、port（端口）
  - 方向：src、dst
  - 协议：ether、ip、tcp、udp、http、ftp
  - 逻辑运算符：&&（与）、||（或）、！（非）

- 举例说明：
  - src host 192.168.1.1 && dst port 80     # 抓取地址为192.168.1.1，端口为80的流量
  - host 192.168.1.1 || host 192.168.1.2    # 抓取 192.168.1.1 和（或） 192.168.1.2 的流量
  - !broadcast                              # 不抓取广播包
  - 过滤mac地址案例：
    - ether host 00:88:c8:a6:50             # 过滤所有mac地址为 00:88:c8:a6:50 的
    - ether src host 00:88:c8:a6:50         # 过滤发送的mac地址为 00:88:c8:a6:50 的
    - ether dst host 00:88:c8:a6:50         # 过滤接收的mac地址为 00:88:c8:a6:50 的
  - 过滤IP地址：
    - host 192.168.1.1                      # 过滤所有ip地址为 192.168.1.1 的
    - src host 192.168.1.1                  # 过滤发送的ip地址为 192.168.1.1 的
    - dst host 192.168.1.1                  # 过滤接收的ip地址为 192.168.1.1 的
  - 过滤端口：
    - port 80
    - !port 80
    - dst port 80
    - src port 80
  - 过滤协议：
    - arp
    - icmp

## Wireshark显示过滤器

使用显示过滤器需先用软件进行抓包，然后在软件filter栏输入过滤规则

- 语法说明：

  - 比较符：
    - == 等于
    - != 不等于
    - > 大于
    - < 小于
    - >= 大于等于
    - <= 小于等于

  - 逻辑操作符：
    - and 两个条件同时满足
    - or 其中一个条件被满足
    - xor 有且仅有一个条件被满足
    - not 没有条件被满足

  - ip地址：
    - ip.addr ip地址
    - ip.src 源ip
    - ip.dst 目标ip

  - 端口过滤：
    - tcp.port
    - tcp.srcport
    - tcp.dstport
    - tcp.flags.syn 过滤包含tcp的syn请求的包
    - tcp.flags.ack 过滤包含tcp的ack应答的包

  - 协议过滤：
    - arp、ip、icmp、udp、tcp、bootp、dns等

- 举例说明：
  - 过滤IP地址：
    - ip.addr == 192.168.1.1        # 过滤该地址的包
    - ip.src == 172.16.1.1          # 过滤发送地址为 172.16.1.1 的包
    - ip.dst == 172.16.1.1          # 过滤接收地址为 172.16.1.1 的包
  - 过滤端口：
    - tcp.port == 80 过滤tcp中端口号为80的包
    - tcp.flags.syn == 1 过滤syn请求为1的包
  - 结合逻辑符综合过滤：
    - ip.src == 192.168.1.1 and ip.dst == 172.16.1.1
    - ip.addr == 192.168.1.1 and udp.port == 4000
