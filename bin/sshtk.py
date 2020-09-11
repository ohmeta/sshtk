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


def config_func(args, unknown):
    """
    generate config
    if node on config, config will update
    """
    conf = configparser.ConfigParser()

    if os.path.exists(args.config):
        print(f"{args.config} exists, updating config")
        conf.read(args.config)
    else:
        print(f"{args.config} is not exists, generating config")

    tunel = ""
    if not args.tunel is None:
        tunel = ",".join(args.tunel)

    conf[f"{args.user}@{args.node}"] = {
        "password": args.password,
        "code": args.code,
        "tunel": tunel,
    }

    with open(args.config, "w") as config_file:
        conf.write(config_file)

    print(f"please see {args.config} for details")


def sigwinch_passthrough(sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack("hhhh", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
    return a


def run_ssh(cmd, password, code, otp):
    # auto login using expect module
    child = pexpect.spawn(cmd)

    # control window size
    window_size = sigwinch_passthrough(1, 2)
    if not child.closed:
        child.setwinsize(window_size[0], window_size[1])

    child.expect("Password:")
    child.sendline(password)

    if otp:
        totp = pyotp.TOTP(code)
        code = totp.now()

        child.expect("Verification code:")
        child.sendline(code)
        signal.signal(signal.SIGWINCH, sigwinch_passthrough)

    child.interact()
    # sys.exit()


def parse(args):
    """
    parse user, node, password, code
    """
    machine = f"{args.user}@{args.node}"
    print(f"{machine}")

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

    return machine, password, code, args.otp, config


def login_func(args, unknown):
    """
    login mode
    """
    machine, password, code, otp, config = parse(args)
    run_ssh(f"""ssh {machine}""", password, code, otp)


def tunel_func(args, unknown):
    """
    tunel mode
    """
    machine, password, code, otp, config = parse(args)

    tunel = args.tunel
    if len(tunel) > 0:
        if args.verbose:
            for i in tunel:
                print(f"tunel in input is {i}")
    else:
        print(f"tunel is empty, using configed in {args.config}")
        tunel = config[machine]["tunel"].split(",")
        if args.verbose:
            for i in tunel:
                print(f"tunel in input is {i}")

    if len(tunel) > 0:
        for i in tunel:
            cmd = f"""ssh -N -f -L {i} {machine}"""
            run_ssh(cmd, password, code, otp)


def dl_func(args, unknown):
    """
    scp download mode
    """
    os.makedirs(args.outdir, exist_ok=True)
    machine, password, code, otp, config = parse(args)

    if args.files is None:
        print("please supply absolute remote files path")
    else:
        for i in args.files:
            cmd = f"scp {machine}:{i} {args.outdir}"
            run_ssh(cmd, password, code, otp)


def up_func(args, unknown):
    """
    scp upload mode
    """
    machine, password, code, otp, config = parse(args)

    if args.files is None:
        print("please supply local files path")
    else:
        for i in args.files:
            cmd = f"scp {i} {machine}:{args.outdir}"
            run_ssh(cmd, password, code, otp)


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
        "--config",
        "-f",
        dest="config",
        type=str,
        default=DEFAULT_CONFIG,
        help=f"config file, default: {DEFAULT_CONFIG}",
    )

    bool_parser = argparse.ArgumentParser(add_help=False)
    bool_parser.add_argument(
        "--otp",
        dest="otp",
        action="store_true",
        default=True,
        help="login with One Time Password, default: True",
    )
    bool_parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="print login details",
    )

    subparsers = parser.add_subparsers(title="available subcommands", metavar="")

    parser_config = subparsers.add_parser(
        "config",
        parents=[common_parser],
        prog="sshtk config",
        help=f"sshtk generate config file, default on: {DEFAULT_CONFIG}",
    )
    parser_config.add_argument(
        "--tunel", "-t", dest="tunel", nargs="+", help="ssh tunel"
    )
    parser_config.set_defaults(func=config_func)

    parser_login = subparsers.add_parser(
        "login",
        parents=[common_parser, bool_parser],
        prog="sshtk login",
        help="sshtk login specific node, support password and OTP",
    )
    parser_login.set_defaults(func=login_func)

    parser_tunel = subparsers.add_parser(
        "tunel",
        parents=[common_parser, bool_parser],
        prog="sshtk tunel",
        help="sshtk tunel specific node, support password and OTP",
    )
    parser_tunel.add_argument("tunel", metavar="TUNEL", nargs="*", help="ssh tunel")
    parser_tunel.set_defaults(func=tunel_func)

    parser_dl = subparsers.add_parser(
        "dl",
        parents=[common_parser, bool_parser],
        prog="sshtk dl",
        help="sshtk download remote files using scp, support password and OTP",
    )
    parser_dl.add_argument(
        "--outdir",
        "-o",
        dest="outdir",
        required=True,
        default="./",
        help="scp files to a directory, default: ./",
    )
    parser_dl.add_argument("files", metavar="FILES", nargs="+", help="scp files")
    parser_dl.set_defaults(func=dl_func)

    parser_up = subparsers.add_parser(
        "up",
        parents=[common_parser, bool_parser],
        prog="sshtk up",
        help="sshtk upload local files using scp, support password and OTP",
    )
    parser_up.add_argument(
        "--outdir",
        "-o",
        dest="outdir",
        required=True,
        help="scp files to a directory, must be a absolute remote path",
    )
    parser_up.add_argument("files", metavar="FILES", nargs="+", help="scp files")
    parser_up.set_defaults(func=up_func)

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