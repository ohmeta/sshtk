## 自动验证双因素，并登录集群  
  
### 介绍：  
您登录集群时，是否在为双因素验证而苦恼？ 


### 使用说明：
  
#### 1. 测试终端 `cygwin`  
#### 2. 依赖包：  

- python3  
- pip3  
- pyotp (pip3 install pyotp)  
- configparser (pip3 install configparser)
- expect  (Linux脚本语言，需要重新安装`cygwin`，选中expect进行安装)
  
### 使用步骤：
  
#### 1. 安装以上依赖库。  
#### 2. 将master分支下`bin`的文件放到`cygwin`可访问路径下，如home下。
#### 3. Usage:  

```
# command line model
$ python login_auto.py -i ID_CODE -u user.name -n 10.225.3.7 -p password  

# with configure file
# 首次登录时：
$ python login_auto.py -i ID_CODE -u user.name -n 10.225.3.7 -p password -c configure.txt

# 再次登录时：
$ python login_auto.py -u user.name -n 10.225.3.7 -c configure.txt

```  

```
$ python login_auto.py -h

usage: login_auto.py [-h] --USER USER [--NODE NODE]
                     [--PASSWORD PASSWORD] [--ID ID] [--Config CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  --USER USER, -u USER  User name
  --NODE NODE, -n NODE  Cluster Node
  --PASSWORD PASSWORD, -p PASSWORD
                        Password in cluster
  --ID ID, -i ID        Identity code
  --Config CONFIG, -c CONFIG
                        Configure files
```

说明：  
**ID_code** :此信息来源于邮箱里的个人二维码中的信息,可使用手机浏览器扫描二维码，获取其中的identity信息。  
**PASSWORD** : 登录集群的密码。  
**USER** ： 集群用户名。  
**NODE** : 集群节点 (default : 10.225.3.7)。
**Config** : 配置文件，可随意命名，首次使用时无需存在次文件。
  

#### 4.一键登录  
  
将上述命令行加入~/.bashrc中，实现一键登录。   

  
**注意**：  
- 千万不要外传，万一被集群管理员封了就......  
