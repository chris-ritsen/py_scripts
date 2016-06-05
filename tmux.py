
from os import environ
from subprocess import check_output

# TODO: I guess class stuff?

tmux_socket = environ["HOME"] + "/.tmp/tmux/tmux-1000/books"

def cmd(command):
  return check_output(command, shell=True).decode()

def attached():
  string = "tmux -S " + tmux_socket + " ls -F '#{session_attached}' | sort -ur | head -n1"
  return int(cmd(string)) > 0

# def session_active():
#   call(["tmux", "-S", tmux_socket, "has-session", "-t", "books"])
#   string = "tmux -S " + tmux_socket + " ls -F '#{session_attached}' | sort -ur | head -n1"
#   return int(cmd(string)) > 0

