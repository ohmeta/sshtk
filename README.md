# sshtk

## 介绍：

您登录集群时，是否在为双因素验证而苦恼？

## 版本说明：v2

- 弃用 expect，采用 pexpect，简化脚本
- 解决终端窗口显示宽度异常的问题。

## 使用说明：

### 安装：

#### 解决依赖

```
conda create -n sshtk python=3.7 mamba
conda install -n sshtk pyotp
```

#### Usage:

```
usage: sshtk [-h] [-v]  ...

ssh toolkit

optional arguments:
-h, --help     show this help message and exit
-v, --version  print software version and exit

available subcommands:

config       sshtk generate config file, default on: ~/.sshtkrc
login        sshtk login specific node, support password and OTP
tunel        sshtk tunel specific node, support password and OTP

```

##### config

```
# config without OTP support
$ sshtk.py config --user <user> --node <node> --password <password>

$ cat ~/.sshtkrc
[<user>@<node>]
password = <password>
code =
tunel =

# config with OTP support
$ sshtk.py config --user <user> --node <node> --password <password> --code <code>

$ cat ~/.sshtkrc
[<user>@<node>]
password = <password>
code = <code>
tunel =

# config with OTP support, and add tunel, tunel can have multi instance
$ sshtk.py config --user <user> --node <node> --password <password> --code <code> \
                  --tunel <port1:node1:port2> <port3:node2:port4>

$ cat ~/.sshtkrc
[<user>@<node>]
password = <password>
code = <code>
tunel = <port1:node1:port2>,<port3:node2:port4>
```

##### login

```
# supply user, node, password
$ sshtk.py login --user <user> --node <node> --password <password>

# supply user, node, password, code with OTP support
$ sshtk.py login --user <user> --node <node> --password <password> --code <code>

# use spefic config file
$ sshtk.py login --user <user> --node <node> --config <config>

# us default config file (recommanded)
sshtk.py login --user <user> --node <node>
```

##### tunel

```
# supply user, node, password
$ sshtk.py tunel --user <user> --node <node> --password <password> \
                 --tunel <port1:node1:port2> <port3:node2:port4>

# supply user, node, password, code with OTP support
$ sshtk.py tunel --user <user> --node <node> --password <password> --code <code> \
                 --tunel <port1:node1:port2> <port3:node2:port4>

# use spefic config file
$ sshtk.py tunel --user <user> --node <node> --config <config> \
                 --tunel <port1:node1:port2> <port3:node2:port4>

# us default config file (recommanded)
sshtk.py tunel --user <user> --node <node>
```

##### 备注：

**user** ： 集群用户名  
**node** : 集群节点 (default : `10.225.3.7`)  
**password** : 登录集群的密码  
**code** :此信息来源于邮箱里的个人二维码中的信息,可使用手机浏览器扫描二维码，获取其中的 identity 信息  
**config** : 配置文件，可随意命名，默认是 `~/.sshtkrc`

##### 一键登录

将上述命令行加入~/.bashrc 中，实现一键登录。

**注意**：

- 千万不要外传，万一被集群管理员封了就......
