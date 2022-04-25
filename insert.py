# -*- coding: UTF-8 -*-
import subprocess
import time
import re
import json

with open('search-terms.json', 'r') as f:
  data = json.loads(f.read())



for i in data[0]:
  term = re.sub(r'[^\w]+', '', i)
  subprocess.run([
    '/Users/agustinbouillet/work/venv/server/bin/python', 
    '/Users/agustinbouillet/work/drae/drae.py',
    '-t',
    term
  ])
  print(i.lower())
  time.sleep(1)
