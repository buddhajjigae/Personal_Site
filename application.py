import json
import os
import sys
# import platform
# import socket

#from flask import Flask, Response
from flask import request

cwd = os.getcwd()
sys.path.append(cwd)

#print("*** PYHTHONPATH = " + str(sys.path) + "***")

import json
import logging
from datetime import datetime
from flask import Flask, render_template, Response, url_for
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pw@url/dbname'
db = SQLAlchemy(application)
#ma = Marshmallow(application)


# 1. Extract the input information from the requests object.
# 2. Log the information
# 3. Return extracted information.
def log_and_extract_input(method, path_params=None):

    path = request.path
    args = dict(request.args)
    data = None
    headers = dict(request.headers)
    method = request.method

    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        data = "You sent something but I could not get JSON out of it."

    log_message = str(datetime.now()) + ": Method " + method

    inputs =  {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data
        }

    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)

    return inputs


def log_response(method, status, data, txt):

    msg = {
        "method": method,
        "status": status,
        "txt": txt,
        "data": data
    }

    logger.debug(str(datetime.now()) + ": \n" + json.dumps(msg, indent=2, default=str))

@application.route("/")
def index():
    return render_template('index.html')

@application.route("/quote", methods=["GET"])
def getQuote():
    #sql = "select author from quotes"
    sql = "SELECT author, quote FROM quotes ORDER BY RAND() LIMIT 1"
    ranQuote = []
    result = db.engine.execute(sql)
    #author = [row for row in result]
    #quote = [row for row in result]

    x = '{ "author":"John", "quote":"New York"}'
    for row in result:
        ranQuote.append(row)
    #rsp = Response("Hello World", status=200, content_type="text/plain")
    #print(author)
    #print(quote)
    #rsp = Response(ranQuote[0], status=200, content_type="text/plain")
    rsp = Response( json.dumps(x) , status=200, content_type="application/json")
    return rsp

getQuote()


# Run the app.
if __name__ == "__main__":
    db.init_app(application)
    application.run(port=8000)
