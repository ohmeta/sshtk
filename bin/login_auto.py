#!/usr/bin/env python

__author__ = "zhun shi"
__version__ = "0.0.1"
__maintainer__ = "zhun shi"
__email__ = "shizhun@genomics.cn"
__status__ = "Developing"


import pyotp
import subprocess
import sys
import os


# configure
ID_code = ""
PASSWORD = ""
NODE = "10.225.3.7"
USER = "user.name"

# OTP
totp = pyotp.TOTP(ID_code)
Verfied_code = totp.now()

print(f"Now verified code is: {Verfied_code}")

cmd_path = os.path.split(os.path.realpath(__file__))[0]
cmd = f"expect {cmd_path}/auto.expect {PASSWORD} {Verfied_code} {USER} {NODE}"

subprocess.call(cmd,shell=True)
