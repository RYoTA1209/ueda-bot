from flask import Flask
import os

port = os.environ['PORT']

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=port)
