using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpinWheel : MonoBehaviour
{
    public  float rotateSpeed = 1;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        Vector3 rotate = new Vector3(0,rotateSpeed,0);
        transform.eulerAngles = transform.eulerAngles + rotate;
    }
}
