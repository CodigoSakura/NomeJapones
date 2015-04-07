# -*- coding: utf-8 -*-

# all the imports

from flask import Flask, request, render_template

import namae
import re


# configuration
DEBUG = False 


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_index():
    error = None
    if request.method == 'POST':
        if re.findall(' ', request.form['user_name']):
            error = 'Insira apenas um nome por vez'
        elif len(request.form['user_name']) > 10:
            error = 'Limite de caracteres excedido!'
        elif len(request.form['user_name']) == 0:
            error = 'Escreva um nome'
        else:
            name_given = request.form['user_name']
            name_sent = receive_user_name(name_given)
            return name_sent

    return render_template('index.html', error=error)


@app.route('/nome', methods=['GET', 'POST'])
def receive_user_name(seu_nome):
    got_user_name = seu_nome.lower()

    # call the conversion happening in the namae.py
    name_hiragana, name_katakana, name_kanji = namae.nipo_name(got_user_name)

    return render_template('nome.html', nome_latin=got_user_name.capitalize(), nome_hiragana=name_hiragana,
                           nome_katakana=name_katakana, nome_kanji=name_kanji)



@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


if __name__ == '__main__':
    app.run()
