## 命令执行函数

```php
eval($_GET["code"])
assert('phpinfo()');
preg_replace('/asd/e', $_POST['a'], 'asdfasdg');
create_function('', $_POST['cmd']);
call_user_func('assert', $_REQUEST['cmd']);
call_user_func_array('assert', $arr);
array_filter(array("a",phpinfo(),2,3,4));
file_put_contents('muma.php', '<?php eval($_REQUEST[cmd]);?>');
fputs(fopen('shell.php', 'w'), '<?php eval($_REQUEST[cmd])?>');
system('whoami');
passthru('whoami')
print(exec('whoami'));
print(shell_exec('whoami && dir'));
print(`whoami`);    ## 加了反引号的字符串将尝试作为外壳命令来执行，并将奇输出信息返回。
array_map(array(1,2,3,4,eval($_GET["code"])));
usort(array(1,3,2,5,phpinfo()));
uasort(array("a"=>4,"b"=>phpinfo()));
uksort(array("a"=>4,"b"=>phpinfo()));
array_reduce(array(phpinfo()));

$_GET['a']($_POST['b']);

```

php任意文件读取函数

```php
fopen()
file_get_contents()
fread
fgets
fgetss
file
fpassthru
parse_ini_file
readfile

allow_url_fopen选项激活了URL形式的fopen封装协议使得可以访问URL对象例如文件。默认的封装协议提供用ftp和http协议来访问远程文件，一些扩展库例如zlib可能会注册更多的封装协议
```

- serialize/unserialize   反序列化漏洞
__wakeup() //使用unserialize时触发
__sleep() //使用serialize时触发
__destruct() //对象被销毁时触发
__call() //在对象上下文中调用不可访问的方法时触发
__callStatic() //在静态上下文中调用不可访问的方法时触发
__get() //用于从不可访问的属性读取数据
__set() //用于将数据写入不可访问的属性
__isset() //在不可访问的属性上调用isset()或empty()触发
__unset() //在不可访问的属性上使用unset()时触发
__toString() //把类当作字符串使用时触发
__invoke() //当脚本尝试将对象调用为函数时触发

```php
<?php
header("Content-type: text/html; charset=utf-8");
class Pers
{
    public $name = '';
    public $age = '18';
    private $ages = 1;

    public function __construct(){
        echo '1-创建对象触发'."<br>";
    }
    public function __destruct(){
        echo '2-销毁对象触发'."<br>";
    }
    public function __toString(){
        return '3-对象当作字符串使用时触发'."<br>";
    }
    public function __wakeup(){
        echo '4-使用unserialize时触发'."<br>";
    }
    public function __sleep(){
        echo '5-使用serialize时触发'."<br>";
        return(array('name'));
    }
    public function __get($p){
        echo '6-获取类的私有属性，或者不存在的方法会触发'."<br>";
    }
    public function __set($n,$v){
        echo "7-设置不存在的类属性会触发"."<br>";
    }
    public function __isset($p){
        echo "8-判断属性不存在的时候触发"."<br>";
    }
    public function __unset($content) {
        echo "9-当在类外部使用unset()函数来删除私有成员时自动调用的<br>";
    }
    public function __invoke($content) {
        echo "10-把一个对象当成一个函数去执行<br>";
    }
}

$per = new Pers();
$per->name = 'laol';
$per->age = '20';
echo $per;
serialize($per);
unserialize('O:4:"Pers":2:{s:4:"name";s:4:"laol";s:3:"age";s:2:"20";}');
$per->p1;
isset($per->ages);
$per->n = 'aa';
unset($per->ages);
$per('111');
```

- in_array函数缺陷

PHP在使用 in_array() 函数判断时，会将 7shell.php 强制转换成数字7,修复方法将 in_array() 函数的第三个参数设置为 true ，或者使用 intval() 函数将变量强转成数字，又或者使用正则匹配来处理变量

```php
?id=1 and 1=1
if (!in_array($_GET['id'], array(1,2,3,4))) {
    die("id $id is not in whitelist.");
}
echo $_GET['id'];
```

- filter_var函数缺陷

filter_var() 函数通过指定的过滤器过滤一个变量。如果成功，则返回被过滤的数据。如果失败，则返回 FALSE。

