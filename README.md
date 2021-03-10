# sshtk: ssh toolkit

### Feature
- login
- tunel
- download
- upload
- support OTP


### Installation：

```bash
mamba install -c ohmeta sshtk

# or
pip install sshtk

# or
git clone https://github.com/ohmeta/sshtk
# run /path/to/sshtk/bin/sshtk.py
```

### Usage:

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
dl           sshtk download remote files using scp, support password and OTP
up           sshtk upload local files using scp, support password and OTP
```

##### config

```bash
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

```bash
# supply user, node, password
$ sshtk.py login --user <user> --node <node> --password <password>

# supply user, node, password, code with OTP support
$ sshtk.py login --user <user> --node <node> --password <password> --code <code> --otp

# use spefic config file with OTP support
$ sshtk.py login --user <user> --node <node> --config <config> --otp

# us default config file (recommanded)
sshtk.py login --user <user> --node <node> --otp
```

##### tunel

```bash
# supply user, node, password
$ sshtk.py tunel --user <user> --node <node> --password <password> \
                 <port1:node1:port2> <port3:node2:port4>

# supply user, node, password, code with OTP support
$ sshtk.py tunel --user <user> --node <node> --password <password> --code <code> --otp \
                 <port1:node1:port2> <port3:node2:port4>

# use spefic config file with OTP support
$ sshtk.py tunel --user <user> --node <node> --config <config> --otp \
                 <port1:node1:port2> <port3:node2:port4>

# us default config file (recommanded)
sshtk.py tunel --user <user> --node <node> --otp
```

##### dl

```bash
# supply user, node, password
$ sshtk.py dl --user <user> --node <node> --password <password> \
              --outdir ./ /absolute/remote/path/to/file1 /absolute/remote/path/to/file2

# supply user, node, password, code with OTP support
$ sshtk.py dl --user <user> --node <node> --password <password> --code <code> --otp \
              --outdir ./ /absolute/remote/path/to/file1 /absolute/remote/path/to/file2

# use spefic config file with OTP support
$ sshtk.py dl --user <user> --node <node> --config <config> --otp \
              --outdir ./ /absolute/remote/path/to/file1 /absolute/remote/path/to/file2

# use default config file (recommanded)
sshtk.py dl --user <user> --node <node> --otp \
            --outdir ./ /absolute/remote/path/to/file1 /absolute/remote/path/to/file2
```

##### up

```bash
# supply user, node, password
$ sshtk.py up  --user <user> --node <node> --password <password> \
               --outdir /absolute/remote/dir /local/path/to/file1 /local/path/to/file2

# supply user, node, password, code with OTP support
$ sshtk.py up --user <user> --node <node> --password <password> --code <code> --otp \
              --outdir /absolute/remote/dir /local/path/to/file1 /local/path/to/file2

# use spefic config file with OTP support
$ sshtk.py up --user <user> --node <node> --config <config> --otp \
              --outdir /absolute/remote/dir /local/path/to/file1 /local/path/to/file2

# use default config file (recommanded)
sshtk.py up --user <user> --node <node> --otp \
            --outdir /absolute/remote/dir /local/path/to/file1 /local/path/to/file2
```