from flask import Flask
from controller.main import blue

app = Flask(__name__)
app.register_blueprint(blue)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
