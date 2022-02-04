from bsp import board
# Let's import the zdm module
from zdm import zdm
# We also need wifi or ethernet
from networking import wifi
import gpio

board.init()
board.summary()

# Set the ssid and password of your wifi network
ssid = "WiFi SSID"
passwd = "WiFi Password"

#################################################
LED_RED_PIN     = D22
LED_GREEN_PIN   = D19
LED_BLUE_PIN    = D21

rgb = gpio.LED(LED_RED_PIN, LED_GREEN_PIN, LED_BLUE_PIN, active=1)

###################################################
def color(agent, args):
    print("Job request received!",args)

    if not "color" in args:
        return {"ERR": "Invalid argument for color job"}

    c = args["color"]
    
    if type(c) != PSTRING:
        return {"ERR": "Type of parameters is wrong"}
    else:
        if c=="red":
            rgb.led(RED)
        elif c=="green":
            rgb.led(GREEN)
        elif c=="blue":
            rgb.led(BLUE)
        elif c=="off":
            rgb.led(BLACK)
        else:
            return {"ERR": "Can't set LED to %s" % c}

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
            try:
                agent.publish({"value":v}, "test")
                print("Published",v)
            except:
                print ("publish failed, discarding message")
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

