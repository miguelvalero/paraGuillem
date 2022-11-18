import json

import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt

import base64
import time
import threading
from matplotlib.patches import Circle
import random


def DirectionDetector (img, sendCommands):
    global client
    global hsvValues

    # color must be detected in the whole picture
    area = 'big'
    # color must be detected within the small rectangle
    #area = 'small'

    # Convert BGR to HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # clear LEDs
    client.publish ('clear')

    # define range of colors in HSV
    lowerYellow = np.array([hsvValues[0], 50, 50])
    upperYellow = np.array([hsvValues[1], 255, 255])

    lowerGreen = np.array([hsvValues[2], 50, 50])
    upperGreen = np.array([hsvValues[3], 255, 255])

    lowerBlueS = np.array([hsvValues[4], 50, 50])
    upperBlueS = np.array([hsvValues[5], 255, 255])

    lowerBlueL = np.array([hsvValues[6], 50, 50])
    upperBlueL = np.array([hsvValues[7], 255, 255])

    lowerPink = np.array([hsvValues[8], 50, 50])
    upperPink = np.array([hsvValues[9], 255, 255])

    lowerPurple = np.array([hsvValues[10], 50, 50])
    upperPurple = np.array([hsvValues[11], 255, 255])



    detectedColour = 'none'

    # ignore selected contour with area less that this
    minimumSize = 0

    areaBiggestContour = 0

    # for each color:
    #   find contours of this color
    #   get the biggest contour
    #   check if the contour is within the target rectangle (if area = 'small')
    #   check if the contour has the minimun area
    #   keet this contour if it is the biggest by the moment
    mask = cv.inRange(hsv, lowerYellow, upperYellow)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=5)
    mask = cv.dilate(mask, kernel, iterations=5)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        cyellow = max(contours, key=cv.contourArea)
        M = cv.moments(cyellow)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if  area == 'big' or (cX in range(210, 420) and cY in range(160, 320)):
            if cv.contourArea(cyellow) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cyellow)
                detectedColour = 'yellow'



    mask = cv.inRange(hsv, lowerGreen, upperGreen)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=5)
    mask = cv.dilate(mask, kernel, iterations=5)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        cGreen = max(contours, key=cv.contourArea)
        M = cv.moments(cGreen)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if area == 'big' or (cX in range(210, 420) and cY in range(160, 320)):
            if cv.contourArea(cGreen) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cGreen)
                detectedColour = 'green'

    mask = cv.inRange(hsv, lowerBlueS, upperBlueS)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=5)
    mask = cv.dilate(mask, kernel, iterations=5)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        cBlueS = max(contours, key=cv.contourArea)
        M = cv.moments(cBlueS)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if area == 'big' or (cX in range(210, 420) and cY in range(160, 320)):
            if cv.contourArea(cBlueS) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cBlueS)
                detectedColour = 'blue strong'

    mask = cv.inRange(hsv, lowerBlueL, upperBlueL)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=5)
    mask = cv.dilate(mask, kernel, iterations=5)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        cBlueL = max(contours, key=cv.contourArea)
        M = cv.moments(cBlueL)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if area == 'big' or (cX in range(210, 420) and cY in range(160, 320)):
            if cv.contourArea(cBlueL) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cBlueL)
                detectedColour = 'blue light'

    mask = cv.inRange(hsv, lowerPink, upperPink)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=5)
    mask = cv.dilate(mask, kernel, iterations=5)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        cPink = max(contours, key=cv.contourArea)
        M = cv.moments(cPink)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if area == 'big' or (cX in range(210, 420) and cY in range(160, 320)):
            if cv.contourArea(cPink) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cPink)
                detectedColour = 'pink'

    mask = cv.inRange(hsv, lowerPurple, upperPurple)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=5)
    mask = cv.dilate(mask, kernel, iterations=5)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        cPurple = max(contours, key=cv.contourArea)
        M = cv.moments(cPurple)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if area == 'big' or (cX in range(210, 420) and cY in range(160, 320)):
            if cv.contourArea(cPurple) > areaBiggestContour:
                areaBiggestContour = cv.contourArea(cPurple)
                detectedColour = 'purple'


    if detectedColour != 'none' and areaBiggestContour > minimumSize:
        cv.putText(img=img, text=detectedColour, org=(50, 50), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1,
                   color=(0, 0, 0), thickness=1)
        # show color in LEDs
        client.publish(detectedColour+'i')
        # send command to autopilot if required
        if sendCommands:
            if detectedColour == 'purple':
                client.publish ('drop')
                client.publish ('RTL')
            elif detectedColour == 'blue strong':
                client.publish ('go', 'North')
            elif detectedColour == 'yellow':
                client.publish('go', 'East')
            elif detectedColour == 'green':
                client.publish('go', 'West')
            elif detectedColour == 'pink':
                client.publish('go', 'South')

    # include rectanble in frame if area = 'small'
    if area == 'small':
        cv.rectangle(img, (210, 160), (420, 320), (0, 255, 0), 3)


