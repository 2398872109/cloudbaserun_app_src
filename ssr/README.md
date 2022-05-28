# ssr

## 项目内容

将 shadowsocksr 最近版本打包为容器镜像，且支持通过环境变量设置启动相关配置。

主要修改点：
1、gz包文件为 shadowsocksr 最新版本，来源 hhttps://github.com/shadowsocksrr/shadowsocksr/archive/3.2.2.tar.gz
2、使用script/config.py 启动，进行配置文件读取、环境变量读取、配置更新、写配置文件操作


## 设置项：

环境变量：

* SERVER_PORT：默认 9000
* PASSWORD：默认 password
* METHOD：默认 aes-256-cfb
* PROTOCOL：默认 origin
* OBFS：默认 plain
* PROTOCOL_PARAM：默认为空
* OBFS_PARAM：默认为空
