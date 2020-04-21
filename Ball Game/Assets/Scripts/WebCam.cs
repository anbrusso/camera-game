using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WebCam : MonoBehaviour
{
    private static WebCam _instance;
    public static WebCam Instance
    {
        get
        {
            return _instance;
        }
    }

    private WebCamRequester webcam;
    private void Awake()
    {
        if (_instance != null && _instance != this)
        {
            Destroy(this.gameObject);
        }
        else
        {
            _instance = this;
            webcam = new WebCamRequester();
            webcam.Start();
        }

    }

    private void OnDestroy()
    {
        if (webcam != null)
        {
            webcam.Stop();
        }
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
