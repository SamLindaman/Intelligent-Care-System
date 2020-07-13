import cv2
import numpy as np
import face_recognition
from PIL import Image,ImageDraw

font = cv2.FONT_HERSHEY_SIMPLEX

imgNabil = face_recognition.load_image_file('Nabil.jpg')
imgNabil_encoding = face_recognition.face_encodings(imgNabil)[0]

imgElon = face_recognition.load_image_file('Elon.jpg')
imgElon_encoding = face_recognition.face_encodings(imgElon)[0]


known_face_encodings = [imgNabil_encoding,imgElon_encoding]
known_face_names = ['Nabil','Elon']

cam = cv2.VideoCapture(1)

while True:
    ret, img =cam.read()
    # testImg = face_recognition.load_image_file(img)
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img,face_locations)
    
    for (top,right,bottom,left),face_encoding in zip(face_locations,face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
        name = 'Unknown'
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        cv2.rectangle(img,(left,top),(right,bottom),(255,0,0),5)
        cv2.putText(img, name, (left+2,top+23), font, 1, (255,255,255), 3)
        cv2.imshow('camera',img)

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()


