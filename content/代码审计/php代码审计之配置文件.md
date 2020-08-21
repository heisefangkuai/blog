# php代码审计之配置文件

配置文件（php.ini）在 PHP 启动时被读取。对于服务器模块版本的 PHP，仅在 web 服务器启动时读取一次。

代码在不同环境下执行的结果也会大有不同，可能就因为一个配置问题，导致一个非常高危的漏洞能够利用;也可能你已经找到的一个漏洞就因为你的配置问题，导致你鼓捣很久都无法构造成功的漏洞利用代码。然而，在不同的PHP版本中配置指令也有不一样的地方，新的版本可能会增加或者删除部分指令，改变指令默认设置或者固定设置指令，因此我们在代码审计之前必须要非常熟悉PHP各个版本中配置文件的核心指令，才能更高效地挖掘到高质量的漏洞。

## php配置的语法

指令是使用以下语法指定的:指令名是*区分大小写的*
directive(指令) = value(值)
foo=bar 不等于 FOO=bar

INI 文件的表达式被限制于位运算符和括号。
|、&、~、!

空字符串可以简单地通过在等号后面不写任何东西来表示或使用None关键字:
foo =         ; 将foo设置为空字符串
foo = none    ; 将foo设置为空字符串
foo = "none"  ; 将foo设置为字符串" none "

可以使用值1、on、True或Yes来打开它们。
可以使用值0、off、False或No来关闭它们。

## php的配置参数

- register_globals(全局变量注册开关)

该选项在设置为on的情况下，会直接把用户GET、POST等方式提交上来的参数注册成全局变量并初始化值为参数对应的值，使得提交参数可以直接在脚本中使用。register_ globals 在PHP版本小于等于4.2.3时设置为PHP_INI_ALL,从PHP 5.3.0起被废弃，不推荐使用，在PHP 5.4.0中移除了该选项。

当register_globals设置为on且PHP版本低于5.4.0时，如下代码输出结果为true。

```php
<?php
if($user == 'admin'){
    echo 'true';
}
?>
访问：
http://localhost/index.php?user=admin
```

- allow_url_include(是否允许包含远程文件)
- allow_url_fopen(是否允许打开远程文件)

在该配置为on的情况下，它可以直接包含远程文件，当存在include($var)且$var可控的情况下，可以直接控制$var变量来执行PHP代码。allow_url_include在PHP 5.2.0后默认设置为off,配置范围是PHP_INI_ALL。与之类似的配置有allow_url_fopen， 配置是否允许打开远程文件。

配置allow_url_include为on，可以直接包含远程文件。

```php
<?php
include $_GET['a'];
?>
访问：
http://localhost/index.php?a=http://fake-blog.com/index.php
```

- magic_quotes_gpc(魔术引号自动过滤)

