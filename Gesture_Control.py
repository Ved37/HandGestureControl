import sys

import cv2
import HandTrackingModule as htm
import time
import autopy
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import pyautogui as p
import os

wCam, hCam=640,480
frameR=100 #frame Reduction
smoothening=7
#for Volume
vol=0
volBar=400
volPer=0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
# print(volRange)
minVol=volRange[0]
maxVol=volRange[1]


pTime=0
plocX,plocY=0,0
clocX,clocY=0,0

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector(maxHands=1)
wScr,hScr=autopy.screen.size()
#print(wScr,hScr)
success=True
while success:
    # 1.Find hand landamarks
    success, img = cap.read()
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)
    cv2.rectangle(img, (310, 20), (410, 50), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, "Exit", (330, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.rectangle(img, (430, 20), (600, 50), (255, 0, 255), cv2.FILLED)
    cv2.putText(img,"Keyboard",(440,45),cv2.FONT_HERSHEY_PLAIN,2,(255, 255, 255),2)
    #2.get the tip of index and middle finger
    if(len(lmList)!=0):
        x1,y1=lmList[8][1:]   #index finger
        x2,y2=lmList[12][1:]   #middle finger

    #3. Check which finger are up
    fingers=detector.fingersUp()
    #print(fingers)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
    #4. if index is up and thumb is down then moving mode
    if(fingers!=[] and fingers[1]==1 and fingers[2]==0 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0):
    #5.convert coordinates

        x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
    #6. smoothen values
        clocX=plocX+(x3-plocX)/smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        autopy.mouse.move(wScr-clocX,clocY)
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        plocX,plocY=clocX,clocY
    #8. both index and middle finger are up and thumb is down then clicking mode
    if (fingers != [] and fingers[1] == 1 and fingers[2] == 1 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0):
    # 9. find distance between fingers
        length,img,lineInfo=detector.findDistance(8,12,img)
        #print(length)
    # 10. click mouse if distance is short
        if(length<35):
            cv2.circle(img,(lineInfo[4],lineInfo[5]) ,15,(0,255,0),cv2.  FILLED)
            autopy.mouse.click()
        if len(lmList)!=0 and 430 < lmList[8][1] < 600 and 20 < lmList[8][2] < 50:
            cv2.rectangle(img, (430, 20), (600, 50), (175, 0, 175), cv2.FILLED)
            cv2.putText(img, "Keyboard", (440, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    #Run the Keyboard Python script
            if(length<35):
                cv2.rectangle(img, (430, 20), (600, 50), (0,255,0), cv2.FILLED)
                success=False
                cv2.destroyWindow("Main")
                cap.release()
                os.system("Keyboard.py")
    #Exit the program
        if len(lmList) != 0 and 310 < lmList[8][1] < 410 and 20 < lmList[8][2] < 50:
            cv2.rectangle(img, (310, 20), (410, 50), (175, 0, 175), cv2.FILLED)
            cv2.putText(img, "Exit", (330, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            if (length < 35):
                sys.exit()
    #11.if last three fingers up then volume change mode
    if(fingers!=[] and fingers[3]==1 and fingers[4]==1 and fingers[0]==1):
        if (len(lmList) != 0):
            # print(lmList[4])
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            # print(length)
            # Hand Range 16 170
            # vol Range -65 0

            vol = np.interp(length, [16, 160], [minVol, maxVol])
            volBar = np.interp(length, [16, 160], [400, 150])
            volPer = np.interp(length, [16, 160], [0, 100])

            print(int(length), vol)
            volume.SetMasterVolumeLevel(vol, None)
            if (length < 30):
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 3)
    #12.test
    if(fingers!=[] and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 and fingers[0]==0):
        if (len(lmList) != 0):
            #index finger pressed down then play/pause
            x3, y3 = lmList[8][1], lmList[8][2]
            x4, y4 = lmList[5][1], lmList[5][2]
            length2 = math.hypot(x4 - x3, y4 - y3)
            if(length2<60):
                p.press('space')

            #pinky finger pressed down then seek forward
            x5, y5 = lmList[20][1], lmList[20][2]
            x6, y6 = lmList[17][1], lmList[17][2]
            length3 = math.hypot(x6 - x5, y6 - y5)
            if(length3<50):
                p.press('right')

            #ring finger pressed then seek backward
            x7, y7 = lmList[16][1], lmList[16][2]
            x8, y8 = lmList[13][1], lmList[13][2]
            length4 = math.hypot(x8 - x7, y8 - y7)
            print(int(length4))
            if(length4<80):
                p.press('left')

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS:{str(int(fps))}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)  # frame rate
    cv2.imshow("Main",img) #display
    cv2.waitKey(1)