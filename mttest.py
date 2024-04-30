
from threading import Thread
import cv2, time
centerv = (320, 240)
faceCenter = (0,0)
pos = (0,0)
#OPEN-CV
cam = cv2.VideoCapture(0)
faceCascPath = 'haarcascades\haarcascade_frontalface_default.xml'
#eyesCascPath = 'haarcascade_eye.xml'
faceCascade = cv2.CascadeClassifier(faceCascPath)
window = {"Xm":0 , "Ym":0, "XM":1920, "YM": 1080}
left = ((0,0), (0,1080))
right = ((1920, 0), (1920, 1080))
top = ((0,0), (1920, 0))
bottom = ((0,1080), (1920, 1080))
stop = False

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(.01)

    def show_frame(self):
        # Display frames in main program
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)
        return self.frame
    def get_frame(self):
        return self.frame

def prepare_frame(frame):
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray,5,1,1) 
    return gray


def detect_face(frame):
    faces = faceCascade.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=6,minSize=(20, 20),flags = cv2.CASCADE_SCALE_IMAGE)
    return faces

if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget()
    while True:
        try:
            frame = video_stream_widget.show_frame()

        except AttributeError:
            pass