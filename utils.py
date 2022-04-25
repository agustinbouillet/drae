import random
import re
import socket
import string
import urllib.request


#https://www.ipify.org
#https://api.ipify.org
def external_ip():
  return urllib.request.urlopen('https://ident.me').read().decode('utf8')


def network_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
      # doesn't even have to be reachable
      s.connect(('10.255.255.255', 1))
      ip = s.getsockname()[0]
  except Exception:
      ip = '127.0.0.1'
  finally:
      s.close()
  return ip


def local_ip():
  hostname = socket.gethostname()
  return socket.gethostbyname(hostname)


def random_chars(size=8, chars=[string.ascii_letters,
                 string.punctuation, string.digits,]):
  """Generador de claves aleatorias.

  Genera claves aleatorias y valida que la clave tenga al menos uno de
  los objetos enviados por argumento `chars`.

  Keyword Arguments:
    size {number} -- Largo de la cadena (default: {8})
    chars {list} -- listado de objetos que deben armar la cadena
        (default: {[string.ascii_letters, string.punctuation,
        string.digits,]})
  """
  # Base para armar el grupo de validación por elemento del listado
  # chars.
  rgx_module = '(?=.*[{}])'
  rgx = ''

  for i in chars:
    rgx += rgx_module.format(i)

  regex = re.compile('^%s(?=.{%s,})' % (rgx, size))

  while True:
    # excluyo caracteres que puedan generar confusión o problemas
    # en la validación.
    chars_blacklisted = re.compile(r'(\||\>|\<|\'|\"|\`|\\|\/|\(|\)|\[|\]|\}|\{|\$)')
    chars_joined = ''.join(chars)
    chars_filtered = re.sub(chars_blacklisted, "", chars_joined)

    password = ''.join(random.choice(chars_filtered) for i in range(size))

    if re.search(regex, password):
      return password
      break
    else:
      continue
