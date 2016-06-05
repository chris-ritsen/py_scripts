#!/usr/bin/python

import json
import pprint
import subprocess
import time

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
    # pprint.pprint(command)
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

if __name__ == '__main__':
  playlist = [
    # "/Media/Big/Videos/TV/star_trek/star_trek.next_generation.the/s02e06.mkv",
    "/Media/Big/Videos/TV/star_trek/star_trek.next_generation.the/s02e07.mkv"
  ]

  seed_playlist(playlist)

  # set_property("time-pos", 193)
  # print(get_property("time-pos"))
  set_property("pause", False)

  # TODO: Check if time-pos is in a range and skip to end (or next video)
  # Filename, start, stop
  # If only a start is given, then match anywhere to the end of the file
  # get_property("length")

  ranges = {
    "s02e06": [
      (196.6, 293.1),        # skip intro after cold-open
      (2678.5, float("inf")) # skip credits
    ],
    "s02e07": [
      (140.52, 237.5),
      (2663.45, float("inf"))
    ]
  }

  # TODO: Reimplement the property save/restore functionality

  while (get_property("path") == "/Media/Big/Videos/TV/star_trek/star_trek.next_generation.the/s02e06.mkv"):
    time.sleep(0.01)
    time_pos = get_property("time-pos") or 0

    if time_pos > 196.6 and time_pos < 293.1:
      set_property("time-pos", 293.1)

    if time_pos > 2678.5:
      playlist_next()

      while get_property("path") != playlist[1]:
        time.sleep(1)

  while (get_property("path") == "/Media/Big/Videos/TV/star_trek/star_trek.next_generation.the/s02e07.mkv"):
    time.sleep(0.01)
    time_pos = get_property("time-pos") or 0

    if time_pos > 140.52 and time_pos < 237.5:
      set_property("time-pos", 237.5)

    if time_pos > 2663.45:
      stop_playback()

  # print(get_property("time-pos"))
  # print(paused(), path())
  # pprint.pprint(get_property("playlist"))

