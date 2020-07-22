# iis漏洞集合

## IIS短文件漏洞

- 检测脚本

```linux
http-iis-short-name-brute       # nmap iis短域名检测脚本，但是并不好使
https://github.com/irsdl/iis-shortname-scanner/     # java 检测脚本
https://github.com/WebBreacher/tilde_enum           # python 检测脚本
https://github.com/lijiejie/IIS_shortname_Scanner   # python 检测脚本,这个好用
```

- 受影响的版本

```iis
IIS 1.0，Windows NT 3.51
IIS 3.0，Windows NT 4.0 Service Pack 2
IIS 4.0，Windows NT 4.0选项包
IIS 5.0，Windows 2000
IIS 5.1，Windows XP Professional和Windows XP Media Center Edition
IIS 6.0，Windows Server 2003和Windows XP Professional x64 Edition
IIS 7.0，Windows Server 2008和Windows Vista
IIS 7.5，Windows 7（远程启用<customErrors>或没有web.config）

IIS 7.5，Windows 2008（经典管道模式）
注意：IIS使用.Net Framework 4时不受影响

IIS 8.0，Windows 8, Windows Server 2012
IIS 8.5，Windows 8.1,Windows Server 2012 R2
IIS 10.0，Windows 10, Windows Server 2016
```

经验证，以上受影响范围主要是针对HTTP GET方法，且需要同时安装ASP.NET应用程序。该漏洞发现者在2014年再次披露：在测试IIS 7.5(Windows 2008 R2)和IIS 8.0(Windows 2012)过程中，当使用OPTIONS来代替GET 方法时，如果请求中的短文件名是存在的，IIS就会返回一个不一样的错误信息。利用这种特点，攻击者就可以在最新的IIS版本中，实现基于短文件名的文件或目录扫描了。

目前IIS支持短文件名猜测的HTTP方法主要包括：DEBUG、OPTIONS、GET、POST、HEAD、TRACE六种，经千里目实验室验证，IIS 8.0、IIS 8.5和IIS 10.0的短文件名称均可以通过OPTIONS和TRACE方法被猜测成功。所以上述受影响版本需要再加上如下版本：

可以看到，IIS全部版本都存在短文件名泄漏的问题，微软似乎忽视了这个问题。从微软回复该漏洞发现者的消息可以看出，IIS短文件漏洞未达到安全更新标准，且需要确定何时在下一个逻辑版本中解决它

- 漏洞危害

利用“~”字符猜解暴露短文件/文件夹名 （主要危害）

Windows 10内置的IIS 10.0默认站点根目录，iisstart.htm和iisstart.png是网站默认文件，文件名前缀字符长度均没有达到9位，所以没有短文件名。IIS10test.html是人为添加的网站文件，文件名前缀字符长度达到了9位，对应的短文件名为IIS10T~1.HTM。根据此特性，我们能够通过访问短文件名间接访问它对应的文件。

由于短文件名的长度固定（xxxxxx~xxxx），因此攻击者可直接对短文件名进行暴力破解 ，从而访问对应的文件。

举个例子，有一个数据库备份文件 backup_20180101.sql ，它对应的短文件名是 backup~1.sql 。因此攻击者只要暴力破解出backup~1.sql即可下载该文件，而无需破解完整的文件名。

IIS短文件名有以下几个特征:

1.只有前六位字符直接显示，后续字符用~1指代。其中数字1还可以递增，如果存在多个文件名类似的文件（名称前6位必须相同，且后缀名前3位必须相同）；
2.后缀名最长只有3位，多余的被截断，超过3位的长文件会生成短文件名；
3.所有小写字母均转换成大写字母；
4.长文件名中含有多个“.”，以文件名最后一个“.”作为短文件名后缀；
5.长文件名前缀/文件夹名字符长度符合0-9和Aa-Zz范围且需要大于等于9位才会生成短文件名，如果包含空格或者其他部分特殊字符，不论长度均会生成短文件

我们可以在启用.net的IIS下使用GET方法暴力列举短文件名，原因是攻击者使用通配符“*”和“?”发送一个请求到IIS,当IIS接收到一个文件路径中包含“~”请求时，它的反应是不同的，即返回的HTTP状态码和错误信息不同。基于这个特点，可以根据HTTP的响应区分一个可用或者不可用的文件。访问构造的某个存在的短文件名，会返回404；访问构造的某个不存在的短文件名，会返回400；

在IIS高版本（如：IIS 8.0/IIS 8.5/IIS 10.0），即使没有安装asp.net，通过OPTIONS和TRACE方法也可以猜解成功。

.Net Framework的拒绝服务攻击 （副危害）
攻击者如果在文件夹名称中向发送一个不合法的.Net文件请求，.NeFramework将递归搜索所有的根目录，消耗网站资源进而导致DOS问题。

- IIS短文件漏洞局限性,此漏洞存在以下几个局限点

1) 此漏洞只能确定前6个字符，如果后面的字符太长、包含特殊字符，很难猜解；
2) 如果文件名本身太短（无短文件名）也是无法猜解的；
3) 如果文件名前6位带空格，8.3格式的短文件名会补进，和真实文件名不匹配；
4) 如果文件夹名前6位字符带点“.”，扫描程序会认为是文件而不是文件夹，最终出现误报；
5) 不支持中文文件名，包括中文文件和中文文件夹。一个中文相当于两个英文字符，故超过4个中文字会产生短文件名，但是IIS不支持中文猜测。

- IIS短文件漏洞解决方案

1) CMD关闭NTFS 8.3文件格式的支持
2) 修改注册表禁用短文件名功能
3) 关闭Web服务扩展- ASP.NET
4) 升级netFramework至4.0以上版本

## IIS-PUT漏洞

- Put漏洞造成原因

IIS Server在Web服务扩展中开启了WebDAV，配置了可以写入的权限，造成任意文件上传。
