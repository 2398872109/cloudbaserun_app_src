# sockd+ssr

## 项目内容

将 sockd1.4.2 及 shadowsocksr3.2.2 合并打包为容器镜像，且支持通过环境变量设置启动相关配置。

主要修改点：
见sockd目录说明、ssr目录说明

## 设置项：

环境变量：

sockd相关：

* SOCKD_PORT：默认 2020
* SOCKD_USERNAME：默认 root
* SOCKD_PASSWORD：默认 123456

ssr相关：

* SERVER_PORT：默认 9000
* PASSWORD：默认 password
* METHOD：默认 aes-256-cfb
* PROTOCOL：默认 origin
* OBFS：默认 plain
* PROTOCOL_PARAM：默认为空
* OBFS_PARAM：默认为空
