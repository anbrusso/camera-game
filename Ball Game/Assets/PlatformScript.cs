using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlatformScript : MonoBehaviour
{

    public Vector3 startPos;
    public Vector3 endPos;
    private Vector3 targetPos;
    public float movementSpeed;
    public GameObject gamestate;
    public bool forward;
    private void Start()
    {
    }
    private void Update()
    {

        GameStateScript state = gamestate.GetComponent<GameStateScript>();
        if (!state.IsGamePaused())
        {
            if (forward)
            {
                targetPos = endPos;
            }
            else
            {
                targetPos = startPos;
            }
            transform.localPosition = Vector3.MoveTowards(transform.localPosition, targetPos, movementSpeed);

            if (transform.localPosition == endPos)
            {
                forward = false;
            }
            else if (transform.localPosition == startPos)
            {
                forward = true;

            }
        }
    }
}
