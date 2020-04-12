using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    public GameObject player;
    public GameObject webcam;
    private Vector3 offset;
    private float turningRate = 30f;
    // Start is called before the first frame update
    void Start()
    {
        transform.LookAt(player.transform.position);
        offset = transform.position - player.transform.position;
    }
    private void Update()
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
        Vector3 rotateVal = new Vector3(transform.eulerAngles.x, transform.eulerAngles.y, angle);
        transform.rotation = Quaternion.RotateTowards(transform.rotation, Quaternion.Euler(rotateVal), turningRate * Time.deltaTime);

    }
    // LateUpdate is called once per frame -- garaunteed to run after all items (e.g. player has moved)
    void LateUpdate()
    {
        //float rotHorizontal = Input.GetAxis("Horizontal");
        PlayerController pc = player.GetComponent<PlayerController>();
       
        /*if ((transform.eulerAngles.z + rotateVal.z) <= 315 && transform.eulerAngles.z >= 315)
        {
            //rotateVal = new Vector3(transform.eulerAngles.x, transform.eulerAngles.y, 315);
            //transform.eulerAngles = rotateVal;
            //Debug.Log("Right Camera Limit");
        }
        else if ((transform.eulerAngles.z + rotateVal.z) >= 45 && transform.eulerAngles.z <= 45)
        {
            //rotateVal = new Vector3(transform.eulerAngles.x, transform.eulerAngles.y, 45);
            //transform.eulerAngles = rotateVal;
            //Debug.Log("Left Camera Limit");
        }
        else
        {*/
        //}
        //Debug.Log(transform.eulerAngles.z);
        transform.position = player.transform.position + offset;
    }
}
