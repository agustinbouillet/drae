# -*- coding: UTF-8 -*-
import json
import os
import sqlite3
from argparse import ArgumentParser

import cloudscraper
import lxml
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILENAME = 'rae.db'

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


def select(term=None):
  try:
    with sqlite3.connect(os.path.join(BASE_DIR, DB_FILENAME)) as connection:
      connection.text_factory = str
      cursor = connection.cursor()
      row = cursor.execute(
          f"SELECT * FROM results where term='{term.lower()}'"
      ).fetchone()

      return row
  except Exception as e:
    return None


def insert(term=None, definition=None, definition_plain=None):
  with sqlite3.connect(os.path.join(BASE_DIR, DB_FILENAME)) as connection:
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
      url = f'https://dle.rae.es/{term}'
      scraper = cloudscraper.create_scraper()
      data = scraper.get(url).text
      soup = BeautifulSoup(data, features="lxml")
      get_result = soup.find(id='resultados').find('article')


      if get_result:
        print(f'{bcolors.OKGREEN}[¡Nuevo término! {term}]{bcolors.ENDC}')
        insert(term, str(get_result), get_result.text.strip())

      if format=='html':
        return str(get_result)
      else:
        return get_result.text.strip()

  except Exception as e:
    with open("noresults.txt", 'a') as f:
      f.write(f'{term}\n')
    return print(f'{bcolors.WARNING}[Sin resultados para {term}]{bcolors.ENDC}')




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
