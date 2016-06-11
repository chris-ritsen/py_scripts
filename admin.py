
import operator
import os
import socket
import subprocess

sessions = [
  {
    "keys": {
      "R": "respawn-window"
    },
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
        "command": "dtach -A /home/chris/.tmp/dtach/notes -zE -r winch vim -u NONE",
        "dir": "/home/chris/.documents/",
        "index": 1,
        "name": "notes",
        "target": "admin"
      },
      {
        "command": "dtach -A /home/chris/.tmp/dtach/finch -zE -r winch $SHELL -c finch --nologin",
        "dir": "/home/chris/.documents/",
        "index": 5,
        "name": "chat",
        "target": "admin"
      },
      {
        "command": "dtach -A /home/chris/.tmp/dtach/irssi -zE -r ctrl_l $SHELL -c irssi --noconnect",
        "dir": "/home/chris/",
        "index": 4,
        "name": "irc",
        "target": "admin"
      },
      {
        "command": "dtach -A /home/chris/.tmp/dtach/mutt -zE -r winch $SHELL -c mutt -e 'push <limit>!~l<enter>'",
        "dir": "/home/chris/",
        "index": 3,
        "name": "mail",
        "target": "admin"
      },
      {
        "command": "vimpc",
        "dir": "/home/chris/",
        "index": 6,
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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ports = [
  "MPD_BOOKS_PORT",
  "MPD_MUSIC_PORT",
  "MPD_STREAM_PORT",
  "MPD_VOICE_PORT"
]

# TODO: Test that emacs server is active
# emacs_socket = "/tmp/emacs1000/server"

ports = set(os.environ.keys()).intersection(ports)
ports = [int(os.environ[key]) for key in ports]
has_mpd = any([sock.connect_ex(('0.0.0.0', port)) == 0 for port in ports])

try:
  subprocess.check_output([
    "emacsclient",
    "--eval",
    "(version)"
  ], stderr=subprocess.PIPE)
except:
  print("derp I gots no emacs")
  # del sessions[0]["windows"][4]

print([key for key, value in sessions[0]["windows"].items() if value == "notes"])

# TODO: Check that emacs is running and run emacsclient

if not has_mpd:
  del sessions[0]["windows"][4]

windows = sessions[0]["windows"]
sessions[0]["windows"] = sorted(windows, key=operator.itemgetter('index'))

