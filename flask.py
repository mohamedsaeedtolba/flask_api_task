# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 22:29:27 2019

@author: Dell
"""

from task import main
from flask import request
import flask

app = flask.Flask(__name__)

@app.route("/", methods=["GET","POST"])

def search__():
    
    print(request.args)

    if(request.args):
        hotels_names = main(request.args['chat_in'])
        print(hotels_names)
        return flask.render_template('task.html',
                                     chat_in=hotels_names,
                                     )
    else: 
        #For first load, request.args will be an empty ImmutableDict
        # type. If this is the case we need to pass an empty string
        # into make_prediction function so no errors are thrown.

        hotels_names = main('')
        return flask.render_template('task.html',
                                     chat_in=hotels_names,
                                     )
if __name__=="__main__":
    app.run()