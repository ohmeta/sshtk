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
import getpass
import argparse
import configparser


DEFAULT_CONFIG = os.path.join(os.path.expanduser("~"), ".sshtkrc")


def generate_config(args, unknown):
    """
    generate config
    if node on config, config will update
    """
    config = configparser.ConfigParser()

    if os.path.exists(args.config):
        print(f"{args.config} exists, updating config")
        config.read(args.config)
    else:
        print(f"{args.config} is not exists, generating config")

    config[f"{args.user}@{args.node}"] = {
        "password": args.password,
        "code": args.code,
    }

    with open(args.config, "w") as config_file:
        config.write(config_file)


def sigwinch_passthrough(sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack("hhhh", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
    return a


def login(args, unknown):
    """
    login node
    """
    print(f"now login to {args.user}@{args.node}")

    machine = f"{args.user}@{args.node}"
    password = ""
    code = ""
    use_config = False

    if not args.password is None:
        password = args.password
        if args.verbose:
            print(f"password in input is {password}")
    else:
        print(f"password is empty, using configed in {args.config}")
        use_config = True

    if args.otp:
        if not args.code is None:
            code = args.code
            if args.verbose:
                print(f"code in input is {code}")
        else:
            print(f"code is empty, using configed in {args.config}")
            use_config = True

    if use_config:
        config = configparser.ConfigParser()

        if os.path.exists(args.config):
            config.read(args.config)

            if machine in config:
                password = config[machine]["password"]
                if args.otp:
                    code = config[machine]["code"]
                if args.verbose:
                    print(f"password in {args.config} is {password}")
                    if args.otp:
                        print(f"code in {args.config} is {code}")
            else:
                print(
                    f"""
                    {machine} is not configed in {args.config}\n
                    please update {args.config}
                    """
                )
                sys.exit()
        else:
            print(
                f"""
                {args.config} is not exists, please generate it first\n
                or supply --user <user> --password <password> [--code <code> --otp]
                """
            )
            sys.exit()

    # auto login using expect module
    child = pexpect.spawn(f"ssh {machine}")

    # control window size
    window_size = sigwinch_passthrough(1, 2)
    if not child.closed:
        child.setwinsize(window_size[0], window_size[1])

    child.expect("Password:")
    child.sendline(password)

    if args.otp:
        totp = pyotp.TOTP(code)
        code = totp.now()

        child.expect("Verification code:")
        child.sendline(code)
        signal.signal(signal.SIGWINCH, sigwinch_passthrough)

    child.interact()
    sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(description="ssh toolkit", prog="sshtk")
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="print software version and exit",
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--user",
        "-u",
        dest="user",
        type=str,
        required=True,
        default=getpass.getuser(),
        help="user name",
    )
    common_parser.add_argument(
        "--password", "-p", dest="password", type=str, help="password"
    )
    common_parser.add_argument("--code", "-c", dest="code", type=str, help="password")
    common_parser.add_argument(
        "--node",
        "-n",
        dest="node",
        type=str,
        required=True,
        default="ssh remote node",
        help="node",
    )
    common_parser.add_argument(
        "--tunel",
        "-t",
        dest="tunel",
        type=str,
        nargs="?",
        default="ssh tunel",
        help="ssh forward remote specific port by ssh tunel",
    )

    common_parser.add_argument(
        "--config",
        "-f",
        dest="config",
        type=str,
        default=DEFAULT_CONFIG,
        help=f"config file, default: {DEFAULT_CONFIG}",
    )

    login_parser = argparse.ArgumentParser(add_help=False)
    login_parser.add_argument(
        "--otp",
        "-o",
        dest="otp",
        action="store_true",
        default=True,
        help="login with One Time Password, default: True",
    )
    login_parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="pritn login details",
    )

    subparsers = parser.add_subparsers(title="available subcommands", metavar="")

    parser_config = subparsers.add_parser(
        "generate-config",
        parents=[common_parser],
        prog="sshtk generate-config",
        help=f"sshtk generate config file on {DEFAULT_CONFIG}",
    )
    parser_config.set_defaults(func=generate_config)

    parser_login = subparsers.add_parser(
        "login",
        parents=[common_parser, login_parser],
        prog="sshtk login",
        help="sshtk login specific node, support password and OTP",
    )
    parser_login.set_defaults(func=login)

    args, unknown = parser.parse_known_args()

    try:
        if args.version:
            print("sshtk version %s" % __version__)
            sys.exit(0)
        args.func(args, unknown)
    except AttributeError as e:
        print(e)
        parser.print_help()


def main():
    parse_args()


if __name__ == "__main__":
    main()
