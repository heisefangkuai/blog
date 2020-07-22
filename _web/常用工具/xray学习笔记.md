# xray学习笔记

下载地址：<https://github.com/chaitin/xray/releases>

xray 是一款功能强大的安全评估工具，web漏洞自动检测。目前支持的漏洞检测类型包括:

- XSS漏洞检测 (key: xss)
- SQL 注入检测 (key: sqldet)
- 命令/代码注入检测 (key: cmd_injection)
- 目录枚举 (key: dirscan)
- 路径穿越检测 (key: path_traversal)
- XML 实体注入检测 (key: xxe)
- 文件上传检测 (key: upload)
- 弱口令检测 (key: brute_force)
- jsonp 检测 (key: jsonp)
- ssrf 检测 (key: ssrf)
- 基线检查 (key: baseline)
- 任意跳转检测 (key: redirect)
- CRLF 注入 (key: crlf_injection)
- Struts2 系列漏洞检测 (高级版，key: struts)
- Thinkphp系列漏洞检测 (高级版，key: thinkphp)
- POC 框架 (key: phantasm)

其中 POC 框架默认内置 Github 上贡献的 poc，用户也可以根据需要自行构建 poc 并运行。

## xray的命令及用法

```xray
NAME:
   xray - A powerful scanner engine [https://xray.cool]

用法:
    [全局选项] 命令 [命令选项] [参数...]

命令S:
    webscan      运行一个web扫描任务
    servicescan  运行服务扫描任务
    poclint      lint yaml poc
    reverse      运行一个独立的反向服务器
    genca        生成CA证书和密钥
    upgrade      检查新版本并升级自我如果发现任何更新
    version      显示版本信息
    help, h      显示一个命令的命令列表或帮助

GLOBAL OPTIONS:
   --config FILE  从文件加载配置
   --help, -h     显示帮助
```

webscan命令选项：

```xray
NAME:
    webscan - 运行一个web扫描任务

USAGE:
    webscan [命令选项] [参数...]

OPTIONS:
   --plugins value         指定要运行的插件用','分隔
   --poc value             指定要运行的poc用','分隔

   --listen value          使用代理资源收集器，值为代理地址
   --basic-crawler value   使用基本的爬行器抓取目标并扫描结果
   --url-file value        从本地文件读取url并扫描这些url
   --url value             扫描一个url
   --data value            data string to be sent through POST (e.g. 'username=admin')
   --raw-request FILE      从文件中加载http原始请求

   --json-output FILE      输出xray结果到json格式的文件
   --html-output FILE      输出xray结果文件的HTML格式
   --webhook-output value  将xray结果以json格式发送到url
```

示例：

```xray
直接对目标进行爬虫扫描：
xray_windows_amd64.exe webscan --basic-crawler http://xxx/

使用浏览器代码扫描并输出html文件：
xray_windows_amd64.exe webscan --listen 127.0.0.1:1111 --html-output 1.html

```