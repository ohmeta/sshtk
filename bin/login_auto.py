#!/usr/bin/env python

__author__ = "zhun shi"
__version__ = "0.0.2"
__maintainer__ = "zhun shi"
__email__ = "shizhun@genomics.cn"
__status__ = "Developing"


import pyotp
import subprocess
import sys
import os
import argparse

def ArgsParser():
    parser = argparse.ArgumentParser(description="Copy files between local and cluster without OTP\n")
    parser.add_argument('--USER',"-u", type=str,help='User name \n')
    parser.add_argument('--NODE',"-n", type=str,default= "10.225.3.7", help='Cluster Node\n')
    parser.add_argument('--PASSWORD',"-p", type=str, help='Password in cluster\n')
    parser.add_argument('--ID',"-i", type=str, help='Identity code\n')

    args = parser.parse_args()
    return args

def main():
    args = ArgsParser()
    ID_code = args.ID
    PASSWORD = args.PASSWORD
    USER = args.USER
    NODE = args.NODE

    # OTP
    totp = pyotp.TOTP(ID_code)
    Verfied_code = totp.now()

    print(f"Now verified code is: {Verfied_code}")

    cmd_path = os.path.split(os.path.realpath(__file__))[0]
    cmd = f"expect {cmd_path}/auto.expect {PASSWORD} {Verfied_code} {USER} {NODE}"

    subprocess.call(cmd,shell=True)


if __name__ == "__main__":
    main()