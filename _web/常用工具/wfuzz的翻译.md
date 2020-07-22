# Wfuzz：强大的Web Fuzz测试工具

wfuzz 是一款Python开发的Web安全测试工具,wfuzz不仅仅是一个web扫描器，wfuzz能够通过发现并利用网站弱点/漏洞的方式帮助你使网站更加安全。wfuzz的漏洞扫描功能由插件支持。

wfuzz是一个完全模块化的框架，这使得即使是Python初学者也能够进行开发和贡献代码。开发一个wfuzz插件是一件非常简单的事，通常只需几分钟。

wfuzz提供了简洁的编程语言接口来处理wfuzz或Burpsuite获取到的HTTP请求和响应。这使得你能够在一个良好的上下文环境中进行手工测试或半自动化的测试，而不需要依赖web形式的扫描器。

Wfuzz是一个为暴力破解Web应用程序而设计的工具，它可以用于查找未链接的资源（目录，servlet，脚本等），暴力GET和POST参数以检查不同类型的注入（SQL，XSS，LDAP等），强力表单参数（用户/密码），Fuzzing等。它支持多种方法来测试WEB应用的漏洞，你可以审计参数、登录认证、GET/POST方式爆破的表单，并且可以发掘未公开的资源，比如目录、文件和头部之类的。

## Wfuzz一些功能

- 具有多个词典的多注入点功能
- 递归（当做目录暴力时）
- 发布，标头和认证数据暴力强制
- 输出到HTML
- 彩色输出
- 按返回码，字数，行号，正则表达式隐藏结果
- Cookies fuzzing 多参数fuzz
- 多线程
- 代理支持
- SOCK支持
- 请求之间的时间延迟
- 身份验证支持（NTLM，基本）
- 所有参数bruteforce（POST和GET）
- 每个有效载荷多个编码器
- 有效载荷与迭代器的组合
- 基线请求（用于过滤结果）
- 蛮力HTTP方法
- 多个代理支持（每个请求通过不同的代理）
- HEAD扫描（资源发现更快）
- 为已知应用量身定制的字典（Weblogic，Iplanet，Tomcat，Domino，Oracle 9i，Vignette，Coldfusion等等）
- Post数据爆破
- 头部爆破
- 输出HTML（详细报告，点击链接查看内容，POST数据也能阅览）
- URL编码

## wfuzz 中文命令

