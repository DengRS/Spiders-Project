from flask import Flask, json, redirect, url_for
from core.database import RedisDataBase

app = Flask(__name__)

db = RedisDataBase()

@app.route('/')
def main():
    return redirect(url_for('core'))

@app.route('/core/')
def proxy():
    data = db.get_proxies
    if data is not None:
        return json.dumps(data)
    else:
        return json.dumps({})
