# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:40:09 2020

@author: nabil
"""
#importing libraries

import cv2
import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier('frontalface_default.xml')
#access the camera and starts video capture 
# 0 will detect laptop camera, 1 will detected USB camera ect 
cap = cv2.VideoCapture(1)
while True:
    #if true video camera is working (returning an Image)
    ret,img = cap.read()
    
    #convert the image to grey (converting the image to Black nd white is better 
    #for the program as it uses less memory)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    #detect a facec inside the image using the classifier above
    #1.3 is for reducing the resolution of the image so that classifier can detect better. 
    #5 is sensitivity of the classifier 
    faces = face_cascade.detectMultiScale(gray,1.3,8)
    # cordinates for the square outside the face

        
    for x,y,w,h in faces:
        #draw arectangle in our image
        # RGB color of the rectangle and thickness
        gray_face = cv2.resize(gray[y:y+h,x:x+w],(100,100))
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),5) 
        
        
    cv2.imshow('Face Detection',gray)
    plt.show()
    # When pressing q on the keyboard it will exit the program
    if cv2.waitKey(1) == ord('q'):
        break
#release the camera 
cap.release()
cv2.destroyAllWindows()
        