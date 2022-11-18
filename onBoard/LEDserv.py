import paho.mqtt.client as mqtt

import time
import board
import neopixel
import RPi.GPIO as GPIO

def LEDsBoot ():
    global pixels
    pixels[0] = (255, 0, 0)
    time.sleep(2)
    pixels[0] = (0, 0, 0)
    pixels[1] = (0, 255, 0)
    time.sleep(2)
    pixels[1] = (0, 0, 0)
    pixels[2] = (0, 0, 255)
    time.sleep(2)
    pixels[2] = (0, 0, 0)
    p.start(2.5) # Initialization
    


def on_message(client, userdata, message):
    global pixels

    if message.topic == 'red':
        # red
        print ('RED')
        pixels[0] = (255, 0, 0)
        time.sleep(5)
        pixels[0] = (0, 0, 0)

    if message.topic == 'green':
        # green
        print ('GREEN')
        pixels[1] = (0, 255, 0)
        time.sleep(4)
        pixels[1] = (0, 0, 0)

    if message.topic == 'blue':
        # blue
        print ('BLUE')
        pixels[2] = (0, 0, 255)
        time.sleep(3)
        pixels[2] = (0, 0, 0)

    if message.topic == 'drop':
        p.ChangeDutyCycle(7.5)
        print ('DROP')
        #time.sleep(2)
        #p.ChangeDutyCycle(2.5)
    if message.topic == 'reset':
        p.ChangeDutyCycle(2.5)

    
    if message.topic == 'bluei':
        print ('BLUE')
        pixels[0] = (0, 0, 255)
    if message.topic == 'redi':
        print ('RED')
        pixels[0] = (107, 0, 0)
    if message.topic == 'greeni':
        print ('GREEN')
        pixels[0] = (0, 255, 0)
    if message.topic == 'yellowi':
        print ('YELLOW')
        pixels[0] = (255, 255, 0)
    if message.topic  == 'pinki':
        print ('PINK')
        pixels[0] = (255, 192,203)
    if message.topic  == 'whitei':
        print ('WHITE')
        pixels[0] = (255, 255,255)
    if message.topic  == 'blacki':
        print ('BLACK')
        pixels[0] = (10, 10,10)


    if message.topic == 'clear':
        pixels[0] = (0, 0, 0)

def LEDsService ():
    global pixels
    global p
    broker_address ="localhost"
    broker_port = 1883
    pixels = neopixel.NeoPixel (board.D18,5)
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    LEDsBoot()
    client = mqtt.Client("LEDs Service")
    client.on_message = on_message
    client.connect(broker_address, broker_port)
    print ('Waiting commands...')
    client.subscribe('red')
    client.subscribe('green')
    client.subscribe('blue')
    client.subscribe ('drop')
    client.subscribe ('reset')
    client.subscribe ('bluei')
    client.subscribe ('greeni')
    client.subscribe ('redi')
    client.subscribe ('yellowi')
    client.subscribe ('pinki')
    client.subscribe ('whitei')
    client.subscribe ('blacki')
    client.subscribe ('clear')
    client.loop_start()

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    LEDsService()

