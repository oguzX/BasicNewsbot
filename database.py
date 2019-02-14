from mysql.connector import connection


class database:
    dbhost = "localhost"
    dbname = "news"
    dbusername = "root"
    dbpass = ""

    def __init__(self):
        self.dbconn = connection.MySQLConnection(host=self.dbhost, user=self.dbusername, password=self.dbpass,
                                                 database=self.dbname)
        self.dbcursor = self.dbconn.cursor(buffered=True)

    def query(self, query):
        type = (query.split())[0].lower()
        self.dbcursor.execute(query)
        self.dbconn.commit()
        if type == "select":
            return self.dbcursor.fetchone()

    def insert(self, tablename, var, notexist=[]):
        sqlcommand = "INSERT INTO " + tablename + " "
        column = ""
        values = ""
        varlength = len(var)
        for n in range(varlength):
            column += var[n][0]
            values += '\'' + var[n][1] + '\''
            if n + 1 < varlength:
                column += ","
                values += ","
        sqlcommand += "(" + column + ")"
        if len(notexist) > 0:
            sqlcommand += " SELECT * FROM "
            sqlcommand += "( SELECT " + values + ") AS tmp WHERE NOT EXISTS (SELECT "
            sqlcommand += ",".join(x[0] for x in notexist)
            sqlcommand += " FROM " + tablename + " WHERE "
            nexistlen = len(notexist)
            for n in range(nexistlen):
                notexist[n][1] = "'" + notexist[n][1] + "'"
                sqlcommand += "=".join(notexist[n])
                if n + 1 > nexistlen:
                    sqlcommand += " and "
            sqlcommand += ") LIMIT 1"
        else:
            sqlcommand += "( " + column + ") "
            sqlcommand += "VALUES (" + values + ")"
        self.query(sqlcommand)

    def getnum(self,table_name):
        sqlcommand = "SELECT count(*) FROM "+table_name
        return self.query(sqlcommand)

    def __del__(self):
        self.dbconn.close()
