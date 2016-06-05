#!/usr/bin/python

from pprint import pprint
import json
import os
import re
import signal
import subprocess
import sys
import time

import tv
import mpv

basename = os.path.basename

filters = "|".join([
  "\.alt",
  "clips",
  "extra",
  "images",
  "jpg",
  "png",
  "screenshots",
  "special_features",
  "srt",
  "unsorted"
])

expr = "".join([
  "^(.(?!(",
  filters,
  ")))*$"
])

regex = re.compile(expr)

bindings = ",".join([
  "ctrl-t:toggle-all",
  "ctrl-j:accept"
  # "ctrl-e:next-history",
  # "ctrl-y:previous-history"
])

fzf_options = [
  # "--ansi",
  # "--black",
  # "--color=bw",
  "--bind=" + bindings,
  "--inline-info",
  "--no-hscroll",
  "--select-1",
  "--prompt=",
  "--tac",
  "-i",
  "-m",
  "-x"
]

def get_episodes():
  shows = get_shows()

  episodes = []
  command = ["echo", "\n".join(shows)]
  ps = subprocess.Popen(command, stdout=subprocess.PIPE)

  try:
    command = ["fzf" ] + fzf_options
    output = subprocess.check_output(command, stdin=ps.stdout).decode()
    ps.wait()

    output = (output.split("\n"))
    shows = list(filter(None, output))
  except:
    exit()

  if not shows:
    exit()

  for show in shows:
    for dirname, dirnames, filenames in os.walk(show):
      for filename in filenames:
        episodes.append(os.path.join(dirname, filename))

  episodes = list(filter(regex.match, episodes))
  # eps = [episode(ep) for ep in episodes]

  return episodes

def get_playlist():
  episodes = get_episodes()
  playlist = []

  try:
    command = ["echo", "\n".join(episodes)]
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)

    command = ["fzf"] + fzf_options
    output = subprocess.check_output(command, stdin=ps.stdout)
    output = output.decode().split("\n")
    playlist = list(filter(None, output))
    ps.wait()
  except:
    return playlist

  return playlist

def get_shows():
  shows = []

  for dirname, dirnames, filenames in os.walk('/Media/Videos/TV'):
    for subdirname in dirnames:
      shows.append(os.path.join(dirname, subdirname))


  shows = list(filter(regex.match, shows))

  return shows

def seed_playlist():
  playlist = get_playlist()

  if not playlist:
    return

  mpv.stop()
  mpv.playlist_replace(playlist)

  while mpv.path() not in playlist:
    time.sleep(0.1)

  mpv.unpause()

def episode(filename=mpv.path()):

  if not filename:
    return ""

  return basename(filename).split(".")[0]

def watch_video():
  playlist = mpv.playlist()

  if not playlist:
    return

  ep = episode()

  if not ep or ep not in tv.episodes:
    time.sleep(0.01)
    return

  if not "length" in tv.episodes[ep]:
    tv.episodes[ep]["length"] = mpv.length()

  length = tv.episodes[ep]["length"]
  pos = mpv.time_pos() or 0
  ranges = tv.episodes[ep]["ranges"]

  for i, (start, stop) in enumerate(ranges):
    if pos < start or pos > stop:
      # Outside of range
      continue

    if pos > start and pos < stop and stop < length:
      # Current position is within range; skip ahead
      mpv.set_property("time-pos", stop)
      continue

    if pos > start and stop > length:
      # Range is here to end of video
      last_file = playlist[-1]["filename"]
      last_ep = episode(last_file)

      if last_ep == ep:
        mpv.stop()
      else:
        mpv.playlist_next()

def sig_handler(signal, frame):
  sys.exit(0)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, sig_handler)

  seed_playlist()

  # while True:
  #   watch_video()

