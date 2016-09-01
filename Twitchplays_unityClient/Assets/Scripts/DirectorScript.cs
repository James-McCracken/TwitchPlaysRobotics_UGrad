using UnityEngine;
using System.Collections;
using System.IO;
using UnityEngine.UI;

public class DirectorScript : MonoBehaviour {

    public int[] touches;
    public GameObject[] parts;
    GameObject plane;
    Net ANN;
    int time = 0;

    public Vector3[] positions;
    public Quaternion[] rotations;

    // Use this for initialization
    void Start()
    {
        touches = new int[4];
        parts = new GameObject[9];
        positions = new Vector3[9];
        rotations = new Quaternion[9];
        plane = GameObject.CreatePrimitive(PrimitiveType.Plane);
        plane.GetComponent<Renderer>().material.color = Color.white;
        plane.tag = "ground";
        plane.transform.position = new Vector3(0, 0, 0);
        plane.transform.localScale = new Vector3(5, 1, 5);
        produceBody();
        enableMotors(parts);
        setInitial();

        ANN = parts[0].AddComponent<Net>();
        ANN.readNet("SPECIFIED_PATH\\testNet.txt");
    }

    public void setInitial()
    {
        for(int i = 0; i < parts.Length; i++)
        {
            positions[i] = parts[i].transform.position;
            rotations[i] = parts[i].transform.rotation;
        }
    }
    public void reset()
    {
        for(int i = 0; i < parts.Length; i++)
        {
            parts[i].transform.position = positions[i];
            parts[i].transform.rotation = rotations[i];
            Rigidbody rb = parts[i].GetComponent<Rigidbody>();
            rb.velocity = new Vector3(0, 0, 0);
            rb.angularVelocity = new Vector3(0, 0, 0);
        }
    }

