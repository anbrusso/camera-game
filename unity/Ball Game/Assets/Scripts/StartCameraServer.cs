using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class StartCameraServer : MonoBehaviour
{
    // Start is called before the first frame update
    System.Diagnostics.Process process;
    void Start()
    {
        //when the game starts, start up the python server.
        process = new System.Diagnostics.Process();
        System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
        //startInfo.UseShellExecute = false;
        startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
        startInfo.FileName = "Python.exe";
        startInfo.Arguments = "-u Assets/Scripts/camera/camera-server.py";
        process.StartInfo = startInfo;
        process.Start();
    }

    private void OnDestroy()
    {
        process.Kill();
    }
}
