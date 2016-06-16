#!/usr/bin/env python3

from time import sleep

import argparse
import signal
import socket
import subprocess
import sys

import tmux
import vim
import x

window_name = 'books'


def set_rate(rate):
    subprocess.check_output(["redis-cli", "set", "reading_speed", str(rate)])


def get_rate():
    output = subprocess.check_output(
      [
        "redis-cli",
        "get",
        "reading_speed"
      ]
    ).decode()

    return float(output)


def make_window():
    class_name = 'bigspaceurxvt'
    desktop = 2

    if socket.gethostname() == 'laptop':
        class_name = 'bigspacelaptop'

    if not tmux.attached():
        x.desktop(desktop)
        x.term("books", class_name)
        x.move(window_name, desktop)

    subprocess.call(["clear"])

    while not tmux.attached():
        sleep(0.1)

    x.activate(window_name)


def delay(seconds):
    wait = seconds * get_rate()
    sleep(wait)


def sig_handler(signal, frame):
    sys.exit(0)


def read_word():
    vim.key('<Esc>')
    vim.key('w')

    cword = vim.expr('expand("<cWORD>")')
    word_len = len(cword)

    if word_len < 2:
        delay(0.1)
        return

    if word_len > 7:
        delay(0.135)
    else:
        delay(0.05)

    vim.key('<Esc>')
    vim.key('e')

    if word_len > 7:
        delay(0.135)
    else:
        delay(0.05)


def read_book():
    if x.idle() < 3 or x.active_window() != window_name:
        sleep(1)
        return

    vim.center_display()
    read_word()


def main():
    make_window()

    while tmux.attached():
        read_book()


def parse_args():
    parser = argparse.ArgumentParser(
      description='Do stuff',
      prog='PROG',
      usage='%(prog)s [options]'
    )

    parser.add_argument('--speed', type=float, help='Rate to do stuff')

    args = parser.parse_args()

    if args.speed and args.speed > 0:
        rate = 1 / args.speed
        set_rate(rate)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sig_handler)
    parse_args()
    main()

