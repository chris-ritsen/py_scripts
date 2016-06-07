
import json
import os
import pprint
import shlex
import subprocess
import time

import redis

class Player(object):
  def __init__(self):
    self.socket = None

  def pause(self):
    set_property("pause", True)

  def unpause(self):
    set_property("pause", False)

  def start(self, merge=False):

    # TODO: Restart player automatically in an attempt to keep playing from the
    # same position.  This would help in cases where the player window is closed
    # or the system restarts.

    # r = redis.StrictRedis(host='localhost', port=6379, db=0)
    # started = r.get("started").decode().lower() == 'true'

    # if not started:
    #   return

    socket = self.socket

    command = [
      "mpv",
      "--input-unix-socket=" + socket,
      "--softvol-max=200",
      "--no-resume-playback",
      "--force-window=yes",
      "--keep-open=yes",
      "--idle=yes",
    ]

    if merge:
      command.append("--merge-files")

    shell = os.environ["SHELL"]

    if not get_property('mpv-version'):
      os.makedirs(os.path.dirname(socket), 0x777, True)
      subprocess.Popen(command)
      print("Started mpv with socket", socket)
    else:
      print("Error: server already active with socket", socket)

player = Player()

def query_raw(command):
  socket = player.socket

  if not socket:
    return

  try:
    command = shlex.quote(command)
    cmd = " ".join(['echo', command, " | socat -", socket, "2> /dev/null"])
    print(cmd)
    output = subprocess.check_output(cmd, shell=True)
    value = json.loads(output.decode())

    if "data" not in value:
      return

    value = value["data"]

    return value
  except:
    return

def query(command):
  socket = player.socket

  if not socket:
    return

  try:
    _json = json.dumps({"command": command})

    cmd = " ".join([
      "echo '",
      _json,
      "' | socat -",
      socket,
      "2> /dev/null"
    ])

    output = subprocess.check_output(cmd, shell=True)
    value = json.loads(output.decode())

    if "data" not in value:
      return

    value = value["data"]

    return value
  except:
    return

def show_text(text):
  query(["show-text", text])

def run(command):
  if type(command) == type(""):
    command = [command]

  shell = os.environ["SHELL"]
  command = shell + ' -c "{}"'.format(";".join(command))

  return query_raw("run " + command)

def get_property_string(_property):
  return query(["get_property_string", _property])

def get_property(_property):
  return query(["get_property", _property])

def set_property(_property, value):
  query(["set_property", _property, value])

def paused():
  return get_property("pause")

def playlist_replace(files):
  temp_file = '/tmp/mpv_playlist'

  with open(temp_file, "w") as file:
    for filename in files:
      file.write("%s\n" % filename)

  cmd = [
    "loadlist",
    temp_file,
    "replace"
  ]

  return query(cmd)

def stop():
  query(["stop"])

def playlist_next():
  query(["playlist_next"])

def time_pos():
  return get_property("time-pos")

def playlist():
  return get_property("playlist")

def path():
  return get_property_string("path")

def length():
  return get_property("length")

