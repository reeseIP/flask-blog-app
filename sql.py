import sqlite3

# connect with DB
with sqlite3.connect('blog.db') as conn:

    # create cursor to communicate with DB
    cursor = conn.cursor()
    
    # create table to hold blog content
    cursor.execute('CREATE TABLE IF NOT EXISTS posts(title TEXT, content TEXT)')
    
    # mock posts
    posts = [("Good", "I'm Good"),
             ("Okay", "I'm Okay"),
             ("Well", "I'm Well"),
             ("Excellent", "I'm Excellent")]
             
    # insert posts into table
    cursor.executemany('INSERT INTO posts VALUES(?,?)', (posts))
    
    
    
    
    