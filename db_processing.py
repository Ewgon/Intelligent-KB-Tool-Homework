import sqlite3 as sql

#Const :
based_pk = 0.5
min_pk = 0.2

#Database : Insert a name into the database
def insertNameIntoDb(name):
    status = {"status": "No connection to db"}
    try :
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO data VALUES('{named}', '{pk}')".format(named = name, pk = based_pk))
            con.commit()
            status = {"status": "Ok"}
    except :
        con.rollback()

    finally :
        return status

#Database : Get the list of possibles names from given characters into the database
def getNamesFromCharsIntoDb(chars):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM data WHERE name LIKE '%{pchars}%'".format(pchars = chars))
        result = cur.fetchall()
        smoothResults = []
        for named in result:
            smoothResults.append(named[0])
    return smoothResults

#Database : Update the database
def updateDatabase(selected, selection):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM data WHERE name = '{selected}'".format(selected = selected))
        result = cur.fetchall()

        if len(result) != 0 :
            selection.remove(selected)
            pk_increased = increasePk(result[0][1], based_pk)
            cur.execute("UPDATE data SET pk = '{updatedPk}' WHERE name = '{selected}'".format(updatedPk = pk_increased, selected = selected))
        else :
            insertNameIntoDb(selected)

        for name in selection:
            cur.execute("SELECT * FROM data WHERE name = '{named}'".format(named = name))
            result = cur.fetchall()
            pk_decreased = decreasePk(result[0][1], based_pk)
            cur.execute("UPDATE data SET pk = '{updatedPk}' WHERE name = '{named}'".format(updatedPk = pk_decreased, named = name))

        cur.execute("DELETE FROM data WHERE pk < {min_pk}".format(min_pk = min_pk))
        con.commit()

#Database : Get the entire table from the database
def getFullTable():
    with sql.connect("database.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM data")
        result = cur.fetchall()
        smoothResults = []
        for row in result:
            smoothResults.append([row[0], row[1]])
    return smoothResults

#Func : Increase the Pk
def increasePk(pk_previous, pk_new):
    return pk_previous + (1-pk_previous) * pk_new

#Func : Decrease the Pk
def decreasePk(pk_previous, pk_new):
    return pk_previous - (1-pk_previous) * pk_new