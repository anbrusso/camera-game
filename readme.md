# [Unity Camera Game](https://andrew.brusso.me/projects/a-face-detection-based-unity-game)

A proof of concept for a webcam based game written in the Unity engine, with image processing done in Python using OpenCV/Dlib. The camera detection/python code is located in: [Ball Game/Assets/Scripts/camera/](https://github.com/anbrusso/camera-game/tree/master/Ball%20Game/Assets/Scripts/camera). The scripts running in the unity engine (C#) are in: [camera-game/Ball Game/Assets/Scripts](https://github.com/anbrusso/camera-game/tree/master/Ball%20Game/Assets/Scripts)

To Run:

1. Install python for windows: https://www.python.org/downloads/windows/
2. Ensure that your python PATH environment variable is set properly, so that running python -version works correctly. This was created and tested with python 3.8.1.
3. Install the requirements in requirements.txt (preferrably, inside a virtual environment): pip install -r requirements.txt
4. Open the folder Ball Game in Unity.

If all is well, you should be able to start the game in unity, and you're webcam should turn on during the main menu.
