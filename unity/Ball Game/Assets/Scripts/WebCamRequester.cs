using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using System;
using UnityEngine;

public class WebCamRequester : RunAbleThread
{
    static TimeSpan timout = TimeSpan.FromMilliseconds(1000);
    public float headAngle = 0;
    public bool connected;
    private float timer = 0;
    private bool reconnectTimeout = false;
    protected override void Run()
    {
        while (Running)
        {   
            //if connection failed, wait 5 seconds before reconnecting.
           /* if (reconnectTimeout)
            {
                Debug.Log("Reconnect Timout....");
                if (timer < 5)
                {
                    timer += Time.deltaTime;
                }
                else
                {
                    reconnectTimeout = false;
                    timer = 0;
                    Debug.Log("Reconnect Timout lapsed, Retrying");
                }
            }
            else
            {*/
                //try connecting to the server
                connected = false;
                try
                {
                    ForceDotNet.Force();
                    using (RequestSocket client = new RequestSocket())
                    {
                        string angle = null;
                        client.Connect("tcp://localhost:5555");//connect to server
                                                               //repeatedly send/receive packets to the server to get the angle.
                        while (Running)
                        {
                            //ask for an angle. If we can't send/receive for over a second, then assume that the server went down.
                            if (client.TrySendFrame("a") && client.TryReceiveFrameString(timout, out angle) && Running)
                            {
                                headAngle = float.Parse(angle);
                                connected = true;
                                Debug.Log("Connected");
                            }
                            else
                            {
                                connected = false;
                                Debug.Log("Not connected");
                            }
                        }
                    }
                    NetMQConfig.Cleanup();
                }
                catch (Exception e)
                {
                    reconnectTimeout = true;
                    NetMQConfig.Cleanup();
                    Debug.Log("Connection Failed.");
                    //Debug.Log(e.StackTrace);
                }
            //}
        }
    }
}
