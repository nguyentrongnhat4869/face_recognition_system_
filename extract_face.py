import platform
import face_recognition
import cv2
from datetime import datetime, timedelta
import numpy as np
import platform
import pickle
import face_utils
import os

dir_path = './test_faiss'
emb_128 = []
labels = []
folders = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]

for folder in folders:
        if not folder.endswith('.DS_Store'):
                folder_name = folder.split('/')[-1]
                files = [os.path.join(folder, f) for f in os.listdir(folder)]
                for file in files:
                        if file.endswith('.jpg'):
                                small_frame = cv2.imread(file)
                                print(file)
                                rgb_small_frame = small_frame[:, :, ::-1]
                                # rgb_small_frame = cropped_frame
                                try:
                                        face_locations = face_recognition.face_locations(rgb_small_frame)
                                        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                                        emb_128.append(face_encodings[0])
                                        labels.append(folder_name)
                                except:
                                        continue

with open('./known_faces_data.dat', 'wb') as f:
    pickle.dump((emb_128, labels), f)
