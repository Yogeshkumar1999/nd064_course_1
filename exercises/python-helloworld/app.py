from flask import Flask, json
import datetime
import logging
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/status")
def health_check():

    response = app.response_class(
                response = json.dumps({"result": "OK - its healthy"}),
                status = 200,
                mimetype = 'application/json'
            )
    app.logger.info('status request success')
    return response 

@app.route("/metrics")
def metrics():
    response = app.response_class(
                response = json.dumps({'data': {'UserCount': 140,
                    'UserCountActive': 23}}),
                status = 200,
                mimetype = 'application/json'
            )
    app.logger.info('metrics request success')
    return response 

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    app.run(host='0.0.0.0', port=8080)
