import face_recognition
import pickle
import numpy as np
import base64
import cv2
import logging
import telegram
import io
from PIL import Image
from datetime import datetime
from config import scale_center_line

def lookup_known_face(face_encoding, known_face_encodings, known_face_metadata):
    metadata = "unknown"
    if len(known_face_encodings) == 0:
        return metadata
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if face_distances[best_match_index] < 0.4: # analysis
        metadata = known_face_metadata[best_match_index]
    return metadata, face_distances[best_match_index]

def select_roi(roi, frame):
    # ROI
    left, top = roi[0], roi[1]   
    right, bottom = roi[0]+roi[2], roi[1]+roi[3]
    
    # Horizontal Line
    y = int(roi[1] + roi[3]*scale_center_line)
    cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
    cv2.line(frame, (0, y), (frame.shape[1], y), (255,255,0), 2)
    return left, top, right, bottom

def detect_face(frame, left, top, right, bottom, f):
    cropped_frame = frame[top:bottom, left:right, :]
    small_frame = cv2.resize(cropped_frame, (0, 0), fx=1./f, fy=1./f)
    rgb_small_frame = small_frame[:, :, ::-1]
    # rgb_small_frame = cropped_frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    return face_locations, face_encodings

def display(ftop, fright, fbottom, fleft, frame, left, top, uname, distance, f):
    #display
    ftop *= f
    fright *= f
    fbottom *= f
    fleft *= f
    cv2.rectangle(frame, (left+fleft, top+ftop), (left+fright, top+fbottom), (0,0,255), 2)
    bbox = (left+fleft, top+ftop, left+fright, top+fbottom)
    centroid = ((bbox[0]+bbox[2])//2, (bbox[1]+bbox[3])//2)
    cv2.circle(frame, centroid, 4, (255,0,0), -1)
    cv2.putText(frame, uname, (bbox[0] + 6, bbox[3] - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
    cv2.putText(frame, str(distance), (0, 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

def send_notification(img, name, bot, userid):
    pillow_image = Image.fromarray(img)
    with io.BytesIO() as output:
        pillow_image.save(output, format="JPEG")
        bot.send_photo(userid, io.BytesIO(output.getvalue()))
        bot.send_message(userid, "person with name: {} has entered the room at {}.".format(name, datetime.now()))

# def send_img(img, file_name):
#     cv2.imwrite(file_name, img)
#     _, buf = cv2.imencode('.jpg', img)
#     txt = base64.b64encode(buf)
#     requests.post(constants.server_url, data={'img': txt})
#     upload_file(file_name, S3_BUCKET)

# def upload_file(file_name, bucket, object_name=None):
#     if object_name == None:
#         object_name = file_name
#     s3_client = boto3.client('s3',
#             aws_access_key_id=ACCESS_KEY_ID,
#             aws_secret_access_key=SECRET_ACCESS_KEY)
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True

