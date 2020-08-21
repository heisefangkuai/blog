# ncat简单使用

## ncat的语法和参数

Ncat 7.70 ( https://nmap.org/ncat )
Usage: ncat [options] [hostname] [port]

Options taking a time assume seconds. Append 'ms' for milliseconds,'s' for seconds, 'm' for minutes, or 'h' for hours (e.g. 500ms).
花时间的选项假设是秒。为毫秒添加“ms”，s表示秒，m表示分钟，h表示小时(例如500毫秒)。

```ncat
-4                                  # 使用IPv4只
-6                                  # 使用IPv6只
-C, --crlf                          # 对EOL序列使用CRLF
-c, --sh-exec <command>             # 通过/bin/sh执行给定的命令
-e, --exec <command>                # 执行给定的命令
    --lua-exec <filename>           # 执行给定的Lua脚本
-g hop1[,hop2,...]                  # 松散源路由跳点(8 max)
-G <n>                              # 松散源路由跳指针(4,8,12，…)
-m, --max-conns <n>                 # 最大<n>同时连接
-h, --help                          # 显示此帮助屏幕
-d, --delay <time>                  # 读/写之间等
-o, --output <filename>             # 将会话数据转储到文件中
-x, --hex-dump <filename>           # 将会话数据作为十六进制转储到文件中
-i, --idle-timeout <time>           # 闲读/写超时
-p, --source-port port              # 指定要使用的源端口
-s, --source addr                   # 指定要使用的源地址(不影响-l)
-l, --listen                        # 绑定并侦听传入连接
-k, --keep-open                     # 在监听模式下接受多个连接
-n, --nodns                         # 不通过DNS解析主机名
-t, --telnet                        # 回答Telnet谈判
-u, --udp                           # 使用UDP而不是默认的TCP
    --sctp                          # 使用SCTP而不是默认的TCP
-v, --verbose                       # 设置冗余级别(可多次使用)
-w, --wait <time>                   # 连接超时
-z                                  # 0 - i /O模式，只报告连接状态
    --append-output                 # 追加而不是删除指定的输出文件
    --send-only                     # 只发送数据，忽略接收;戒烟对EOF
    --recv-only                     # 只接收数据，不发送任何东西
    --allow                         # 只允许给定的主机连接到Ncat
    --allowfile                     # 允许连接到Ncat的主机文件
    --deny                          # 拒绝给定主机连接到Ncat
    --denyfile                      # 拒绝连接到Ncat的主机文件
    --broker                        # 启用Ncat的连接代理模式
    --chat                          # 启动一个简单的Ncat聊天服务器
    --proxy <addr[:port]>           # 指定要通过代理的主机地址
    --proxy-type <type>             # 指定代理类型(“http”或“socks4”或“socks5”)

    --proxy-auth <auth>             # 使用HTTP或SOCKS代理服务器进行身份验证
    --ssl                           # 使用SSL连接或侦听
    --ssl-cert                      # 指定用于监听的SSL证书文件(PEM)
    --ssl-key                       # 指定用于监听的SSL私钥(PEM)
    --ssl-verify                    # 验证证书的信任和域名
    --ssl-trustfile                 # 包含可信SSL证书的PEM文件
    --ssl-ciphers                   # 包含要使用的SSL密码的密文列表  
    --ssl-alpn                      # 使用的ALPN协议列表。
    --version                       # 显示Ncat的版本信息并退出
```

## win：链接

```ncat
ncat -c bash --allow 192.168.14.20 -vnl 333 --ssl
ncat -nv 192.168.171.132 333 --ssl
```

## win和linux聊天

```ncat
win||linux
ncat -v -lp 8081
linux||win
ncat -v  192.168.3.219 8081
```

## linux|win链接

```ncat
win先监听，linux连win，在linux中执行命令（linux主动连接）
win:
ncat -c cmd.exe -v -lp 444
linux:
ncat -v  192.168.3.219 444

linux先监听，win连linux，在win中执行命令（win主动连接）
linux:
ncat -c bash -v -lp 444
win:
ncat -v  192.168.22.154 444

win先监听，linux连win，在win中执行命令（win被动连接）
win：
ncat -v -lp 444 --ssl
linux：
ncat -v -c bash 192.168.3.219 444 --ssl

linux先监听，win连linux，在linux中执行命令（linux被动连接）
linux：
ncat -v -lp 444
win：
ncat -v -c cmd.exe 192.168.22.154 444
```

## 文件传输

```ncat
linux先传输，win后接收
linux:
ncat -v -lp 444 < 1.txt
win:
ncat -v  192.168.22.154 444 > 1.txt

win先传输，linux后接收
win:
ncat  -v -lp 444 <  2.txt
linux:
ncat -v 192.168.3.219 444 > 2.txt

win连接收，linux后传输
win:
ncat -v -lp 444 > 3.txt
linux:
ncat -v 192.168.3.219 444 < 2.txt

linux连接收，win后传输
linux:
ncat -v -lp 444 > 4.txt
win:
ncat -v  192.168.22.154 444 < 1.txt
```

## 目录传输

```ncat
tar cvf - nc_dir | nc -v -lp 8081
nc -nv 192.168.1.130 8081 | tar xvf -
```