def SendVideoStream (sendCommands):
    global sendingVideoStream
    global cap

    while sendingVideoStream:
        # Read Frame
        ret, frame = cap.read()
        if ret:
            # detect direction and insert annotation in frame
            DirectionDetector(frame, sendCommands)
            _, buffer = cv.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            client.publish('videoFrame', jpg_as_text)
        time.sleep(0.25)



def SendVideoForCalibration ():
    global sendingVideoForCalibration
    global cap

    while sendingVideoForCalibration:
        # Read Frame
        ret, frame = cap.read()
        if ret:

            cv.circle(frame, (106, 120), 50, (0, 255, 255), 3)
            cv.putText(img=frame, text='Yellow here', org=(106, 120), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.5,
                       color=(0, 255, 255), thickness=1)

            cv.circle(frame, (319, 120), 50, (0, 255, 0), 3)
            cv.putText(img=frame, text='Green here', org=(319, 120), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.5,
                       color=(0, 255, 0), thickness=1)

            cv.circle(frame, (532, 120), 50, (240, 106, 23), 3)
            cv.putText(img=frame, text='Blue Strong here', org=(532, 120), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.5,
                       color=(240, 106, 23), thickness=1)

            cv.circle(frame, (106, 360), 50, (250,240,30), 3)
            cv.putText(img=frame, text='Blue Light here', org=(106, 360), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.5,
                       color=(250,240,30), thickness=1)

            cv.circle(frame, (319, 360), 50, (139,1,240), 3)
            cv.putText(img=frame, text='Pink here', org=(319, 360), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.5,
                       color=(139,1,240), thickness=1)

            cv.circle(frame, (532, 360), 50, (240, 29, 140), 3)
            cv.putText(img=frame, text='Purple here', org=(532, 360), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.5,
                       color=(240, 29, 140), thickness=1)

            _, buffer = cv.imencode('.jpg', frame)
            # Converting into encoded bytes
            jpg_as_text = base64.b64encode(buffer)
            client.publish('videoForCalibration', jpg_as_text)
        time.sleep(0.25)


def Calibrate (frame):
    global hsvValues
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # for each color (circle) generate 50 random points
    # and keep the max and min H values
    # cabibrate yellow
    yellowCircle = Circle( (106, 120), radius=50)
    yellowMax = -1
    yellowMin = 300
    for n in range (1,50):
        x = random.randint(50,150)
        y = random.randint(70, 170)
        if yellowCircle.contains_point([x,y]):
            value = hsv[y, x][0]
            if (value > yellowMax):
                yellowMax = value
            if (value < yellowMin):
                yellowMin = value


    # cabibrate green
    greenCircle = Circle((319, 120), radius=50)
    greenMax = -1
    greenMin = 300
    for n in range (1,50):
        x = random.randint(270,370)
        y = random.randint(70, 170)
        if greenCircle.contains_point([x,y]):
            value = hsv[y, x][0]
            if (value > greenMax):
                greenMax = value
            if (value < greenMin):
                greenMin = value

    # cabibrate blue strong
    blueSCircle = Circle((532, 120), radius=50)
    blueSMax = -1
    blueSMin = 300
    for n in range (1,50):
        x = random.randint(480,580)
        y = random.randint(70, 170)
        if blueSCircle.contains_point([x,y]):
            value = hsv[y, x][0]
            if (value > blueSMax):
                blueSMax = value
            if (value < blueSMin):
                blueSMin = value

    # cabibrate blue light
    blueLCircle = Circle((106, 360), radius=50)
    blueLMax = -1
    blueLMin = 300
    for n in range(1, 50):
        x = random.randint(56, 156)
        y = random.randint(300, 400)
        if blueLCircle.contains_point([x, y]):
            value = hsv[y, x][0]
            if (value > blueLMax):
                blueLMax = value
            if (value < blueLMin):
                blueLMin = value

    # cabibrate pink
    pinkCircle = Circle((319, 360), radius=50)
    pinkMax = -1
    pinkMin = 300
    for n in range (1,50):
        x = random.randint(270,360)
        y = random.randint(310, 410)
        if pinkCircle.contains_point([x,y]):
            value = hsv[y, x][0]
            if (value > pinkMax):
                pinkMax = value
            if (value < pinkMin):
                pinkMin = value
    # cabibrate purple
    purpleCircle = Circle((532, 360), radius=50)
    purpleMax = -1
    purpleMin = 300
    for n in range (1,50):
        x = random.randint(480,580)
        y = random.randint(310, 410)
        if purpleCircle.contains_point([x,y]):
            value = hsv[y, x][0]
            if (value > purpleMax):
                purpleMax = value
            if (value < purpleMin):
                purpleMin = value

    # include a margin of 2 units for min and max values
    margin = 2
    hsvValues = [int(yellowMin)-margin, int(yellowMax)+margin,
                 int(greenMin)-margin, int(greenMax)+margin,
                 int(blueSMin)-margin, int(blueSMax)+margin,
                 int(blueLMin)-margin, int(blueLMax)+margin,
                 int(pinkMin)-margin, int(pinkMax)+margin,
                 int(purpleMin)-margin,int(purpleMax)+margin]
    values_json = json.dumps(hsvValues)
    client.publish ('calibrationResult', values_json)


