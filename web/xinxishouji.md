# 基础信息

## 需要收集的信息

1. 域名、rebost.txt、whois信息、备案信息、DNS记录、ip、端口
2. 网站子域名
3. 敏感目录和文件
4. 网站指纹：服务器(Linux/Windows)、网站容器(Apache/Nginx/Tomcat/IIS)、脚本(php/jsp/asp/aspx)、数据库(Mysql/Oracle/Accees/Mqlserver/...)
5. 旁站和C段
6. Github/SVN信息：泄露源码，敏感信息等
7. 邮箱信息
8. 信息泄露

### whois查询方法

一、whois能查询到什么信息

- 域名所有人
- 域名注册商
- 注册人地址
- 域名注册时间/到期时间
- 域名状态
- 域名DNS服务器
- 域名联系信息
- 等等

二、网站查询

第三方：

- *站长工具: `http://whois.chinaz.com/`
- 腾讯WHOIS：`https://whois.cloud.tencent.com/`
- 爱站 `https://whois.aizhan.com/`
- 5118 `https://www.5118.com/`
- 国际域名whois: `https://whois.cnnic.cn/WelcomeServlet`
- *国外多信息查询：`https://www.yougetsignal.com/`
- *国外查询网站：`https://bgp.he.net/dns/`

各大注册商以及第三方站长工具的域名WHOIS信息查询地址：

- 万网WHOIS：`https://whois.aliyun.com/`
- 西部数码WHOIS：`https://whois.west.cn/`
- 新网WHOIS：`http://whois.xinnet.com/domain/whois/index.jsp`
- 纳网WHOIS：`http://whois.nawang.cn/`
- 中资源WHOIS：`https://www.zzy.cn/domain/whois.html`
- 三五互联WHOIS：`https://cp.35.com/chinese/whois.php`
- 新网互联WHOIS：`http://www.dns.com.cn/show/domain/whois/index.do`
- 美橙互联WHOIS：`https://whois.cndns.com/`
- 爱名网WHOIS：`https://www.22.cn/domain/`
- 易名网WHOIS：`https://whois.ename.net/`

三、查询工具

```shell
nmap --script=whois-domain 域名

dmitry -w 域名

whois 域名
```

四、whois信息利用

- 在社工库查询邮箱和手机号，获得更多相关联的信息资产，若查到，可尝试登陆服务器商或域名商。
- 利用注册人电话，邮箱等信息通过自由拼接组合成针对网站的社工字典。最后利用字典进行爆破或社工钓鱼，也可用过邮箱和手机号反查找到更多注册域名。
- DNS解析记录可以查ip,查NS、mx邮件交换记录。
- MX记录是邮件服务交换记录，邮件服务经常搭建在目标办公网络，可以让快速我们定位目标核心区域并展开渗透。

查询mx记录,命令：`nslookup -qt=mx baidu.com` (目标地址)

### 备案信息

这个只针对于国内来说。国外服务器不需要备案。也没有什么好说的，查一查先查一查网站的备案主体，在查主体的企业信息，直接放上几个网站，有很多就不整理了

```url
https://www.beian88.com/
http://www.beianbeian.com/
https://www.qichacha.com/
https://www.tianyancha.com/
http://www.gsxt.gov.cn/index.html
```

### DNS记录

- 站长工具DNS: `https://tool.chinaz.com/dns/`
- Nslookup域名解析：`http://www.jsons.cn/nslookup/`

### ip查询

```linux
ping 域名
https://ipinfo.io/
https://www.ip138.com/
https://www.ipip.net/ip.html
```

ip段整理：中国互联网络信息中心:`http://ipwhois.cnnic.cn/index.jsp`

找真实ip：
钟馗之眼：`https://www.zoomeye.org/`
censys：`https://censys.io/`
shodan：`https://www.shodan.io/`
全球dns搜索引擎：`https://dnsdb.io/zh-cn/`
FOFA：`https://fofa.so/`
surfwax元搜索：`http://lookahead.surfwax.com/`
Way Back Machine(搜索网站过去的样子)：`http://www.wayback.com/`
google学术：`https://scholar.google.com/`

还有一种方法就是让网站只要与我建立连接

