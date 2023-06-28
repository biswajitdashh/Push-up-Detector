import time
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np

cap = cv2.VideoCapture(0)

detect = PoseDetector()
ptime = 0 #currentime
ctime = 0 #previoustime
direction = 0
pushup = 0
color = (0,0,255)
test = 0
while True:
    _, img = cap.read()
    detect.findPose(img)
    lmarklist, boundbox = detect.findPosition(img,draw=False)
    if lmarklist:
        a1 = detect.findAngle(img, 12, 14, 16)
        a2 = detect.findAngle(img, 15, 13, 11)
        performval1 = int(np.interp(a1, (90, 180), (100, 0)))
        performval2 = int(np.interp(a1, (90, 180), (100, 0)))
        barval1 = int(np.interp(performval1, (0, 100), (45+350, 45)))
        barval2 = int(np.interp(performval2, (0, 100), (45 + 350, 45)))
        #1st bar
        cv2.rectangle(img, (570, barval2), (570 + 35, 45 + 350), color, cv2.FILLED)
        cv2.rectangle(img,(570,45),(570+35,45+350),(),4)
        #2nd bar
        cv2.rectangle(img, (35, barval1), (35 + 35, 45 + 350), color, cv2.FILLED)
        cv2.rectangle(img, (35, 45), (35 + 35, 45 + 350), (), 4)
        #bar1%
        cvzone.putTextRect(img,f'{performval2}%',  (30, 30), 1.3, 2, colorT=(255, 255, 255), colorR=color,border=3, colorB=())
        #bar2%
        cvzone.putTextRect(img, f'{performval2}%', (570, 30), 1.3, 2, colorT=(255, 255, 255), colorR=color,border=3, colorB=())
        #pushup counting logic
        if performval1 == 100 and performval2 == 100:
            if direction == 0:
                pushup += 0.5
                direction = 1
                color = (0, 255, 0)
                test = 0
        elif performval1 == 0 and performval2 == 0:
            if direction == 1:
                pushup += 0.5
                direction = 0
                color = (0, 255, 0)
                test += 1
        else:
            color = (0, 0, 255)
        if test == 1:
            cvzone.putTextRect(img, 'Its a Push-up', (175, 475), 2, 2, colorT=(255, 255, 255), colorR=(255, 0, 0),border=3, colorB=())
        else:
            cvzone.putTextRect(img, 'Its not a Push-up', (175, 475), 2, 2, colorT=(255, 255, 255), colorR=(255, 0, 0),border=3, colorB=())

        cvzone.putTextRect(img,f'Push-ups:{int(pushup)}',(228,35), 2, 2,colorT=(255,255,255),colorR=(255, 0, 0),border=3,colorB=())
        cvzone.putTextRect(img,'Left Hand', (15, 358+68), 2, 2, colorT=(255, 255, 255), colorR=(255, 0, 0),border=3, colorB=())
        cvzone.putTextRect(img,'Right Hand', (445, 350+80), 2, 2, colorT=(255, 255, 255), colorR=(255, 0, 0),border=3, colorB=())

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cvzone.putTextRect(img,f'FPS : {int(fps)}',(270,420),1.6,2,colorT=(255,255,255),colorR=(0,135),border=3,colorB=())
    cv2.imshow('Pushup Detector',img)
    if cv2.waitKey(1) == ord('x'):
        break




