import logging
import sqlite3
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

count_db_connection = 0


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global count_db_connection
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    count_db_connection += 1
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
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
        return render_template('404.html'), 404
    else:
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')


# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')


# Define /metrics endpoint
@app.route("/metrics")
def metrics():
    metrics_response = {"db_connection_count": count_db_conn(), "post_count": count_post()}
    response = app.response_class(json.dumps(metrics_response), status=200, mimetype="application/json")

    return response


# Define /healthz endpoint
@app.route("/healthz")
def health():
    count_post_query = """
    SELECT COUNT(*) FROM posts;
    """
    healthy_response = {"result": "OK - healthy"}
    unhealthy_response = {"result": "ERROR - unhealthy"}
    # try:
    db_conn = get_db_connection()
    db_conn.execute(count_post_query).fetchone()
    response = app.response_class(json.dumps(healthy_response), status=200, mimetypes="application/json")
    db_conn.close()
    # except sqlite3.OperationalError:
    #     response = app.response_class(json.dumps(unhealthy_response), status=500, mimetype="application/json")
    #
    return response


# Count number of posts table
def count_post():
    no_posts = """
    SELECT COUNT(*) FROM posts;
    """
    conn = get_db_connection()
    cur = conn.cursor()
    result = cur.execute(no_posts).fetchone()[0]
    conn.close()

    return result


# Count database connections
def count_db_conn():
    return count_db_connection


# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s:%(filename)s:%(asctime)s',
                        datefmt='%d/%m/%Y, %H:%M:%S')
    app.run(host='0.0.0.0', port='3111')
