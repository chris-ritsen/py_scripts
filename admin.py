
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
  os.environ["MPD_BOOKS_PORT"],
  os.environ["MPD_MUSIC_PORT"],
  os.environ["MPD_STREAM_PORT"],
  os.environ["MPD_VOICE_PORT"]
]

ports = [int(i) for i in ports]

for port in ports:
  result = sock.connect_ex(('0.0.0.0', port))

  if result == 0:
    print("Port is open")
  else:
    print("Port is not open")

exit()

del sessions[0]["windows"][4]

sessions[0]["windows"] = sorted(sessions[0]["windows"], key=operator.itemgetter('index'))

# print(list(map(lambda x: x["name"], sessions)))
# print(list(map(lambda x: x["name"], sessions[0]["windows"])))
# print(sessions)

