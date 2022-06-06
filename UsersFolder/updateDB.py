import sqlite3
from contextlib import closing

connection = sqlite3.connect("users.db")
###Check connection
# print(connection.total_changes)

###Create cursor
cursor = connection.cursor()
###Create table
# cursor.execute("CREATE TABLE users (name TEXT, score INTEGER)")

### Create new user:
# cursor.execute("INSERT INTO users VALUES ('master', 1000000)")
# cursor.execute("INSERT INTO users VALUES ('test', 7)")

# allUsers = cursor.execute("SELECT name, score FROM users").fetchall()
# print(allUsers)

###Target specific user
# target_user = "master"
# rows = cursor.execute(
#     "SELECT name, score FROM users WHERE name = ?",
#     (target_user,),
# ).fetchall()
# print(rows)

###Update user score
# new_score = 5
# user = "test"
# cursor.execute("UPDATE users SET score = ? WHERE name = ?", (new_score, user))
# rows = cursor.execute("SELECT name, score FROM users").fetchall()
# print(rows)

###Delete user
# delete_user = "master"
# cursor.execute("DELETE FROM users WHERE name = ?", (delete_user,))
# rows = cursor.execute("SELECT name, score FROM users").fetchall()
# print(rows)

connection.commit()

with closing(sqlite3.connect("users.db")) as connection:
    with closing(connection.cursor()) as cursor:
        rows = cursor.execute("SELECT 1").fetchall()
        print(rows)