    private void ActuateJoint(int legIndex, float desiredAngle)
    {
        float force = 50;
        float velo = 5f;
        HingeJoint currentJoint = parts[legIndex].GetComponent<HingeJoint>();
        float currentAngle = currentJoint.angle;
        float difference = Mathf.Abs((currentAngle - desiredAngle));

        if (currentAngle < desiredAngle)
        {
            JointMotor motor = currentJoint.motor;
            motor.force = force;
            motor.targetVelocity = velo * difference;
            currentJoint.motor = motor;
            currentJoint.useMotor = true;
        }
        else if (currentAngle > desiredAngle)
        {
            JointMotor motor = currentJoint.motor;
            motor.force = force;
            motor.targetVelocity = velo * difference * -1;
            currentJoint.motor = motor;
            currentJoint.useMotor = true;
        }
        else
        {
            JointMotor motor = currentJoint.motor;
            motor.force = force;
            motor.targetVelocity = 0;
            currentJoint.motor = motor;
        }
    }
    public void enableMotors(GameObject[] parts)
    {
        for(int i = 1; i < parts.Length; i++)
        {
            parts[i].GetComponent<HingeJoint>().useMotor = true;
        }
    }
    public void produceBody()
    {
        GameObject model = new GameObject();
        model.GetComponent<Transform>().position = new Vector3(0,0,0);
        model.name = "Robot";
        addToParent(model, CreateBody(0, 0, 1, 0, 1, .2f, 1));

        //NORTH
        CreateLeg(1, 0, 1, 0 + 1, .20f, .5f, 90, 180, 0, parts);
        CreateLeg(2, 0, .5f, 0 + 1.5f, .20f, .5f, 0, 180, 0, parts);
        // EAST
        CreateLeg(3, 0 + 1, 1, 0, .20f, .5f, 90, -90, 0, parts);
        CreateLeg(4, 0 + 1.5f, .5f, 0, .20f, .5f, 0, -90, 0, parts);
        // SOUTH
        CreateLeg(5, 0, 1, 0 + -1, .20f, .5f, 90, 0, 0, parts);
        CreateLeg(6, 0, .5f, 0 + -1.5f, .20f, .5f, 0, 0, 0, parts);
        // WEST
        CreateLeg(7, 0 + -1f, 1, 0, .20f, .5f, 90, 90, 0, parts);
        CreateLeg(8, 0 + -1.5f, .5f, 0, .20f, .5f, 0, 90, 0, parts);
        CreateJoints(parts);
    }
    private GameObject CreateBody(int index, float x, float y, float z, float length, float height, float width)
    {
        // CreateBody ----- trib function which creates the box.


        //initialize values
        Vector3 position = new Vector3(x, y, z);
        Vector3 size = new Vector3(length, height, width);

        //create box for main body
        parts[index] = (GameObject.CreatePrimitive(PrimitiveType.Cube));
        parts[index].transform.position = position;
        parts[index].transform.localScale = size;
        parts[index].GetComponent<Renderer>().material.color = Color.cyan;
        parts[index].transform.name = "Body";
        parts[index].AddComponent<Rigidbody>().mass = 1;
        parts[index].AddComponent<MeshCollider>().convex = true;

        return parts[index];
    }
    private GameObject CreateLeg(int index, float x, float y, float z, float diameter, float height, float xRot, float yRot, float zRot, GameObject[] parts)
    {
        // CreateLeg ----- trib function which creates a leg.

        //initialize values
        Vector3 position = new Vector3(x, y, z);
        Vector3 size = new Vector3(diameter, height, diameter);
        Vector3 rotation = new Vector3(xRot, yRot, zRot);


        //create leg segment
        parts[index] = (GameObject.CreatePrimitive(PrimitiveType.Cylinder));
        //parts[index].AddComponent<LegTouch>();
        parts[index].transform.position = position;
        parts[index].transform.localScale = size;
        parts[index].transform.eulerAngles = rotation;
        parts[index].AddComponent<MeshCollider>().convex = true;

        if (index % 2 == 1)
            parts[index].AddComponent<Rigidbody>().mass = 1;

        //Naming Convention:
        //U = Upper
        //N,S,E,W = North, South, East, and West

        if (index == 1)
        {
            parts[index].transform.name = "UN";
            //parts[index].GetComponent<LegTouch>().touchTag = "none";
            parts[index].GetComponent<Renderer>().material.color = Color.blue;
        }
        else if (index == 2)
        {
            parts[index].transform.name = "LN";
            parts[index].AddComponent<touch>();
            parts[index].GetComponent<Renderer>().material.color = Color.blue;
        }
        else if (index == 3)
        {
            parts[index].transform.name = "UE";
            //parts[index].GetComponent<LegTouch>().touchTag = "none";
            parts[index].GetComponent<Renderer>().material.color = Color.red;
        }
        else if (index == 4)
        {
            parts[index].transform.name = "LE";
            parts[index].AddComponent<touch>();
            parts[index].GetComponent<Renderer>().material.color = Color.red;
        }
        else if (index == 5)
        {
            parts[index].transform.name = "US";
            //parts[index].GetComponent<LegTouch>().touchTag = "none";
            parts[index].GetComponent<Renderer>().material.color = Color.yellow;
        }
        else if (index == 6)
        {
            parts[index].transform.name = "LS";
            parts[index].AddComponent<touch>();
            parts[index].GetComponent<Renderer>().material.color = Color.yellow;
        }
        else if (index == 7)
        {
            parts[index].transform.name = "UW";
            //parts[index].GetComponent<LegTouch>().touchTag = "none";
            parts[index].GetComponent<Renderer>().material.color = Color.green;
        }
        else if (index == 8)
        {
            parts[index].transform.name = "LW";
            parts[index].AddComponent<touch>();
            parts[index].GetComponent<Renderer>().material.color = Color.green;
        }
        return parts[index];
    }
    private void CreateJoints(GameObject[] partsJoints)
    {
        // CreateJoints ----- trib function which creates all joints for the robot.

        for (int i = 1; i < 8; i += 2)
        {
            HingeJoint currentHinge = partsJoints[i].AddComponent<HingeJoint>();
            currentHinge.connectedBody = partsJoints[0].GetComponent<Rigidbody>();
            Vector3 anchor = new Vector3(0, 1, 0);
            Vector3 axis = new Vector3(1, 0, 0);
            currentHinge.anchor = anchor;
            currentHinge.axis = axis;
            //currentHinge.enablePreprocessing = true;
            currentHinge.autoConfigureConnectedAnchor = true;


            // Joint limits
            JointLimits jl = new JointLimits();
            float jointLimit = 35;
            jl.max = jointLimit;
            jl.min = -jointLimit;
            currentHinge.limits = jl;
            currentHinge.useLimits = true;
        }

        for (int i = 2; i < 9; i += 2)
        {
            partsJoints[i].AddComponent<HingeJoint>();
            HingeJoint currentHinge = partsJoints[i].GetComponent<HingeJoint>();
            currentHinge.connectedBody = partsJoints[i - 1].GetComponent<Rigidbody>();
            Vector3 anchor = new Vector3(0, 1, 0);
            Vector3 axis = new Vector3(1, 0, 0);
            currentHinge.anchor = anchor;
            currentHinge.axis = axis;
            //currentHinge.enablePreprocessing = true;
            currentHinge.autoConfigureConnectedAnchor = true;
            partsJoints[i].GetComponent<MeshCollider>().material = Resources.Load<PhysicMaterial>("friction");

            // Joint limits
            JointLimits jl = new JointLimits();
            jl.max = 35;
            jl.min = -35;
            currentHinge.limits = jl;
            currentHinge.useLimits = true;

        }

    }

