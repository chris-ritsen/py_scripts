#!/usr/bin/env python3

import argparse
import os
import signal
import sys

import admin
import tmux


def sig_handler(signal, frame):
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Create tmux sessions on different sockets',
        usage='%(prog)s [options]',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "--socket",
        default=os.environ["XDG_RUNTIME_DIR"] + '/default',
        help='Socket for tmux',
        type=str
    )

    parser.add_argument(
        "-a",
        "--attach",
        action='store_true',
        default=False,
        help='Attach to tmux session'
    )

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sig_handler)
    args = parse_args()

    if "XDG_RUNTIME_DIR" in os.environ:
        socket_dir = os.environ["XDG_RUNTIME_DIR"]
    else:
        socket_dir = "/tmp/tmux-1000/"

    socket_dir = "/home/chris/.tmp/tmux/tmux-1000/"
    socket_file = socket_dir + "admin"

    t = tmux.Tmux()
    t.socket = socket_file
    t.sessions = admin.sessions

    if not t.has_server():
        t.start_server()

    if args.attach:
        t.command(["attach"])
    else:
        t.command(["list-sessions"])

