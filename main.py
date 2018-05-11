import numpy as np
import cv2
import random
import time
import os
import shutil
chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
timeout = 0
save_im_cooldown = 0
last_x = 0
last_y = 0
last_w = 0
last_h = 0
cv2.namedWindow('img', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('img', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
while True:

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    
    if len(faces) == 0 and timeout != 0:
        cv2.rectangle(frame, (last_x, last_y),(last_x+last_w,last_y+last_h),(255,0,0),2)
        bottomleft_x = last_x
        bottomleft_y = int(last_y + (last_h)) + 20
        subject_name = ""
        with open("names.txt", "r") as n:
            name_list = n.read().split("\n")
            subject_name += random.choice(name_list)
            subject_name += " "
            subject_name += random.choice(name_list)
        cv2.putText(frame,f'{subject_name}',(bottomleft_x, bottomleft_y), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        roi_gray = gray[last_y:last_y+last_h, last_x:last_x+last_w]
        roi_color = frame[last_y:last_y+last_h, last_x:last_x+last_w]
    
    if len(faces) != 0 and save_im_cooldown == 0:
        imname = str(time.time()).replace(".", "") + ".png"
        cv2.imwrite(imname, frame)
        os.rename(imname, f"Faces/" + imname)
        save_im_cooldown = 30
    
    for (x,y,w,h) in faces:
        last_x = x
        last_y = y
        last_w = w
        last_h = h
        subject_name = ""
        with open("names.txt", "r") as n:
            name_list = n.read().split("\n")
            subject_name += random.choice(name_list)
            subject_name += " "
            subject_name += random.choice(name_list)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
        bottomleft_x = last_x
        bottomleft_y = int(y + (h)) + 20
        cv2.putText(frame,f'{subject_name}',(bottomleft_x, bottomleft_y), font, 0.5,(255,255, 255),2,cv2.LINE_AA)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        if timeout < 20:
            timeout += 5
        
    if len(faces) != 0 or timeout != 0:
        crop_img = frame[last_y:last_y+last_h, last_x:last_x+last_w]
        r = 100.0 / crop_img.shape[1]
        dim = (100, int(crop_img.shape[0] * r))
        crop_img = cv2.resize(crop_img, dim, interpolation = cv2.INTER_AREA)
        frame[50:50+crop_img.shape[0], 50:50+crop_img.shape[1]] = crop_img
    if timeout > 0:
        timeout -= 1
    if save_im_cooldown > 0:
        save_im_cooldown -= 1
    cv2.imshow('img', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        exit()
    elif k == ord('r'):
        shutil.rmtree("Faces")
        os.makedirs("Faces")
        exit()