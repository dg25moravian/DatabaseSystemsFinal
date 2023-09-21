# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import mysql.connector

# function creates the connection to mysql and returns the connection variable cnx
# and the cursor variable used access the database.
def connectToMySQL():
    cnx = mysql.connector.connect(password = 'project', user='project')
    cursor = cnx.cursor()
    return cursor, cnx


def createDatabase(cursor, DB_NAME):
    '''
    :param cursor: instance of the connection to the database
    :param DB_NAME: name of the database to create
    Creates the database at cursor with the given name.
    '''
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)



def makeTable(cursor):

    sql = "CREATE TABLE bases(baseID int PRIMARY KEY AUTO_INCREMENT, component varchar(255), site varchar(255), joint_base varchar(255), state varchar(255), status varchar(16), perimeter DECIMAL(19 , 8), area DECIMAL(19 , 8));"
    cursor.execute(sql)
    sql = "CREATE TABLE branches(branch varchar(255) PRIMARY KEY, manpower int, totalFunds DECIMAL(19,4));"
    cursor.execute(sql)
    sql = "CREATE TABLE ComponentToBranch (component varchar(255), branch varchar(255));"
    cursor.execute(sql)

    print("tables created")

def insertData(cursor):
    file1 = csv.reader(open('final.csv'))
    header = next(file1)
    for row in file1:
        cursor.execute("INSERT INTO bases (component, site, joint_base, state, status, perimeter, area) VALUES (%s, %s, %s, %s, %s, %s, %s)", row)


    infile = open("branches.txt", "r")
    for line in infile:
        sql = ""
        line = line.strip()
        record = line.split(",")
        data = "'"
        data = "'" + record[0] + "', "
        data += "'" + record[1] + "', "
        data += "'" + record[2]  + "'"
        sql = "INSERT INTO branches VALUES (" + data + ");"
        cursor.execute(sql)
    infile.close()

    infile = open("compToBranch.txt", "r")
    for line in infile:
        sql = ""
        line = line.strip()
        record = line.split(",")
        data = "'"
        data = "'" + record[0] + "', "
        data += "'" + record[1] + "'"
        sql = "INSERT INTO ComponentToBranch VALUES (" + data + ");"
        cursor.execute(sql)
    infile.close()

def question1(cursor, outfile):
    print("List all bases in Hawaii alongside which branch operates them", file=outfile)
    sql = "SELECT bases.site, bases.state, ComponentToBranch.branch  FROM bases INNER JOIN ComponentToBranch ON bases.component = ComponentToBranch.component WHERE bases.state = 'Hawaii';"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1], result[2], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question2(cursor, outfile):
    print("List the branches of military with active bases in California", file=outfile)
    sql = "SELECT DISTINCT ComponentToBranch.branch  FROM bases INNER JOIN ComponentToBranch ON bases.component = ComponentToBranch.component WHERE bases.state = 'California';"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question3(cursor, outfile):
    print("Show the ten largest military bases by area", file = outfile)
    sql = "SELECT site, area FROM bases ORDER BY area DESC LIMIT 10;"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question4(cursor, outfile):
    print("Show the ten largest bases by perimeter run by the airforce", file = outfile)
    sql = "SELECT bases.site, bases.state, bases.perimeter  FROM bases INNER JOIN ComponentToBranch ON bases.component = ComponentToBranch.component WHERE bases.component = 'AF Active' OR bases.component = 'AF Reserve' OR bases.component = 'AF Guard' ORDER BY perimeter DESC LIMIT 10;"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1],result[2], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question5(cursor, outfile):
    print("Show all joint bases", file = outfile)
    sql = "SELECT site, joint_base FROM bases WHERE NOT joint_base = 'N/A';"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question6(cursor, outfile):
    print("List all branches in order of how many military bases they operate", file= outfile)
    sql = "SELECT ComponentToBranch.branch, COUNT(branch)  FROM bases INNER JOIN ComponentToBranch ON bases.component = ComponentToBranch.component GROUP BY branch ORDER BY COUNT(branch) DESC;"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question7(cursor, outfile):
    print("List all States in order of how many military bases they contain", file=outfile)
    sql = "SELECT state, COUNT(state) FROM bases GROUP BY state ORDER BY COUNT(state) DESC; "
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question8(cursor,outfile):
    print("List the branches in order of how much funding they receive", file = outfile)
    sql = "SELECT branch, totalFunds FROM branches ORDER BY totalFunds DESC;"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question9(cursor, outfile):
    print("Show all inactive bases and who used to operate them", file=outfile)
    sql = "SELECT site, branch FROM bases INNER JOIN ComponentToBranch ON bases.component = ComponentToBranch.component WHERE bases.status = 'Inactive';"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def question10(cursor, outfile):
    print("Show all branches with more then 200,000 manpower", file=outfile)
    sql = "SELECT branch, manpower FROM branches WHERE manpower > 200000;"
    print(sql, file=outfile)
    cursor.execute(sql)
    result = cursor.fetchone()
    while result is not None:
        print(result[0], result[1], sep=",", file=outfile)
        result = cursor.fetchone()
    print(file=outfile)

def main():
    DB_NAME = 'militaryBases'
    cursor, connection = connectToMySQL()
    ##createDatabase(cursor, DB_NAME)
    cursor.execute("USE {}".format(DB_NAME))
    ##makeTable(cursor)
    ##insertData(cursor)
    outfile = open("results.txt", "w")
    question1(cursor, outfile)
    question2(cursor, outfile)
    question3(cursor, outfile)
    question4(cursor, outfile)
    question5(cursor, outfile)
    question6(cursor, outfile)
    question7(cursor, outfile)
    question8(cursor, outfile)
    question9(cursor, outfile)
    question10(cursor, outfile)





    connection.commit()
    cursor.close()
    connection.close()


main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
