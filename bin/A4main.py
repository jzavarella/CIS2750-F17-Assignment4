# /*
#  * CIS2750 F2017
#  * Assignment 4
#  * Jackson Zavarella 0929350
#  * This file is the entry point for the application
#  * No code was used from previous classes/ sources
#  */

import calGUI
import sys
import getpass
from sql import sqlDriver
import mysql.connector

def main():
    args = sys.argv
    app = None
    if len(args) > 1 and args[1] != None:
        attempts = 3
        while attempts > 0:
            password = getpass.getpass("Enter password for " + args[1] + ": ")
            database = input("Enter a database to access: ")
            try:
                sql = sqlDriver.sqlDriver("dursley.socs.uoguelph.ca", database, args[1], password)
                app = calGUI.App("iCalGUI", sql)
                break
            except mysql.connector.Error as err:
                attempts = attempts - 1
                if attempts > 0:
                    print("Invalid credentials or table for " + args[1] + ". Attempts left: " + str(attempts))
                else:
                    print("Too many attempts...")
                    sys.exit(1)
    else:
        sql = sqlDriver.sqlDriver("dursley.socs.uoguelph.ca", "jzavarel", "jzavarel", "0929350")
        app = calGUI.App("iCalGUI", sql)
    app.mainloop()

if __name__ == '__main__':
    main()
