using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EndTrigger : MonoBehaviour
{
    public GameStateScript gameState;
    private void OnTriggerEnter(Collider other)
    {
        gameState.CompleteLevel();
    }
}
