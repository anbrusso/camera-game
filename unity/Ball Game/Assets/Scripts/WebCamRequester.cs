using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using System;
using UnityEngine;

public class WebCamRequester : RunAbleThread
{
    static TimeSpan timout = TimeSpan.FromMilliseconds(2000);
    public float headAngle = 0;
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5555");//connect to server
            while (Running)
            {
                //Debug.Log("Waiting for Angle");
                client.SendFrame("angle");//ask for angle
                string response = null;
                //wait until we get an angle back
                while(!client.TryReceiveFrameString(timout, out response) && Running);
                headAngle = float.Parse(response);
            }
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}
