# MerakiMVMaskDetection





| :exclamation:  External repository notice   |
|:---------------------------|
| This repository is now mirrored at "PLEASE UPDATE HERE - add External repo URL after code review is completed"  Please inform a https://github.com/gve-sw/ organization admin of any changes to mirror them to the external repo |
## Contacts
* Eda Akturk 
* Ogul Celiksoydan

## Solution Components
*  Python 3.8
*  Cisco Meraki MV Camera 
*  Webex Teams
*  TensorFlow

## Installation/Configuration

1. Clone the repo 

```
    $ git clone (link)
```

#### *(Optional) Create Virtual Environment :*
Initialize a virtual environment 

```virtualenv venv```

Activate the virtual env

*Windows*   ``` venv\Scripts\activate```

*Linux* ``` source venv/bin/activate```

Now you have your virtual environment setup and ready

2. Intall requirements 
```
    $ pip install -r requirements.txt
```



## Usage

1. Train you model with the data set. 
```
$ python train_mask_detector.py --dataset dataset
```

2. Create a Webex Bot from https://developer.webex.com/docs/bots

3. Add you Bot Access Token to detect_mask_video.py
```
ACCESS_TOKEN = " " 
```
4. Add the email address of the Webex user(s) to recieve the webex notification. 
```
to = " " 
```
5. Follow the steps [here](https://documentation.meraki.com/MV/Advanced_Configuration/External_RTSP) to activate an RTSP stream link and add the Meraki RTSP Link to the VideoStream. 
```
vs = VideoStream(" ").start()
```

6. Run the code. Go to the terminal and into the directory of the code then enter the following to run the code.
```
    $ python detect_mask_video.py
```

# Screenshots

![/IMAGES/0image.png](/IMAGES/maskdetection.PNG)

### Thank you!

The Mask Detector model and the dataset is from the repository which can be found [here.](https://github.com/chandrikadeb7/Face-Mask-Detection)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