```python
Usage:    wfuzz [options] -z payload,params <url>
    FUZZ, ..., FUZnZ              payload占位符，wfuzz会用指定的payload代替相应的占位符，n代表数字.
    FUZZ{baseline_value}     FUZZ 会被 baseline_value替换，并将此作为测试过程中第一个请求来测试，可用来作为过滤的一个基础。
Options:
    -h/--help                   : 帮助文档
    --help                      : 高级帮助文档
    --version                   : Wfuzz详细版本信息
    -e <type>                   : 显示可用的encoders/payloads/iterators/printers/scripts列表
    --recipe <filename>         : 从文件中读取参数
    --dump-recipe <filename>    : 打印当前的参数并保存成文档
    --oF <filename>             : 将测试结果保存到文件，这些结果可被wfuzz payload 处理
    -c                          : 彩色化输出
    -v                          : 详细输出
    -f filename,printer         : 将结果以printer的方式保存到filename (默认为raw printer).
    -o printer                  : 输出特定printer的输出结果
    --interact                  : (测试功能) 如果启用，所有的按键将会被捕获，这使得你能够与程序交互
    --dry-run                   : 打印测试结果，而并不发送HTTP请求
    --prev                      : 打印之前的HTTP请求（仅当使用payloads来生成测试结果时使用）
    -p addr                     : 使用代理，格式 ip:port:type. 可设置多个代理，type可取的值为SOCKS4,SOCKS5 or HTTP（默认）
    -t N                        : 指定连接的并发数，默认为10
    -s N                        : 指定请求的间隔时间，默认为0
    -R depth                    : 递归路径探测，depth指定最大递归数量
    -L,--follow                 : 跟随HTTP重定向
    -Z                          : 扫描模式 (连接错误将被忽视).
    --req-delay N               : 设置发送请求允许的最大时间，默认为 90，单位为秒.
    --conn-delay N              : 设置连接等待的最大时间，默认为 90，单位为秒.
    -A                          : 是 --script=default -v -c 的简写
    --script=                   : 与 --script=default 等价
    --script=<plugins>          : 进行脚本扫描， <plugins> 是一个以逗号分开的插件或插件分类列表
    --script-help=<plugins>     : 显示脚本的帮助
    --script-args n1=v1,...     : 给脚本传递参数. ie. --script-args grep.regex="<A href=\"(.*?)\">"
    -u url                      : 指定请求的URL
    -m iterator                 : 指定一个处理payloads的迭代器 (默认为product)
    -z payload                  : 为每一个占位符指定一个payload，格式为 name[,parameter][,encoder].编码可以是一个列表, 如 md5-sha1. 还可以串联起来, 如. md5@sha1.还可使用编码各类名，如 url使用help作为payload来显示payload的详细帮助信息，还可使用--slice进行过滤
    --zP <params>               : 给指定的payload设置参数。必须跟在 -z 或-w 参数后面
    --slice <filter>            : 以指定的表达式过滤payload的信息，必须跟在-z 参数后面
    -w wordlist                 : 指定一个wordlist文件，等同于 -z file,wordlist
    -V alltype                  : 暴力测试所有GET/POST参数，无需指定占位符
    -X method                   : 指定一个发送请求的HTTP方法，如HEAD或FUZZ
    -b cookie                   : 指定请求的cookie参数，可指定多个cookie
    -d postdata                 : 设置用于测试的POST data (ex: "id=FUZZ&catalogue=1")
    -H header                   : 设置用于测试请求的HEADER (ex:"Cookie:id=1312321&user=FUZZ"). 可指定多个HEADER.
    --basic/ntlm/digest auth    : 格式为 "user:pass" or "FUZZ:FUZZ" or "domain\FUZ2Z:FUZZ"
    --hc/hl/hw/hh N[,N]+        : 以指定的返回码/行数/字数/字符数作为判断条件隐藏返回结果 (用 BBB 来接收 baseline)
    --sc/sl/sw/sh N[,N]+        : 以指定的返回码/行数/字数/字符数作为判断条件显示返回结果 (用 BBB 来接收 baseline)
    --ss/hs regex               : 显示或隐藏返回结果中符合指定正则表达式的返回结果
    --filter <filter>           : 显示或隐藏符合指定filter表达式的返回结果 (用 BBB 来接收 baseline)
    --prefilter <filter>        : 用指定的filter表达式在测试之前过滤某些测试条目
```

## wfuzz中的Payloads

一个wfuzz中的payload就是一个输入的源。

```python
得到所有可用的payload列表:
python wfuzz-cli.py -e payloads

关于payloads的更详细的信息:
python wfuzz-cli.py -z help

还可以使用--slice参数来对输出结果进行过滤：
python wfuzz-cli.py -z help --slice "stdin"

stdin这个payload可以在使用一些外部字典生成工具时很方便：
crunch 2 2 ab | wfuzz -z stdin http://testphp.vulnweb.com/FUZZ
```

## wfuzz的关键字

payload为wfuzz生成的用于测试的特定字符串，一般情况下，会替代被测试URL中的FUZZ占位符。

```python
python wfuzz-cli.py -e payloads:

guitab              | 从可视化的标签栏中读取请求
dirwalk             | 递归获得本地某个文件夹中的文件名
file                | 获取一个文件当中的每个词
autorize            | 获取autorize的测试结果Returns fuzz results from autororize.
wfuzzp              | 从之前保存的wfuzz会话中获取测试结果的URL
ipnet               | 获得一个指定网络的IP地址列表
bing                | 获得一个使用bing API搜索的URL列表 (需要 api key).
stdin               | 获得从标准输入中的条目
list                | 获得一个列表中的每一个元素，列表用以 - 符号分格
hexrand             | 从一个指定的范围中随机获取一个hex值
range               | 获得指定范围内的每一个数值
names               | 从一个以 - 分隔的列表中，获取以组合方式生成的所有usernames值
burplog             | 从BurpSuite的记录中获得测试结果
permutation         | 获得一个在指定charset和length时的字符组合
buffer_overflow     | 获得一个包含指定个数个A的字符串.
hexrange            | 获得指定范围内的每一个hex值
iprange             | 获得指定IP范围内的IP地址列表
burpstate           | 从BurpSuite的状态下获得测试结果
```

