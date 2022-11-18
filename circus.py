
import time
from tkinter import *
from pygame import mixer
from tkinter import font
from PIL import Image, ImageTk
from tkvideo import tkvideo
from DetectorClass import DetectorClass
from ColorsClass import ColorsClass

mixer.init()
mixer.music.load('assets/circo.mp3')
mixer.music.play(10)

root = Tk()
root.geometry("800x800")

image = Image.open("assets/entrada.png")
image = image.resize((800,600), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(image)
canvas1 = Canvas(root, width=800,height=600)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg,anchor="nw")

myFont = font.Font(family='Bernard MT Condensed', size=28, weight='bold')


def colors ():
    mixer.music.stop()
    mixer.music.load('assets/aplausos.mp3')
    mixer.music.play(10)
    time.sleep(5)
    mixer.music.stop()

    newWindow = Toplevel(root)
    newWindow.title("Colores")
    newWindow.geometry("450x800")
    color = ColorsClass()
    frame = color.buildFrame(newWindow)
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    newWindow.mainloop()



def fingers ():
    mixer.music.stop()
    mixer.music.load('assets/aplausos.mp3')
    mixer.music.play(10)
    time.sleep(5)
    mixer.music.stop()

    newWindow = Toplevel(root)
    newWindow.title("Dedos")
    newWindow.geometry("450x800")
    detector = DetectorClass()
    frame = detector.buildFrame(newWindow, 'fingers')
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    newWindow.mainloop()



def pose ():
    mixer.music.stop()
    mixer.music.load('assets/aplausos.mp3')
    mixer.music.play(10)
    time.sleep(5)
    mixer.music.stop()

    newWindow = Toplevel(root)
    newWindow.title("Pose")
    newWindow.geometry("450x800")
    detector = DetectorClass()
    frame = detector.buildFrame(newWindow, 'pose')
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    newWindow.mainloop()


def faces ():
    mixer.music.stop()
    mixer.music.load('assets/aplausos.mp3')
    mixer.music.play(10)
    time.sleep(5)
    mixer.music.stop()

    newWindow = Toplevel(root)
    newWindow.title("Pose")
    newWindow.geometry("450x800")
    detector = DetectorClass()
    frame = detector.buildFrame(newWindow, 'face')
    frame.pack(fill="both", expand="yes", padx=10, pady=10)
    newWindow.mainloop()

def bye():
    newWindow = Toplevel(root)
    newWindow.title("bye")
    newWindow.geometry("800x700")

    image = Image.open("assets/bye.png")
    image = image.resize((800, 600), Image.ANTIALIAS)
    bg = ImageTk.PhotoImage(image)
    canvas1 = Canvas(newWindow, width=800, height=600)
    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0, 0, image=bg, anchor="nw")
    label = Label(newWindow, text="Gracias por su visita", height=2, width = 20, bg='white', fg='#367E18')
    label['font'] = myFont
    label.pack()
    newWindow.mainloop()



def enter ():
    mixer.music.stop()
    mixer.music.load('assets/redoble.mp3')  # Loading Music File
    mixer.music.play(10)
    newWindow = Toplevel(root)
    newWindow.title("Select")
    newWindow.geometry("1400x800")
    newWindow.columnconfigure(0, weight=1)
    newWindow.columnconfigure(1, weight=1)
    newWindow.columnconfigure(2, weight=1)
    newWindow.columnconfigure(3, weight=1)
    newWindow.rowconfigure(0, weight=1)
    newWindow.rowconfigure(1, weight=1)
    newWindow.rowconfigure(2, weight=1)

    image2 = Image.open("assets/gallery.png")
    image2 = image2.resize((1400, 600), Image.ANTIALIAS)
    bg2 = ImageTk.PhotoImage(image2)
    canvas2 = Canvas(newWindow, width=1400,height=600)
    canvas2.grid (row = 0, column = 0, columnspan = 4,padx=5, pady=5, sticky=N + S + E + W)
    canvas2.create_image(0, 0, image=bg2 ,anchor="nw")

    colorsButton = Button(newWindow, text="Colores", height=1, bg='#367E18', fg='#FFE9A0', command = colors)
    colorsButton.grid (row = 1, column = 0,padx=5, pady=5, sticky=N + S + E + W)
    colorsButton['font'] = myFont
    poseButton = Button(newWindow, text="Poses", height=1, bg='#367E18', fg='#FFE9A0', command = pose)
    poseButton.grid(row=1, column=1,padx=5, pady=5, sticky=N + S + E + W)
    poseButton['font'] = myFont
    fingersButton = Button(newWindow, text="Dedos", height=1, bg='#367E18', fg='#FFE9A0', command = fingers)
    fingersButton.grid(row=1, column=2,padx=5, pady=5, sticky=N + S + E + W)
    fingersButton['font'] = myFont
    facesButton = Button(newWindow, text="Caras", height=1, bg='#367E18', fg='#FFE9A0', command=faces)
    facesButton.grid(row=1, column=3,padx=5, pady=5, sticky=N + S + E + W)
    facesButton['font'] = myFont


    byeButton = Button(newWindow, text="Salir", height=1, bg='#FFE9A0', fg='#367E18', command=bye)
    byeButton.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)
    byeButton['font'] = myFont
    newWindow.mainloop()




enterButton = Button(root, text="Pasen y vean", height = 1, bg= '#367E18', fg='#FFE9A0', width = 14, command = enter)
enterButton['font'] = myFont
enterButton_canvas = canvas1.create_window(280, 620,anchor="nw",window=enterButton)

def close ():
    global sponsor
    sponsor.destroy()


def showVideo ():
    global sponsor
    sponsor = Toplevel(root)
    sponsor.title("Castelldefels terra de drons")
    sponsor.geometry("1200x900")
    closeButton = Button(sponsor, text="Cerrar", height=1, bg='green', fg='yellow',
                   width=14, command=close)
    closeButton.pack()
    label = Label(sponsor)
    label.pack()
    player = tkvideo("assets/terraDeDrons.mp4", label, loop=1, size=(1200, 900))
    player.play()

    root.mainloop()




showVideoButton = Button(root, text="Patrocinado por ...", height = 1, bg= '#CC3636', fg='white',
          width = 24, command = showVideo)
myFont2 = font.Font(family='Bernard MT Condensed', size=8)
showVideoButton['font'] = myFont2

# Display Buttons
showVideoButton_canvas = canvas1.create_window(340, 700,
                                       anchor="nw",
                                       window=showVideoButton)


# Execute tkinter
root.mainloop()



