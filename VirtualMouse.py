import cv2
import mediapipe as mp
import HandTrackingModule as htm
import time
import autopy
import numpy as np

wCam, hCam=640,480
frameR=100 #frame Reduction
smoothening=7

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
        x2,y2=lmList[12][1:]   #middle finger

    #3. Check which finger are up
    fingers=detector.fingersUp()
    #print(fingers)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
    #4. if index is up then moving mode
    if(fingers!=[] and fingers[1]==1 and fingers[2]==0):
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
    #8. both index and middle finger are up then clicking mode
    if (fingers != [] and fingers[1] == 1 and fingers[2] == 1):
        # 9. find distance between fingers
        length,img,lineInfo=detector.findDistance(8,12,img)
        print(length)
        # 10. click mouse if distance is short
        if(length<35):
            cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
            autopy.mouse.click()

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3) #frame rate
    cv2.imshow("Image",img) #display
    cv2.waitKey(1)


