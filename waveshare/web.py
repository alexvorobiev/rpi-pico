import PCA9685 as p

import network
import socket
from time import sleep
from machine import Pin
import secrets
import wifi
from website import Website

# led_one = Pin(14, Pin.OUT)
# led_two = Pin(15, Pin.OUT)
def parseRequest(s):
    if s.find('?') == -1 or s.find('=') == -1:
        return {}
    return {k:v for k, v in [tuple(x.split('=', 1)) for x in s[(s.find('?') + 1):s.find(' HTTP')].split('&')]}

status = wifi.connect(secrets.SSID, secrets.PASSWORD)
print('IP-adress: ' + status[0])

m = p.MotorDriver()
name = 'default'

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
while True:
    try:
        cl, addr = s.accept()
        print('Connection from ', addr, "accepted!")

        request = cl.recv(1024)
        request = str(request, 'utf-8')
        print(request)

        params = parseRequest(request)
        print(params)

        # if request.find('/led/one') == 6:
        #     led_one.toggle()

        # if request.find('/led/two') == 6:
        #     led_two.toggle()

        if request.find('/on?') >= 0:
            # then motor=MA&speed=50, etc.
            if 'motor' not in params or 'speed' not in params:
                print("Both motor and speed are needed")

            elif params['motor'] not in {'MA', 'MB', 'MC', 'MD'}:
                print("Motor should be one of MA, MB, MC, MD")

            else:
                speed = params['speed']
                speedOk = True

                try:
                    speed = int(speed)
                    speedOk = abs(speed) <= 100
                except ValueError:
                    speedOk = False

                if not speedOk:
                    print("Speed should be an integer -100..100")
                else:
                    print("Starting motor " + params['motor'] + ' speed ' + params['speed'])
                    m.motorStop(params['motor'])
                    m.motorStart(params['motor'], speed)

        if request.find('/off?') >= 0:
            if 'motor' not in params:
                print("Motor is needed")

            elif params['motor'] not in {'MA', 'MB', 'MC', 'MD'}:
                print("Motor should be one of MA, MB, MC, MD")

            else:
                print("Stop motor " + params['motor'])
                m.motorStop(params['motor'])

        if request.find('/begin?') >= 0:
            if 'name' not in params:
                name = 'default'

            print("Starting recording as program " + name)

        if request.find('/end?') >= 0:
            print("Stopping recording as program " + name)

        if request.find('/run?') >= 0:
            if 'name' not in params:
                name = 'default'

            dir = 'forward'
            if 'dir' not in params:
                dir = 'forward'
            print("Running program " + name + " " + dir)

        cl.send('HTTP/1.0 200 OK\r\n')
        cl.send('Content-type: text/html; charset=utf-8\r\n\r\n')
        cl.send(Website())
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')
