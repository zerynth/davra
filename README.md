#  Demo firmware - Led job

This firmware is a simple demo firmware that publishes a random value every 10 seconds.
It handles 3 leds (red, green, blue); it is possible to change the led turned on sending a job to the device, called **color**.
This job expects a string argument representing the color of the led to turn on.

* Job name: **color**
* Job payload: **{ "color": x}**

Where **x** can be "green", "red" or "blue". If you send the job with another value, all the led will be turned off.

You can send the job to the device using the Zerynth Cloud Web Interface (https://cloud.zerynth.com) or via HTTP request.


### Send job request 
* Method: *POST*
* Endpoint: https://api.zdm.zerynth.com/v3/devices/{your_device_id}/jobs/color
* Request body: 
  ```json
  {
    "value": {
      "color": "green"
    }
  }
  ```
* Auth: the request's header must contain the following key-value pair
  ```X-API-KEY: "{Zerynth Cloud API Key}"``` [you can create a new API key from the Settings section inside the workspace page of the Zerynth Cloud]


### Get job status
* Method: *GET*
* Endpoint: https://api.zdm.zerynth.com/v3/devices/{your_device_id}/jobs/color
* Auth: the request's header must contain the following key-value pair
  ```X-API-KEY: "{Zerynth Cloud API Key}"```
  