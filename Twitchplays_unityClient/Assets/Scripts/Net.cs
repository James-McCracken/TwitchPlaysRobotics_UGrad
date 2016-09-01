using UnityEngine;
using System.Collections;
using System.IO;
using System.Collections.Generic;

public class Net : MonoBehaviour {

    public List<Ron> rons;
    public List<Syn> syns;
    public int ronOutput;
    public int synOutput;
    public List<float> ronValue;

    public class Ron
    {
        public int id;
        public int type;
        public float value;

        public Ron(int idInput, int typeInput)
        {
            id = idInput;
            type = typeInput;
            value = 0;
        }
    }
    public class Syn
    {
        public int id;
        public List<Ron> heldRons;
        public float weight;

        public Syn(int idInput, int callerRonId, int recieverRonId, float weightInput, List<Ron> ronMasterList)
        {
            heldRons = new List<Ron>();
            heldRons.Add(ronMasterList[callerRonId]);
            heldRons.Add(ronMasterList[recieverRonId]);
            weight = weightInput;
        }
    }

    void Update()
    {
        ronValue.Clear();
        foreach(Ron ron in rons)
        {
            ronValue.Add(ron.value);
        }
    }

    public void readNet(string path)
    {

        rons = new List<Ron>();
        syns = new List<Syn>();
        ronOutput = 0;
        synOutput = 0;
        ronValue = new List<float>();

        /* loadRobot ----- loads each of the net.dat files in the given directory to the nets member
         * of the agent member of the robot.
         * 
         * NOTE: the loadRobot function can only be called after a robot has already loaded it's
         * sensors and effectors, additionally if the robot has not loaded it's corresponding sensors
         * and effectors it will not load properly.
         */
        int counter = 0;
        string[] netStringArray = File.ReadAllLines(path);

        string typeReading = "";

        if (netStringArray[counter].Contains("Rons"))
        {
            typeReading = "Rons";
            counter += 1;
        }
        while (typeReading.Contains("Rons"))
        {
            // Masterlist Populator
            int ronID;
            int.TryParse(netStringArray[counter], out ronID);
            counter += 1;
            int type;
            int.TryParse(netStringArray[counter], out type);

            Ron ron = new Ron(ronID, type);
            rons.Add(ron);
            counter += 1;
            ronOutput += 1;

            if (netStringArray[counter].Contains("Syns"))
            {
                typeReading = "Syns";
                counter += 1;
            }
        }
        while (typeReading.Contains("Syns"))
        {
            int synID;
            int.TryParse(netStringArray[counter], out synID);
            int synCallerID;
            int.TryParse(netStringArray[counter + 1], out synCallerID);
            int synRecieverID;
            int.TryParse(netStringArray[counter + 2], out synRecieverID);
            float synWeight;
            float.TryParse(netStringArray[counter + 3], out synWeight);
            counter += 4;
            synOutput += 1;
            Syn syn = new Syn(synID, synCallerID, synRecieverID, synWeight, rons);
            syns.Add(syn);
            if (netStringArray[counter].Contains("End"))
            {
                typeReading = "end";
            }
        }
    }
}
