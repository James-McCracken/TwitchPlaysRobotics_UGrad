import pymysql;
import pymysql.cursors;
from pymysql import cursors



#cursor = conn.cursor(cursors.DictCursor);

class DB_Connect(object):
    
#____________________Connection Settup______________________________________ 
    connection = None
    cursor = None

    def __init__(self):
        self.connection = pymysql.connect(host="ip",
                       #port = 3306,
                       user="user",
                       password="test",
                       db="test_db",
                       charset = "utf8",
                       autocommit = True)
        
        self.cursor = self.connection.cursor(cursors.DictCursor);





#_________________________Functions_________________________________________
    #single table currently taking in a string of column names with the column type
    def create_table(self, name, column_names, primary_key):
        all_columns = itterate_dictionary(column_names)
        #!!!!!!!!!!uses the grave accent for the PRIMARY KEY!!!!!!!!!!!!!!!!#
        self.cursor.execute( """CREATE TABLE IF NOT EXISTS `%s`(%s PRIMARY KEY( `%s` ))Engine = MyISAM""" %(name, all_columns, primary_key))
              
#working:
#self.cursor.execute( """CREATE TABLE IF NOT EXISTS `%s`(%s, PRIMARY KEY( `%s` ))Engine = MyISAM""" %(name, column_names, primary_key))    //takes in string for columns names and datatypes
#self.cursor.execute( """CREATE TABLE IF NOT EXISTS `%s`(%s PRIMARY KEY( `%s` ))Engine = MyISAM""" %(name, all_columns, primary_key))      //takes in a dictionary for columns names: datatypes
 
    def drop_table(self, table):
        self.cursor.execute("DROP TABLE IF EXISTS %s" %table)
            
    #remove table from database
    def drop_tables(self, tables):
        for i in range(len(tables)):
            self.cursor.execute("DROP TABLE IF EXISTS %s" %tables[i])
     
    
    #remove column from spesified table   
    def drop_column(self, table, column):
     self.cursor.execute("ALTER TABLE %s DROP COLUMN %s" %(table, column))
    
    def drop_columns(self, table, column):
        for item in column:
            self.cursor.execute("ALTER TABLE %s DROP COLUMN %s" %(table, column))    
    
    #single column
    def add_column(self, table, column_name, column_data_type):
        self.cursor.execute("ALTER TABLE %s ADD %s %s" %(table, column_name, column_data_type))
    
    #takes in table Name as string, the columns as list and values as a list
    #columns and values are taken in as strings i.e "foo" and "bar" 
    #the Grave Accent are added by private funtions to the columns and table name
    def insert(self, table, columns, values):
        all_columns = itterate_list(columns)
        all_values = itterate_without_grave_accent(values)
        #print("INSERT INTO `%s` (%s) VALUES (%s)" %(name, all_columns, all_values))
        self.cursor.execute("INSERT INTO `%s` (%s) VALUES (%s)" %(table, all_columns, all_values))
        
    #columns is a list, table is a string, and clause is a string
    def select_columns(self, columns, table, clause):
        all_columns = itterate_list(columns)
        if (clause == "null"):
            self.cursor.execute("SELECT %s FROM %s" %(all_columns, table))
            result = self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT %s FROM %s WHERE %s" %(all_columns, table, clause))
            result = self.corsor.fetchall()
        return(result)#retuned as a ditcionary
     
    def select_max(self, column, table):
        print ("SELECT MAX(%s) FROM %s" %(column, table))
        self.cursor.execute("SELECT MAX(%s) FROM %s" %(column, table))
        result = self.cursor.fetchall()
        return(result)#retuned as a ditcionary
#_________________________________________________^^working   

 
  
    
    #many columns  (name is a single table name), column names is a 
                    #dictionary of column names and corosponding data types)
    def add_columns(self, table, column_names):
        for key, value in column_names.items():
            self.cursor.execute("ALTER TABLE %s ADD %s %s" %(table, key, value))
            
             


    
    
    
    def select_all(self, table, column, value):    
       self.cursor.execute("DELETE FROM %s WHERE %s = %s") 
    
    #take in table, column and value as string
    def delete(self, table, column, value):    
       self.cursor.execute("DELETE FROM %s WHERE %s = %s" %(table, column, value)) 
    
    #takes in table as string, deletes all from given table
    def delete_all(self, table):    
       self.cursor.execute("DELETE FROM %s"%(table))
       
    def commit(self):
        self.connecttion.commit();

    #close connection    
    def __del__(self):
        self.connection.close()        

















#_____________________________Private Class Funtions________________________
        
def itterate_dictionary(dictionary):
    s = ""
    for key in dictionary:
        s+=( key + " " + dictionary[key] + ", ")
    return (s)#wrap all of the db column commands in () for mySQL syntax
        

def itterate_list(l):
    s = ""
    for i in range(len(l)):
        if i == len(l)-1:
            s+=("`" + l[i] + "`")
            i+=1;
        else:
            s+=("`" + l[i] + "`, ")
            i+= 1;
    return s



def itterate_without_grave_accent(l):
    s = ""
    for i in range(len(l)):
        if i == len(l)-1:
            s+=("'" + l[i] + "'")
            i+=1;
        else:
            s+=("'" + l[i] + "', ")
            i+= 1;
    return s

#def main():
    #    lists = ["foo", "bar"]
#    s = itterate_list(lists)
#    print s;


#main();





