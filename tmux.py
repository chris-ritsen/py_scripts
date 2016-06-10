
import subprocess
import os

class Tmux(object):
  def __init__(self):
    self.socket = None
    self.sessions = []

  def command(self, cmd):
    cmd = [
      "/usr/local/bin/tmux",
      "-S",
      self.socket
    ] + cmd

    subprocess.call(cmd)

  def start_server(self):
    for session in self.sessions:
      windows = session["windows"]
      self.new_session(session, windows[0])

      for window in windows[1:]:
        self.new_window(window)

  def new_session(self, session, window):
    cmd = [
      "new-session",
      "-d",
      "-s", session["name"],
      "-c", window["dir"],
      "-n", window["name"],
      window["command"]
    ]

    self.command(cmd)

  def new_window(self, window):
    cmd = [
      "new-window",
      "-t", window["target"],
      "-c", window["dir"],
      "-n", window["name"],
      window["command"]
    ]

    self.command(cmd)

  def has_server(self):
    # if stat.S_ISSOCK(mode):
    #   print("Socket file exists")

    try:
      subprocess.check_output([
        "/usr/local/bin/tmux",
        "-S",
        self.socket,
        "list-sessions",
      ], stderr=subprocess.PIPE)
      return True
    except:
      return False

tmux_socket = os.environ["HOME"] + "/.tmp/tmux/tmux-1000/books"

def cmd(command):
  return subprocess.check_output(command, shell=True).decode()

def attached():
  string = "tmux -S " + tmux_socket + " ls -F '#{session_attached}' | sort -ur | head -n1"
  return int(cmd(string)) > 0

