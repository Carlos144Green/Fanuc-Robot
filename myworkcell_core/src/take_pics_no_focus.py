import cv2
import os

os.system('v4l2-ctl -d /dev/video2 -c focus_auto=0')
os.system('v4l2-ctl -d /dev/video2 -c focus_absolute=0')


cap = cv2.VideoCapture(2) # video capqture source camera (Here webcam of laptop) 
count = 0
while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("exit")
        cv2.destroyAllWindows()
        break
    ret,frame = cap.read()

    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        name = "img" + str(count) + ".jpg"
        count += 1
        
        cv2.imwrite(os.path.join("myworkcell_core/calibration_imgs",name),frame)
        
        print("image saved")
        # break

cv2.destroyAllWindows()
cap.release()