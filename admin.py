#!/usr/bin/env python3

import argparse
import os
import signal
import stat
import subprocess
import sys

import tmux

def sig_handler(signal, frame):
  sys.exit(0)

def parse_args():
  parser = argparse.ArgumentParser(
      description='A way of scripting creation of tmux session on different sockets',
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

  mode = os.stat(socket_file).st_mode

  t = tmux.Tmux()
  t.socket = socket_file

  t.sessions = [
    {
      "detached": True,
      "options": {
        "remain-on-exit": True,
        "set-remain-on-exit": True
      },
      "env": {
        "MAIL": "/Media/Mail"
      },
      "name": "admin",
      "windows": [
        {
          "command": "vim -u NONE",
          "dir": "/home/chris/.documents/",
          "name": "notes",
          "target": "admin"
        },
        {
          "command": "vimpc",
          "dir": "/home/chris/",
          "name": "music",
          "target": "admin"
        }
      ]
    },
    {
      "name": "admin@laptop"
    },
    {
      "name": "admin@www"
    }
  ]

  if not t.has_server():
    t.start_server()

  t.command(["list-sessions"])

  if args.attach:
    t.command(["attach"])

