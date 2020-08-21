# wfuzz 测试工具基本用法总结

## 基本用法

```python
生成随机数
python wfpayload.py -z range,0-10

加密解密
python wfencode.py -e md5 123456
python wfencode.py -e base64 123456
python wfencode.py -d base64 MTIzNDU2

wfuzz寻找常见目录:
python wfuzz-cli.py  -w ../wordlist/general/common.txt http://www.baidu.com/FUZZ
python wfuzz-cli.py  -z file,../wordlist/general/common.txt http://www.baidu.com/FUZZ

wfuzz寻找常见文件:
python wfuzz-cli.py  -w ../wordlist/general/common.txt http://www.baidu.com/FUZZ.php

URL中的模糊参数:
python wfuzz-cli.py  -z range,0-10 --hl 97 http://www.baidu.com/listproducts.php?id=FUZZ

使用多个payloads（使用-z 或-w 参数可以同时指定多个payloads，使用FUZZ, … , FUZnZ来表示）
wfuzz -w 1.txt -w 2.txt -w 2.txt --hc 404 http://www.baidu.com/FUZZ/FUZ2ZFUZ3Z

模糊POST请求，传入-d参数即可：
python wfuzz-cli.py  -z file,../wordlist/others/common_pass.txt -d "uname=FUZZ&pass=FUZZ"  --hc 302 http://www.baidu.com/userinfo.php

测试Cookies，设置cookies，可以使用-b参数指定，多个cookies使用多次。
wfuzz -z file,/common.txt -b cookie1=value1 -b cookie2=value2 http://www.baidu.com/FUZZ

测试自定义请求头，和修改请求头，使用-H参数来指定HTTP请求的请求头，多次指定多次使用
wfuzz -z file,/common.txt -H "myheader1: headervalue" -H "myheader2: headervalue2" http://www.baidu.com/FUZZ
python wfuzz-cli.py -w ../general/common.txt -H "User-Agent: Googlebot-News"  http://www.baidu.com/FUZZ

测试HTTP请求方法，通过指定-X参数指定：
python wfuzz-cli.py -z list,GET-HEAD-POST-TRACE-OPTIONS -X FUZZ http://www.baidu.com/

使用代理，可使用多个-p参数同时指定，每次请求都会选取不同的代理进行：
wfuzz -z file,/common.txt -p localhost:8080 -p localhost:9090 http://www.baidu.com/FUZZ

认证，wfuzz可以通过--basec/ntml/digest来设置认证头。
想要测试一个需要HTTP Basic Auth保护的内容可使用如下命令：
wfuzz -z list,nonvalid-httpwatch --basic FUZZ:FUZZ https://www.xxx.com/default.aspx

递归测试,使用-R参数可以指定一个payload被递归的深度。
wfuzz -z list,"admin-CVS-cgi\-bin" -R 1 http://www.baidu.com/FUZZ

测试速度与效率:
使用-t参数可以增加或减少同时发送HTTP请求的数量。
使用-s参数可以调节每次发送HTTP的时间间隔。

输出到文件:wfuzz通过printers插件来将结果以不同格式保存到文档中
wfuzz -f /tmp/outfile,json -w /general/common.txt http://www.baidu.com/FUZZ
```

## wfuzz过滤器

1. 隐藏响应结果:通过--hc，--hl，--hw，--hh参数可以隐藏某些HTTP响应。
2. 显示响应结果:显示响应结果的使用方法跟隐藏时的原理一样，只不过参数变为了：--sc，--sl，--sw，--sh。

- --hc 根据响应报文状态码进行隐藏（hide code）
- --hl根据响应报文行数进行隐藏（hide lines）
- --hw根据响应报文字数进行隐藏（hide word）
- --hh根据响应报文字符数进行隐藏（hide chars 这里因为code和chars首字母都是c，–hc参数已经有了，所以hide chars的参数就变成了–hh）
- --hs根据返回页面包含的内容

e.g:

```python
python wfuzz-cli.py --hc 404,400 --hl 6 --hw 123 --hh 1528 --hs "Not Found" --script=robots -z list,robots.txt http://www.fake-blog.com/FUZZ
```

## Iterators：组合payloads

不同的payload可以通过-m参数指定的方式组合起来，在wfuzz中，提供这种组合能力的功能的，我们称为迭代器。 

举例说明各个iterator是如何工作的:

