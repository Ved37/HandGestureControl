# Hand Gesture Control Project

## Overview

This project enables hand gesture control for various functionalities, including mouse control, volume adjustment, media controls, and a keyboard menu. It offers a unique and intuitive way to interact with your computer using hand gestures.

## Getting Started

To run the program, follow these steps:

1. Set up Python 3.7 as your interpreter.
2. Initialize the required Python modules using the following command:
    ```bash
    pip install opencv mediapipe==9.0.1 numpy autopy pycaw pyautogui
    ```
3. Once the above steps are completed, run the `Gesture_Control.py` file.

**Note:**
- The project includes three important files: `Gesture_Control.py`, `HandTrackingModule.py`, and `Keyboard.py`. Others are experimental or trial files.

## Functionalities

### Mouse Control
- To Hover: Freely move your index finger while keeping all other fingers down
![Finger Mouse](https://github.com/Ved37/HandGestureControl/assets/77605086/b3581e51-3a93-4fbf-86d0-2bac88cad669)
- To click: touch the middle and index finger tips.

### Volume Control
- Open your palm, and the distance between the tip of your index finger and thumb determines the volume.
![Volume Change](https://github.com/Ved37/HandGestureControl/assets/77605086/c6117cc6-8691-4d25-978c-c2b24c61a4b3)

### Media Controls
- Keep in mind to keep thumb down always
- To Play/Pause: lower your index finger 90 degrees.
![Play/Pause](https://github.com/Ved37/HandGestureControl/assets/77605086/28eaf951-b69c-40d4-9783-4caf29f3bbd6)
- To Seek Forwards: lower your pinky finger 90 degree.
![Fast Forward](https://github.com/Ved37/HandGestureControl/assets/77605086/2533fc4f-93e6-4ec9-b585-eec4bf13920e)
- To Seek Backwards: lower your ring finger 90 degree.
![Backward](https://github.com/Ved37/HandGestureControl/assets/77605086/a49ae006-15d7-42f4-8972-b83788583548)

### Keyboard Menu
- Click the Keyboard button on the top right corner using your click gesture to open the keyboard menu.
- Use gesture clicks to input characters. To return to the main menu, click on the Main button, and to exit, click on the Exit button.
![Keyboard](https://github.com/Ved37/HandGestureControl/assets/77605086/b8b166f5-463b-496c-b607-335fbd549ed4)

## Key Aspects
   - Pinky, ring finger, and thumb down: Mouse control.
   - All fingers up: Volume control.
   - Thumb down: Media controls.

**Inspiration:**
   - This project is inspired by Murtaza's Workshop - Robotics and AI's YouTube Channel [(@murtazasworkshop)](https://www.youtube.com/@murtazasworkshop).





 





