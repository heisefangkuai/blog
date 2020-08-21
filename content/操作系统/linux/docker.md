# Docker 的使用

## docker 介绍

Docker 是一个开源的应用容器引擎，基于 Go 语言 并遵从Apache2.0协议开源。

Docker 可以让开发者打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。

容器是完全使用沙箱机制，相互之间不会有任何接口（类似 iPhone 的 app）,更重要的是容器性能开销极低。

Docker 从 17.03 版本之后分为 CE（Community Edition: 社区版） 和 EE（Enterprise Edition: 企业版），我们用社区版就可以了。

- 虚拟机：如 VMware ， VisualBox 之类的
- 容器：是 Linux 另一种虚拟化技术，Linux 容器不是模拟一个完整的操作系统，而是对进程进行隔离，相当于是在正常进程的外面套了一个保护层。对于容器里面的进程来说，它接触到的各种资源都是虚拟的，从而实现与底层系统的隔离。

## 安装docker

一、安装所需的包：

```yum
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

二、设置稳定存储库。

```yum
sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
```

三、安装最新版本的Docker CE和containerd

```yum
sudo yum install -y docker-ce docker-ce-cli containerd.io
```

四、启动Docker。

```yum
sudo systemctl start docker
```

五、通过运行hello-world 映像验证是否正确安装了Docker CE 。

```yum
sudo docker run hello-world
```

如果出现错误提示，尝试更换国内的docker镜像试试：

```yum
设置国内阿里云的镜像加速器
创建文件/etc/docker/daemon.json 添加如下内容如下

vi /etc/docker/daemon.json
{
    "registry-mirrors": ["https://alzgoonw.mirror.aliyuncs.com"] 
}

修改完要重启docker
```

[更多详情请到官网](https://docs.docker.com/install/linux/docker-ce/centos/)

## 卸载Docker CE

一、卸载Docker包

```yum
sudo yum remove docker-ce

或者：

sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```

二、主机上的图像，容器，卷或自定义配置文件不会自动删除。要删除所有图像，容器和卷

```yum
sudo rm -rf /var/lib/docker
```

## 系统命令操作docker的常用命令

```docker

systemctl start docker      # 启动
systemctl restart docker    # 重启
systemctl stop docker       # 关闭

systemctl enable docker     # 设置开机自启
systemctl disable docker    # 设置开机自启

systemctl reload  docker    # 重新加载docker的配置文件
systemctl status  docker    # 查看docker 进程状态
```

## docker的常用命令

常用

```docker

docker [命令] --help        # 查看docker的命令/子命令帮助
docker version              # 查看docker 的版本
docker info                 # 查看docker 的信息

```

镜像：docker image

```docker
docker image ls [子命令]                    # 列出本地的镜像
docker image history 镜像                   # 查看镜像的历史分层
docker image inspect 镜像                   # 查看镜像的详情
docker image pull 镜像:版本                 # 下载一个镜像
docker image rm 镜像                        # 删除一个镜像
docker image tag 镜像:版本 名:tag           # 给镜像打一个tag标签
docker image save 镜像 > 保存名称.tar       # 保存一个镜像
docker image load < 保存名称.tar            # 导入保存的镜像

配合使用：
docker image import 保存名称.tar 名:tag     # 导入容器文件系统
docker container export 容器id >保存名称.tar # 导出容器文件系统
```

容器：docker container

```docker
docker container run -itd --name 容器名 镜像        # 创建一个容器
    --name 设置容器名
    -i      交互式
    -t      分配一个伪终端
    -d      后台运行容器
    -p      发布容器端口到主机。用法：-p 映射的主机端口:容器端口

docker container start 容器名                       # 运行一个容器
docker container stop 容器名                        # 关闭一个容器
docker container restart 容器名                     # 重启一个容器
docker container rm 容器名                          # 删除一个容器

docker container exec -it 容器名 /bin/sh            # 进入一个容器终端，exit退出时容器不会关闭
docker container attach 容器名                      # 进入一个容器终端，exit退出时容器关闭

docker container ls                                 # 查看容器 -a 是查看所有容器
docker container inspect 容器名                     # 查看容器的信息
docker container top 容器名                         # 查看容器的进程
docker container cp 本地文件 容器名:目录             # 将本地文件cp到容器中
docker container logs 容器名                        # 查看容器的日志
docker container port 容器名                        # 查看容器的端口
docker container stats 容器名                       # 查看容器的资源

还有commit和update
```

## 用docker搭建sql-lab

```docker
docker pull acgpiano/sqli-labs

docker run -dt --name sqli-lab -p [你要映射的端口]:80 acgpiano/sqli-labs:latest

然后在sql-lab上直接初始化数据库就好了。
```

## 其他笔记

- 将docker主机数据挂载到容器上

Docker提供三种不同的方式将数据从宿主机挂载到容器中: volumes, bind mounts和tmpfs.

1. volumes: Docker管理宿 主机文件系统的一部分 (/var/lib/docker/volumes)。
2. bind mounts:可以存储在宿主机系统的任意位置。
3. tmpfs:挂载存储在宿主机系统的内存中，而不会写入宿主机的文件系统。

- 上传到阿里云镜像

docker login --username=975686955@qq.com registry.cn-beijing.aliyuncs.com
sudo docker tag [ImageId] registry.cn-beijing.aliyuncs.com/fake/ceshi:[镜像版本号]
docker push registry.cn-beijing.aliyuncs.com/fake/ceshi:[镜像版本号]


