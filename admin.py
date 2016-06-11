
import operator
import os
import socket

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

ports = list(set(os.environ.keys()).intersection(ports))
ports = [int(os.environ[i]) for i in ports]
has_mpd = False

for port in ports:
  address = ('0.0.0.0', port)
  result = sock.connect_ex(address)

  if result == 0:
    has_mpd = True
    break

# TODO: Check that emacs is running and run emacsclient

if not has_mpd:
  del sessions[0]["windows"][4]

windows = sessions[0]["windows"]
sessions[0]["windows"] = sorted(windows, key=operator.itemgetter('index'))

