import sqlite3
from datetime import datetime

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
import logging
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`
TIMEFORMAT = "%d/%m/%Y, %H:%m:%S"
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error("%s, A non-existing article is accessed artical id %d and a 404 page is returned."%(str(datetime.now().strftime(TIMEFORMAT)), post_id))
      return render_template('404.html'), 404
    else:
      app.logger.info("%s, Article \"%s\" retrieved!"%(str(datetime.now().strftime(TIMEFORMAT)), post['title']))
      return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    app.logger.info( "%s, \"About Us\" page is retrieved."%str(str(datetime.now().strftime(TIMEFORMAT))))
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            app.logger.error("%s, Title requiered in order to post an article"%str(datetime.now().strftime(TIMEFORMAT)))
            flash('Title is required!')
        else:
            app.logger.info("%s, A new article is created \"%s\" "%(str(datetime.now().strftime(TIMEFORMAT)), title))
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def health():
    response = app.response_class(
            response = json.dumps({"result": "OK - its healthy"}),
            status = 200,
             mimetype = 'application/json'
             )
    return response

@app.route('/metrics')
def metrics():
    logging.info("metrics request success")
    connection = get_db_connection()
    post_count = connection.execute('SELECT count(1) as count FROM posts').fetchone()
    connection.close()
    response = app.response_class(
            response = json.dumps({"db_connection_count": 4, "post_count":
                post_count['count']}),
            status = 200,
            mimetype = 'application/json'
            )
    return response

# start the application on port 3111
if __name__ == "__main__":
   logging.root.handlers = []
   logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO, filename='app.log')

   # set up logging to console
   console = logging.StreamHandler()
   console.setLevel(logging.DEBUG)
   # set a format which is simpler for console use
   formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
   console.setFormatter(formatter)
   logging.getLogger("").addHandler(console)
   app.run(host='0.0.0.0', port='3111', debug = True)
