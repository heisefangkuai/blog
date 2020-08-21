# 代码审计

php危险函数

```cmd
$_SERVER["PHP_SELF"]
$_SERVER["PHP_SELF"] 变量能够被黑客利用！
<form method="post" action="<?php echo $_SERVER["PHP_SELF"];?>">
http://locahost.com/index.php/%22%3E%3Cscript%3Ealert('hacked')%3C/script%3E
防御
通过使用 htmlspecialchars() 函数能够避免 $_SERVER["PHP_SELF"] 被利用。
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
str_ireplace("1", "2", "123")

将第三个参数中的`1`替换成`2`,存在利用的可能
```
