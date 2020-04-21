using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameStateScript : MonoBehaviour
{
    private bool camControls = false;
    private bool isPaused = true;
    private bool isStarting = false;
    private bool hasEnded = false;
    public GameObject NoCamWarningText;
    public GameObject CamWarningText;
    public GameObject player;
    public GameObject countdownTimer;
    public GameObject completeLevelUI;
    public float startDelay;//2f;
    // Start is called before the first frame update
    void Start()
    {
        //if cam is connected, already, we can just start the game
        if (WebCam.Instance.IsConnected())
        {
            camControls = true;
            PauseGame();
            StartGame();
        }
        else
        {
            camControls = false;
            //otherwise start off paused with the warning
            NoCamWarningText.SetActive(true);
            CamWarningText.SetActive(false);
            PauseGame();
        }
    }

    // Update is called once per frame
    void Update()
    {
        //Debug.Log("Pause " + IsGamePaused() + " CamControls" + UseCamControls());
        if (isPaused && !isStarting){
            //Debug.Log("Paused");
            if (WebCam.Instance.IsConnected())
            {
                //Debug.Log("Camera");
                if (!UseCamControls())
                {
                    //Debug.Log("No Camera Controls");
                    NoCamWarningText.SetActive(false);
                    CamWarningText.SetActive(true);
                    //they want to start the game with camera controls
                    if (Input.GetKeyUp(KeyCode.Space))
                    {
                        //Debug.Log("Starting with camera...");
                        camControls = true;
                        NoCamWarningText.SetActive(false);
                        CamWarningText.SetActive(false);
                        StartGame();
                    }
                    //they want to start the game without camera controls
                    if (Input.GetKeyUp(KeyCode.Escape))
                    {
                        //Debug.Log("Starting without camera...");
                        camControls = false;
                        NoCamWarningText.SetActive(false);
                        CamWarningText.SetActive(false);
                        StartGame();
                    }
                }
            }
            else
            {
                NoCamWarningText.SetActive(true);
                CamWarningText.SetActive(false);
                //Debug.Log("No Camera");
                //they want to start the game without a camera
                if (Input.GetKeyUp(KeyCode.Space))
                {
                    //Debug.Log("Starting...");
                    camControls = false;
                    NoCamWarningText.SetActive(false);
                    CamWarningText.SetActive(false);
                    StartGame();
                }
            }
        }
        //during normal game play, not as much to think about.
        else
        {
            //if the camera disconnected, then we have to pause the game and show the warning.
            if (!WebCam.Instance.IsConnected() && UseCamControls())
            {
                //Debug.Log("Pausing Because No Camera");
                NoCamWarningText.SetActive(true);
                CamWarningText.SetActive(false);
                PauseGame();
            }
        }
    }
    public void PauseGame() {
        isPaused = true;
        PlayerController play = player.GetComponent<PlayerController>();
        play.FreezePlayer();
        //Debug.Log("Game Paused");
    }
    public void UnPauseGame()
    {
        isPaused = false;
        isStarting = false;
        PlayerController play = player.GetComponent<PlayerController>();
        play.UnFreezePlayer();
        //Debug.Log("Game Unpaused");
    }
        public bool IsGamePaused()
    {
        return isPaused;
    }
    public bool UseCamControls()
    {
        return camControls;
    }

    public void StartGame()
    {
        //Debug.Log("Starting Game");
        PlayerController play = player.GetComponent<PlayerController>();
        isStarting = true;
        NoCamWarningText.SetActive(false);
        CamWarningText.SetActive(false);
        CountDownController cd = countdownTimer.GetComponent<CountDownController>();
        cd.countdownDisplay.gameObject.SetActive(true);
        cd.BeginTimer();
        Invoke("UnPauseGame", startDelay);//wait a little bit to start
    }
    public void CompleteLevel()
    {
        hasEnded = true;
        completeLevelUI.SetActive(true);
    }
}

