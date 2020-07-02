import cv2
import face_recognition

####### Initialize faces for facial recognition #######
imgSam = face_recognition.load_image_file('faces/Sam.png')
imgSamEncoding = face_recognition.face_encodings(imgSam)[0]

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
learnedFaceNames = ['Sam', 'Nabil', 'Sungho Roh', 'Park', 'Antonio', 'Kim']

# End face initialization
# Initialize camera and font for displaying face recognition

cam = cv2.VideoCapture(0)   # Enter 0,1,2 etc. for the selected camera 0 is default built in laptop camera
font = cv2.FONT_HERSHEY_SIMPLEX
font2 = cv2.QT_FONT_NORMAL
exitText = 'Enter "esc" to exit.'
# Open camera and run program until user choses to exit
while True:
    ret, img = cam.read()
    # testImg = face_recognition.load_image_file(img)
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(learnedFaceEncodings, face_encoding)
        name = 'Unknown'
        if True in matches:
            first_match_index = matches.index(True)
            name = learnedFaceNames[first_match_index]

        cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 5)
        cv2.putText(img, name, (left + 2, top + 23), font, 1, (255, 255, 255), 3)
        cv2.putText(img, exitText, (30, 30), font2, .75, (255, 255, 255), 1)
        cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()



