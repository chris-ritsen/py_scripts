
from subprocess import call, check_output

servername = 'BOOKS'

def key(key):
  call(["vim", "--servername", servername, "--remote-send", key])

def expr(expr):
  return check_output([
      "vim",
      "--servername",
      servername,
      "--remote-expr",
      expr
  ]).decode()

