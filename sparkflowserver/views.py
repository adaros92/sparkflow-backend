from flask import url_for, render_template

from sparkflowserver import app


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
