using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float gravitySpeed;
    public GameObject camera;
    public GameObject gamestate;
    private Rigidbody rb;
    private Vector3 oldVelocity;
    private bool stopped = false;
    private void Start()
    {
        rb = GetComponent<Rigidbody>();
    }
    private void Update()
    {
        GameStateScript state = gamestate.GetComponent<GameStateScript>();
        if (!state.IsGamePaused()) {
            if (Input.GetKeyDown(KeyCode.Space) && !stopped)
            {
                FreezePlayer();
                //Debug.Log("Down, not stopped");
            }
            if (Input.GetKeyUp(KeyCode.Space) && stopped)
            {
                UnFreezePlayer();
                //Debug.Log("Up, stopped");
            }
        }
    }
    //physics related code
    private void FixedUpdate()
    {
        GameStateScript state = gamestate.GetComponent<GameStateScript>();
        Vector3 dir = Quaternion.AngleAxis(-camera.transform.eulerAngles.z, Vector3.up) * Vector3.back;//gravity should always be in the direction of the camera

        if (!stopped) {
            rb.AddForce(gravitySpeed * dir);
        }
    }
    public void FreezePlayer()
    {
        oldVelocity = rb.velocity;
        rb.velocity = Vector3.zero;
        stopped = true;
    }
    public void UnFreezePlayer()
    {
        rb.velocity = oldVelocity;
        oldVelocity = Vector3.zero;
        stopped = false;

    }
}
