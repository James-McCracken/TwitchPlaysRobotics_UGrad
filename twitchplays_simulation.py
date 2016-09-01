# Twitchplays Python Client #
# - Slayton Marx

# Forward #
# Hi, if you're reading this you're probably a grad-student or professor Bongard.
# Here's the basics:

# 1) This program opens connection to an offsite server.
# 2) It downloads a neural net from the server and copies that net into a 
#     text file which the Unity program reads. It may seem a little round about,
#      but it keeps everything tidy.
# 3) Unity returns a fitness file which this program reads, and then enters
#     into the database.
# 4) itera ad nauseum

import random
import os.path
import msvcrt
import Big_Green_Button;

connection = Big_Green_Button.DB_Connect(); #access to python mySQL wrapper
    
def simulation():    
    # ----------- Replace with a function that pulls down a new net from the server and writes it to a path
    #NN_number = createNet("C:\\Users\\13mcc\\Desktop\\exchange\\testNet.txt", 4, 8, NN_number) 
    
    # Pulls down the neural network from the net
    neural_network = connection.get_status()
    neural_network = neural_network[0] #removes set
    while(neural_network['STATUS'] == None):
        print("waiting on optimizer")
        neural_network = connection.get_status()
        neural_network = neural_network[0] #removes set
    status = int(neural_network['STATUS']) #(gets int value)
    network_number = int(neural_network['MAX(CONTROLLER_NUMBER)'])
    

    if (status == 0):
        #query database for controller number table, 
        NN_table = connection.select_columns(["SOURCE_NEURON","TARGET_NEURON","WEIGHT"],"CONTROLLER_"+str(network_number), "null")
        #print NN_table;
        
        f = open("SPECIFIED_PATH\\testNet.txt","w")
        # Writes the neurons to the file
        f.write("Rons\n")
        for i in range(0,4):
            f.write(str(i) + "\n" + str(0) + "\n" )
        for i in range(4,12):
            f.write(str(i) + "\n" + str(1) + "\n" )
        f.write("Syns\n")
        
        synID = 0
        for i in NN_table: #(list of dictionaries) i.e. each row is a dictionary with the key=column name and value = value of column
            #print i
            source = i['SOURCE_NEURON'].strip('u')
            target = i['TARGET_NEURON'].strip('u')
            weight = i['WEIGHT'].strip("u")
            print(source, target, weight)
            f.write(str(synID) + "\n" + str(int(float(source))) + "\n" + str(int(float(target))) + "\n" + weight + "\n")
            synID += 1
        
        f.write("End")
        f.close()    
        print(network_number)
        connection.update_status(str(1), str(network_number)) #CHANGE STATUS IN db FROM 0 TO 1, MEANING IT IS BEING RUN
        while(os.path.exists("SPECIFIED_PATH\\testNet.txt")):
            1 + 1
    #elif (status == 1 or status == 2):
        #create new NN and store in DB.
        
    
        print("ran")
        while(os.path.exists("SPECIFIED_PATH\\fits.txt") is False):
            print("waiting")

        
        g = open("SPECIFIED_PATH\\fits.txt", "r")
        fitness = g.read()
        # Write to the database
        list1 = ["test"] # column; will become controler number
        list2 = [str(fitness)]# the controler number, currently testing 
        connection.insert("EVALUATION", list1, list2);
        g.close()
        
        # Get net from database
        # ----------- Replace with pulldown function
        
        os.remove("SPECIFIED_PATH\\fits.txt")
        # ----------- We need a line that sets status to 2 here
        connection.update_status(str(2), str(network_number)) #UPDATES STATUS IN db TO 2, MEANING IS HAS BEEN TESTED

# pullControllerFromServer ----- pulls the next unevaluated network from the server
# and writes it to a .dat file at the path specified.
def pullControllerFromServer(path):
    print("so it goes")
    #ect.
        
def mainLoop():
    pullControllerFromServer("path")
    print("initialized")
    key = ord(msvcrt.getch())
    while(key == 255):
        key = ord(msvcrt.getch())
        print(key)
        print("ffffff");
    print("we're done here")
        

def main():
    while(True):
        simulation()

main()
    
