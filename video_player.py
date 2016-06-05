#!/usr/bin/python

from pprint import pprint
import argparse
import json
import os
import random
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
  # "ctrl-b:page-up",
  # "ctrl-d:page-down",
  # "ctrl-f:page-down",
  "ctrl-j:accept",
  "ctrl-t:toggle-all",
  # "ctrl-u:page-up"
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
  "+s",
  "--select-1",
  "--prompt=",
  "--tac",
  "-i",
  "-m",
  "-x"
]

def get_episodes(shows, ask=True, sort="normal"):
  episodes = []

  if ask:
    command = ["echo", "\n".join(shows)]
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)

    try:
      command = ["fzf" ] + fzf_options
      output = subprocess.check_output(command, stdin=ps.stdout).decode()
      ps.wait()

      output = (output.split("\n"))
      shows = list(filter(None, output))
    except:
      shows = []

    if not shows:
      return

  for show in shows:
    for dirname, dirnames, filenames in os.walk(show):
      for filename in filenames:
        episodes.append(os.path.join(dirname, filename))

  episodes = list(set(filter(regex.match, episodes)))

  if sort == "normal":
    episodes.sort()
  elif sort == "random":
    random.shuffle(episodes)
  # eps = [episode(ep) for ep in episodes]

  return episodes

def get_playlist(shows_path, ask=True, sort="normal"):
  shows = get_shows(shows_path)
  episodes = get_episodes(shows, ask, sort)
  playlist = []

  try:
    temp_file = '/tmp/mpv_filenames'

    with open(temp_file, "w") as file:
      for filename in episodes:
        file.write("%s\n" % filename)

    command = ["cat", temp_file]
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)

    command = ["fzf"] + fzf_options
    output = subprocess.check_output(command, stdin=ps.stdout)
    output = output.decode().split("\n")
    playlist = list(filter(None, output))
    ps.wait()
    exit()
  except:
    pass

  return playlist

def get_shows(shows_path):
  shows = []

  for dirname, dirnames, filenames in os.walk(shows_path):
    shows.append(os.path.join(dirname))

    for subdirname in dirnames:
      shows.append(os.path.join(dirname, subdirname))


  shows = list(set(filter(regex.match, shows)))
  shows.sort()

  return shows

def seed_playlist(shows_path, ask_shows=True, sort="normal"):
  playlist = get_playlist(shows_path, ask_shows, sort)

  if not playlist:
    return

  mpv.stop()
  mpv.playlist_replace(playlist)

  while mpv.path() not in playlist:
    time.sleep(0.1)

  mpv.unpause()

def get_current_dir():
  filename=mpv.path()

  if not filename:
    return ""

  return basename(os.path.dirname(filename))

def episode(filename=mpv.path()):

  if not filename:
    return ""

  return basename(filename).split(".")[0]

def watch_video():
  playlist = mpv.playlist()

  if not playlist:
    return

  ep = episode()
  show_name = get_current_dir()

  if not show_name or not ep or ep == '' or ep not in tv.shows[show_name]:
    time.sleep(0.01)
    return

  if not "length" in tv.shows[show_name][ep]:
    tv.shows[show_name][ep]["length"] = mpv.length()

  length = tv.shows[show_name][ep]["length"]
  pos = mpv.time_pos() or 0
  ranges = tv.shows[show_name][ep]["ranges"]

  for i, (start, stop) in enumerate(ranges):
    if pos < start or pos > stop:
      # Outside of range
      continue

    if pos > start and pos < stop and stop < length:
      # Current position is within range; skip ahead
      mpv.set_property("time-pos", stop)
      time.sleep(0.1)
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

def parse_args():
  parser = argparse.ArgumentParser(
      description='Do stuff',
      prog='video_player.py',
      usage='%(prog)s [options]',
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument(
      '-d',
      '--dir',
      type=str,
      default="/Media/Videos",
      help='Directory to check for files.')

  parser.add_argument(
      "--loop",
      action='store_true',
      default=False,
      help='Keep asking for videos to play'
  )

  parser.add_argument(
      "--sort",
      choices=["normal", "random", "reverse"],
      default="normal",
      help='Sort order',
      type=str
  )

  group = parser.add_mutually_exclusive_group()

  group.add_argument(
      '--ask-shows',
      default=True,
      action='store_true',
      help='Ask for shows from a list')

  group.add_argument(
      '--seed',
      default=False,
      action='store_true',
      help='Seed playlist')

  group.add_argument(
      '--no-ask-shows',
      default=False,
      action='store_true',
      help='Show all files in one list')

  args = parser.parse_args()

  if args.no_ask_shows:
    args.ask_shows = False

  return args

if __name__ == '__main__':
  signal.signal(signal.SIGINT, sig_handler)
  args = parse_args()

  if args.seed:
    seed_playlist(args.dir, args.ask_shows and not args.no_ask_shows, args.sort)

  while True:
    # if args.loop:
    #   seed_playlist(args.dir, args.ask_shows and not args.no_ask_shows, args.sort)
    # else:
    #   break
    watch_video()