```python
zip:
wfuzz -z list,a-b-c -z list,1-2-3 -m zip http://www.baidu.com/FUZZ/FUZ2Z
000001: C=302 7 L 18 W 222 Ch "a - 1"
000002: C=302 7 L 18 W 222 Ch "b - 2"
000003: C=302 7 L 18 W 222 Ch "c - 3"

chain:
wfuzz -z list,a-b-c -z list,1-2-3 -m chain http://www.baidu.com/FUZZ
000001: C=302 7 L 18 W 222 Ch "a"
000002: C=302 7 L 18 W 222 Ch "b"
000003: C=302 7 L 18 W 208 Ch "c"
000004: C=302 7 L 18 W 222 Ch "1"
000005: C=302 7 L 18 W 222 Ch "2"
000006: C=302 7 L 18 W 222 Ch "3"

product:
wfuzz -z list,a-b-c -z list,1-2-3 -m product http://www.baidu.com/FUZZ/FUZ2Z
000008: C=302 7 L 18 W 222 Ch "c - 2"
000009: C=302 7 L 18 W 222 Ch "c - 3"
000001: C=302 7 L 18 W 222 Ch "a - 1"
000002: C=302 7 L 18 W 222 Ch "a - 2"
000003: C=302 7 L 18 W 222 Ch "a - 3"
000004: C=302 7 L 18 W 222 Ch "b - 1"
000005: C=302 7 L 18 W 222 Ch "b - 2"
000006: C=302 7 L 18 W 222 Ch "b - 3"
000007: C=302 7 L 18 W 222 Ch "c - 1"
```

## Encoders

在wfuzz中，encoder的作用是将payload从一种格式转换成另一种格式。 

```python
encoders是通过payload参数传进去的。
python wfuzz-cli.py -z file --zP fn=common.txt,encoder=md5 http://www.baidu.com/FUZZ
python wfuzz-cli.py -z file,../wordlist/general/common.txt,md5  http://www.baidu.com/FUZZ

python wfuzz-cli.py -w ../wordlist/general/common.txt,md5  http://www.baidu.com/FUZZ

使用多个Encoder,使用-号分隔的列表来指定
wfuzz -z list,1-2-3,md5-sha1-none http://www.baidu.com/FUZZ

同时按顺序使用多个encoders，可以使用一个@号分隔的列表来指定，如：
参数中的sha1@none，会将payload先进行sha1，然后传给none这个encoder。
wfuzz -z list,1-2-3,sha1-sha1@none http://www.baidu.com/FUZZ

Encoders是分类的，我们还可以使用类型名称来指定同类的所有encoders：
wfuzz -z list,1-2-3,hashes http://www.baidu.com/FUZZ

```

## 保存使用的wfuzz命令

- --dump-recipe 参数用来保存命令
- --recip 参数用来调用保存的命令

```python
python  wfuzz-cli.py -z list,1-2-3 --dump-recipe ./1.json http://www.baidu.com/FUZZ
python wfuzz-cli.py  --recip ./1.json
```

## 扫描模式

当出现网络问题，如DNS解析失败，拒绝连接等时，wfuzz会抛出一个异常并停止执行，当我们使用-Z(注意是大写)参数时，wfuzz就会忽略这些网络错误而继续执行：

出现错误的payload会以返回码XXX来表示，Payload中还有出现的错误。

```python
wfuzz -z list,support-none -Z http://FUZZ.baidu.com/
```

超时：这些功能有时候会很有用，比如使用代理/某个端口/主机名/虚拟主机进行扫描时。

- 使用--conn-delay来设置wfuzz等待web server响应接连的秒数。
- 使用--req-delay来设置wfuzz等待响应完成的最大秒数。

## 过滤器语法

wfuzz的过滤器是基于pyparsing开发的，所以在使用--filter，--prefilter，--slice之前，请先安装上pyparsing。

一个过滤器表达式必须使用由以下符号或操作符构成：

- Boolean Operators 是非操作符：and，or，not
- Expression Operators 逻辑操作符：=，!=，<，>，>=，<=

除此之外，还有下列用于文本的操作符：

- =~ 符合正则表达式则为True
- ~  等同于Python语法中的 “str2” in “str1”，不区分大小写
- !~ 与上面一条相反，“str2” not in “str1”，不区分大小写

URL解析模块urlparse，会把url拆分

