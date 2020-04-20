using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WebCam : MonoBehaviour
{
    private WebCamRequester webcam = new WebCamRequester();
    void Start()
    {
        webcam.Start();
    }

    private void OnDestroy()
    {
        webcam.Stop();
    }

    public float GetAngle()
    {
        return webcam.GetAngle();
    }
    public bool IsConnected()
    {
        return webcam.IsConnected();
    }
}
