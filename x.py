
from os import environ
from subprocess import call, check_output


def desktop(n):
    call([
      "wmctrl",
      "-s",
      str(n)
    ])


def move(window, desktop_id):
    call([
      "wmctrl",
      "-r",
      window,
      "-t",
      str(desktop_id)
    ])


def idle():
    idle_ms = int(check_output(["xprintidle"]))
    return idle_ms / 1000


def activate(window):
    call([
      "wmctrl",
      "-a",
      window
    ])


def active_window():
    return check_output([
        "xdotool",
        "getactivewindow",
        "getwindowname"
    ]).decode().strip()


def term(command, class_name):
    if isinstance(command, str):
        command = command.split(" ")

    shell = environ["SHELL"]

    shell_cmd = [
      shell,
      "-ic"
    ] + command

    urxvt_cmd = [
      "urxvtc",
      "-name",
      class_name,
      "-e"
    ]

    command = urxvt_cmd + shell_cmd

    call(command)

