from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
import tensorflow as tf

face_classifier = cv2.CascadeClassifier('/Users/alex/Documents/GitHub/Intelligent-Care-System/App/model/haarcascade_frontalface_default.xml')
classifier =load_model('/Users/alex/Documents/GitHub/Intelligent-Care-System/App/model/Emotion_little_vgg_epoch25.h5')


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):

        ret, frame = self.video.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # preds = classifier.predict(roi)
                # max_index = np.argmax(preds[0])
                # class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']
                # label = class_labels[max_index]

                label_position = (x, y)
                cv2.putText(frame, 'face', label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)
                break

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')