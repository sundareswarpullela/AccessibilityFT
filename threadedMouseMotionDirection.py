import math
from threading import *
from time import sleep
import cv2
import pyautogui as mauto
import sys
mauto.PAUSE = 0.0
mauto.FAILSAFE = False

#Variables
centerv = (320, 240)
faceCenter = (0,0)
pos = (0,0)
#OPEN-CV
cam = cv2.VideoCapture(0)
faceCascPath = 'haarcascades\haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(faceCascPath)
window = {"Xm":0 , "Ym":0, "XM":1920, "YM": 1080}
left = ((0,0), (0,1080))
right = ((1920, 0), (1920, 1080))
top = ((0,0), (1920, 0))
bottom = ((0,1080), (1920, 1080))
stop = False

def getSlope(point1, point2):
    delX = point2[0] - point1[0]
    delY = point2[1] - point1[1]
    return [delY, delX]

def secondPoint(point, slope):
    y = slope[0] + point[1]
    x = slope[1] + point[0]
    return (x,y)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    div = det(xdiff, ydiff)
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return (x, y)

def getDistance(point1, point2):
    x1,y1 = point1
    x2,y2 = point2
    return (math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

def getAngle(point1, point2):
    x1,y1 = point1
    x2,y2 = point2
    radians = math.atan2(y2-y1,x2-x1)
    return radians * (180 / math.pi)


def getBorderIntersect(point1, point2):
    angle = getAngle(point1, point2)
    line = (point1, point2)
    if(-135 <= angle <= -45):
        print("bottom")
        return line_intersection(bottom, line)
    elif(-45 <= angle <= 45):
        print("left")
        return line_intersection(left, line)
    elif(45 <= angle <= 135):
        print("top")
        return line_intersection(top, line)
    elif(-180 <= angle <= -135 or 135 <= angle <= 180):
        print("right")
        return line_intersection(right, line)

def incircle(point, center, radius):
    if(getDistance(center, point) <= radius):
        # print("Inside")
        return True
    return False

def distanceToSpeed():
    return 130 - int(getDistance(centerv, faceCenter))


class CV(Thread):
    def run(self):
        print("CV Thread")
        global faceCenter
        global pos
        while(True):
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray,5,1,1) 
            faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=6,minSize=(20, 20),flags = cv2.CASCADE_SCALE_IMAGE)
            #print("Found {0} face!".format(len(faces)))

            try:
                cv2.circle(frame, centerv, 10, (0, 255, 0), 2)
                cv2.circle(frame, centerv, 100, (0, 255, 0), 2)
                for (x, y, w, h) in faces:
                    faceCenter = (x+w // 2, y + (h // 2))
                    cv2.circle(frame, faceCenter, 1, (0, 255, 0), 2)
                    cv2.line(frame, faceCenter, centerv, (0, 255, 0), 2)
                    #print(faceCenter)
                    #print(getAngle(centerv, faceCenter))
                    pos = getBorderIntersect(mauto.position(), secondPoint(mauto.position(), getSlope(faceCenter, centerv)))
                    #print(pos)
            except: pass
            cv2.imshow("Faces found", frame)
            if cv2.waitKey(1) == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                break



def mouserun():
    total_time = 100  # in milliseconds
    # total_time = distanceToSpeed()
    draw_steps = 1000  # total times to update cursor
    step_time = total_time / draw_steps
    x0,y0 = mauto.position()
    xf, yf = pos
    dx = (xf-x0)/draw_steps
    dy = (yf-y0)/draw_steps
    for n in range(draw_steps):
        if(incircle(faceCenter, centerv, 100) and pos == (xf,yf) and not incircle(faceCenter, centerv, 10)):
            x = int(x0+dx*n)
            y = int(y0+dy*n)
            mauto.moveTo(x,y, duration = step_time, _pause = False)  
        else:
            break


if __name__ == "__main__":
    cv = CV()
    cv.start()
    while(cv.is_alive()):
        mouserun()
