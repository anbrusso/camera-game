using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    public GameObject player;
    private Vector3 offset;
    // Start is called before the first frame update
    void Start()
    {
        transform.LookAt(player.transform.position);
        offset = transform.position - player.transform.position;
    }

    // LateUpdate is called once per frame -- garaunteed to run after all items (e.g. player has moved)
    void LateUpdate()
    {
        float rotHorizontal = Input.GetAxis("Horizontal");
        PlayerController pc = player.GetComponent<PlayerController>();
        Vector3 rotateVal = new Vector3(0,0,pc.rotSpeed * rotHorizontal);
        if ((transform.eulerAngles.z + rotateVal.z) <= 315 && transform.eulerAngles.z >= 315)
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
        {
            transform.eulerAngles = transform.eulerAngles + rotateVal;
        }
        //Debug.Log(transform.eulerAngles.z);
        transform.position = player.transform.position + offset;
    }
}
