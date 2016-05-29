#!/usr/bin/python3

from getopt import getopt
from os import path, environ
from subprocess import call, check_output, check_call
from time import sleep
import argparse
import signal
import socket
import sys

def cmd(command):
  return check_output(command, shell=True).decode()

def acmd(command):
  return check_output(command).decode()

servername = 'BOOKS'
tmux_socket = environ["HOME"] + "/.tmp/tmux/tmux-1000/books"
window_name = 'books'

def vim_key(key):
  call(["vim", "--servername", servername, "--remote-send", key])

def vim_expr(expr):
  return acmd(["vim", "--servername", servername, "--remote-expr", expr])

def get_rate():
  return float(check_output(["redis-cli", "get", "reading_speed"]).decode())

def is_attached():
  string = "tmux -S " + tmux_socket + " ls -F '#{session_attached}' | sort -ur | head -n1"
  return int(cmd(string)) > 0

def session_active():
  string = "tmux -S " + tmux_socket + " ls -F '#{session_attached}' | sort -ur | head -n1"
  return int(cmd(string)) > 0

def make_window():
  class_name = 'bigspaceurxvt'
  desktop = 2

  if socket.gethostname() == 'laptop':
    class_name = 'bigspacelaptop'

  if not is_attached():
    call(["wmctrl", "-s", str(desktop)])
    call(["urxvtc", "-name", class_name, "-e", "zsh", "-ic", "books"])
    call(["wmctrl", "-r", window_name, "-t", str(desktop)])

  call(["clear"])

  while not is_attached():
    call(["tmux", "-S", tmux_socket, "has-session", "-t", "books"])
    sleep(0.1)

  call(["wmctrl", "-a", window_name])

def active_window():
  return acmd(["xdotool", "getactivewindow", "getwindowname"]).strip()

def delay(seconds):
  rate = get_rate()
  wait = seconds * rate
  sleep(wait)

def char_count(string):
  return len(string)

def sig_handler(signal, frame):
  sys.exit(0)

def idle():
  return int(check_output(["xprintidle"])) / 1000

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Do stuff', prog='PROG', usage='%(prog)s [options]')
  parser.add_argument('--speed', type=float, help='Rate to do stuff')
  args = parser.parse_args()

  signal.signal(signal.SIGINT, sig_handler)

  if args.speed and args.speed > 0:
    rate = 1 / args.speed
    check_output(["redis-cli", "set", "reading_speed", str(rate)])

  make_window()

  while is_attached():
    if idle() < 3 or active_window() != window_name:
      sleep(1)
      continue

    vim_key('<Esc>')
    vim_key('zz')

    delay(0.01)

    vim_key('<Esc>')
    vim_key('w')

    cword = vim_expr('expand("<cWORD>")')

    if len(cword) < 2:
      delay(0.1)
      continue
    elif len(cword) > 7:
      delay(0.135)
    else:
      delay(0.05)

    vim_key('<Esc>')
    vim_key('e')

    if len(cword) > 7:
      delay(0.135)
    else:
      delay(0.05)

