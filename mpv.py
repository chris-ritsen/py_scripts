
import json
import os
import pprint
import shlex
import socket
import subprocess
import time

class Player(object):
  def __init__(self):
    self.socket = None

  def write_socket(self, text):
    buffer = "{}\n".format(text).encode()

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(self.socket)
    s.send(buffer)
    output = s.recv(65565).decode()
    s.close()
    return output

  def pause(self):
    set_property("pause", True)

  def unpause(self):
    set_property("pause", False)

  def start(self, merge=False):

    # TODO: Restart player automatically in an attempt to keep playing from
    # the same position.  This would help in cases where the player window is
    # closed or the system restarts.

    # r = redis.StrictRedis(host='localhost', port=6379, db=0)
    # started = r.get("started").decode().lower() == 'true'

    # if not started:
    #   return

    command = [
      "mpv",
      "--input-unix-socket=" + self.socket,
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
      os.makedirs(os.path.dirname(self.socket), 0o775, True)
      os.chmod(os.path.dirname(self.socket), 0o775)
      # TODO: Check that the directory is actually usable
      subprocess.Popen(command)
      print("Started mpv with socket", self.socket)
    else:
      print("Server already active with socket", self.socket)

    # FIXME: hack
    time.sleep(0.5)

player = Player()

def query(command):
  if not player.socket:
    return

  try:
    if type(command) == type([]):
      command = json.dumps({"command": command})
    elif type(command) == type(""):
      command = shlex.quote(command)

    output = player.write_socket(command)
    value = json.loads(output)

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

  return query("run " + command)

def get_property_string(_property):
  return query(["get_property_string", _property])

def get_property(_property):
  return query(["get_property", _property])

def set_property(_property, value):
  query(["set_property", _property, str(value)])

def set_property_string(_property, value):
  query(["set_property_string", _property, value])

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

def shuffle():
  query(["playlist-shuffle"])

