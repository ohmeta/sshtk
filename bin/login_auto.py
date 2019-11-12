#!/usr/bin/env python3

__author__ = "zhun shi"
__version__ = "0.0.3"
__maintainer__ = "zhun shi"
__email__ = "shizhun@genomics.cn"
__status__ = "Developing"


import pyotp
import subprocess
import sys
import os
import argparse
import configparser

def ArgsParser():
    parser = argparse.ArgumentParser(description="Copy files between local and cluster without OTP\n")
    parser.add_argument('--USER',"-u", type=str,required=True,help='User name \n')
    parser.add_argument('--NODE',"-n", type=str,default= "10.225.3.7", help='Cluster Node\n')
    parser.add_argument('--PASSWORD',"-p", type=str, help='Password in cluster\n')
    parser.add_argument('--ID',"-i", type=str, help='Identity code\n')
    parser.add_argument("--Config","-c",type=str,help="Configure files\n")

    args = parser.parse_args()
    return args

def ConfigureParser(args):
    if args.Config is not None:
        if not os.path.exists(args.Config):
            open(args.Config,'w').close()
        cf = configparser.ConfigParser()
        cf.read(args.Config)
        secs = cf.sections()

        if args.USER in secs:
            ID_code = cf.get(args.USER,ID_code)
            PASSWORD = cf.get(args.USER,PASSWORD)
        elif args.ID is not None and args.PASSWORD is not None:
            cf.add_section(args.USER)
            cf.set(args.USER,"ID_code",args.ID)
            cf.set(args.USER,"PASSWORD",args.PASSWORD)
            cf.write(open(args.Config,'w'))
        else:
            print("Need PAASWORD or ID code")
            sys.exit(1)
    if args.PASSWORD is not None:
        PASSWORD = args.PASSWORD
    if args.ID is not None:
        ID_code = args.ID
    return ID_code,PASSWORD

def main():
    args = ArgsParser()
    USER = args.USER
    NODE = args.NODE
    ID_code, PASSWORD = ConfigureParser(args)

    # OTP
    totp = pyotp.TOTP(ID_code)
    Verfied_code = totp.now()

    #print(f"Now verified code is: {Verfied_code}")

    cmd_path = os.path.split(os.path.realpath(__file__))[0]
    cmd = f"expect {cmd_path}/auto.expect {PASSWORD} {Verfied_code} {USER} {NODE}"

    subprocess.call(cmd,shell=True)


if __name__ == "__main__":
    main()
