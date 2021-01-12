# -*- coding: UTF-8 -*-
import json

from drae import search
from flask import Flask, Markup, jsonify, render_template, url_for

app = Flask(__name__)

@app.route('/rae/<string:term>')
def example(term):
  return jsonify({'data':search(term, 'html')})


@app.route('/')
@app.route('/<string:name>')
def index(name=None):
  return render_template('index.html',name='buscar')



if __name__ == '__main__':
    app.run()
