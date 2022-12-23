import cv2
import time
import board
import digitalio
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gpio0 = digitalio.DigitalInOut(board.C0) # 0 and 1 are comunications to the Pi
gpio0.direction = digitalio.Direction.OUTPUT
gpio1 = digitalio.DigitalInOut(board.C1)
gpio1.direction = digitalio.Direction.OUTPUT
gpio2 = digitalio.DigitalInOut(board.C2)# 2 and 3 and comunications from the Pi
gpio2.direction = digitalio.Direction.INPUT
gpio3 = digitalio.DigitalInOut(board.C3)
gpio3.direction = digitalio.Direction.INPUT

def camfunc():
    cap = cv2.VideoCapture(1)# selecting the camera
    maxValue = 20;# max amount of frames needed. So far 5 is to few, 50 is to much. Should play around with 20
    currentValue = maxValue#maxValue is static value, currentValue is what is going to change. Doing this so we only have to change 1 number in the code instead of all over the place when we want to reset currentValue
    while cap.isOpened(): # a loop that is going when the camera is open
        # ret, frame = cap.read()
        
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        def face_data():
            faces = face_cascade.detectMultiScale(gray, 1.1, 6, minSize=(30,30))
            return faces


        face_out = face_data()   

        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 6, minSize=(30,30))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#no idea whats going on above, i guess its getting an image, setting it to grey scale then throwing it into cv2
        # show image
        cv2.imshow('Webcam', img)
        if (len(face_out) < 1):#if there is no face just turn off motors 
            gpio0.value = False
            gpio1.value = False

        else:
            height = face_out[0,1] # we want tuple 0, with the 2nd element, which is height.

            if height < 40:
                if (gpio2.value == 0) and (gpio3.value == 1):#checking to see if the Pi is saying we are maxed at height. If we try to go up, but its at max height. by setting currentValue to 0, one of the if loops will get us out of here
                    currentValue = 0
                else:    
                    gpio0.value = True
                    gpio1.value = False
                    currentValue = maxValue
                    print('to high')
                #print('To high!')
            elif height > 180:
                if (gpio2.value == 1) and (gpio3.value == 0):#checking to see if the Pi is saying we are lowest at height. If we try to go down, but its at lowest height. by setting currentValue to 0, one of the if loops will get us out of here
                    currentValue = 0
                else:
                    gpio0.value = False
                    gpio1.value = True
                    currentValue = maxValue
                #print('To low!')
            else:
                gpio0.value = False
                gpio1.value = False
                currentValue = currentValue - 1# face is good, decrement the number if frames needed
                
            
            #time.sleep(1)
            print(currentValue)    
            #print(face_out[0,1])

        if currentValue == 0: # gets us out of here when we are done
            break
        # checks if Q has been pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):# need something in the loop, might as well have something that we can manually exit.
            break

    # release webcam
    gpio0.value = True# telling the pi we are done and will wait
    gpio1.value = True
    
    while (gpio0.value == 0) or (gpio0.value == 0):# just waiting for the PI to reply with 11
    # we want to wait here to give time for the pi to process. Once the pi says ok we are moving on(11) then we will wait for the 11 the change.
        print('Waiting for 1 1')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   
    print('Exiting camfunc')
    cap.release()
    cv2.destroyAllWindows()