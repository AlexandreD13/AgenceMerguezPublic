import os

from flask import Flask, redirect

app = Flask(__name__)


def main():
    port = os.environ.get('PORT')
    app.run(port=port)


@app.route('/')
def home():
    return 'hello'


@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')


if __name__ == "__main__":
    main()
