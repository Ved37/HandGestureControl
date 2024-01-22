import sys
import cv2
import HandTrackingModule as htm
from time import sleep
import pyautogui as p
import os

wCam, hCam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector(maxHands=1)

keys=[["Q","W","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L",";"],
      ["Z","X","C","V","B","N","M",",",".","/"]]

def drawAll(img,buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 8, y + 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    cv2.rectangle(img, (310, 10), (410, 40), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, "Exit", (330, 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.rectangle(img, (430, 10), (600, 40), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, "Main", (480, 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.rectangle(img,(20,230),(250,280),(255,0,255),cv2.FILLED)
    cv2.putText(img,"Space",(90,265),cv2.FONT_HERSHEY_PLAIN,2,(255, 255, 255),3)

    cv2.rectangle(img,(260,230),(450,280),(255,0,255),cv2.FILLED)
    cv2.putText(img,"Backspace",(270,265),cv2.FONT_HERSHEY_PLAIN,2,(255, 255, 255),3)

    cv2.rectangle(img, (460, 230), (610, 280), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, "Enter", (490, 265), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    return img

class Button():
    def __init__(self,pos,text,size=[50,50]):
        self.pos=pos
        self.size=size
        self.text=text

buttonList=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([j * 60 + 20, 60 * i + 50], key))

success=True
while success:
    success, img = cap.read()
    img=detector.findHands(img)
    lmList,_=detector.findPosition(img)

    img=drawAll(img,buttonList)



    if (len(lmList)!=0):
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x<lmList[8][1]<x+w and y<lmList[8][2]<y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175,0,175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 8, y + 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                if (l < 40):
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    p.press(button.text)
                    sleep(0.15)

            if 20 < lmList[8][1] < 250 and 230 < lmList[8][2] < 280:
                cv2.rectangle(img, (20, 230), (250, 280), (175,0,175), cv2.FILLED)
                cv2.putText(img, "Space", (70, 270), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                if (l < 40):
                    cv2.rectangle(img, (20, 230), (250, 280), (0,255,0), cv2.FILLED)
                    p.press("Space")
                    sleep(0.15)

            if 260 < lmList[8][1] < 450 and 230 < lmList[8][2] < 280:
                cv2.rectangle(img, (260, 230), (450, 280), (175,0,175), cv2.FILLED)
                cv2.putText(img, "Backspace", (270, 265), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                if (l < 40):
                    cv2.rectangle(img, (260, 230), (450, 280), (0,255,0), cv2.FILLED)
                    p.press("Backspace")
                    sleep(0.15)

            if 460 < lmList[8][1] < 610 and 230 < lmList[8][2] < 280:
                cv2.rectangle(img, (460, 230), (610, 280), (175,0,175), cv2.FILLED)
                cv2.putText(img, "Enter", (490, 265), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                if (l < 40):
                    cv2.rectangle(img, (460, 230), (610, 280), (0,255,0), cv2.FILLED)
                    p.press("Enter")
                    sleep(0.15)

            if 430 < lmList[8][1] < 600 and 10 < lmList[8][2] < 40:
                cv2.rectangle(img, (430, 10), (600, 40), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, "Main", (480, 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                # Run the Main Python script
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                if (l < 40):
                    cv2.rectangle(img, (430, 10), (600, 40), (0, 255, 0), cv2.FILLED)
                    # sys.exit()
                    success = False
                    cv2.destroyWindow("Keyboard")
                    cap.release()
                    os.system("Gesture_Control.py")

            if 310 < lmList[8][1] < 410 and 10 < lmList[8][2] < 40:
                cv2.rectangle(img, (310, 10), (410, 40), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, "Exit", (330, 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                if (l < 40):
                    sys.exit()

    cv2.imshow("Keyboard", img)  # display
    cv2.waitKey(1)