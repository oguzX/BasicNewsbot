from mysql.connector import connection

import error


class database:
    dbhost = "localhost"
    dbname = "news"
    dbusername = "root"
    dbpass = ""
    dbport = 33066

    def __init__(self):
        self.dbconn = connection.MySQLConnection(host=self.dbhost, user=self.dbusername, password=self.dbpass,
                                                 database=self.dbname,port=self.dbport)
        self.dbcursor = self.dbconn.cursor(buffered=True)
        self.startUp()

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

    def startUp(self):
        localQuery = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '"+self.dbname+"'"
        ret = self.query(localQuery)
        if(not ret):
            error.show("\""+self.dbname+"\" Database not exist, please try again after create one")

    # def checkTable(self,tname):
    #     checkQuery = "SELECT * FROM information_schema.tables WHERE table_schema = '"+self.dbname+"' AND table_name = '"+tname+"' LIMIT 1;"
    #     ret = self.query(checkQuery)
    #     if(not ret):
    #         userRes = input(tname+" table not exist, Add? yes [y] no [n] ")
    #         while(userRes != 'n' or userRes != 'y'):
    #             if (userRes.lower() == 'y'):
    #                 createTableQuery = "CREATE TABLE "+tname+" "
    #             elif (userRes.lower() == 'n'):
    #                 break;

    def __del__(self):
        self.dbconn.close()
