from flask import Flask, render_template
from app.insights import allPostInsights, computeStat

app = Flask(__name__)

# print(allPostInsights())

@app.route('/')
def hello():
    return render_template('index.html', data=allPostInsights(), stat=computeStat())