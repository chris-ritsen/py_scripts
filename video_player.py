#!/usr/bin/python

from pprint import pprint
import argparse
import os
import random
import re
import signal
import subprocess
import sys
import time

import mpv
import playlist
import tv

basename = os.path.basename

def sig_handler(signal, frame):
  sys.exit(0)

def slideshow(speed=1):

  filters = "|".join([
    "feh.*filelist",
    "unsorted"
  ])

  expr = "".join([
    "^(.(?!(",
    filters,
    ")))*$"
  ])

  regex = re.compile(expr)

  photos = []
  graphics_dir = "/Media/Big/Graphics/sorted/jpg"

  for dirname, dirnames, filenames in os.walk(graphics_dir):
    files = [os.path.join(dirname, filename) for filename in filenames]
    photos = files

  photos = list(set(filter(regex.match, photos)))
  random.shuffle(photos)
  mpv.playlist_replace(photos)
  mpv.set_property("speed", speed)
  mpv.unpause()

def seed_playlist(shows_path, ask_shows=True, sort="normal", query=''):
  files = playlist.get_playlist(shows_path, ask_shows, sort, query)

  if not files:
    return

  mpv.playlist_replace(files)

  # while mpv.path() not in files:
  #   time.sleep(0.1)

  mpv.unpause()

def get_current_dir():
  filename=mpv.path()

  if not filename:
    return ""

  return basename(os.path.dirname(filename))

def episode(filename=''):

  if not filename:
    return ""

  return basename(filename).split(".")[0]

def watch_video():
  mpv_playlist = mpv.playlist()

  if not mpv_playlist:
    return

  ep = episode(mpv.path())
  show_name = get_current_dir()

  try:
    if not show_name or not ep or ep == '' or ep not in tv.shows[show_name]:
      time.sleep(0.01)
      return
  except:
    return

  ep_info = tv.shows[show_name][ep]

  if not "length" in ep_info:
    ep_info["length"] = mpv.length()

  length = ep_info["length"]
  pos = mpv.time_pos() or 0
  ranges = ep_info["ranges"]

  if mpv.get_property("pause"):
    return

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

def parse_args():
  parser = argparse.ArgumentParser(
      description='Load files into mpv for playback',
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
      "--daemon",
      action='store_true',
      default=False,
      help='Run mpv'
  )

  parser.add_argument(
      "--merge",
      action='store_true',
      default=False,
      help='Act like everything in the playlist is one big file'
  )

  parser.add_argument(
      "--socket",
      default=os.environ["XDG_RUNTIME_DIR"] + '/mpv/video',
      help='Socket for mpv',
      type=str
  )

  parser.add_argument(
      "--sort",
      choices=["normal", "random", "reverse"],
      default="normal",
      help='Sort order',
      type=str
  )

  parser.add_argument(
      '--query',
      help='Initial filter for directory search',
      type=str)

  parser.add_argument(
      '--speed',
      default=1.0,
      help='Slideshow speed in seconds',
      type=float)

  parser.add_argument(
      '--slideshow',
      default=False,
      action='store_true',
      help='Photos slideshow')

  parser.add_argument(
      '--seed',
      default=False,
      action='store_true',
      help='Seed playlist')

  parser.add_argument(
      '--skip',
      default=False,
      action='store_true',
      help='Skip over boring sections of videos')

  group = parser.add_mutually_exclusive_group()

  group.add_argument(
      '--ask-shows',
      default=True,
      action='store_true',
      help='Ask for shows from a list')

  group.add_argument(
      '--no-ask-shows',
      default=False,
      action='store_true',
      help='Show all files in one list')

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

  args = parser.parse_args()

  if args.no_ask_shows:
    args.ask_shows = False

  return args

if __name__ == '__main__':
  args = parse_args()

  ask = args.ask_shows and not args.no_ask_shows

  mpv.set_socket(args.socket)

  if args.daemon and args.socket:
    mpv.player_go(args.merge)
    exit()

  if args.seed:
    seed_playlist(args.dir, ask, args.sort, args.query)
    mpv.set_property("speed", args.speed)

  if args.slideshow:
    slideshow(args.speed)

  if not args.skip and not args.loop:
    exit()

  subprocess.call(["clear"])

  while True:
    # TODO: watch redis pub/sub for events instead of querying mpv directly
    time.sleep(0.01)
    signal.signal(signal.SIGINT, sig_handler)

    if args.loop:
      seed_playlist(args.dir, ask, args.sort, args.query)
    else:
      if args.skip:
        watch_video()

