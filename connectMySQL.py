import mysql.connector

# TODO change the user and password to be for your mysql account. The database
# menagerie should already exist. It contains the pet table from the on-line tutorial.
# You cannot proceed with this assignment until this program runs without error.

cnx = mysql.connector.connect(user='project', password='project', host='localhost',database='menagerie')
cnx.close()