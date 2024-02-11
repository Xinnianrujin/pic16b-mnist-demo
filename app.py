# import necessary libraries, including Flask, g, render_template, request, os, and sqlite3
from flask import Flask, g, render_template, request
import os
import sqlite3

# create a Flask app
app = Flask(__name__)

# define the route for the home page, here is the submit page
@app.route('/', methods=['POST', 'GET'])

# define the function that "renders_template" for the submit page
def submit():
    # if the request method is GET, render the submit page
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        # if the request method is POST, first access the message database
        get_message_db()
        msg, handle = insert_message(request)
        # add a thank you note
        thank_note = "Thank you for your submission!"
        # render the submit page with the message, handle, and thank you note
        return render_template('submit.html', message=msg, 
                               handle=handle, thank_note=thank_note)

# define the route for the view page
@app.route('/view/')
# define the function that "renders_template" for the view page
def view():
    # access the message database and get 5 random messages
    messages = random_messages(5)
    # render the view page with the 5 random messages
    return render_template('view.html', messages=messages)

# define the function that creates the database for messages
def get_message_db():
  # if the database exists, return the db
  try:
      return g.message_db
    # if not, create the db
  except:
      # use sqlite3 to create the database
      g.message_db = sqlite3.connect("messages_db.sqlite")
      # The SQL command creates a table called messages
      # with two columns: handle and message
      cmd = '''
      CREATE TABLE IF NOT EXISTS messages(
      handle TEXT,
      message TEXT
      );
      '''
      # use a cursor to execute the command
      cursor = g.message_db.cursor()
      cursor.execute(cmd)
      # return the database
      return g.message_db

def insert_message(request):
    # Extract the message and the handle from request
    message = request.form['message']
    handle = request.form['handle']
    # Access the message database
    db = get_message_db()
    # Use SQL to insert the message and handle into the database
    cmd = "INSERT INTO messages (handle, message) VALUES (?, ?)"
    # Use a cursor to execute the command
    cursor = db.cursor()
    cursor.execute(cmd, (handle, message))
    db.commit()
    # close cursor and db, then return the message and handle
    cursor.close()
    db.close()
    return message, handle

def random_messages(n):
    # Access the message database and create a cursor
    db = get_message_db()
    cursor = db.cursor()
    # Use SQL to select n random messages from the database
    cmd = "SELECT * FROM messages ORDER BY RANDOM() LIMIT ?"
    # Use a cursor to execute the command, fetch messages
    cursor.execute(cmd, (n,))
    rand_msg = cursor.fetchall()
    # close cursor and db, then return the random messages
    cursor.close()
    db.close()
    return rand_msg

if __name__ == "__main__":
    # run the app
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
