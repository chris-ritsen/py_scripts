
from subprocess import call, check_output

def _get_mouse_id():
  match = 's/^.*=([0-9]+).*$/\\1/g'
  grep = "grep -E '[0-9]+'"
  sed = "sed -E '" + match + "'"
  cmd1 = "xinput | grep Mouse | " + sed + " | " + grep
  mouse_id = check_output(cmd1, shell=True).decode().strip()
  # TODO: What if there is more than one mouse attached?
  return int(mouse_id)

def off():
  try:
    _device = _get_mouse_id()
    call(["xinput", "disable", str(_device)])
  except:
    pass

  call(["xdotool", "mousemove", "0", "0"])

def on():
  try:
    _device = _get_mouse_id()
    call(["xinput", "enable", str(_device)])
  except:
    pass


