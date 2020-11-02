import os
import sys

#from flask import Flask, Response
from flask import request

cwd = os.getcwd()
sys.path.append(cwd)

#print("*** PYHTHONPATH = " + str(sys.path) + "***")

import json
import logging
import pymysql
from datetime import datetime
from flask import Flask, render_template, Response

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

application = Flask(__name__)
conn = pymysql.connect("url", user="", port=, passwd="",db="")
c = conn.cursor()

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
    sql = "SELECT author, quote FROM quotes ORDER BY RAND() LIMIT 1"
    result = c.execute(sql)
    ans = c.fetchall()
    dict = {"author": ans[0][0], "quote": ans[0][1]}
    rsp = Response(json.dumps(dict), status=200, content_type="application/json")
    return rsp

# Run the app.
if __name__ == "__main__":
    application.run(port=8000)
