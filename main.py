import numpy as np
import cv2
import random
chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if not len(faces) == 0:
        cv2.putText(frame,'I can see you',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
    for (x,y,w,h) in faces:
        subject_name = ""
        for i in range(6):
            subject_name += random.choice(chars) 
        cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(frame, f"Test Subject {subject_name}", (x - (0.5 * w), y - (0.5 * h)), font, 1.0, (255, 255, 255), 1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

    cv.imshow('img',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

