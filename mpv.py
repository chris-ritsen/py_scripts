#!/usr/bin/python

import json
import os
import pprint
import subprocess
import time

basename = os.path.basename

def query(command):
  socket = get_socket()

  # p1 = subprocess.Popen(["echo", json], stdout=subprocess.PIPE)
  # p2 = subprocess.Popen(["socat", "-", socket], stdin=p1.stdout, stdout=subprocess.PIPE)
  # value = p2.communicate()[0]
  # p1.stdout.close()

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

def get_path():
  return get_property_string("path")

def get_socket():
  return subprocess.check_output(["redis-cli", "get", "socket"]).decode()

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

def stop_playback():
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


def seed_playlist(playlist):
  playlist_replace(playlist)

  while get_property("path") not in playlist:
    time.sleep(0.1)

def episode():
  filename = get_property("path")
  return basename(filename).split(".")[0]

def time_pos():
  return get_property("time-pos")

if __name__ == '__main__':
  playlist = [
    # "/Media/Big/Videos/TV/star_trek/star_trek.next_generation.the/s02e06.mkv",
    "/Media/Big/Videos/TV/star_trek/star_trek.next_generation.the/s02e07.mkv"
  ]

  seed_playlist(playlist)
  time.sleep(1)
  mpv_playlist = get_property("playlist")

  set_property("pause", False)

  episodes = {
    "s02e06": {
      "ranges": [
        (196.6, 293.1),
        (2678.5, float("inf"))
      ]
    },
    "s02e07": {
      "ranges": [
        (140.52, 237.5),
        (2663.45, float("inf"))
      ]
    }
  }

  # TODO: Reimplement the property save/restore functionality

  while True:
    mpv_playlist = get_property("playlist")

    if not mpv_playlist:
      break

    ep = episode()

    if not ep or ep not in episodes:
      time.sleep(0.01)
      continue

    pos = time_pos() or 0

    if not "length" in episodes[ep]:
      episodes[ep]["length"] = get_property("length")

    length = episodes[ep]["length"]
    ranges = episodes[ep]["ranges"]

    for i, (a, b) in enumerate(ranges):
      if pos > a and pos < b:
        if pos > a and b >= length:
          last = basename(mpv_playlist[-1]["filename"]).split(".")[0]

          if last == ep:
            stop_playback()
          else:
            playlist_next()
        else:
          set_property("time-pos", b)

