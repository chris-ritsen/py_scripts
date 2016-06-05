#!/usr/bin/python

import json
import os
import pprint
import subprocess
import time

basename = os.path.basename

def get_socket():
  return subprocess.check_output(["redis-cli", "get", "socket"]).decode()

def query(command):
  socket = get_socket()

  try:
    _json = json.dumps(command)
    cmd = " ".join(["echo '", _json, "' | socat -", socket])
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

