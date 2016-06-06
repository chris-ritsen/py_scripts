
import os
import random
import re
import subprocess

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

filters = "|".join([
  "\.alt",
  "clips",
  "extra",
  "feh.*filelist",
  "images",
  "screenshots",
  "special_features",
  "srt",
  "unsorted",
  "vtt"
  # "\.png",
  # "\.jpg",
])

expr = "".join([
  "^(.(?!(",
  filters,
  ")))*$"
])

regex = re.compile(expr)

def get_episodes(shows, ask=True, sort="normal", query=''):
  episodes = []

  if ask:

    temp_file = '/tmp/mpv_dirnames'

    with open(temp_file, "w") as file:
      for filename in shows:
        file.write("%s\n" % filename)

    command = ["cat", temp_file]
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)

    try:
      command = ["fzf" ] + fzf_options

      if query:
        command += ["--query='" + query]

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

def get_playlist(shows_path, ask=True, sort="normal", query=''):
  shows = get_shows(shows_path)
  episodes = get_episodes(shows, ask, sort, query)
  playlist = []

  try:
    temp_file = '/tmp/mpv_filenames'

    with open(temp_file, "w") as file:
      for filename in episodes:
        file.write("%s\n" % filename)

    command = ["cat", temp_file]
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)

    command = ["fzf"] + fzf_options

    if not ask and query:
      command += ["--query='" + query + " "]

    output = subprocess.check_output(command, stdin=ps.stdout)
    output = output.decode().split("\n")
    playlist = list(set(filter(None, output)))
    playlist.sort()
    ps.wait()
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

