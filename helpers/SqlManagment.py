# Sql Managment
# Author: RedstonedLife
import sqlite3
import os

def create_table(file_name,sql_statement):
  if(os.path.isfile("/storage/"+file_name+".db")==True):
    print("Found Database File, executing sql statement...")
    
    db = sqlite3.connect("storage/"+file_name+".db") # Connects to the database
    
    cursor = db.cursor() # Creates a cursor for the db
    
    # Executing sql statement
    cursor.execute(sql_statement)
    
    # Commit changes to db (Database)
    db.commit()
  else:
    print("Didn't find a database creating file...")
    
    db = sqlite3.connect("storage/"+file_name+".db") # Connects to database file and creats one
    
    print("Created a database " + file_name + ".db ")
    
    cursor = db.cursor()
    
    print("executing sql statement")
    
    cursor.execute(sql_statement)
    
    # Commit Changes to db (Database)
    db.commit()
    
def select(specfic : bool = False,file_name : str = "",table_name : str = "",sid : str = "")
  if(os.path.isfile("/storage/"+file_name+".db")==True):
    pass
  else:
    print("Didn't find a database file")
    return
  #
  if(specific == False):
    # Returns the whole table, not a specific user
    db = sqlite3.connect("storage/"+file_name+".db")
    
    cursor = db.cursor()
    
    sql_statement = '''SELECT * FROM '''+table_name+''';'''
    
    cursor.execute(sql_statement)
    rows = cursor.fetchall()
    
    return rows # Returns a list object (E.G. [(0,True,0,1),(1,False,1,0)] )
  else:
    # Returns a specific user from a table
    db = sqlite3.connect("storage/"+file_name+".db")
    
    cursor = db.cursor()
    
    sql_statement = '''SELECT * FROM '''+table_name+''' WHERE id='''+str(sid)+''';'''
    
    cursor.execute(sql_statement)
    rows = cursor.fetchall()
    return rows # Returns a list object (E.G. [(0,True,0,1)] )
    
def add(file_name,table_name,sql_statement,args):
  """Pass args as a list like this (value1,value2,...) , the values should be what you said in the table
  first value is the PRIMARY KEY aka the id it is always an int.
  If its a numeric(9,2) or int(#) then pass a number,
  If its a varchar(255) then pass a string"""
  if(os.path.isfile("/storage/"+file_name+".db")==True):
    pass
  else:
    print("Didn't find a database file")
    return
  #
  db = sqlite3.connect("storage/"+file_name+".db")
  
  cursor = db.cursor()
  
  cursor.execute(sql_statement,(args))
  
  db.commit()
  
def change(file_name,table_name,value,newValue,sid):
  """Changes a value in a table in a sql databaese file
  file_name : str : File name (.db is added after automatically)
  table_name : str : Table name (Table saved in the file, a .db file can store many tables)
  value : str : Value name (Name you gave to the value e.g: USERNAME)
  newValue : str/int : (New Value for the *value , e.g: RedstonedLife) (P.S: It depends what format is the value, If its varchar then str, If its numeric then int)
  sid : str/int : (Id of the user in table, you can pass a number or a string, It will automatically be turned into the string for the sql statement)
  """
  if(os.path.isfile("/storage/"+file_name+".db")==True):
    pass
  else:
    print("Didn't find a database file")
    return
  
  db = sqlite3.connect("storage/"+file_name+".db")
  
  cursor = db.cursor()
  
  sql_statement = '''UPDATE ''' + str(table_name) + ''' SET ''' + str(value) + '''=''' + str(newValue) + ''' WHERE id='''+str(sid)+''';'''
  
  cursor.execute(sql_statement)
  
  db.commit()
