import mysql.connector

# Open database connection
dbName = "dbNameGoesHere"
uName = "userNameGoesHere"
passwd = "passwordGoesHere"


try:
    conn = mysql.connector.connect(host="dursley.socs.uoguelph.ca",database=dbName,user=uName, password=passwd)
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
    exit()
        
# prepare a cursor object using cursor() method
cursor = conn.cursor()

# **** uncomment if you want to create the table on the fly ****

#createQuery="create table students (id int not null auto_increment,  last_name char(15),  first_name char(15), mark char(2), primary key(id) )"
#try:
#    cursor.execute(createQuery)
#except mysql.connector.Error as err:
#    print("Something went wrong: {}".format(err))

# *** If you uncommented code above, remember to also uncomment the "drop table" code at the bottom of this file ****



records = [ "INSERT INTO students VALUES (1,'Hugo','Victor','B+')", "INSERT INTO students VALUES  (4,'Rudin','Walter','A-')", "INSERT INTO students VALUES  (5,'Stevens','Richard','C')"]

# execute SQL query using execute() method.
for record in records:
    try:
        cursor.execute(record)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


print("Database contents sorted by last name:")

try:
    cursor.execute("SELECT * FROM students ORDER BY last_name")
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
  
for r in cursor:
    # r is a tuple of column values
    # this means that r has constant length
    print(r)
    
print("\n\n")

print("Database contents sorted by first name:")

try:
    cursor.execute("SELECT * FROM students ORDER BY first_name")
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
  
for r in cursor:
    # r is a tuple of column values
    # this means that r has constant length
    print(r)
    
print("\n\n")

#clear data from table
cursor.execute("delete from students")

# **** uncomment this if you also uncomment the "create table" code at the front ****
#cursor.execute("drop table students")

cursor.close()    
conn.close()