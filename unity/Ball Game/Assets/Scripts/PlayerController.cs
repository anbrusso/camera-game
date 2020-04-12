using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float rotSpeed;
    public float gravitySpeed;
    public GameObject webcam;
    private Vector3 gravityDir;
    private Rigidbody rb;
    private Vector3 oldVelocity;
    private bool stopped = false;
    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        gravityDir = new Vector3(0, 0, -1);
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

        WebCam cam = webcam.GetComponent<WebCam>();
        float angle = cam.getAngle();
        //threshold values to prevent rotating too far.
        if (angle > 45)
        {
            angle = 45;
        }
        if (angle < -45)
        {
            angle = -45;
        }
        //convert angle to be within 0 to 360 range.
        if (angle < 0)
        {
            angle = 360 + angle;
        }


        float rotHorizontal = Input.GetAxis("Horizontal");
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
        }

        if (!stopped) {
            rb.AddForce(gravitySpeed * gravityDir);
        }
    }
}
