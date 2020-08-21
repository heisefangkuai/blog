# GIT 进阶

## 命令：

```git
1. git init                 # 初始化git
2. git status               # 查看git状态
3. git add .                # 添加文件到git
4. git commit -m "注释"     # 注释并管理本地的版本
5. git log                  # 查看git日志
6. git reset --hard "版本"  # 滚到某个版本
7. git reflog               # 显示所有的版本信息
8. git checkout .           # 还原修改没有管理的文件

```

```stash
将目前还不想提交的但是已经修改的内容进行保存至堆栈中，方便后续操作

git stash               # 暂存当前正在进行的工作
git stash save "备注"   # 暂存并备注当前正在进行的工作
git stash pop           # 还原暂存的工作
git stash list          # 暂存列表
git stash apply "编号"  # 取出到指定编号的
git stash clear         # 清除 stash 缓存
git stash drop "编号"   # 删除指定编号的缓存

```

```branch
分支

git branch              # 查看分支
git branch "分支名"     # 创建分支
git checkout "分支名"   # 切换分支
git branch -d "分支名"  # 删除某个分支

分支合并

git checkout master     # 会到主分支
git merge "分支名"      # 和并某个分支

```

```git
提交文件

git remote add origin "提交的地址"      # 添加提交地址，origin 为别名
git push origin master                  # 提交 master上分支的代码

提交其他分支的代码
git checkout aaa            # 切换到aaa分支
git push origin aaa         # 提交aaa分支的代码

```

```git

拉代码
git clone "代码的地址"      # 拉取一份代码（克隆）

拉取其他分支的代码，并保持原分支
git branch aaa              # 创建aaa分支
git checkout aaa            # 切换aaa分支
git pull origin aaa         # 拉取aaa分支上的代码

如果想拉取其他分支的代码在主分支上，直接拉取就好
git pull origin aaa         # 拉取aaa分支上的代码

```

git常用

```git
git clone https://github.com/typecho/typecho.git --branch v1.0-14.10.10-release

```
