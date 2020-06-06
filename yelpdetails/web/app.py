from flask import Flask,request,render_template,redirect
import requests
from os import listdir

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('home.html')
@app.route('/', methods=['POST'])
def my_form_post():
    find = request.form['input1']
    near = request.form['input2']
    if request.method == 'POST':
       with open('option.txt', 'w') as f:
            f.write(str(find))
       with open('location.txt', 'w') as f:
           f.write(str(near))
    # return render_template('home.html', find=find,near=near)
    return redirect('http://127.0.0.1:5000/')



@app.route('/show')
def index():
    resp = requests.get(
        url = 'http://127.0.0.1:9080/crawl.json?start_requests=true&spider_name=yelpspider'
    ).json()
    items = resp.get('items')
    return render_template('index.html',details=items)
    # return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)