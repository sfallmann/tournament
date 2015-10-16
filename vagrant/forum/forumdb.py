#
# Database access functions for the web forum.
#

import time
import psycopg2

## Database connection
conn = psycopg2.connect("dbname=forum")
cur = conn.cursor()

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    cur.execute('Select * from posts order by time ASC')
    posts = ({'content': str(row[1]), 'time': str(row[0])}
             for row in cur.fetchall())


    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    t = time.strftime('%c', time.localtime())
    cur.execute('Insert into posts (content, time) VALUES (%s, %s)', (content, t))
    conn.commit()

