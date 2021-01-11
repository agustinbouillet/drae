# -*- coding: UTF-8 -*-
import json
import sqlite3
from argparse import ArgumentParser

import lxml
import requests as r
from bs4 import BeautifulSoup


def select(term=None):
  try:
    with sqlite3.connect("rae.db") as connection:
      connection.text_factory = str
      cursor = connection.cursor()
      row = cursor.execute(
          f"SELECT * FROM results where term='{term.lower()}'"
      ).fetchone()

      return row
  except Exception as e:
    return None


def insert(term=None, definition=None, definition_plain=None):
  with sqlite3.connect("rae.db") as connection:
    connection.text_factory = str
    cursor = connection.cursor()

    try:
      cursor.execute(
        '''
        CREATE TABLE "results" (
          "term"  TEXT NOT NULL UNIQUE,
          "definition"  TEXT NOT NULL,
          "definition_plain"  TEXT NOT NULL
        )
        '''
      )
    except Exception as e:
      pass

    cursor.execute(
        '''
        INSERT INTO results (term, definition, definition_plain)
        VALUES ('{term}','{definition}','{definition_plain}')
        '''.format(
            term=term.lower(),
            definition=definition.replace("'", "''"),
            definition_plain=definition_plain.replace("'", "''")
        )
    )


def search(term, format='text'):
  try:
    row = select(term)
    if row:
      if format=='html':
        return row[1]
      else:
        return row[2]

    else:
      url         = f'https://dle.rae.es/{term}'
      search_term = r.get(url)
      soup        = BeautifulSoup(search_term.text, features="lxml")
      get_result  = soup.find(id='resultados').find('article')

      if get_result:
        print('¡Nuevo término!\n')
        insert(term, str(get_result), get_result.text)

      if format=='html':
        return str(get_result)
      else:
        return get_result.text

  except Exception as e:
    return 'Sin resultados'




if __name__ == '__main__':

  parser = ArgumentParser(
      description=('Retorna búsquedas del diccionario de la '
                   'Real Academia Española')
  )
  parser.add_argument(
      '-f',
      '--format',
      type=str,
      help=('Format de retorno: text, html')
  )
  parser.add_argument(
      '-t',
      '--term',
      type=str,
      help='Término a buscar'
  )

  args = parser.parse_args()
  print(search(args.term, args.format))