encoder的作用是将payload进行编码或加密。

```python
wfuzz -e encoders:

url_safe, url   | urlencode         | 用`%xx`的方式替换特殊字符， 字母/数字/下划线/半角点/减号不替换
url_safe, url   | double urlencode  | 用`%25xx`的方式替换特殊字符， 字母/数字/下划线/半角点/减号不替换
default         | random_upper      | 将字符串中随机字符变为大写
default         | hexlify           | 每个数据的单个比特转换为两个比特表示的hex表示
default         | none              | 不进行任何编码
hashes          | md5               | 将给定的字符串进行md5加密
hashes          | base64            | 将给定的字符串中的所有字符进行base64编码
hashes          | sha1              | 将字符串进行sha1加密
html            | html_escape       | 将`&`，`<`，`>`转换为HTML安全的字符
html            | html_hexadecimal  | 用 `&#xx;` 的方式替换所有字符
html            | html_decimal      | 将所有字符以 `&#dd; ` 格式进行编码
url             | uri_double_hex    | 用`%25xx`的方式将所有字符进行编码
url             | doble_nibble_hex  | 将所有字符以`%%dd%dd`格式进行编码
url             | utf8              | 将所有字符以`\u00xx` 格式进行编码
url             | first_nibble_hex  | 将所有字符以`%%dd?` 格式进行编码
url             | uri_hex           | 将所有字符以`%xx` 格式进行编码
url             | second_nibble_hex | 将所有字符以`%?%dd` 格式进行编码
url             | utf8_binary       | 将字符串中的所有字符以 `\uxx` 形式进行编码
url             | uri_triple_hex    | 将所有字符以`%25%xx%xx` 格式进行编码
url             | uri_unicode       | 将所有字符以`%u00xx` 格式进行编码
db              | mssql_char        | 将所有字符转换为MsSQL语法的`char(xx)`形式
db              | oracle_char       | 将所有字符转换为Oracle语法的`chr(xx)`形式
db              | mysql_char        | 将所有字符转换为MySQL语法的`char(xx)`形式
```

wfuzz的iterator提供了针对多个payload的处理方式。

```python
wfuzz -e iterator:

product     | 返回输入条目的笛卡尔积
zip         | Retns an iterator that aggregates elements from each of the iterables.（翻译不好，请自行理解）
chain       | Returns an iterator returns elements from the first iterable until it is exhaust| ed, then proceeds to the next iterable, until all of the iterables are exhausted| （翻译不好，请自行理解）
```

wfuzz的printers用于控制输出打印。

```python
wfuzz -e printers:

raw         | “原始”的输出格式
json        | 结果为“json”格式
csv         | “CSV”打印机增值
magictree   | 打印结果为“magictree”格式
html        | 以“html”格式打印结果
```

暂时不知道怎么使用

```python
wfuzz -e scripts:

default, passive            | cookies       | 查找新的cookies
default, passive            | errors        | 查找错误信息
passive                     | grep          | HTTP response grep
active                      | screenshot    | 用linux cutycapt tool 进行屏幕抓取
default, active, discovery  | links         | 解析HTML并查找新的内容
default, active, discovery  | wc_extractor  | 解析subversion的wc.db文件
default, passive            | listing       | 查找列目录漏洞
default, passive            | title         | 解析HTML页面的title
default, active, discovery  | robots        | 解析robots.txt文件来查找新内容
default, passive            | headers       | 查找服务器的返回头
default, active, discovery  | cvs_extractor | 解析 CVS/Entries 文件
default, active, discovery  | svn_extractor | 解析 .svn/entries 文件
active, discovery           | backups       | 查找已知的备份文件名
default, active, discovery  | sitemap       | 解析 sitemap.xml 文件
```