[元搜索](./qt/元素搜索引擎.md)
[绕过CDN寻找真实IP的8种方法](./qt/绕过CDN寻找真实IP的8种方法.md)

### 端口

[端口服务和测试方法](./qt/端口服务和测试方法.md)

端口扫描工具：
nmap
masscan
scanport
[御剑端口扫描工具](https://github.com/saulty4ish/Dir_Scan_ByQT5)


### 网站子域名

为什么要进行子域名收集？

1. 子域名探测可以帮我们发现渗透测试中更多的服务，它们在安全评估的范围内，从而增加了发现漏洞的机会。
2. 查找一些用户上较少，被人遗忘的子域名，其上运行的应用程序可能会使我们发现关键漏洞。
3. 通常，同一组织的不同域名/应用程序中存在相同的漏洞。

子域名查询的几种方法：

1. 爬虫爬取页面提取子域名
2. 文件泄漏(crossdomain.xml、robots.txt)
3. 搜索引擎查询(Google Hacking:site:域名、inurl、intitle、filetype、intext、Index of/、cache：缓存)
4. 网络空间资产搜索引擎(Zoomeye、Shodan、Fofa)
5. 备案号反查(`http://www.beianbeian.com/`)
6. 子域名枚举扫描器或爆破工具
7. ssl证书查询(`https://crt.sh/`、`https://censys.io/`、`https://dnsdumpster.com/`)
8. DNS转送漏洞
9. 子域名监控(sublert/get_domain/assetnote/LangSrcCurise)
10. 通过 IP 反查（类似于旁站查询）
11. 在线网站收集
12. 数据聚合网站
13. 其他(git、burp插件domain_hunter)
14. 火狐浏览器证书泄密：访问一个https的网站可能会出现，安全风险，点击连接详情

- 数据聚合网站

```l
threatcrowd
https://scans.io/study/sonar.rdns_v2
https://opendata.rapid7.com/
```

- 在线网站收集

```url
https://d.chinacycc.com/
http://tool.chinaz.com/subdomain/
https://www.virustotal.com/
https://censys.io/
https://x.threatbook.cn/
https://phpinfo.me/domain/
http://z.zcjun.com/
https://crt.sh/
https://dnsdumpster.com/
https://spyse.com/site/not-found?q=domain%3A%22github%22&criteria=cert
```

- 子域名枚举扫描器或爆破工具

```linux
https://github.com/euphrat1ca/LayerDomainFinder/releases(Layer子域名挖掘机5.0)
https://github.com/lijiejie/subDomainsBrute (lijiejie开发的一款使用广泛的子域名爆破枚举工具)
https://github.com/ring04h/wydomain (猪猪侠开发的一款域名收集全面、精准的子域名枚举工具)
https://github.com/le4f/dnsmaper (子域名枚举爆破工具以及地图位置标记)
https://github.com/0xbug/orangescan (提供web界面的在线子域名信息收集工具)
https://github.com/TheRook/subbrute （高效精准的子域名爆破工具,同时也是扫描器中最常用的子域名API库)
https://github.com/We5ter/GSDF (基于谷歌SSL透明证书的子域名查询脚本)
https://github.com/mandatoryprogrammer/cloudflare_enum （使用CloudFlare进行子域名枚举的脚本）
https://github.com/guelfoweb/knock (Knock子域名获取，可用于查找子域名接管漏洞)
https://github.com/exp-db/PythonPool/tree/master/Tools/DomainSeeker （多方式收集目标子域名信息）
https://github.com/code-scan/BroDomain (兄弟域名查询）
https://github.com/chuhades/dnsbrute (高效的子域名爆破工具)
https://github.com/yanxiu0614/subdomain3 (一款高效的子域名爆破工具）
https://github.com/michenriksen/aquatone (子域名枚举、探测工具。可用于子域名接管漏洞探测)
https://github.com/evilsocket/dnssearch (一款子域名爆破工具)
https://github.com/reconned/domained (可用于子域名收集的一款工具）
https://github.com/bit4woo/Teemo (域名收集及枚举工具)
https://github.com/laramies/theHarvester (邮箱、服务器信息收集及子域名枚举工具）
https://github.com/swisskyrepo/Subdomino (子域名枚举，端口扫描，服务存活确认）
https://github.com/nmalcolm/Inventus (通过爬虫实现的子域名收集工具）
https://github.com/aboul3la/Sublist3r (快速子域枚举工具)
https://github.com/jonluca/Anubis （子域名枚举及信息搜集工具）
https://github.com/n4xh4ck5/N4xD0rk (子域名查询工具)
https://github.com/infosec-au/altdns (一款高效的子域名爆破工具)
https://github.com/FeeiCN/ESD (基于AsyncIO协程以及非重复字典的子域名爆破工具)
https://github.com/giovanifss/Dumb (快速而灵活的子域名爆破工具)
https://github.com/UnaPibaGeek/ctfr (通过域名透明证书记录获取子域名)
https://github.com/caffix/amass (Go语言开发的子域名枚举工具)
https://github.com/Ice3man543/subfinder (继承于sublist3r项目的模块化体系结构，一个强劲的子域名枚举工具)
https://github.com/k8gege/K8tools (k8最近分享了很多工具具体见github：)
https://github.com/projectdiscovery/shuffledns(shuffleDNS是一款基于MassDNS开发的强大工具，该工具采用Go语言开发)
https://github.com/wangoloj/dnsdumpster(第三方服务收集的dns数据来检索)

https://github.com/Screetsec/Sudomy(Sudomy子域枚举工具,收集了20个第三方站点收集数据)
https://github.com/bitquark/dnspop/tree/master/results 子域名字典
```

- 子域名后处理

```l
在线去重平台： http://quchuchongfu.renrensousuo.com/
http状态码批量检测工具： http://dx3.pc0359.cn/soft/h/httpztmpljc.rar
轻量WebTitle扫描器：https://mega.nz/#!j7hz0KQS!ePUMUKZuSVnguGkcc78CZxarIuEVY1lfpQCVh69wob4
批量获取网站首页截图工具：https://mega.nz/#!5WAXHapS!zUM_CX6iQfv5IZmJvmQsoL7AXy12T3oXATfPETWkQJE
```

### 敏感目录和文件

[FileScan](https://github.com/Mosuan/FileScan)
[dirmap](https://github.com/H4ckForJob/dirmap)-体验不是很好
[7kbscan](https://github.com/7kbstorm/7kbscan-WebPathBrute/releases)

### 网站指纹

云悉：`https://www.yunsee.cn/`
米斯特：`https://www.godeye.vip/`
TScan：`https://scan.top15.cn/`
浏览器插件：wappalyzer

#### 服务器类型

服务器信息包括服务器用的操作系统：Linux 还是 Windows 。现在企业网站服务器的操作系统有百分之九十以上用的是Linux操作系统。知道了服务器的操作系统之后，还需要知道操作系统使用的具体版本。因为很多低版本的操作系统都存在已知的漏洞。

- ping判断

判断是Linux还是Windows最简单就是通过ping来探测，Windows的TTL值都是一般是128，Linux则是64。所以大于100的肯定是Windows，而几十的肯定是Linux。但是，通过TTL值来判断服务器类型也不是百分之百准确的，有些windows服务器的TTL值也是几十，而且有的服务器禁止ping。

- nmap判断

而判断目标网站服务器的具体的版本的话，可以采用 nmap 进行扫描， -O 和 -A 参数都能扫描出来

### 旁站和C段

https://webscan.cc/

















[github监控程序](https://github.com/0xbug/Hawkeye)

邮箱信息
推荐星数：★★

常见的在线邮箱收集网站，这些网站通过爬虫，搜索引擎等方式，获取互联网上暴露的邮箱地址。

```url
http://www.skymem.info/
https://hunter.io/
https://email-format.com/
```

网盘信息收集

```url
http://magnet.chongbuluo.com/
http://www.panduoduo.net/
http://www.zhuzhupan.com/
https://www.quzhuanpan.com/
https://www.panc.cc
```

漏洞库信息

查询历史漏洞，获取目标之前存在的安全问题，可以利用已知漏洞直接对目标系统进行攻击。

http://www.anquan.us/