#  Demo firmware - Frequency job

This firmware is a simple demo firmware that publishes a random value every 10 seconds.
It is possible to change the data publishing frequency sending a job to the device, called **set_frequency**.
This job expects an int argument representing the new data publishing interval, in seconds.

* Job name: **set_frequency**
* Job payload: **{ "frequency": x}**

Where **x** must be an integer between 1 and 300 (5 minutes) seconds. If you send the job with an invalid value, 
the device will answer with an error message.

You can send the job to the device using the Zerynth Cloud Web Interface (https://cloud.zerynth.com) or via HTTP request.


### Send job request 
* Method: *POST*
* Endpoint: https://api.zdm.zerynth.com/v3/devices/{your_device_id}/jobs/set_frequency
* Request body: 
  ```json
  {
    "value": {
      "frequency": 15
    }
  }
  ```
* Auth: the request's header must contain the following key-value pair
  ```X-API-KEY: "{Zerynth Cloud API Key}"``` [you can create a new API key from the Settings section inside the workspace page of the Zerynth Cloud]


### Get job status
* Method: *GET*
* Endpoint: https://api.zdm.zerynth.com/v3/devices/{your_device_id}/jobs/set_frequency
* Auth: the request's header must contain the following key-value pair
  ```X-API-KEY: "{Zerynth Cloud API Key}"```
