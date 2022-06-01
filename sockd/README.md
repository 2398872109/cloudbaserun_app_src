# sockd

## 项目内容

将sockd1.4.2版本打包为容器镜像，且支持通过环境变量设置启动相关配置。

主要修改点：
1、默认sockd.passwd文件为初始用户名密码，root：12345678
2、通过script/start 脚本启动；
3、通过 envset 读取环境变量，修改端口及用户名密码
4、使用 pam 脚本设置用户密码
5、使用 sed 命令行修改配置文件中的端口设置


## 设置项：

环境变量：

* PORT：默认 2020，可修改；
* USERNAME：默认 root，可修改，需要与 PASSWORD 同时设置才生效；
* PASSWORD：默认 123456，可修改，需要与 USERNAME 同时设置才生效；
