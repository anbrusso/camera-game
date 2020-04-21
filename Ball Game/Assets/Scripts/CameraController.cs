using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    public GameObject player;
    public GameObject gamestate;
    private Vector3 offset;
    public float turnUpdateSpeed;//60
    public float turningRateCamera;//1.5
    public float turningRateKeyboard;//2
    public float cameraLimit;//45
    // Start is called before the first frame update
    void Start()
    {
        transform.LookAt(player.transform.position);
        offset = transform.position - player.transform.position;
    }
    private void Update()
    {
        GameStateScript state = gamestate.GetComponent<GameStateScript>();

        Vector3 rotateVal;
            //use the webcam for controls
            if (state.UseCamControls())
        {
            float angle = WebCam.Instance.GetAngle() * turningRateCamera;
            //threshold values to prevent rotating too far.
            if (angle > cameraLimit)
            {
                angle = cameraLimit;
            }
            if (angle < -cameraLimit)
            {
                angle = -cameraLimit;
            }
            //convert angle to be within 0 to 360 range.
            if (angle < 0)
            {
                angle = 360 + angle;
            }
            rotateVal = new Vector3(transform.eulerAngles.x, transform.eulerAngles.y, angle);
            }
        //use keyboard based controls.
        else
        {
            float rotHorizontal = Input.GetAxis("Horizontal");//keypress value
            float curAngle = transform.eulerAngles.z;
            float delta = rotHorizontal * turningRateKeyboard;
            float nextAngle = (curAngle + delta) % 360;
            if (nextAngle >= cameraLimit && nextAngle <= 360 - cameraLimit)
            {
                if (Math.Abs(cameraLimit - nextAngle) > Math.Abs(nextAngle - (360 - cameraLimit)))
                {
                    nextAngle = 360 - cameraLimit;
                }
                else
                {
                    nextAngle = cameraLimit;
                }
            }
            rotateVal = new Vector3(transform.eulerAngles.x, transform.eulerAngles.y, nextAngle);
            }
        //only do the update while game isn't paused
        if (!state.IsGamePaused())
        {
            transform.rotation = Quaternion.RotateTowards(transform.rotation, Quaternion.Euler(rotateVal), turnUpdateSpeed * Time.deltaTime);

        }
    }
    // LateUpdate is called once per frame -- garaunteed to run after all items (e.g. player has moved)
    void LateUpdate()
    {
        //float rotHorizontal = Input.GetAxis("Horizontal");
        PlayerController pc = player.GetComponent<PlayerController>();
        transform.position = player.transform.position + offset;
    }
}
