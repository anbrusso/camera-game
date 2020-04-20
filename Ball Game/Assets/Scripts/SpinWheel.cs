using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpinWheel : MonoBehaviour
{
    public  float rotateSpeed = 1;
    public GameObject gamestate;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        Vector3 rotate = new Vector3(0,rotateSpeed,0);
        GameStateScript state = gamestate.GetComponent<GameStateScript>();
        if (!state.IsGamePaused()) {
            transform.eulerAngles = transform.eulerAngles + rotate;
        }
    }
}
