using UnityEngine;
using System.Collections;

public class touch : MonoBehaviour {

    public bool isTouching;

    void OnCollisionEnter(Collision collision)
    {
        foreach (ContactPoint contact in collision.contacts)
        {
            Debug.DrawRay(contact.point, contact.normal, Color.white);
        }
        if (collision.collider.gameObject.CompareTag("ground"))
        {
            isTouching = true;
        }
    }

    void OnCollisionExit(Collision collision)
    {
        foreach (ContactPoint contact in collision.contacts)
        {
            Debug.DrawRay(contact.point, contact.normal, Color.white);
        }
        if (collision.collider.gameObject.CompareTag("ground"))
        {
            isTouching = false;
        }
    }
}
