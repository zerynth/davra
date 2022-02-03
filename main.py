from bsp import board
# import the zdm module
from zdm import zdm
from networking import wifi
import gpio

board.init()
board.summary()

# Set the ssid and password of your wifi network
ssid = "Wifi SSID"
passwd = "Wifi Password"

#################################################
LED_RED_PIN     = D22
LED_GREEN_PIN   = D19
LED_BLUE_PIN    = D21

gpio.mode(LED_RED_PIN,OUTPUT)
gpio.mode(LED_GREEN_PIN,OUTPUT)
gpio.mode(LED_BLUE_PIN,OUTPUT)

#change if leds doesn't work
ON = 1
OFF = 0

###################################################
def color(agent, args):
    print("Job request received!",args)
    if not "color" in args:
        return {"msg": "Invalid argument for color job"}

    c = args["color"]
    if c=="red":
        gpio.set(LED_GREEN_PIN,OFF)
        gpio.set(LED_BLUE_PIN,OFF)
        gpio.set(LED_RED_PIN,ON)
    elif c=="green":
        gpio.set(LED_GREEN_PIN,ON)
        gpio.set(LED_BLUE_PIN,OFF)
        gpio.set(LED_RED_PIN,OFF)
    elif c=="blue":
        gpio.set(LED_GREEN_PIN,OFF)
        gpio.set(LED_BLUE_PIN,ON)
        gpio.set(LED_RED_PIN,OFF)
    else:
        gpio.set(LED_GREEN_PIN,OFF)
        gpio.set(LED_BLUE_PIN,OFF)
        gpio.set(LED_RED_PIN,OFF)
        c="off"

    return {"msg": "LED set to %s" % c}

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

        # the Agent class implements all the logic to talk with the ZDM
        # it also accepts a dictionary of functions to be called as jobs
        agent = zdm.Agent(jobs={"color":color})
        # just start it
        agent.start()

        while True:

            # use the agent to publish values to the ZDM
            # Just open the device page from VSCode and check that data is incoming
            v = random(0,100)
            agent.publish({"value":v}, "test")
            print("Published",v)
            sleep(5000)
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

