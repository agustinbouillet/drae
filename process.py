# -*- coding: UTF-8 -*-
import os
import sqlite3
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILENAME = 'rae.db'

def chunks(lst, n):
  for i in range(0, len(lst), n):
    yield lst[i:i + n]


def noresults():
  with open(os.path.join(BASE_DIR, 'noresults.txt'), 'r') as f:
    return f.readlines()


def terms():
  try:
    with sqlite3.connect(os.path.join(BASE_DIR, DB_FILENAME)) as connection:
      connection.text_factory = str
      cursor = connection.cursor()
      row = cursor.execute(
        'SELECT term FROM results;'
      ).fetchall()

      return row
  except Exception as e:
    return None



def select():
  try:
    with sqlite3.connect(os.path.join(BASE_DIR, DB_FILENAME)) as connection:
      connection.text_factory = str
      cursor = connection.cursor()
      row = cursor.execute(
        'SELECT definition_plain FROM results;'
      ).fetchall()

      return row
  except Exception as e:
    return list()



db_terms = [i[0] for i in terms()]
no_results = [ re.sub(r'\n', '', i.lower()) for i in noresults()]





words = []
for i in select():
  words += re.sub(r'([\d]*|[^\w\s]*)', '', str(i[0]).lower()).split()
  
unique_words = list(set(words))



filter = set(db_terms + no_results)

new_unique_words = [word for word in list(unique_words) if word not in filter]

lj = 30
rj = 8
print('-' * (lj + rj + 1))

def visual(desc, value):
  print(desc.ljust(lj, ' '), f'{value}'.rjust(rj,' '))
  
visual('Términos en DB', len(db_terms))
visual('Términos no encontrados', len(no_results))
visual('Todos los términos únicos', len(unique_words))
visual('Filtro', len(filter))
visual('Términos únicos', len(new_unique_words))
print('-' * (lj + rj + 1))


with open(os.path.join(BASE_DIR, 'search-terms.json'), 'w') as f:
  f.write(json.dumps(list(chunks(unique_words, 5000))))