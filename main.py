from flask import flask
app = flask(_name_)

@app.route('/')
def hello_world():
    return "<h2>Hello, World! From KM: 172.16.14.35</h2>"

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=3000, debug=True)