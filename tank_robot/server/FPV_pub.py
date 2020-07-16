#!/usr/bin/env/python3
# FPV_pub heavily modified by PHIL - use this one PHIL!


import time
import threading
import cv2
import zmq
import base64
import picamera
from picamera.array import PiRGBArray
import argparse
import imutils
from collections import deque
import psutil
import os
import servo
import ultra
import PID
import LED
import datetime
from rpi_ws281x import *
import move

pid = PID.PID()
pid.SetKp(0.5)
pid.SetKd(0)
pid.SetKi(0)
Y_lock = 0
X_lock = 0
tor    = 17
FindColorMode = 0
WatchDogMode  = 0 
UltraData = 3
LED  = LED.LED()
camera = None

ap = argparse.ArgumentParser()            #OpenCV initialization
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
pts = deque(maxlen=args["buffer"])

font = cv2.FONT_HERSHEY_SIMPLEX

camera = picamera.PiCamera() 
camera.resolution = (640, 480)
camera.framerate =  6 #20 this is original
rawCapture = PiRGBArray(camera, size=(640, 480))



class FPV: 
    def __init__(self):
        self.frame_num = 0
        self.fps = 0
        self.stream_on = False  

        # orange-yellowish
        self.colorUpper = (54, 255, 255)
        self.colorLower = (24, 100, 100)

        if FindColorMode:
            move.setup()

    def set_stream(self,on):
        self.stream_on = on
        print("//////////////////////////////////")
        print("[FPV_pub.py] stream is now: {}".format(on))
        print("[FPV_pub.py] FindColorMode: {}".format(FindColorMode))
        print("[FPV_pub.py] WatchDogMode: {}".format(WatchDogMode))

        #if on:
        #    self.capture_thread()

    def SetIP(self,invar):
        self.IP = invar


    def FindColor(self,invar):
        global FindColorMode
        FindColorMode = invar
        if not FindColorMode:
            servo.camera_ang('home',0)
        if invar:
            print('FindColorMode enabled')
            if WatchDogMode:
                self.WatchDog(0)
        else:
            print('FindColorMode disabled')

    def WatchDog(self,invar):
        global WatchDogMode
        WatchDogMode = invar
        if invar:
            print('WatchDogMode enabled')
            if FindColorMode:
                self.FindColor(0)
        else:
            print('WatchDogMode disabled')


    def UltraData(self,invar):
        global UltraData
        UltraData = invar



    def find_color_fnc(self, frame_image):
        
        ####>>>OpenCV Start<<<####
        hsv = cv2.cvtColor(frame_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            cv2.putText(frame_image,'Target Detected',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            X = int(x)
            Y = int(y)
            if radius > 10:
                cv2.rectangle(frame_image,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),(255,255,255),1)

            if Y < (240-tor):
                error = (240-Y)/5
                outv = int(round((pid.GenOut(error)),0))
                servo.camera_ang('lookup',outv)
                Y_lock = 0
            elif Y > (240+tor):
                error = (Y-240)/5
                outv = int(round((pid.GenOut(error)),0))
                servo.camera_ang('lookdown',outv)
                Y_lock = 0
            else:
                Y_lock = 1

            
            if X < (320-tor*3):
                move.move(70, 'no', 'left', 0.6)
                time.sleep(0.1)
                #move.motorStop()
                X_lock = 0
            elif X > (330+tor*3):
                move.move(70, 'no', 'right', 0.6)
                time.sleep(0.1)
                #move.motorStop()
                X_lock = 0
            else:
                move.motorStop()
                X_lock = 1

            if X_lock == 1: # and Y_lock == 1:
                UltraData = ultra.checkdist()
                if UltraData > 3:
                    move.motorStop()
                elif UltraData > 0.5:
                    move.move(70, 'forward', 'no', 0.6)
                elif UltraData < 0.4:
                    move.move(70, 'backward', 'no', 0.6)
                    print(UltraData)
                else:
                    move.motorStop()

        else:
            cv2.putText(frame_image,'Target Detecting',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
            move.motorStop()

        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame_image, pts[i - 1], pts[i], (0, 0, 255), thickness)
        ####>>>OpenCV Ends<<<####

        return frame_image, mask

    def watchdog_mode_fnc(self, frame_image):
        global avg, motionCounter, lastMotionCaptured, timestamp

        timestamp = datetime.datetime.now()

        gray = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if avg is None:
            print("[INFO] starting background model...")
            avg = gray.copy().astype("float")
            return frame_image # just return, dont draw rects on it

        cv2.accumulateWeighted(gray, avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        #print('x')
     
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 5000:
                continue
     
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame_image, (x, y), (x + w, y + h), (128, 255, 0), 1)
            text = "Occupied"
            motionCounter += 1
            #print(motionCounter)
            #print(text)
            #LED.colorWipe(Color(255,16,0))
            lastMotionCaptured = timestamp

        if (timestamp - lastMotionCaptured).seconds <= 0.1:
            #LED.colorWipe(Color(255,255,0))
            #print('WATCHDOG : Motion Detected! {}'.format(motionCounter))
            cv2.putText(frame_image, 'WATCHDOG : Motion Detected! {}'.format(motionCounter), (10,30), \
                cv2.FONT_HERSHEY_COMPLEX,0.8,(128,255,0),1)
        return frame_image


    def capture_thread(self):

        footage_socket = setup_pub(5555)
        mask_socket    = setup_pub(5556)

        # for watchdog
        global avg, motionCounter, lastMotionCaptured, timestamp
        avg = None
        motionCounter = 0
        #time.sleep(4)
        lastMotionCaptured = datetime.datetime.now()
        timestamp = datetime.datetime.now()

        num_frames=0

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            while self.stream_on == False: # TODO need way to flush buffer ...?
                time.sleep(0.3)
                rawCapture.truncate(0)
                continue
                

            frame_image = frame.array

            if FindColorMode:
                frame_image, mask = self.find_color_fnc(frame_image)   

            if WatchDogMode:
                frame_image = self.watchdog_mode_fnc(frame_image)

            cv2.line(frame_image,(300,240),(340,240),(128,255,128),1)
            cv2.line(frame_image,(320,220),(320,260),(128,255,128),1)
            dist = str(ultra.checkdist())
            cv2.putText(frame_image,dist,(340,260),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            timestamp = datetime.datetime.now()

            send_mask=False
            if send_mask: # TODO probs should do socket creation in init ..
                print('sending mask frame')
                send_frame(mask, mask_socket)

            blend_images=FindColorMode
            if blend_images:
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                frame_image = cv2.addWeighted( frame_image, 1.0, mask, 0.5, 0.0 )

            send_frame(frame_image, footage_socket)
            print('sent frame {}'.format(num_frames))
            num_frames += 1
            #time.sleep(1)

            rawCapture.truncate(0)

def destroy():
    global camera
    camera.close()
    print('camera closed')
    # TODO add unset sockets

def setup_pub(port): # connect / bind doesn't matter?
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    #footage_socket.bind('tcp://*:5555')
    IP = '192.168.1.224'
    socket.connect("tcp://{}:{}".format(IP,port))
    return socket   
def send_frame(img,socket):
    encoded, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    socket.send(jpg_as_text)   



if __name__ == '__main__':
    try:
        fpv=FPV()
        fpv.set_stream(1)
        fpv.FindColor(1)
        while 1:
            fpv.capture_thread()
            pass
    except KeyboardInterrupt:
        camera.close()
        if FindColorMode:
            move.destroy()




