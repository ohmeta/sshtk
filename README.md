## 自动验证双因素，并登录集群  
  
### 介绍：  
您登录集群时，是否在为双因素验证而苦恼？ 


### 使用说明：
  
#### 1. 测试终端 `cygwin`  
#### 2. 依赖包：  

- python 3  
- pip  
- pyotp  
- expect  
  
### 使用步骤：
  
#### 1. 安装以上依赖库。  
#### 2. 将master分支下的两个文件放到`cygwin`可访问路径下，如home下。
#### 3. 编辑器打开`login_auto.py`,并配置以下信息：  
- ID_code = ""  
- PASSWORD = ""  
- NODE = "10.225.3.7"  
- USER = "user.name"  

说明：  
**ID_code** :此信息来源于邮箱里的个人二维码中的信息,可使用手机浏览器扫描二维码，获取其中的identity信息。  
**PASSWORD** : 登录集群的密码。  
**USER** ： 集群用户名。  
**NODE** : 集群节点。  

#### 4.运行  
{python login_auto.py}  
