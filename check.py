import platform
import face_recognition
import cv2
from datetime import datetime, timedelta
import numpy as np
import pickle
import pathlib
import threading
from camera import open_cam_usb
import face_utils
from config import height_cam, weight_cam, token_tele, id_tele
import telegram

# Load emb_128
with open('known_faces_data.dat', 'rb') as f:
    known_face_encodings, known_face_metadata = pickle.load(f)

# Open a USB webcam
cap = open_cam_usb(0, height_cam, weight_cam)

# Telegram_bot
bot = telegram.Bot(token_tele)
userid = id_tele

# Select Roi
cv2.namedWindow("video")
r = None
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("video", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            showCrosshair = False
            fromCenter = False
            # warm up
            face_locations = face_recognition.face_locations(frame[:100, :100])
            face_encodings = face_recognition.face_encodings(frame[:100, :100], face_locations)
            # left, top, width, height
            r = cv2.selectROI("video", frame, fromCenter=fromCenter, showCrosshair=showCrosshair)
            print(r)
            break

# Scale factor
f = 1
name = 'null'

# Process
while True:
    ret, frame = cap.read()
    if ret:
        left, top, right, bottom = face_utils.select_roi(r, frame)
        
        face_locations, face_encodings = face_utils.detect_face(frame, left, top, right, bottom, f)
              
        for (ftop, fright, fbottom, fleft), face_encoding in zip(face_locations, face_encodings):
            # look for face and get name
            uname, distance = face_utils.lookup_known_face(face_encoding, known_face_encodings, known_face_metadata) 

            # display
            face_utils.display(ftop, fright, fbottom, fleft, frame, left, top, uname, distance, f)

            # send notify
            if uname != name:
                print("send")
                thread = threading.Thread(target=face_utils.send_notification, args=(frame[:,:,::-1], uname, bot, userid))
                thread.start()
                name = uname
        
        cv2.imshow('video', frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
    else:
        break
        
cap.release()
