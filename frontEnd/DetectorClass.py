import threading
import time
import tkinter as tk
from tkinter import *
import cv2
import paho.mqtt.client as mqtt
from PIL import Image, ImageTk

from fingerDetector import FingerDetector
from poseDetector import PoseDetector
from faceDetector import FaceDetector
#from MapFrameClass import MapFrameClass
from prueba2 import MapFrameClass
from PIL import ImageTk
from tkinter import messagebox


class DetectorClass:
    def buildFrame(self, fatherFrame, mode):
        # mode can be: fingers, face or pose
        self.fatherFrame = fatherFrame
        self.mode = mode


        # use this when simulating the system using the mosquitto broker installed in your PC
        #broker_address = "localhost"

        #use this when connecting with the RPi
        #broker_address = "10.10.10.1"

        # use pon of these when simulating the system in case you do not have a mosquitto broker installed in your PC
        #broker_address = "broker.hivemq.com"
        broker_address = "test.mosquitto.org"

        broker_port = 1883
        self.client = mqtt.Client("Dectector")
        self.client.on_message = self.on_message
        self.client.connect(broker_address, broker_port)
        self.client.loop_start()


        self.cap = cv2.VideoCapture(0)

        if self.mode == 'fingers':
            self.detector = FingerDetector()
        elif self.mode == 'pose':
            self.detector = PoseDetector()
        else:
            self.detector = FaceDetector()


        self.master = tk.Frame(self.fatherFrame)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)


        self.topFrame = tk.LabelFrame(self.master, text="Control")
        self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.columnconfigure(1, weight=1)
        self.topFrame.rowconfigure(0, weight=1)
        self.topFrame.rowconfigure(1, weight=1)
        self.topFrame.rowconfigure(2, weight=1)
        self.topFrame.rowconfigure(3, weight=1)

        # state can be: initial, practising, flying, closed
        self.state = 'initial'

        # level can be easy or difficult
        self.level = 'easy'

        self.easyButton = tk.Button(self.topFrame, text="Fácil", bg='#367E18', fg="white", command=self.easy)
        self.easyButton.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.difficultButton = tk.Button(self.topFrame, text="Difícil", bg='#CC3636', fg="white", command=self.difficult)
        self.difficultButton.grid(row=0, column=1, padx=5, pady=5, sticky=N + S + E + W)
        # next button to be shown when level (easy or difficult) selected
        self.practice = tk.Button(self.topFrame, text="Practica los movimientos", bg='#F57328', fg="white",
                                  command=self.practice)
        self.closeButton = tk.Button(self.topFrame, text="Salir", bg='#FFE9A0', fg="black",
                                  command=self.close)

        # frame to be shown when practise is finish and user wants to fly
        self.buttonFrame = tk.Frame(self.topFrame)
        self.buttonFrame.rowconfigure(0, weight=1)
        self.buttonFrame.rowconfigure(1, weight=1)
        self.buttonFrame.columnconfigure(0, weight=1)
        self.buttonFrame.columnconfigure(1, weight=1)
        self.buttonFrame.columnconfigure(2, weight=1)
        self.buttonFrame.columnconfigure(2, weight=1)



        self.setLevelButton = tk.Button(self.buttonFrame, text="Set level", bg='#CC3636', fg="white", command=self.setLevel)
        self.setLevelButton.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.connectButton = tk.Button(self.buttonFrame, text="Connect", bg='#CC3636', fg="white", command=self.connect)
        self.connectButton.grid(row=0, column=1, padx=5, pady=5, sticky=N + S + E + W)

        self.armButton = tk.Button(self.buttonFrame, text="Arm", bg='#CC3636', fg="white", command=self.arm)
        self.armButton.grid(row=0, column=2, padx=5, pady=5, sticky=N + S + E + W)
        self.takeOffButton = tk.Button(self.buttonFrame, text="Take Off", bg='#CC3636', fg="white", command=self.takeOff)
        self.takeOffButton.grid(row=0, column=3, padx=5, pady=5, sticky=N + S + E + W)

        # button to be shown when flying
        self.returnHomeButton = tk.Button(self.buttonFrame, text="Retorna", bg='#CC3636', fg="white", command=self.returnHome)

        # button to be shown when the dron is back home
        self.closeButton2 = tk.Button(self.buttonFrame, text="Salir", bg='#FFE9A0', fg="black", command=self.close)

        self.topFrame.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)

        # by defaulf, easy mode is selected
        self.bottomFrame = tk.LabelFrame(self.master, text="EASY")


        if self.mode == 'fingers':
            self.image = Image.open("assets/dedos_faciles.png")
        elif self.mode == 'pose':
            self.image = Image.open("assets/poses_faciles.png")
        else:
            self.image = Image.open("assets/caras_faciles.png")


        self.image = self.image.resize((400, 600), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.image)
        canvas1 = Canvas(self.bottomFrame, width=400,height=600)
        canvas1.pack(fill="both", expand=True)
        canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        self.bottomFrame.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)

        return self.master

    def showMap (self, position):
        newWindow = Toplevel(self.master)
        newWindow.title("Map")
        newWindow.geometry("800x600")
        self.map = MapFrameClass()
        frame = self.map.buildFrame(newWindow, position, self.selectedLevel)
        frame.pack(fill="both", expand="yes", padx=10, pady=10)
        #newWindow.mainloop()


    def on_message(self, cli, userdata, message):
        if message.topic == 'connected':
            self.connectButton['text'] = 'connected'
            self.connectButton['bg'] = '#367E18'
            self.client.subscribe('homePosition')
            self.client.publish('getHomePosition')


        if message.topic == 'armed':
            self.armButton['text'] = 'armed'
            self.armButton['bg'] = '#367E18'

        if message.topic == 'takenOff':
            self.takeOffButton['text'] = 'flying'
            self.takeOffButton['bg'] = '#367E18'
            self.client.publish('guideManually', 'Stop')
            self.state = 'flying'
            # this thread will start taking images and detecting patterns to guide the drone
            x = threading.Thread(target=self.flying)
            x.start()
            self.returnHomeButton.grid(row=2, column=0, padx=5, columnspan=3, pady=5, sticky=N + S + E + W)


        if message.topic == 'atHome':
            # the dron completed the RTL
            self.map.markAtHome()
            messagebox.showwarning("Success", "Ya estamos en casa", parent=self.master)
            self.returnHomeButton.grid_forget()
            self.closeButton2.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)

            # return to the initial situation
            self.connectButton['bg'] = '#CC3636'
            self.connectButton['text'] = 'Connect'
            self.armButton['bg'] ='#CC3636'
            self.armButton['text'] = 'Arm'
            self.takeOffButton['bg'] = '#CC3636'
            self.takeOffButton['text'] = 'TakeOff'
            self.state ='initial'

        if message.topic == 'homePosition':
            positionStr = str (message.payload.decode ('utf-8'))
            position = positionStr.split ('*')
            self.showMap(position)
            self.client.subscribe('dronePosition')

        if message.topic == 'dronePosition':
            positionStr = str (message.payload.decode ('utf-8'))
            position = positionStr.split ('*')
            self.map.moveDrone(position)
          


    def connect(self):
        print ('voy a conectar')
        # do not allow connect if level of difficulty is not fixed
        if self.setLevelButton['bg'] == '#367E18':
            self.closeButton2.grid_forget()
            self.client.subscribe('connected')
            self.client.publish('connect')
        else:
            messagebox.showwarning("Error", "Antes de conectar debes fijar el nivel de dificultad", parent=self.master)



    def setLevel (self):
        self.selectLevelWindow = Toplevel(self.master)
        self.selectLevelWindow.title("Select level")
        self.selectLevelWindow.geometry("1000x300")
        selectLevelFrame =  tk.Frame(self.selectLevelWindow)
        selectLevelFrame.pack()
        selectLevelFrame.rowconfigure(0, weight=1)
        selectLevelFrame.rowconfigure(1, weight=1)
        selectLevelFrame.columnconfigure(0, weight=1)
        selectLevelFrame.columnconfigure(1, weight=1)
        selectLevelFrame.columnconfigure(2, weight=1)

        self.image1 = Image.open("assets/no_fence.png")
        self.image1 = self.image1.resize((320,240), Image.ANTIALIAS)
        self.bg1 = ImageTk.PhotoImage(self.image1)
        canvas1 = Canvas(selectLevelFrame, width=320,height=240)
        canvas1.create_image(0, 0, image=self.bg1,anchor="nw")
        canvas1.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)

        self.image2 = Image.open("assets/fence_case1.png")
        self.image2 = self.image2.resize((320,240), Image.ANTIALIAS)
        self.bg2 = ImageTk.PhotoImage(self.image2)
        canvas2 = Canvas(selectLevelFrame, width=320,height=240)
        canvas2.create_image(0, 0, image=self.bg2,anchor="nw")
        canvas2.grid(row=0, column=1, padx=5, pady=5, sticky=N + S + E + W)

        self.image3 = Image.open("assets/fence_case2.png")
        self.image3 = self.image3.resize((320,240), Image.ANTIALIAS)
        self.bg3 = ImageTk.PhotoImage(self.image3)
        canvas3 = Canvas(selectLevelFrame, width=320,height=240)
        canvas3.create_image(0, 0, image=self.bg3,anchor="nw")
        canvas3.grid(row=0, column=2, padx=5, pady=5, sticky=N + S + E + W)


        self.level1Button = tk.Button(selectLevelFrame, text="Básico", bg='#CC3636', fg="white", command= self.level1)
        self.level1Button.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.level2Button = tk.Button(selectLevelFrame, text="Medio", bg='#CC3636', fg="white", command=self.level2)
        self.level2Button.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)
        self.level3Button = tk.Button(selectLevelFrame, text="Avanzado", bg='#CC3636', fg="white", command=self.level3)
        self.level3Button.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)


    def level1 (self):
        self.selectedLevel = 'Basico'
        self.selectLevelWindow.destroy()
        self.setLevelButton['text'] = 'Básico'
        self.setLevelButton['bg'] = '#367E18'

    def level2 (self):
        self.selectedLevel = 'Medio'
        self.selectLevelWindow.destroy()
        self.setLevelButton['text'] = 'Medio'
        self.setLevelButton['bg'] = '#367E18'

    def level3 (self):
        self.selectedLevel = 'Avanzado'
        self.selectLevelWindow.destroy()
        self.setLevelButton['text'] = 'Avanzado'
        self.setLevelButton['bg'] = '#367E18'

    def arm(self):
        # do not allow arming if destination is not fixed
        if self.connectButton['bg'] == '#367E18':
            self.client.subscribe('armed')
            self.client.publish('Arm')
        else:
            messagebox.showwarning("Error", "Antes de armar debes conectar", parent=self.master)

    def takeOff(self):
        # do not allow taking off if not armed
        if self.armButton['bg'] == '#367E18':
            self.client.subscribe('takenOff')
            self.client.subscribe('dronePosition')
            self.client.publish('takeOff')
        else:
            messagebox.showwarning("Error", "Antes de despegar debes armar",  parent=self.master)

    def close (self):
        # this will stop the video stream thread
        self.state = 'closed'
        self.cap.release()
        self.client.loop_stop()
        self.client.disconnect()
        self.fatherFrame.destroy()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    def practice(self):
        if self.state == 'initial':
            # start practising
            self.practice['bg'] = '#367E18'
            self.practice['text'] = 'Estoy preparado. Quiero volar'
            self.state = 'practising'
            # startvideo stream to practice
            x = threading.Thread(target=self.practising)
            x.start()

        elif self.state == 'practising':
            #stop the video stream thread for practice
            self.state = 'closed'

            self.practice.grid_forget()

            # show buttons for connect, arm and takeOff
            self.buttonFrame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

    def easy(self):
        # show button to start practising
        self.practice.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.closeButton.grid(row=1, column=1, padx=5,pady=5, sticky=N + S + E + W)
        # highlight codes for easy pattern
        self.difficultButton['bg'] = '#CC3636'
        self.easyButton['bg'] = '#367E18'
        self.bottomFrame.destroy()
        self.bottomFrame = tk.LabelFrame(self.master, text="EASY")
        self.level = 'easy'
        if self.mode == 'fingers':
            self.image = Image.open("assets/dedos_faciles.png")
        elif self.mode == 'pose':
            self.image = Image.open("assets/poses_faciles.png")
        else:
            self.image = Image.open("assets/caras_faciles.png")

        self.image = self.image.resize((400, 600), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.image)
        canvas1 = Canvas(self.bottomFrame, width=400, height=600)
        canvas1.pack(fill="both", expand=True)
        canvas1.create_image(0, 0, image=self.bg,anchor="nw")

        self.bottomFrame.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)

    def difficult(self):
        # show button to start practising
        self.practice.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.closeButton.grid(row=1, column=1, padx=5,pady=5, sticky=N + S + E + W)

        # highlight codes for difficult pattern
        self.difficultButton['bg'] = '#367E18'
        self.easyButton['bg'] = '#CC3636'
        self.bottomFrame.destroy()
        self.bottomFrame = tk.LabelFrame(self.master, text="DIFFICULT")

        # we still do not have difficult patters. So we use again easy patters

        if self.mode == 'fingers':
            self.image = Image.open ("assets/dedos_faciles.png")
        elif self.mode == 'pose':
            self.image = Image.open ("assets/poses_dificiles.png")

        else:
            self.image = Image.open("assets/caras_faciles.png")

        self.image = self.image.resize((400, 600), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.image)

        canvas1 = Canvas(self.bottomFrame, width=400,height=600)
        canvas1.pack(fill="both", expand=True)

        canvas1.create_image(0, 0, image=self.bg,anchor="nw")

        self.bottomFrame.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
        self.level = 'difficult'

    def __setDirection (self, code):
        if code == 1:
            return 'Norte'
        elif code == 2:
            return 'Sur'
        elif code == 3:
            return 'Este'
        elif code == 4:
            return 'Oeste'
        elif code == 5:
            return  'Drop'
        elif code == 6:
            return 'Retorna'
        elif code == 0:
            return 'Stop'
        else:
            return ''

    def practising(self):
        # when the user changes the pattern (new face, new pose or new fingers) the system
        # waits some time (ignore 8 video frames) for the user to stabilize the new pattern
        # we need the following variables to control this
        prevCode = -1
        cont = 0

        while self.state == 'practising':
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            #use the selected detector to get the code of the pattern and the image with landmarks
            code, img = self.detector.detect(image, self.level)
            img = cv2.resize(img, (800, 600))
            img = cv2.flip(img, 1)

            # if user changed the pattern we will ignore the next 8 video frames
            if (code != prevCode):
                cont = 4
                prevCode = code
            else:
                cont = cont -1
                if cont < 0:
                    # the first 8 video frames of the new pattern (to be ignored) are done
                    # we can start showing new results
                    direction = self.__setDirection(code)
                    cv2.putText(img, direction, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 10)

            cv2.imshow('video', img)
            cv2.waitKey(1)
        cv2.destroyWindow ('video')
        cv2.waitKey(1)

    def flying (self):
        # see comments for practising function
        prevCode = -1
        cont = 0
        # we need to know if the dron is returning to lunch to show an apropriate message
        self.returning = False

        self.direction = ''
        while self.state == 'flying':
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            code, img = self.detector.detect(image, self.level)
            img = cv2.resize(img, (800, 600))
            img = cv2.flip(img, 1)
            if not self.returning:
                if (code != prevCode):
                    cont = 8
                    prevCode = code
                else:
                    cont = cont - 1
                    if cont < 0:
                        self.direction = self.__setDirection(code)
                        if code == 1:
                            # north
                            self.client.publish('go', 'North')
                        elif code == 2:  # south
                            self.client.publish('go', 'South')
                        elif code == 5:
                            self.client.publish('drop')
                            time.sleep(2)
                            self.client.publish('reset')
                        elif code == 3:  # east
                            self.client.publish('go', 'East')
                        elif code == 4:  # west
                            self.client.publish('go', 'West')
                        elif code == 6:
                            self.returnHome()
                        elif code == 0:
                            self.client.publish('go', 'Stop')

            cv2.putText(img, self.direction, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 10)
            cv2.imshow('video', img)
            cv2.waitKey(1)

        cv2.destroyWindow('video')
        cv2.waitKey(1)

    def returnHome(self):
        self.returning = True
        self.direction = 'Volviendo a casa'
        self.client.subscribe('atHome')
        self.client.publish('RTL')

