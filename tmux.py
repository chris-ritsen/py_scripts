
from os import environ
from subprocess import check_output

tmux_socket = environ["HOME"] + "/.tmp/tmux/tmux-1000/books"

def cmd(command):
  return check_output(command, shell=True).decode()

def is_attached():
  string = "tmux -S " + tmux_socket + " ls -F '#{session_attached}' | sort -ur | head -n1"
  return int(cmd(string)) > 0

def session_active():
  string = "tmux -S " + tmux_socket + " ls -F '#{session_attached}' | sort -ur | head -n1"
  return int(cmd(string)) > 0

