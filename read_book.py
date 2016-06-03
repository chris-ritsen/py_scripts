#!/usr/bin/python3

from getopt import getopt
from os import path, environ
from subprocess import call, check_output, check_call
from time import sleep

import argparse
import signal
import socket
import sys

import tmux
import vim

window_name = 'books'

def get_rate():
  return float(check_output(["redis-cli", "get", "reading_speed"]).decode())

def make_window():
  class_name = 'bigspaceurxvt'
  desktop = 2

  if socket.gethostname() == 'laptop':
    class_name = 'bigspacelaptop'

  if not tmux.is_attached():
    call(["wmctrl", "-s", str(desktop)])
    call(["urxvtc", "-name", class_name, "-e", "zsh", "-ic", "books"])
    call(["wmctrl", "-r", window_name, "-t", str(desktop)])

  call(["clear"])

  while not tmux.is_attached():
    sleep(0.1)

  call(["wmctrl", "-a", window_name])

def active_window():
  return check_output([
      "xdotool",
      "getactivewindow",
      "getwindowname"
  ]).decode().strip()

def delay(seconds):
  rate = get_rate()
  wait = seconds * rate
  sleep(wait)

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

  while tmux.is_attached():
    if idle() < 3 or active_window() != window_name:
      sleep(1)
      continue

    vim.key('<Esc>')
    vim.key('zz')

    delay(0.01)

    vim.key('<Esc>')
    vim.key('w')

    word_len = len(vim.expr('expand("<cWORD>")'))

    if word_len < 2:
      delay(0.1)
      continue
    elif word_len > 7:
      delay(0.135)
    else:
      delay(0.05)

    vim.key('<Esc>')
    vim.key('e')

    if word_len > 7:
      delay(0.135)
    else:
      delay(0.05)

