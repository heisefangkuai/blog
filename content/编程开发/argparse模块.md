# argparse - 用于命令行选项，参数和子命令的解析器

从版本3.2开始optparse不推荐使用：不推荐使用该模块，将不再进行开发。该argparse模块将继续开发。

## 实例化argparse对象

案例：

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)
```

## argparse三个主要函数

1. parser = argparse.ArgumentParser()   # 第一步是创建ArgumentParser对象
2. parser.add_argument()        # 调用add_argument()向对象添加命令行参数信息，这些信息告诉对象如何处理命令行参数。
3. args = parser.parse_args()   # 通过调用parse_args()来解析对象中保存的命令行参数：将命令行参数解析成相应的数据类型并采取相应的动作，它返回一个Namespace对象。parse_args()一般并不使用参数。

## ArgumentParser参数

```python
parser.ArgumentParser(
    prog=None,          # 帮助信息中的程序名
    usage=None,         # 描述信息,会替换掉prog参数
    description=None,   # help信息前显示的信息
    epilog=None,        # help信息之后显示的信息
    parents=[],     
    formatter_class='', # help信息输出的格式，为了美观…（不修改）
    prefix_chars='-',   # 参数前缀，默认为'-'(不修改)
    fromfile_prefix_chars=None, # 文件前缀字符(不修改)
    argument_default=None,      # 参数的默认值
    conflict_handler='error',   # 冲突处理(不修改)
    add_help=True,      # 是否禁用-h –help选项
    allow_abbrev=True)  # 是否使用参数缩写

# parents：有时多个解析器可能有相同的参数集，为了实现代码复用，我们可以将这些相同的参数集提取到一个单独的解析器中，在创建其它解析器时通过parents指定父解析器，这样新创建的解析器中就包含了相同的参数集。
```



## add_argument()方法

```python
parser.add_argument(
    name or flags...# 指定一个可选参数或必选参数，可选参数默认以-开始，其它的为必选参数。
    [,action]
    [,nargs]
    [,const]    # 参数的常量值，通常与append_const和store_const相关。
    [,default]  # 参数的默认值。
    [,type]     # 参数的数据类型。可以是任意Python支持的数据类型。
    [,choices]  # 参数的取值范围
    [,required] # 参数是否可以忽略不写,仅对可选参数有效
    [,help]     # 参数的说明信息
    [,metavar]  # 用法消息中参数的帮助信息。
    [,dest])    # 允许自定义ArgumentParser的参数属性名称,对象的属性名

```

- action：参数的处理方法，预置的操作有以下几种:
    1. action='store' 仅仅保存参数值，为action默认值
    2. action='store_const' 与store基本一致，但store_const只保存const关键字指定的值
    3. action='store_true'或'store_false' 与store_const一致，只保存True和False,当指定这个选项的时候为True或False
    4. action='append' 将相同参数的不同值保存在一个list中
    5. action='count' 统计该参数出现的次数
    6. action='help' 输出程序的帮助信息
    7. action='version' 输出程序版本信息
    8. action='append_const' 存为列表，会根据const关键参数进行添加
- nargs：参数的数量:
   1. 值可以为整数N(N个)，*(任意多个，可以为0个)，+(一个或更多)，有点像正则表达式啊
   2. 值为?时，首先从命令行获得参数，如果有-y后面没加参数，则从const中取值，如果没有-y，则从default中取值


## add_argument_group对命令行参数进行概念性分组

```
foo_group = parser.add_argument_group(title='Foo options')
target = parser.add_argument_group("Target", "设置Target")
```

## 互斥参数

```
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
```

-q和-v不出现，或仅出现一个都可以，同时出现就会报错。

## parse_args()方法

parse_args()方法将命令行参数字符串转换为相应对象并赋值给Namespace对象的相应属性，默认返回一个Namespace对象。

## The Namespace object

调用parse_args()的返回值是一个Namespace对象，它具有很多属性，每个属性都代表相应的命令行参数。

Namespace对象是一个非常简单的类，可以通过vars()将之转换成字典类型。

还可以将ArgumentParser对象赋值给别的命令空间，而不是新建一个Namespace对象，例如：

```python
class C:
    pass

c = C()
parser = argparse.ArgumentParser()
parser.add_argument('--foo')
parser.parse_args(args=['--foo', 'BAR'], namespace=c)
c.foo
'BAR'
```
