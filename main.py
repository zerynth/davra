###############################################################################
# Hello Davra!
###############################################################################

# First, import the board module from the bsp (board support package).
# The bsp loads board specific names, variables and settings so that
# this project can be run on different Zerynth hardware
# without changing a line of code.
from bsp import board

# The Zerynth Device Manager is the entrypoint for the zCloud.
# Let's connect and send data to the ZDM with a simple example.
# Before exeuting this code, please associate the device with your
# ZDM account by selecting "ZDM target" in VSCode Control Panel.

# Let's import the zdm module
from zdm import zdm
# We also need wifi or ethernet
from networking import wifi
# the DHT11 driver
from components.dht11 import dht11
# and some control over the button
import gpio


# how fast we produce messages in milliseconds
publish_frequency = 5000
# DHT11 data pin
dhtpin = D18
# and how many time the button has bee pressed
btnpress = 0

def on_press(pin, value):
    global publish_frequency, btnpress
    if publish_frequency<=3000:
        publish_frequency = 10000
    else:
        publish_frequency= publish_frequency-1000
    print("Now publishing every",publish_frequency,"milliseconds")
    btnpress = btnpress+1

# configure button
gpio.on_rise(D0, on_press, pull=INPUT_PULLUP)


##################################################
# Set the ssid and password of your wifi network!
##################################################
ssid = "Zerynth3"
passwd = "zerynthwifi"

while True:
    try:
        # Let's connect to the wifi
        print("configuring wifi...")
        wifi.configure(
            ssid=ssid,
            password=passwd)
        print("connecting to wifi...")
        wifi.start()
        print("connected!",wifi.info())

        # the Agent class implements all the logic for interacting with the ZDM
        agent = zdm.Agent()
        # just start it
        agent.start()

        hum = None
        temp = None
                
        while True:
            # use the agent to publish values to the ZDM
            # Just open the device page from VSCode and check that data is incoming
            try:
                # DHT11 can fail reading 
                hum, temp = dht11.read(dhtpin)
            except Exception as e:
                print("DHT11 failed to read!",e)

                

            agent.publish({
                "hum":hum, 
                "temp":temp, 
                "freq":publish_frequency,
                "btn":btnpress}, "davra")
            
            sleep(publish_frequency)
            # The agent automatically handles connections and reconnections
            print("ZDM is online:    ",agent.online())
            # And provides info on the current firmware version
            print("Firmware version: ",agent.firmware())
            
        wifi.stop()
        print("disconnected from wifi")
    except WifiBadPassword:
        print("Bad Password")
    except WifiBadSSID:
        print("Bad SSID")
    except WifiException:
        print("Generic Wifi Exception")
    except Exception as e:
        raise e

    sleep(3000)


