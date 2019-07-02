from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index_html():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard_html():
    return render_template('dashboard.html', name="New Team Name", password="32143")


if __name__ == '__main__':
    app.run()
