import json
import requests
import os
import logging
from flask import Flask, render_template

logging.basicConfig(
    format='%(asctime)s %(msecs)d - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('werkzeug') 
handler = logging.FileHandler('access.log') 
logger.addHandler(handler)

app = Flask(__name__)
url = 'http://openlibrary.org/api/books?bibkeys=ISBN:ISBN_PlaceHolder&jscmd=details&format=json'
cover_url = 'https://covers.openlibrary.org/b/id/COVERID.jpg'

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/book/<ISBN>')
def get_book_info(ISBN):
    try:
        Updated_URL = url.replace('ISBN_PlaceHolder', ISBN)
        output = requests.get(Updated_URL).json()
        json_object = json.dumps(output, indent = 4)   
        return json_object
    except Exception as ex:
        return "### Can't find the book you searched for.." + str(ex) + " ###"

@app.route('/book_image/<ISBN>')
def get_book_image(ISBN):
    json_data = get_book_info(ISBN)
    try:
        py_json = json.loads(json_data)
        objectid = 'ISBN:' + ISBN
        cover_id = str(py_json[objectid]['details']['covers'])[1:-1]
        img_url = cover_url.replace('COVERID', cover_id)
        title = str(py_json[objectid]['details']['full_title'])
        return render_template('index.html',
                                ISBN = ISBN,
                                title = title,
                                book_image = img_url,
                                details = json_data)
    except Exception as ex:
        return "### Can't find the book you searched for.. ISBN:" + ISBN + " ###"


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)