使用--filter参数加上上面的过滤器语法，我们可以写出比--hc/hl/hw/hh，--sc/sl/sw/sh和--ss/hs更加复杂和精细的过滤条件。

```python
检测状态码200和l>97的
wfuzz -z range,0-10 --filter "c=200 and l>97" http://www.baidu.com/listproducts.php?

利用输出结果和payload检查来找出含有某些特定内容的返回体：
wfuzz -z list,echoedback -d searchFor=FUZZ --filter "content~FUZZ" http://www.baidu.com/search.php?test=query

wfuzz -z list,echoedback -d searchFor=FUZZ --ss "echoedback" http://www.baidu.com/search.php?test=query

wfuzz -w fuzzdb/attack/xss/xss-rsnake.txt -d searchFor=FUZZ --filter "intext~FUZZ" http://www.baidu.com/search.php?test=query

过滤payload
切片：使用--slice参数，结合过滤器语法，我们可以对payload进行过滤。--slice参数必须在-z参数后。 
wfuzz -z list,one-two-one-one --slice "FUZZ|u()" http://localhost/FUZZ

预过滤
--prefilter参数与--slice相似，不过它并没有和任何payload相关。它是一个通用的过滤，在HTTP请求发送之前进行。
```

## 输出结果再利用

之前获得的HTTP请求/响应中包含很多有价值的数据。利用已经得到的数据，我们可以进行下列方面的挖掘：

- 单个请求重放
- 对比测试请求与正常请求中的响应体中的头和体
- 从请求中查找URL中带有CSRF token的请求
- 从返回中查找返回体为Json内容但返回头的content-type设置错误。

为了能够使用之前得到的结果，我们需要使用能够生成完整FuzzResult对象的payload。

```python
wfuzz结果可以通过使用-oF参数进行保存：
wfuzz --oF /tmp/session -z range,0-10 http://www.baidu.com/dir/test.php?id=FUZZ
```

burpstate 和 burplog payload

wfuzz能够读取burpsuite保存的state和日记文档，使得我们能够重复利用能够burpsuite代理生成的请求和响应信息。

```python
要重放burp保存的请求，我们需要在命令行中使用FUZZ占位符：
wfuzz -z burpstate,a_burp_state.burp FUZZ
wfuzz -z burplog,a_burp_log.burp FUZZ
wfuzz -z wfuzzp,/tmp/session FUZZ

之前的请求还能够像平时那样通过命令行参数进行更改，比如：

增加新的header：
wfuzz -z burpstate,a_burp_state.burp -H "addme: header" FUZZ

使用新的cookie：
wfuzz -z burpstate,a_burp_state.burp -z list,1-2-3 -b "cookie=FUZ2Z" FUZZ

已经保存的HTTP请求还可以通过--prev参数被打印出来与新的结果进行比较：
wfuzz -z burpstate,testphp.burp --slice "cookies.request and url|u()" --filter "c!=FUZZ[c]" -b "" --prev FUZZ

将相同的请求发送到另一个URL上：
wfuzz -z burpstate,a_burp_state.burp -H "addme: header" -u http://www.otherhost.com FUZZ

如果不想使用保存的所有请求：

使用attr我们可以获得一些特定的HTTP对象内容：
wfuzz -z wfuzzp,/tmp/session --zP attr=url FUZZ

或者，通过FUZZ[field]的方式：
wfuzz -z wfuzzp,/tmp/session FUZZ[url]

比如，我们可以在保存的值的基础上发送新的请求：
wfuzz -z wfuzzp,/tmp/session -p localhost:8080 http://www.baidu.com/FUZZ[url.path]?FUZZ[url.query]
```

## 扫描/解析插件

wfuzz的扫描和解析都是通过插件来实现的。 插件脚本（scripts）是分类的。一个脚本可以同时属于多个分类。

wfuzz有两个分类：

1. passive：这些插件实现分析已经得到的请求和响应，不产生新的请求。
2. active：这些插件会向目标发送请求来探测漏洞是否存在。

还有一类附加插件：

1. discovery：这些插件会自动帮助wfuzz对目标站进行爬取，并将发现的内容提供给wfuzz进行请求。

使用-A与--script=default相同。

```python
一个分析robots.txt的wfuzz命令如下：
wfuzz --script=robots -z list,robots.txt http://www.webscantest.com/FUZZ

```

自定义插件:用户自己开发的脚本插件，应放在如下目录下：~/.wfuzz/scripts


