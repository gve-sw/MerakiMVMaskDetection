from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os

from webexteamssdk import WebexTeamsAPI


ACCESS_TOKEN = ' ' #Access token for the Database Update Bot in Webex
SERIAL_NUMBER= '' 
NETWORK_ID= '' 
MERAKI_API_KEY= ''
api = WebexTeamsAPI(access_token=ACCESS_TOKEN) #Connection to the webex bot via the access token


def send_alert_message():
    to = ' '
    url = "https://api.meraki.com/api/v0/networks/{1}/cameras/{0}/snapshot".format(SERIAL_NUMBER, NETWORK_ID)
    headers = {
       'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
        "Content-Type": "application/json"
    }
    resp = requests.post(url, headers=headers, json={})
    r = json.loads(resp.text)
    snapshot = str(r["url"])
    url = snapshot.replace(" ", "")
    message = '[ALERT] Person without a mask detected! \n '+ url
    api.messages.create(toPersonEmail=to, markdown=message)

def detect_and_predict_mask(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    faceNet.setInput(blob)
    detections = faceNet.forward()

    faces = []
    locs = []
    preds = []

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            faces.append(face)
            locs.append((startX, startY, endX, endY))

    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    return (locs, preds)

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
                default="face_detector",
                help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
                default="mask_detector.model",
                help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

print("Loading...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"], "res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

maskNet = load_model(args["model"])

print("Starting Video")
vs = VideoStream(src=0).start()
# vs = VideoStream(" ").start()

time.sleep(2.0)

start_time = time.time()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=700)
    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        label = "Mask" if mask > withoutMask else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

        cv2.putText(frame, label, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        now = time.time()
        if now-start_time > 10 :

            start_time = now
            if 'No' in label:
                print('Person without mask on camera! Now sending notification')
                send_alert_message()

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


cv2.destroyAllWindows()
vs.stop()