def on_message(cli, userdata, message):
    global takingPictures, GWYB, sendingVideoStream, sendingVideoForCalibration
    global sendingVideoStream
    global client
    global cap
    global hsvValues

    if message.topic == 'set_hsv_values':
        # new values are received
        hsvValues = json.loads(message.payload)

    if message.topic == 'startGuideWithColors':
        sendingVideoStream = True
        # Send video stream with direction annotation
        # AND SEND commands to autopilot
        w = threading.Thread(target=SendVideoStream, args=(True,))
        w.start()

    if message.topic == 'showVideoStream':
        sendingVideoStream = True
        # Send video stream with direction annotation
        # BUT DO NOT send commands to autopilot
        w = threading.Thread(target=SendVideoStream, args=(False,))
        w.start()

    if message.topic == 'stopVideoStream':
        sendingVideoStream = False

    if message.topic == 'calibrate':
        sendingVideoForCalibration = False
        # take the picture to be used for calibration
        ret, frame = cap.read()
        w = threading.Thread(target=Calibrate, args=(frame,))
        w.start()
    if message.topic == 'startVideoForCalibration':
        sendingVideoForCalibration = True
        w = threading.Thread(target=SendVideoForCalibration)
        w.start()
    if message.topic == 'stopVideoForCalibration':
        sendingVideoForCalibration = False
    if message.topic == 'getCurrentValues':
        print ('Send current values',  hsvValues)
        hsvValuesJson = json.dumps(hsvValues)
        client.publish ('currentValues', hsvValuesJson)


def cameraService ():
    global client
    global cap
    global GWYB
    global hsvValues
    # default min,max values for Yellow, Green, Blue Strong, Blue Light, Pink and Purple
    hsvValues = [25,38, 152,170, 50,60, 90,110, 168, 175, 45, 67]
    GWYB = False
    cap = cv.VideoCapture(0)  # video capture source camera (Here webcam of laptop)

    # broker address for production mode or simulation mode when using a
    # local mosquitto broker
    # broker_address ="localhost"

    # public broker addresses for simulation mode
    # broker_address = "broker.hivemq.com"
    broker_address = "test.mosquitto.org"

    broker_port = 1883
    client = mqtt.Client("Camera Service")
    client.on_message = on_message
    client.connect(broker_address, broker_port)
    print ('Waiting commands...')

    client.subscribe('startGuideWithColors')
    client.subscribe('set_hsv_values')
    client.subscribe('showVideoStream')
    client.subscribe('stopVideoStream')
    client.subscribe('getCurrentValues')
    client.subscribe('startVideoForCalibration')
    client.subscribe('stopVideoForCalibration')
    client.subscribe('calibrate')
    client.loop_forever()

if __name__ == '__main__':

    cameraService()
