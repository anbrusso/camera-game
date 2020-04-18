using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float rotSpeed;
    public float gravitySpeed;
    public GameObject camera;
    private Rigidbody rb;
    private Vector3 oldVelocity;
    private bool stopped = false;
    private void Start()
    {
        rb = GetComponent<Rigidbody>();
    }
    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space) && !stopped)
        {
            oldVelocity = rb.velocity;
            rb.velocity = Vector3.zero;
            stopped = true;
            //Debug.Log("Down, not stopped");
        }
        if (Input.GetKeyUp(KeyCode.Space) && stopped)
        {
            rb.velocity = oldVelocity;
            oldVelocity = Vector3.zero;
            stopped = false;
            //Debug.Log("Up, stopped");
        }
    }
    //physics related code
    private void FixedUpdate()
    {
        /*float rotHorizontal = Input.GetAxis("Horizontal");
        if (gravityDir.x > .5 && rotHorizontal > 0)
        {
            //Debug.Log("Left Limit Player");
        }
        else if (gravityDir.x < -.5 && rotHorizontal < 0)
        {
            //Debug.Log("Right Limit Player");
        }
        else
        {
            gravityDir = Quaternion.AngleAxis(-rotSpeed * rotHorizontal, Vector3.up) * gravityDir;
        }*/
        Vector3 dir = Quaternion.AngleAxis(-camera.transform.eulerAngles.z, Vector3.up) * Vector3.back;
        //Debug.Log(dir);


        if (!stopped) {
            rb.AddForce(gravitySpeed * dir);
        }
    }
}
