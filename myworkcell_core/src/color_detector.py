import numpy as np
import cv2
import os


def setup():
    # os.system('v4l2-ctl -d /dev/video2 -c focus_auto=0')
    # os.system('v4l2-ctl -d /dev/video2 -c focus_absolute=0')
    print("focus up")

def nothing(x):
    pass

def find_ball(hsv, lower_bound, upper_bound):
    # Apply mask
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    # result = cv2.bitwise_and(src, src, mask=mask)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Get image moments
        M = cv2.moments(contour)
        
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])  # Centroid X
            cy = int(M["m01"] / M["m00"])  # Centroid Y
        else:
            cx, cy = 0, 0  # Default if area is 0
        break





    return (cx, cy)

setup()
path = '/home/fanuc-i3d-robot/Pictures/Webcam/2025-03-24-185349.jpg'
src = cv2.imread(path)

while True:
    # Capture frame-by-frame

    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV) 

    # Create HSV range
    blue_lower_bound = np.array([90, 145, 100])
    blue_upper_bound = np.array([115, 255, 255])
    blue_cord = find_ball(hsv, blue_lower_bound, blue_upper_bound)

    # red_lower_bound = np.array([0, 45, 120])
    # red_upper_bound = np.array([25, 200, 255])

    # yellow_lower_bound = np.array([10, 0, 90])
    # yellow_upper_bound = np.array([60, 132, 255])

    # green_lower_bound = np.array([72, 38, 188])
    # green_upper_bound = np.array([84, 78, 255])

    # black_lower_bound = np.array([86, 44, 20])
    # black_upper_bound = np.array([112, 142, 78])

    # black_lower_bound = np.array([0, 0, 172])
    # black_upper_bound = np.array([180, 8, 246])

    cv2.circle(src, blue_cord, 4, (80, 255, 20), 1)
    cv2.putText(src, "blue", blue_cord, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
    # Show result
    cv2.imshow('result', src)
    # cv2.imshow('Result', result)

    # # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # Display the resulting frame
    # cv2.imshow('frame', gray)
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()