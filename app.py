from flask import Flask, g, render_template, request
import sklearn as sk
import numpy as np
import os
import sqlite3

### stuff from last class
app = Flask(__name__)

# @app.route('/')
# def main():
#     return render_template('main_better.html')

@app.route('/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        get_message_db()
        msg, handle = insert_message(request)
        thank_note = "Thank you for your submission!"
        return render_template('submit.html', message=msg, 
                               handle=handle, thank_note=thank_note)


@app.route('/view/')
def view():
    messages = random_messages(5)
    print(messages)
    return render_template('view.html', messages=messages)

def get_message_db():
  # write some helpful comments here
  try:
      return g.message_db
  except:
      g.message_db = sqlite3.connect("messages_db.sqlite")
      cmd = '''
      CREATE TABLE IF NOT EXISTS messages(
      handle TEXT,
      message TEXT
      );
      '''
      cursor = g.message_db.cursor()
      cursor.execute(cmd)
      return g.message_db

def insert_message(request):
    message = request.form['message']
    handle = request.form['handle']
    db = get_message_db()
    cmd = "INSERT INTO messages (handle, message) VALUES (?, ?)"

    cursor = db.cursor()
    cursor.execute(cmd, (handle, message))
    db.commit()

    cursor.close()
    db.close()
    return message, handle

def random_messages(n):
    db = get_message_db()
    cursor = db.cursor()
    cmd = "SELECT * FROM messages ORDER BY RANDOM() LIMIT ?"
    cursor.execute(cmd, (n,))
    rand_msg = cursor.fetchall()
    cursor.close()
    return rand_msg

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
