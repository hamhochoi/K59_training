from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def a():
	return render_template("realtime_diag.html")

app.run(host='0.0.0.0')