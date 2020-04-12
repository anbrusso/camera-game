using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WebCam : MonoBehaviour
{
    private WebCamRequester webcam;
    void Start()
    {
        webcam = new WebCamRequester();
        webcam.Start();
    }

    private void OnDestroy()
    {
        webcam.Stop();
    }
}
