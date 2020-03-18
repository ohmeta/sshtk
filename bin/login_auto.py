#!/usr/bin/env python3

__author__ = "zhun shi"
__version__ = "0.0.3"
__maintainer__ = "zhun shi"
__email__ = "shizhun@genomics.cn"
__status__ = "Developing"


import pyotp
import pexpect
import struct
import fcntl
import termios
import signal
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
            ID = cf.get(args.USER,"id_code")
            pwd = cf.get(args.USER,"password")
        elif args.ID is not None and args.PASSWORD is not None:
            cf.add_section(args.USER)
            cf.set(args.USER,"ID_code",args.ID)
            cf.set(args.USER,"PASSWORD",args.PASSWORD)
            cf.write(open(args.Config,'w'))
        else:
            print("Need PAASWORD or ID code")
            sys.exit(1)
    if args.PASSWORD is not None:
        pwd = args.PASSWORD
    if args.ID is not None:
        ID = args.ID
    return ID,pwd

def sigwinch_passthrough (sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(),
        termios.TIOCGWINSZ , s))
    if not child.closed:
        child.setwinsize(a[0],a[1])



args = ArgsParser()
USER = args.USER
NODE = args.NODE
ID_code, PASSWORD = ConfigureParser(args)


# OTP
totp = pyotp.TOTP(ID_code)
Verfied_code = totp.now()

# auto login using expect module
child = pexpect.spawn(f'ssh {USER}@{NODE}')
sigwinch_passthrough(1,2)

child.expect("Password:")
child.sendline(PASSWORD)
child.expect("Verification code:")
child.sendline(Verfied_code)
signal.signal(signal.SIGWINCH, sigwinch_passthrough)

child.interact()
sys.exit()

