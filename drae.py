import requests as r
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import lxml

def search(term, format='text'):
  try:
    url = f'https://dle.rae.es/{term}'
    search_term = r.get(url)
    soup = BeautifulSoup(search_term.text, features="lxml")
    get_result = soup.find(id='resultados').find('article')


    if format=='html':
      return get_result
    else:
      return get_result.text

  except:
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