    // Update is called once per frame
    void Update () {
        while (!File.Exists("SPECIFIED_PATH\\testNet.txt"))
        {

        }

        ANN.readNet("SPECIFIED_PATH\\testNet.txt");

            foreach (GameObject part in parts)
        {
            Rigidbody rb = part.GetComponent<Rigidbody>();
            //rb.velocity = new Vector3(0, 0, 0);
            rb.angularVelocity = new Vector3(0, 0, 0);
        }
        for (int i = 2; i < 9; i+=2)
        {
            if (parts[i].GetComponent<touch>().isTouching)
                touches[i / 2 - 1] = 1;
            else
                touches[i / 2 - 1] = 0;
        }

        if(time % 25 == 0)
        {
            readNet();
        }

        actuateJoints();
        time += 1;
        if(time % 150 == 0)
        {
            float fitness = parts[0].transform.position.x;
            string[] fit = new string[1];
            fit[0] = fitness.ToString();
            File.Delete("SPECIFIED_PATH\\testNet.txt");
            File.WriteAllLines("SPECIFIED_PATH\\fits.txt", fit);
            reset();
        }
        while (File.Exists("SPECIFIED_PATH\\fits.txt"))
        {

        }

    }

    void readNet()
    {
        foreach(Net.Ron ron in ANN.rons)
        {
            ron.value = 0;
        }

        for (int i = 0; i < 4; i++)
        {
            ANN.rons[i].value = touches[i];
        }
        foreach(Net.Syn syn in ANN.syns)
        {
            syn.heldRons[1].value += syn.heldRons[0].value * syn.weight;
        }
        foreach(Net.Ron ron in ANN.rons)
        {
            if (ron.value > 1)
                ron.value = 1;
            if (ron.value < -1)
                ron.value = -1;
        }
    }
    void actuateJoints()
    {
        int counter = 1;
        foreach(Net.Ron ron in ANN.rons)
        {
            if(ron.type == 1)
            {
                ActuateJoint(counter, ron.value * 35);
                counter += 1;
            }
        }
    }

    public void addToParent(GameObject parent, GameObject child)
    {
        child.transform.parent = parent.transform;
    }
}
