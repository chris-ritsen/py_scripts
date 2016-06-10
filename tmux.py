
import os
import subprocess
import time

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
      if "windows" in session:
        windows = session["windows"]
        self.new_session(session, windows[0])

        for window in windows[1:]:
          self.new_window(window)

      if session != self.sessions[0]:
        cmd = [
          "new-session",
          "-d",
          "-c",
          "/home/chris",
          "-s",
          session["name"],
          "-t",
          self.sessions[0]["name"]
        ]

        self.command(cmd)

    for session in self.sessions:
      self.command([
        "select-window",
        "-t",
        session["name"] + ":1"
      ])

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

    for key, value in session["keys"].items():
      self.command([
        "bind-key",
        key,
        value
      ])

    for key, value in session["options"].items():
      if type(value) == type(True):
        value = "on" if value else "off"

      self.command([
        "set-option",
        "-g",
        key,
        value
      ])

    for key, value in session["env"].items():
      self.command([
        "set-environment",
        key,
        value
      ])

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