magic_quotes_gpc 在安全方面做了很大的贡献，只要它被开启，在不存在编码或者其他特殊绕过的情况下，可以使得很多漏洞无法被利用，它也是让渗透测试人员很头疼的一个东西。当该选项设置为on时，会自动在GET、POST、COOKIE变量中的单引号(')、 双引号(")、 反斜杠(\)及空字符(NULL)的前面加上反斜杠(\)， 但是在PHP 5中magic_quotes_gpc 并不会过滤$_SERVER变量，导致很多类似client-ip、referer一类的漏洞能够利用。在PHP 5.3之后的不推荐使用magic_quotes_gpc , PHP 5.4之后干脆被取消，所以你下载PHP 5.4之后的版本并打开配置文件会发现找不到这个配置选项。在PHP版本小于4.2.3时，配置范围是PHP_INI_ALL;在PHP版本大于4.2.3时，是PHP_INI_PERDIR。

```php
<?php
echo $_GET['a'];
?>
访问：
http://localhost/index.php?a=aa'"\
```

- magic_quotes_runtime(魔术引号自动过滤)

magic_quotes_runtime也是自动在单引号(')双引号(")、反斜杠(\)及空字符(NULL)的前面加上反斜杠(\)。它跟magic_quotes_gpc的区别是，处理的对象不一样，magic_quotes_runtime只对从数据库或者文件中获取的数据进行过滤，它的作用也非常大，因为很多程序员只对外部输人的数据进行过滤，却没有想过从数据库获取的数据同样也会有特殊字符存在，所以攻击者的做法是先将攻击代码写人数据库，在程序读取、使用到被污染的数据后即可触发攻击。同样, magic_quotes_runtime在PHP 5.4之后也被取消，配置范围是PHP_INI_ALL。

有一个点要记住，只有部分函数受它影响，所以在某些情况下这个配置是可以绕过的，受影响的函数包括：
get_meta_tags()、file_get_contents()、file()、fgets()、fwrite()、fread()、fputcsv()、stream_socket_recvfrom()、exec()、system()、passthru()、stream_get_contents()、bzread()、gzfile()、gzgets()、gzwrite()、gzread()、exif_read_data()、dba_insert()、dba_replace()、dba_fetch()、ibase_fetch_row()、ibase_fetch_assoc()、ibase_fetch_object()、mssql_fetch_row()、mssql_fetch_object()、mssql_fetch_array()、mssql_fetch_assoc()、mysqli_fetch_row()、mysqli_fetch_array()、mysqli_fetch_assoc()、mysqli_fetch_object()、pg_fetch_row()、pg_fetch_assoc()、pg_fetch_array()、pg_fetch_object()、pg_fetch_all()、pg_select()、sybase_fetch_object()、sybase_fetch_array()、sybase_fetch_assoc()、SplFileObject::fgets()、SplFileObject::fgetcsv()、SplFileObject::fwrite()

```php
# 1.txt文件
1'2"3\4'

# index.php文件
<?php
ini_get('magic_quotes_runtime','1');
echo file_get_contents('1.txt');
?>
```

- magic_quotes_sybase(魔术引号自动过滤)

magic_quotes_sybase指令用于自动过滤特殊字符，当设置为on时，它会覆盖掉magic_quotes_gpc=on的配置，也就是说，即使配置了gpc=on也是没有效果的。这个指令与gpc的共同点是处理的对象一致，即都对GET、POST、Cookie进行处理。而它们之前的区别在于处理方式不一样，magic_quotes_sybase仅仅是转义了空字符和把单引号(')变成了双引号(")。与gpc相比，这个指令使用得更少，它的配置范围是PHP_INI_ALL,在PHP5.4.0中移除了该选项。

```php
<?php
echo $_GET['a'];
?>
访问：
http://localhost/index.php?a=aa'
```

- safe_mode(安全模式)

安全模式是PHP内嵌的一种安全机制，当safe_mode=On时，联动可以配置的指令有：
safe_mode_include_dir、safe_mode_exec_dir、safe_mode_allowed_env_vars、safe_mode_protected_env_vars。safe_mode指令的配置范围为PHP_INI_SYSTEM，PHP5.4之后被取消。

这个配置会出现下面限制:

1. 所有文件操作函数(例如unlink()、file()和include())等都会受到限制。例如，文件a.php和文件c.txt的文件所有者是用户a,文件b.txt的所有者是用户b并且与文件a.php不在属于同一个用户的文件夹中，当启用了安全模式时，使用a用户执行a.php,删除文件c.txt可成功删除，但是删除文件b.php会失败。对文件操作的include等函数也一样，如果有一些脚本文件放在非Web服务启动用户所有的目录下，需要利用include等函数来加载一些类或函数，可以使用safe_mode_include_dir指令来配置可以包含的路径。
2. 通过雨数popen()、system()以及exec()等函数执行命令或程序会提示错误。如果我们需要使用一些外部脚本，可以把它们集中放在一个目录下，然后使用safe_mode_exec_dir指令指向脚本的目录。

下面是启用safe_mode指令时受影响的函数、变量及配置指令的完整列表:
apache_request_headers()、ackticks()、hdir()、hgrp()、chmode()、chown()、copy()、dbase_open()、dbmopen()、dl()、exec()、filepro()、filepro_retrieve()、ilepro_rowcount()、fopen()、header()、highlight_file()、ifx_*、ingres_*、link()、mail()、max_execution_time()、mkdir()move_uploaded_file()、mysql_*、parse_ini_file()、passthru()、pg_lo_import()、popen()、posix_mkfifo()、putenv()、rename()、zmdir()、set_time_limit()、shell_exec()、show_source()、symlink()、system()、touch()。

安全模式下执行命令失败的提示：

```php
<?php
echo `whoami`;
```

- safe_mode_allowed_env_vars(限制环境变量存取)

指定 PHP 程序可以改变的环境变量的前缀,当这个选项的值为空时，那么 php 可以改变任何环境变量。如:safe_mode_allowed_env_vars = PHP_ , 当这个选项的值为空时，那么 php可以改变任何环境变量

- com.allow_dcom(com组件)

PHP设置在安全模式下(safe_mode)，仍旧允许攻击者使用COM()函数来创建系统组件来执行任意命令，我推荐关闭这个函数来防止出现此漏洞使用COM()函数需要在PHP.ini中配置extension=php_com_dotnet.dll，如果PHP<5.4.5 则不需要

- open_basedir(PHP可访问目录)

open_basedir指令用来限制PHP只能访问哪些目录，通常我们只需要设置Web文件目录即可，如果需要加载外部脚本，也需要把脚本所在目录路径加人到open__basedir指令中，多个目录以分号(;)分割。使用open_basedir需要注意的一点是，指定的限制实际上是前缀，而不是目录名。例如，如果配置open_basedir =/www/a那么目录
/www/a和/www/ab都是可以访问的。所以如果要将访问仅限制在指定的目录内，请用斜线结束路径名。例如设置成: open_basedir =/www/a/。

当open_basedir配置目录后，执行脚本访问其他文件都需要验证文件路径，因此在执行效率，上面也会有一定的影响。该指令的配置范围在PHP版本小于5.2.3时是PHP_INI_SYSTEM，在PHP版本大于等于5.2.3是PHP_INI_ALL。

- disable_functions(禁用函数)

在正式的生产环境中，为了更安全地运行PHP，也可以使用disable_functions 指令来禁止一些敏感函数的使用。当你想用本指令禁止一些危险函数时，切记要把dl()函数也加到禁止列表，因为攻击者可以利用dI()函数来加载自定义的PHP扩展以突破disable_functions 指令的限制。

本指令配置范围为php.ini only。配置禁用函数时使用逗号分割函数名，例如:
disable_functions=phpinfo,eval,passthru,exec,system。

- display_errors和error_reporting(错误提示)

display_errors表明是否显示PHP脚本内部错误的选项，在调试PHP的时候，通常都把PHP错误显示打开，但是在生产环境中，建议关闭PHP错误回显，即设置display_errors=off，以避免带来一些安全隐患。在设置display_errors=on时，还可以配置的一个指令是error_reporting,这个选项用来配置错误显示的级别，可使用数字也可使用内置常量配置。

这两个指令的配置范围都是PHP_INI_ALL。

- 常用指令及说明

|       指令   |可配置范围|说明|
|:------------:|:--------:|:--:|
|safe_mode_gid|PHP_INI_SYSTEM|以安全模式打开文件时默认使用UID来比对;设置本指令为on时使用GID做宽松的比对|
|expose_php|php.ini only|是否在服务器返回信息HTTP头显示PHP版本|
|max_execution_time|PHP_INI_ALL|每个脚本最多执行秒数|
|memory_limit|PHP_INI_ALL|每个脚本能够使用的最大内存数量|
|log_errors|PHP_INI_ALL|将错误输人到日志文件|
|log_errors_max_len|PHP_INI_ALL|设定log_errors的最大长度|
|variables_order|PHP_INI_PERDIR|此指令描述了PHP注册GET、POST、Cookie环境和内置变量的顺序，注册使用从左往右的顺序,新的值会覆盖旧的值|
|post_max_size|PHP_INI_PERDIR |PHP可以接受的最大的POST数据大小|
|auto_prepend_file|PHP_INI_PERDIR|在任何PHP文档之前自动包含的文件|
|auto_append_file|PHP_INI_PERDIR|在任何PHP文档之后自动包含的文件|
|extension_dir|PHP_INI_SYSTEM|可加载的扩展(模块)的目录位置|
|file_uploads|PHP_INI_SYSTEM|是否允许HTTP文件上传|
|upload_tmp_dir|PHP_INI_SYSTEM|对于HTTP上传文件的临时文件目录|
|upload_max_filesize|PHP_INI_SYSTEM|允许上传的最大文件大小|
|safe_mode_exec_dir|不知道|外部程序执行目录|