#______________________________Testing_____________________________________        
 
        
  #Testing              
        #self.cursor.execute("CREATE TABLE IF NOT EXISTS `USER`(Time_Stamp TIMESTAMP DEFAULT NOW(),`user_name` VARCHAR( 200 ) NOT NULL,PRIMARY KEY ( `Time_Stamp` ))Engine = MyISAM" )                   
        #print( """CREATE TABLE IF NOT EXISTS `%s`(%s, PRIMARY KEY( `%s` ))Engine = MyISAM""" %(name, column_names, primary_key))
        #self.cursor.execute( "CREATE TABLE IF NOT EXISTS '" + name + "' (" + all_columns+ " PRIMARY KEY ( '"+ primary_key + "' ))Engine = MyISAM")
        #all_columns = itterate_dictionary(column_names)
        #print( "'CREATE TABLE IF NOT EXISTS '"s + name + "' (" + all_columns+ " PRIMARY KEY ( '"+ primary_key + "' ))Engine = MyISAM'")
                                     
       
'''        
def main():
    tb_name = 'test'
    table = {"Time_Stamp TIMESTAMP" : "DEFAULT NOW()", "`user_name` ": "VARCHAR( 200 ) NOT NULL"}
    print(create_table(tb_name, table))
main()        
'''        
        
        
        
        
'''    
    def name_user(self):
        self.cursor.execute( """CREATE TABLE IF NOT EXISTS `USER`
            (
                Time_Stamp TIMESTAMP DEFAULT NOW(),
                `user_name` VARCHAR( 200 ) NOT NULL,
                PRIMARY KEY ( `Time_Stamp` )
            )Engine = MyISAM""" )        
        
        
 '''       
        
        
        
        
        
        
        
        
        
        
        
        #self.cursor.execute( "CREATE TABLE IF NOT EXISTS `%s`"  %name)
    #many tables
#    def name_tables(self, *names):
#        for i in names:
#            self.cursor.execute( "CREATE TABLE IF NOT EXISTS `%s`"  %i)
    
    
 
    
'''
conn = pymysql.connect(host="96.126.111.207",
                       #port = 3306,
                       user="testiser",
                       password="test",
                       db="testdb",
                       charset = "utf8")
                       #cursorclass = pymysql.cursors.DictCursor);
'''                       

'''
Create tables = {"USER": {"Time_Stamp": "TIMESTAMP DEFAULT NOW(),", 
                          "user_name": "VARCHAR(200) NOT NULL,",
                          "PRIMARY KEY ('Time_Stamp')"},
                          "USER": {"Time_Stamp": "TIMESTAMP DEFAULT NOW(),", 
                          "user_name": "VARCHAR(200) NOT NULL,",
                          "PRIMARY KEY ('Time_Stamp')"}}
'''    
    
'''  

        








#user table
cursor.execute( """CREATE TABLE IF NOT EXISTS `USER`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `user_name` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )


#robot table
cursor.execute( """CREATE TABLE IF NOT EXISTS `ROBOT`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#controller table
cursor.execute( """CREATE TABLE IF NOT EXISTS `CONTROLLER`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )

#evaluation table
cursor.execute( """CREATE TABLE IF NOT EXISTS `EVALUATION`
    (
         Time_Stamp TIMESTAMP DEFAULT NOW(),
        `Robot` VARCHAR( 200 ) NOT NULL,
        `Controller` VARCHAR( 200 ) NOT NULL,
        `Command` VARCHAR( 200 ) NOT NULL,
        `Color` VARCHAR( 200 ) NOT NULL,
        `Satus` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#sensorValue table
cursor.execute( """CREATE TABLE IF NOT EXISTS `SENSOR_VALUE`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `robotSensor` VARCHAR( 200 ) NOT NULL,
        `evaluation` VARCHAR( 200 ) NOT NULL,
        `value` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#command table
cursor.execute( """CREATE TABLE IF NOT EXISTS `COMMAND`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `user_name` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#reinforcement table
cursor.execute( """CREATE TABLE IF NOT EXISTS `REINFORCEMENT`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `user_name` VARCHAR( 200 ) NOT NULL,
        `evaluation` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )

#robotObject table
cursor.execute( """CREATE TABLE IF NOT EXISTS `ROBOT_OBJECT`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `Robot` VARCHAR( 200 ) NOT NULL,
        `Position` VARCHAR( 200 ) NOT NULL,
        `Shape` VARCHAR( 200 ) NOT NULL,
        `Orientation` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#RobotJoint table
cursor.execute( """CREATE TABLE IF NOT EXISTS `ROBOT_JOINT`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `ParentObject` VARCHAR( 200 ) NOT NULL,
        `ChildObject` VARCHAR( 200 ) NOT NULL,
        `Normal` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#RobotSensor table
cursor.execute( """CREATE TABLE IF NOT EXISTS `ROBOT_SENSOR`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `RobotObject` VARCHAR( 200 ) NOT NULL,
        `Touch` VARCHAR( 200 ) NOT NULL,
        `Distance` VARCHAR( 200 ) NOT NULL,
        `Proprioceptive` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#RobotMotor table
cursor.execute( """CREATE TABLE IF NOT EXISTS `ROBOT_MOTOR`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `RobotJoint` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#ControllerNeuron table
cursor.execute( """CREATE TABLE IF NOT EXISTS `CONTROLLER_NEURON`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `Controller` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    
#ControllerSynapse table
cursor.execute( """CREATE TABLE IF NOT EXISTS `CONTROLLER_SYNAPSE`
    (
        Time_Stamp TIMESTAMP DEFAULT NOW(),
        `SourceNeuron` VARCHAR( 200 ) NOT NULL,
        `TargetNeuron` VARCHAR( 200 ) NOT NULL,
        `Weight` VARCHAR( 200 ) NOT NULL,
        PRIMARY KEY ( `Time_Stamp` )
    )Engine = MyISAM""" )
    

'''