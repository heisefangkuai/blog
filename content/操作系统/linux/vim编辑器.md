# vim编辑器

## 命令模式(底线)

保存命令操作

```linux
:q      # 退出
:w      # 保存
:q!     # 强制退出
:e!     # 放弃修改，打开原来的文件
:wq     # 保存并退出
```

撤回于重置

```linux
u           # 撤销前次操作
ctrl+r      # 重复前次操作
:e!         # 文档还原原始状态
```

移动屏幕

```linux
ctrl+u          # 向上滚动半屏
ctrl+d          # 向下滚动半屏
Pgup|ctrl+b     # 向上滚动一屏
PgDn|ctrl+f     # 向下滚动一屏
```

查找命令

```linux
/text       # 查找text, 按n查找下一个，按N查找前一个
?text       # 查找text, 反向查找，按n查找下一个，按N查找前一个
:set ignorecase/noignorecase    # 忽略/不忽略大小写的查找
:set hlsearch/nohlsearch        # 高亮搜索结果/关闭高亮，所有结果都高亮显示，而不是只显示一个匹配
```

其他命令

```linux
:set number/nu      # 显示行号
:set nonu           # 取消行号
ctrl +g             # 当前行信息
shift+g             # 移动的最后一行
:r filename         # 把filename文件的内容插入到当前光标所在位置下
```

选择、复制、粘贴、删除(剪切)命令

```linux
shift+v             # 选择一行
v|V|ctrl+v          # 进入选择模式

y           # 复制当前选中的内容
yy          # 复制当前行
y$          # 复制当前光标至行尾处

p           # 粘贴到光标之后
P           # 粘贴到光标之前

d           # 删除选中的内容
shift+d     # 删除光标后面的内容
dd          # 删除行
d$          # 删除光标到行尾
d^          # 删除至行首
:n,m d      # 将第n行到m行的内容删除
```

替换命令

```linux
:s/regexp/replacement   # 替换当前行第一个匹配
:S/regexp/replacement   # 替换当前行所有匹配
:n,\$s/regexp/replacement/  # 替换n行到最后一行中第一个匹配
:n,$S/regexp/replacement/g  # 替换第n行到最后的每个匹配
```

## 插入模式

进入插入模式

```linux
i       # 在光标所在字符前开始输入文字并进入插入模式
a       # 在光标所在字符后开始输入文字并进入插入模式
```
