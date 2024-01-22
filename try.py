import cv2
import HandTrackingModule as htm
import time
import autopy
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

wCam, hCam=640,480
frameR=100 #frame Reduction
smoothening=7
#for Volume
vol=0
volBar=400
volPer=0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
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
while True:
    # 1.Find hand landamarks
    success, img = cap.read()
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)

    #2.get the tip of index and middle finger
    if(len(lmList)!=0):
        x1,y1=lmList[8][1:]   #index finger
        #x2,y2=lmList[12][1:]   #middle finger
        x2,y2=lmList[5][1:]   #index lowest point


    #3. Check which finger are up
    fingers=detector.fingersUp()
    #print(fingers)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
    #4. if index is up and thumb is down then moving mode
    if(fingers!=[] and fingers[1]==1 and fingers[2]==0 and fingers[0]==0):
    #5.convert coordinates

        x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
    #6. smoothen values
        clocX=plocX+(x3-plocX)/smoothening
        clocY = plocY + (y3 - plocY) / smoothening
    #7. move mouse
        autopy.mouse.move(wScr-clocX,clocY)
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        plocX,plocY=clocX,clocY
    #8. both index and index lowest point distance is less and thumb is down then clicking mode
    if (fingers != [] and fingers[0]==0):
    # 9. find distance between fingers
        length,img,lineInfo=detector.findDistance(8,5,img)
        print(length)
    # 10. click mouse if distance is short
        if(length<50):
            cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
            autopy.mouse.click()
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

            #print(int(length), vol)
            volume.SetMasterVolumeLevel(vol, None)
            if (length < 30):
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 3)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS:{str(int(fps))}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)  # frame rate
    cv2.imshow("Image",img) #display
    cv2.waitKey(1)


