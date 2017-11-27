# /*
#  * CIS2750 F2017
#  * Assignment 4
#  * Jackson Zavarella 0929350
#  * This file is a python wrapper for sql
#  * No code was used from previous classes/ sources
#  */

import mysql.connector

class sqlDriver(object):
    """docstring for sqlDriver."""
    def __init__(self, server, db, username, password):
        try:
            self.connection = mysql.connector.connect(host=server, database=db, user=username, password=password)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            raise err
        self.cursor = self.connection.cursor()
        self.initTables()

    def initTables(self):
        self.createOrganizerTable()
        self.createEventTable()

    def createOrganizerTable(self):
        try:
            self.execute("create table ORGANIZER (org_id INT AUTO_INCREMENT, name VARCHAR(60) NOT NULL, contact VARCHAR(60) NOT NULL, PRIMARY KEY(org_id))")
        except mysql.connector.Error as err:
           print("table ORGANIZER must already exist")

    def createEventTable(self):
        try:
            self.execute("create table EVENT (event_id INT AUTO_INCREMENT, summary VARCHAR(60) NOT NULL, start_time DATETIME NOT NULL, location VARCHAR(60), organizer INT, num_alarms INT, PRIMARY KEY(event_id), FOREIGN KEY(organizer) REFERENCES ORGANIZER(org_id) ON DELETE CASCADE)")
        except mysql.connector.Error as err:
           print("table EVENT must already exist")

    def getOrgId(self, name):
        self.cursor.execute("SELECT org_id FROM ORGANIZER WHERE name=\'" + str(name) + "\'")
        for r in self.cursor:
            return r[0]
        return None

    def insertOrganizer(self, name, contact):
        orgId = self.getOrgId(name)
        if orgId != None:
            return orgId
        self.cursor.execute("INSERT INTO ORGANIZER (name, contact) VALUES(%s, %s)", (name, contact))

        self.connection.commit()
        return self.getOrgId(name)

    def insertEvent(self, summary, startTime, location, numAlarms, organizer):
        orgId = None
        if organizer != None and organizer != '':
            temp = organizer.replace(";", ":")
            organizerDeats = temp.split(":")
            name = None
            contact = None
            contactFlag = 0
            for p in organizerDeats:
                if contactFlag == 1:
                    contact = p
                    contactFlag = 0
                    continue
                if p.startswith("CN="):
                    name = p[3:]
                    continue
                if p.upper() == "MAILTO":
                    contactFlag = 1
                    continue

            if name == None or contact == None:
                return "There was an issue with the name or contact option of the organizer"
            orgId = self.insertOrganizer(name, contact)


        if location == None or location == '':
            location = "NULL"

        self.cursor.execute("SELECT COUNT(*) FROM EVENT WHERE summary=%s AND start_time=%s", (summary, startTime))
        for r in self.cursor:
            if r[0] != 0:
                return "The event with the summary \'" + summary + "\' and start time \'" + str(startTime) + "\' already exists."
        self.cursor.execute("INSERT INTO EVENT (summary, organizer, start_time, location, num_alarms) VALUES(%s, %s, %s, %s, %s)", (summary, orgId, startTime, location, numAlarms))
        self.connection.commit()

        return "Successfully inserted the event with  the summary \'" + summary + "\' and start time \'" + str(startTime) + "\'."

    def tablesHaveRows(self):
        if self.execute("SELECT COUNT(*) FROM EVENT")[0] != 0 or self.execute("SELECT COUNT(*) FROM ORGANIZER")[0] != 0:
            return True
        return False

    def execute(self, q):
        self.cursor.execute(q)
        res = []
        for r in self.cursor:
            res.append(r)
        self.connection.commit()
        return res

    def destroy(self):
        self.cursor.close()
        self.connection.close()
