import cv2
import sys
import pyautogui as auto
auto.PAUSE = 0
import mouse

#Variables
centerv = (320, 240)
rectHeight,rectWidth = 60, 108
window = {"Xm":0 , "Ym":0, "XM":1920, "YM": 1080}
rectangle = {"Xm":centerv[0] - rectWidth, "Ym":centerv[1] - rectHeight, "XM":centerv[0] + rectWidth, "YM":centerv[1] + rectHeight}
tlv, brv = (rectangle["Xm"], rectangle["Ym"]), (rectangle["XM"], rectangle["YM"])
sx = (rectangle["XM"] - rectangle["Xm"]) / (window["XM"] - window["Xm"])
sy = (rectangle["YM"] - rectangle["Ym"]) / (window["YM"] - window["Ym"])
mousex, mousey = centerv
def inRect(x,y):
    if(tlv[0] <= x <=brv[0] and tlv[1] <= y <=brv[1]):
        return True
    return False


def rectToWindow(point):
    xw = ((point[0] - rectangle["Xm"])/ sx) + window["Xm"]
    yw = ((point[1] - rectangle["Ym"]) / sy) + window["Ym"]
    return [xw,yw]


def invertX(max,x):
    return window["XM"] - x



#OPEN-CV
cam = cv2.VideoCapture(0)
faceCascPath = 'haarcascades\haarcascade_frontalface_default.xml'
#eyesCascPath = 'haarcascade_eye.xml'
faceCascade = cv2.CascadeClassifier(faceCascPath)
paused = False

#mouse.move(1280 // 2, 720 // 2)

while(True):
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray,5,1,1) 
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(20, 20),flags = cv2.CASCADE_SCALE_IMAGE)
    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    try:
        cv2.rectangle(frame, tlv, brv, (0, 255, 0), 2)
        cv2.circle(frame, centerv, 2, (0, 255, 0), 5)
        for (x, y, w, h) in faces:
            cv2.circle(frame, (640//2, 480//2), 2, (0, 255, 0), 5)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            faceCenter = (x+w // 2, y + (h // 2))
            cv2.circle(frame, faceCenter, 1, (0, 255, 0), 2)
            if(inRect(faceCenter[0], faceCenter[1])):
                mousex, mousey = rectToWindow(faceCenter)
                auto.moveTo(invertX(window["XM"],mousex),mousey, _pause = False)
            
    except:
        pass

    cv2.imshow("Faces found", cv2.flip(frame, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cam.release()
cv2.destroyAllWindows()