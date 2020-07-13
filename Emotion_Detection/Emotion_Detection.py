from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
import face_recognition
import dlib
from imutils import face_utils

####### Initialize faces for facial recognition #######
imgSam = face_recognition.load_image_file('faces/Sam.png')
imgSamEncoding = face_recognition.face_encodings(imgSam)[0]

imgTrev = face_recognition.load_image_file('faces/Trev.png')
imgTrevEncoding = face_recognition.face_encodings(imgTrev)[0]

imgNabil = face_recognition.load_image_file('faces/Nabil.png')
imgNabilEncoding = face_recognition.face_encodings(imgNabil)[0]

imgSunghoRoh = face_recognition.load_image_file('faces/Sungho_Roh.png')
imgSunghoRohEncoding = face_recognition.face_encodings(imgSunghoRoh)[0]

imgPark = face_recognition.load_image_file('faces/Park.png')
imgParkEncoding = face_recognition.face_encodings(imgPark)[0]

imgAntonio = face_recognition.load_image_file('faces/Antonio.png')
imgAntonioEncoding = face_recognition.face_encodings(imgAntonio)[0]

imgKim = face_recognition.load_image_file('faces/Kim.png')
imgKimEncoding = face_recognition.face_encodings(imgKim)[0]

imgLee = face_recognition.load_image_file('faces/Lee.png')
imgLeeEncoding = face_recognition.face_encodings(imgLee)[0]

learnedFaceEncodings = [imgSamEncoding, imgNabilEncoding, imgSunghoRohEncoding, imgParkEncoding,
                        imgAntonioEncoding, imgKimEncoding]
learnedFaceNames = ['Sam', 'Trevor', 'Nabil', 'Sungho Roh', 'Park', 'Antonio', 'Kim']
# End face initialization

# set local or full pathname for the haarcascades and vgg.h5 files
face_classifier = cv2.CascadeClassifier(
    '/Users/samlindaman/PycharmProjects/Emotion/haarcascade_frontalface_default.xml')
classifier = load_model('/Users/samlindaman/PycharmProjects/Emotion/Emotion_little_vgg.h5')

class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']
cap = cv2.VideoCapture(0)

# set variable for falling check
arrHeights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
count = 0
fallenText = "FALLEN"
fallen = False
#

font = cv2.FONT_HERSHEY_SIMPLEX
font2 = cv2.QT_FONT_NORMAL
exitText = 'Press "q" to exit.'

while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (x, y, w, h) in faces:

        # Falling check
        arrHeights.append(y)  # append array of y coordinates for each face
        size = len(arrHeights)

        # loop through the last 10 x coordinates to check for downward trend
        for s in range(size - 11, size - 1):
            if arrHeights[s] > arrHeights[s - 1]:
                count = count + 1
            else:
                count = 0
                fallen = False
                # if user comes back into screen, the fallen message should disappear

            # make sure that the fall is large/fast enough and the user wan't just moving their head downward
            if count >= 6 and arrHeights[s] - arrHeights[s - 5] >= 175:
                fallen = True
                break

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(learnedFaceEncodings, face_encoding)
            name = 'User'
            if True in matches:
                first_match_index = matches.index(True)
                name = learnedFaceNames[first_match_index]
                cv2.putText(frame, 'Admin: ' + name, (left + 2, top - 100), font, 1, (255, 255, 255), 3)
            else:
                cv2.putText(frame, name, (left + 2, top - 100), font, 1, (255, 255, 255), 3)

        # draw rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        # rect,face,image = face_detector(frame)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # make a prediction on the ROI, then lookup the class

            preds = classifier.predict(roi)[0]
            label = class_labels[preds.argmax()]
            label_position = (x, y - 10)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        else:
            cv2.putText(frame, 'No Face Found', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    if fallen:
        cv2.putText(frame, fallenText, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    cv2.putText(frame, exitText, (1000, 30), font2, .75, (255, 255, 255), 1)
    cv2.imshow('Emotion Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()







