using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using System;
using UnityEngine;

public class WebCamRequester : RunAbleThread
{
    static TimeSpan timout = TimeSpan.FromMilliseconds(1000);
    private float headAngle = 0;
    private bool is_eyes_closed = false;
    private bool connected = false;
    protected override void Run()
    {
        while (Running)
        {   
            //try connecting to the server
            connected = false;
            try
            {
                ForceDotNet.Force();
                using (RequestSocket client = new RequestSocket())
                {
                    string angle = null;
                    string eyes_closed = null;
                    client.Connect("tcp://localhost:5555");//connect to server
                                                            //repeatedly send/receive packets to the server to get the angle.
                    while (Running)
                    {
                        //ask for an angle. If we can't send/receive for over a second, then assume that the server went down.
                        if (client.TrySendFrame("a") && client.TryReceiveFrameString(timout, out angle) && Running)
                        {
                            headAngle = float.Parse(angle);
                            //ask for whether the eyes are closed
                            if (client.TrySendFrame("e") && client.TryReceiveFrameString(timout, out eyes_closed) && Running)
                            {
                                is_eyes_closed = bool.Parse(eyes_closed);
                                connected = true;
                            }
                            //Debug.Log("Connected");
                        }
                        else
                        {
                            connected = false;
                            //Debug.Log("Disconnected");
                        }
                    }
                }
                NetMQConfig.Cleanup();
            }
            catch (Exception)
            {
                NetMQConfig.Cleanup();
                //Debug.Log("Connection Failed.");
                //Debug.Log(e.StackTrace);
            }
        }
    }
    public bool IsConnected()
    {
        return connected;
    }
    public float GetAngle()
    {
        return headAngle;
    }
    public bool IsEyesClosed()
    {
        return is_eyes_closed;
    }
}
