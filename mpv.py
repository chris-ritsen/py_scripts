
import json
import os
import pprint
import subprocess
import time

import redis

basename = os.path.basename

class Player(object):
  def __init__(self):
    self.socket = None

  def set_socket(self, socket):
    self.socket = socket

  def get_socket(self):
    return self.socket

# _socket = subprocess.check_output(["redis-cli", "get", "socket"]).decode().strip()

player = Player()

def set_socket(socket):
  player.set_socket(socket)

def query(command):
  socket = player.get_socket()

  if not socket:
    return

  try:
    _json = json.dumps(command)
    cmd = " ".join(["echo '", _json, "' | socat -", socket, "2> /dev/null"])
    output = subprocess.check_output(cmd, shell=True)
    value = json.loads(output.decode())

    if "data" not in value:
      return

    value = value["data"]

    return value
  except:
    return

def get_property_string(_property):
  cmd = {
    "command": [
      "get_property_string",
      _property
    ]
  }

  return query(cmd)

def get_property(_property):
  cmd = {
    "command": [
      "get_property",
      _property
    ]
  }

  return query(cmd)

def set_property(_property, value):
  cmd = {
    "command": [
      "set_property",
      _property,
      value
    ]
  }

  return query(cmd)

def paused():
  return get_property("pause")

def playlist_replace(files):
  temp_file = '/tmp/mpv_playlist'

  with open(temp_file, "w") as file:
    for filename in files:
      file.write("%s\n" % filename)

  cmd = {
    "command": [
      "loadlist",
      temp_file,
      "replace"
    ]
  }

  return query(cmd)

def stop():
  cmd = {
    "command": [
      "stop",
    ]
  }

  return query(cmd)

def playlist_next():
  cmd = {
    "command": [
      "playlist_next",
    ]
  }

  return query(cmd)

def time_pos():
  return get_property("time-pos")

def playlist():
  return get_property("playlist")

def pause():
  set_property("pause", False)

def unpause():
  set_property("pause", False)

def path():
  return get_property_string("path")

def length():
  return get_property("length")

def player_go(merge=False):
  
  # TODO: Restart player automatically in an attempt to keep playing from the
  # same position.  This would help in cases where the player window is closed
  # or the system restarts.

  # r = redis.StrictRedis(host='localhost', port=6379, db=0)
  # started = r.get("started").decode().lower() == 'true'

  # if not started:
  #   return

  command = [
    "mpv",
    "--input-unix-socket=" + player.get_socket(),
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
    os.makedirs(os.environ["XDG_RUNTIME_DIR"] + '/mpv')
    subprocess.call(command)

