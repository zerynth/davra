from bsp import board
# Let's import the zdm module
from zdm import zdm
# We also need wifi or ethernet
from networking import wifi

# Set the ssid and password of your wifi network
ssid = "WiFi SSID"
passwd = "WiFi Password"

# Data publish interval
frequency = 10000

def data_frequency(agent, args):
    global frequency
    print("Job request received!",args)
    if not "frequency" in args:
        return {"msg": "Invalid argument for frequency job: missing 'frequency' arg"}

    f = args["frequency"]

    if type(f)> PINTEGER:
        message = "Invalid argument for frequency job: 'frequency' arg must be an integer. Received: " + str(type(f))
        return {"msg": message}

    if f < 1 or f > 300: 
        return {"msg": "Invalid argument for frequency job: 'frequency' arg must be between 1 and 300 seconds"}

    frequency = f * 1000
    return {"msg": "frequency set to %d seconds" % f }

   
while True:
    try:
        # Let's connect to the wifi
        print("configuring wifi...")
        wifi.configure(ssid=ssid, password=passwd)
        print("connecting to wifi...")
        wifi.start()
        print("connected!",wifi.info())

        # the Agent class implements all the logic to talk with the ZDM
        # it also accepts a dictionary of functions to be called as jobs
        agent = zdm.Agent(jobs={"set_frequency":data_frequency})
        # just start it
        agent.start()

        while True:
            v = random(0,100)
            agent.publish(payload={"value":v}, tag="data")
            print("Published",v)
            sleep(frequency)
           
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