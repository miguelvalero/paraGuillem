import dronekit
import paho.mqtt.client as mqtt
import time
import threading
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions


def arm():
    global vehicle
    print("Basic pre-arm checks") # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = dronekit.VehicleMode("GUIDED")
    vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    print ('armed')

def takeOff(aTargetAltitude):
    global vehicle
    vehicle.simple_takeoff(aTargetAltitude)
    while True:
        print(" Altitude: ",vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


def prepare_command(velocity_x, velocity_y, velocity_z):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    return msg

def sendPosition ():
    global client
    global sendingPositions

    while sendingPositions:
        lat = vehicle.location.global_frame.lat
        lon = vehicle.location.global_frame.lon
        position = str(lat) + '*' + str(lon)
        print ('envio position')
        client.publish("dronePosition", position)
        time.sleep (0.25)

def returning ():
    global sendingPositions
    # wait until the drone is at home
    while vehicle.armed:
        time.sleep(1)
    print('At home')
    vehicle.close()
    client.publish("atHome")
    sendingPositions = False


def flying ():
    global direction, go
    speed = 1
    end = False
    cmd = prepare_command(0, 0, 0)  # stop
    while not end:
        go = False
        while not go:
            vehicle.send_mavlink(cmd)
            time.sleep(1)
        # a new go command has been received. Check direction
        if direction == 'North':
            cmd = prepare_command(speed,0, 0) #NORTH
        if direction == 'South':
            cmd = prepare_command(-speed, 0, 0) #SOUTH
        if direction == 'East':
            cmd = prepare_command(0, speed, 0) #EAST
        if direction == 'West':
            cmd = prepare_command(0,-speed, 0) #WEST
        if direction == 'Stop':
            cmd = prepare_command (0,0,0) #STOP
        if direction == 'RTL':
            end = True

def on_message(client, userdata, message):
    global vehicle
    global go
    global direction
    global sendingPositions

    if message.topic == 'connect':
        print('Connecting to autopilot .....')
        # connection string in production mode
        #connection_string = "/dev/ttyS0"
        # connection string in simulation mode
        connection_string = "tcp:127.0.0.1:5763"
        vehicle = connect(connection_string, wait_ready=True, baud=115200)
        print ('Connected')
        print('Ready to arm')
        client.subscribe('Arm')
        client.subscribe('getPosition')
        client.subscribe('getHomePosition')
        client.subscribe('getDestinationPosition')
        client.publish ('connected')
        sendingPositions = True
        y = threading.Thread(target=sendPosition)
        y.start()

    if message.topic == 'Arm':
        arm()
        print ('Armed')
        print('Ready to takeOff')
        client.subscribe('takeOff')
        client.publish ('armed')

    if message.topic == 'takeOff':
        takeOff (2)
        print ('Flying')
        print('Ready to go')
        client.subscribe('go')
        client.subscribe('RTL')
        client.publish('takenOff')
        w = threading.Thread(target=flying)
        w.start()


    if message.topic == 'getHomePosition':
        lat = vehicle.location.global_frame.lat
        lon = vehicle.location.global_frame.lon
        position = str(lat) + '*' + str(lon)
        client.publish("homePosition", position)

    if message.topic == 'getDestinationPosition':
        lat = vehicle.location.global_frame.lat
        lon = vehicle.location.global_frame.lon
        position = str(lat) + '*' + str(lon)
        client.publish("destinationPosition", position)

    if message.topic == 'RTL':
        vehicle.mode = dronekit.VehicleMode("RTL")
        direction = 'RTL'
        go = True
        w = threading.Thread(target=returning)
        w.start()


    if message.topic == 'go':
        direction = message.payload.decode("utf-8")
        print ('Going ', direction)
        go = True

def AutoServ():
    global client
    # broker address for production mode or simulation mode when using a
    # local mosquitto broker
    #broker_address ="localhost"

    # public broker addresses for simulation mode
    #broker_address = "broker.hivemq.com"
    broker_address = "test.mosquitto.org"

    broker_port = 1883
    client = mqtt.Client("Autopilot Service")
    client.on_message = on_message
    client.connect(broker_address, broker_port)
    print ('Ready to connect')
    client.subscribe('connect')
    client.loop_start()



if __name__ == '__main__':

    AutoServ()
