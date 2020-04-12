using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

public class WebCamRequester : RunAbleThread
{
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5555");//connect to server
            while (Running)
            {
                Debug.Log("Waiting for Angle");
                client.SendFrame("angle");
                string response = null;
                response = client.ReceiveFrameString();
                Debug.Log("Angle:" + response);
            }
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}
