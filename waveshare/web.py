import PCA9685 as p

import network
import socket
from time import sleep
from machine import Pin
import secrets
import wifi

# led_one = Pin(14, Pin.OUT)
# led_two = Pin(15, Pin.OUT)
def parseRequest(s):
    return {k:v for k, v in [tuple(x.split('=', 1)) for x in s[(s.find('?') + 1):s.find(' HTTP')].split('&')]}

def Website():
    value_one = led_one.value()
    value_two = led_two.value()
    website = """<!DOCTYPE html>
    <html>
        <head> <title>Lutz Embedded Tec! Raspberry Pico W</title> </head>
        <body>
            <h1>Lutz Embedded Tec! Raspberry Pico W</h1>

            <table style="width:400px" class="center">
                  <tr>
                    <th><center>LED Number </center></th>
                    <th><center>Button </center> </th>
                    <th><center>Pin State</center> </th>
                  </tr>
                  <tr>
                    <td><center>one </td>
                    <td><center><input type='button' value='toggle' onclick='toggleLed("one")'/> </center></td>
                    <td> <center>  <span id="value_one">""" + str(value_one) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>two</center> </td>
                    <td><center><input type='button' value='toggle' onclick='toggleLed("two")'/></center></td>
                    <td><center>  <span id="value_two">""" + str(value_two) + """</span></center></td>
                   </tr>
            </table>

            <input type='button' value='update' onclick='update()'/>

            <script>
                function toggleLed(led){
                    var xhttp = new XMLHttpRequest();
                    xhttp.open('GET', '/led/'+led, true);
                    xhttp.send();
                }
                function update(){
                    location.reload(true);
                }

            </script>
        </body>
    </html>
    """
    return website

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
        # cl.send('Content-type: text/html\r\n\r\n')
        # cl.send(Website())
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')
