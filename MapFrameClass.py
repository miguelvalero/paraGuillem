import json
import math
import time
import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
from geographiclib.geodesic import Geodesic
import mpu
import requests

class MapFrameClass:

    def buildFrame(self, fatherFrame, position, selectedLevel):
        self.fatherFrame = fatherFrame
        self.MapFrame = tk.Frame(fatherFrame)
        self.droneLat = float (position[0])
        self.droneLon = float (position[1])
        print ('drone position ', position)

        self.MapFrame.rowconfigure(0, weight=1)
        self.MapFrame.columnconfigure(0, weight=1)

        dronLabCenterPoint =[41.2763551, 1.9886434]


        self.map_widget = tkintermapview.TkinterMapView(self.MapFrame, width=800, height=600, corner_radius=0)
        self.map_widget.grid(row=0, column=0, sticky="nesw")
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",max_zoom=20)
        #to center the map
        self.map_widget.set_position(dronLabCenterPoint[0], dronLabCenterPoint[1])
        self.map_widget.set_zoom(20)
        time.sleep(5)

        #marker = self.map_widget.set_marker(self.droneLat,self.droneLon)
        print (self.map_widget.canvas.winfo_reqwidth(), self.map_widget.canvas.winfo_reqheight())
        self.geod = Geodesic.WGS84
        self.ppm = 1 / 0.1122
        # one point (x,y) in the canvas and the corresponding position (lat,lon)
        x = 402
        y = 260
        position= [41.27638533666021, 1.9886594932540902]

        g = self.geod.Inverse(self.droneLat, self.droneLon, position[0], position[1])
        azimuth = 180 - float(g['azi2'])
        dist = float(g['s12'])

        #ATENCION: NO SE POR QUE AQUI TENGO QUE RESTAR EN VEZ DE SUMAR
        self.droneX = x - math.trunc(dist * self.ppm * math.sin(math.radians(azimuth)))
        self.droneY = y - math.trunc(dist * self.ppm * math.cos(math.radians(azimuth)))


        self.point = self.map_widget.canvas.create_oval(self.droneX-8,self.droneY-8,self.droneX+8,self.droneY+8, fill = 'blue')


        # lines pointing to North, South, East and West
        pointNorthX = self.droneX + math.trunc(10 * self.ppm * math.sin(math.radians(180)))
        pointNorthY = self.droneY + math.trunc(10 * self.ppm * math.cos(math.radians(180)))
        self.toNorth = self.map_widget.canvas.create_line(self.droneX, self.droneY, pointNorthX, pointNorthY,
                                                          fill='blue')

        pointEastX = self.droneX + math.trunc(10 * self.ppm * math.sin(math.radians(90)))
        pointEastY = self.droneY + math.trunc(10 * self.ppm * math.cos(math.radians(90)))
        self.toEast = self.map_widget.canvas.create_line(self.droneX, self.droneY, pointEastX, pointEastY,
                                                         fill='yellow')

        pointSouthX = self.droneX + math.trunc(10 * self.ppm * math.sin(math.radians(0)))
        pointSouthY = self.droneY + math.trunc(10 * self.ppm * math.cos(math.radians(0)))
        self.toSouth = self.map_widget.canvas.create_line(self.droneX, self.droneY, pointSouthX, pointSouthY, fill='pink')

        pointWestX = self.droneX + math.trunc(10 * self.ppm * math.sin(math.radians(270)))
        pointWestY = self.droneY + math.trunc(10 * self.ppm * math.cos(math.radians(270)))
        self.toWest = self.map_widget.canvas.create_line(self.droneX, self.droneY, pointWestX, pointWestY, fill='green')
        dronLabLimits = self.map_widget.set_polygon(
            [(41.27640750, 1.98829200),  # Index 1: Same point as index N.
            (41.27622110, 1.98836580),
            (41.27637020, 1.98906320),
            ( 41.27655070, 1.98899210),
            (41.27640750, 1.98829200)],
            outline_color="red")

        #self.map_widget.canvas.tag_raise(self.point)

        #self.map_widget.add_left_click_map_command(self.left_click_event)

        self.map_widget.canvas.bind ("<ButtonPress-1>", self.click)
        if selectedLevel == 'Medio':
            self.setCase1()
        elif selectedLevel == 'Avanzado':
            self.setCase2()

        return self.MapFrame
    def click (self, e):
        print ('click:', e)
        p= self.map_widget.convert_canvas_coords_to_decimal_coords(e.x,e.y)
        print('point:', p)

    def setDestination (self, position):
        position[0] = 41.2763108
        position[1] = 1.9883282
        #self.geod = Geodesic.WGS84

        g = self.geod.Inverse(self.droneLat, self.droneLon, float (position[0]), float (position[1]))

        azimuth = 180 - float(g['azi2'])
        dist = float(g['s12'])
        print ('*****',dist,azimuth)

        destX = self.droneX + math.trunc(dist * self.ppm * math.sin(math.radians(azimuth)))
        destY = self.droneY + math.trunc(dist * self.ppm * math.cos(math.radians(azimuth)))

        self.dest = self.map_widget.canvas.create_oval(destX - 8, destY - 8, destX + 8,
                                                        destY + 8, fill='green')


    def setCase1 (self):
        case1Fence = self.map_widget.set_polygon(
            [(41.27639040, 1.98845029),
             (41.27642971, 1.98849052),
             (41.27633497, 1.98878422),
             (41.27632186, 1.98874131),
             (41.27639040, 1.98845029)],
            fill_color="red",
            outline_color=None)




    def setCase2 (self):
        case2Fence_1 = self.map_widget.set_polygon(
            [(41.27648111, 1.98836982),
             (41.27649320, 1.98841810),
             (41.27628659, 1.98849723),
             (41.27628155, 1.98847845),
             (41.27648111, 1.98836982)],
            fill_color="red",
            outline_color=None)
        case2Fence_2 = self.map_widget.set_polygon(
            [(41.27640552, 1.98860586),
             (41.27641257, 1.98864743),
             (41.27624325, 1.98871583),
             (41.27623720, 1.98868766),
             (41.27640552, 1.98860586)],
            fill_color="red",
            outline_color=None)
        case2Fence_3 = self.map_widget.set_polygon(
            [(41.27655469, 1.98868632),
             (41.27656376, 1.98872253),
             (41.27634807, 1.98882177),
             (41.27634101, 1.98879227),
             (41.27655469, 1.98868632)],
            fill_color="red",
            outline_color=None)


    def moveDrone (self, position):
        print('position ', position)
        lat = float(position[0])
        lon = float (position[1])
        g = self.geod.Inverse(self.droneLat, self.droneLon, lat, lon)
        azimuth = 180 - float(g['azi2'])
        dist = float(g['s12'])



        newposx = self.droneX + math.trunc(dist * self.ppm * math.sin(math.radians(azimuth)))
        newposy = self.droneY + math.trunc(dist * self.ppm * math.cos(math.radians(azimuth)))
        print('new position ', newposx,newposy)
        self.map_widget.canvas.itemconfig(self.point, fill='red')
        self.map_widget.canvas.coords(self.point, newposx - 8, newposy - 8, newposx + 8, newposy + 8)
        self.droneLat = lat
        self.droneLon = lon
        self.droneX = newposx
        self.droneY = newposy

        self.map_widget.canvas.delete(self.toSouth)
        self.map_widget.canvas.delete(self.toEast)
        self.map_widget.canvas.delete(self.toNorth)
        self.map_widget.canvas.delete(self.toWest)

        # lines pointing to North, South, East and West
        pointNorthX = self.droneX + math.trunc(10 * self.ppm * math.sin(math.radians(180)))
        pointNorthY = self.droneY + math.trunc(10 * self.ppm * math.cos(math.radians(180)))
        self.toNorth = self.map_widget.canvas.create_line(self.droneX, self.droneY, pointNorthX, pointNorthY,
                                                          fill='blue')

        pointEastX = self.droneX + math.trunc(10 * self.ppm * math.sin(math.radians(90)))
        pointEastY = self.droneY + math.trunc(10 * self.ppm * math.cos(math.radians(90)))
        self.toEast = self.map_widget.canvas.create_line(self.droneX, self.droneY, pointEastX, pointEastY,
                                                         fill='yellow')

        pointSouthX = self.droneX + math.trunc(10 * self.ppm * math.sin(math.radians(0)))
        pointSouthY = self.droneY + math.trunc(10 * self.ppm * math.cos(math.radians(0)))
        self.toSouth = self.map_widget.canvas.create_line(self.droneX, self.droneY, pointSouthX, pointSouthY,
                                                          fill='pink')

        pointWestX = self.droneX + math.trunc(10 * self.ppm * math.sin(math.radians(270)))
        pointWestY = self.droneY + math.trunc(10 * self.ppm * math.cos(math.radians(270)))
        self.toWest = self.map_widget.canvas.create_line(self.droneX, self.droneY, pointWestX, pointWestY, fill='green')

    def markAtHome (self):
        self.map_widget.canvas.itemconfig(self.point, fill='blue')

        