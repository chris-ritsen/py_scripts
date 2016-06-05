#!/usr/bin/python

from pprint import pprint
import argparse
import os
import signal
import subprocess
import sys
import time

import mpv
import playlist
import tv

basename = os.path.basename

def seed_playlist(shows_path, ask_shows=True, sort="normal"):
  files = playlist.get_playlist(shows_path, ask_shows, sort)

  if not files:
    return

  mpv.stop()
  mpv.playlist_replace(files)

  while mpv.path() not in files:
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
  mpv_playlist = mpv.playlist()

  if not mpv_playlist:
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
      last_file = mpv_playlist[-1]["filename"]
      last_ep = episode(last_file)

      if last_ep == ep:
        mpv.stop()
      else:
        mpv.playlist_next()

def sig_handler(signal, frame):
  sys.exit(0)

def parse_args():
  parser = argparse.ArgumentParser(
      description='Load files into mpv for playback',
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
      '--skip',
      default=False,
      action='store_true',
      help='Skip over boring sections of videos')

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

  if not args.skip and not args.loop:
    exit()

  while True:
    if args.loop:
      seed_playlist(args.dir, args.ask_shows and not args.no_ask_shows, args.sort)
    else:
      if args.skip:
        watch_video()

