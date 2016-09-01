# Twitchplays Python Client #
# - Slayton Marx

# Forward #
# Hi, if you're reading this you're probably a grad-student or professor Bongard.
# Here's the basics:

# 1) This program opens connection to an offsite server.
# 2) It uploads a neural net to the offsight server so long as
#       there are no other nets there waiting to be evaluated.
# 3) When a new net doesn't need to be made it enters a holding pattern
# 4) itera ad nauseum

import numpy as np
import random
import os.path
import msvcrt
import Big_Green_Button;

connection = Big_Green_Button.DB_Connect(); #access to python mySQL wrapper

def mainLoop():
    ContNum = 0
    createNet(4,8,ContNum);
    while(True):
        # Checks the Status of the most Recent Controller
        neural_network = connection.get_status()
        neural_network = neural_network[0] #removes set
        status = int(neural_network['STATUS']) #(gets int value)
        if( status == 2 ):
            ContNum += 1
            createNet(4,8,ContNum)
            print(ContNum)
            print("one pass")
    print("optimizer has run")

# createNet ----- function creates a net and puts it onto the server.
def createNet(numberOfInputRons, numberOfOutputRons, NN_number):
    
    # Explanation: no neurons are written in the server, only synapses.
    
    # The synapse matrix has three axis. The first is the parent neuron of the
    # synapse, the second axis is it's child neuron, and the third is the
    # synapses weight. They are written to the file as:
    # ID \n ParentID \n ChildID \n weight
    
    # Writes the rons into the new file
    random.seed()
    #_________________________________________
            
    connection.insert("CONTROLLER_TABLE", ["CONTROLLER_NUMBER"], [str(NN_number)])  #fills controller table with new neural networks

    NNtable = {"SOURCE_NEURON":"VARCHAR(100)", "TARGET_NEURON":"VARCHAR(100)", "WEIGHT":"VARCHAR(100)", "ID": "INT NOT NULL AUTO_INCREMENT"} #dict of columns used for the neurons, synapses, and weights table for each NN
    name = "CONTROLLER_"+str(NN_number)

    connection.create_table(name, NNtable, "ID")#using the NN counter, creates a new NN table for a new set of neurons and synapses
    columns = ["SOURCE_NEURON","TARGET_NEURON","WEIGHT"]
    #_________________________________________

    # Creates the synapses, choosing random rons
    syns = matrixCreate(3,numberOfInputRons*numberOfOutputRons)
    synsNumber = 0
    for i in range(0, numberOfInputRons):
        for j in range(numberOfInputRons, numberOfInputRons + numberOfOutputRons):
            syns[0][synsNumber] = i
            syns[1][synsNumber] = j
            # Makes it possible for the weight to be negative
            chanceOfNegative = random.randrange(0,10)
            if chanceOfNegative % 2 == 0:
                chanceOfNegative = -1
            else:
                chanceOfNegative = 1            
            syns[2][synsNumber] = random.random() * chanceOfNegative
            synsNumber += 1
    
    # Uploads the synapses onto the server
    connection.update_status(str(0), str(NN_number))
    for i in range(0, len(syns[0])):
        #insert 
        #__________________________________________________
        values = [str(syns[0][i]),str(syns[1][i]),str(syns[2][i])]
        connection.insert(name, columns, values)
        #__________________________________________________
        # Prints the synpases to the file

    return NN_number;
    
# Creates a two dimensional list to serve as our matrix
def matrixCreate(row, columns):
    dstep = np.zeros((row,columns));
    return dstep;
    
mainLoop()