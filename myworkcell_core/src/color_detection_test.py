import numpy as np
import cv2
import os


def setup():
    os.system('v4l2-ctl -d /dev/video2 -c focus_auto=0')
    os.system('v4l2-ctl -d /dev/video2 -c focus_absolute=0')
    print("focus up")


    # Create a window
    cv2.namedWindow('Trackbars')

    # Create sliders for Hue, Saturation, Value min and max
    cv2.createTrackbar('H_min', 'Trackbars', 0, 179, nothing)
    cv2.createTrackbar('H_max', 'Trackbars', 179, 179, nothing)
    cv2.createTrackbar('S_min', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('S_max', 'Trackbars', 255, 255, nothing)
    cv2.createTrackbar('V_min', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('V_max', 'Trackbars', 255, 255, nothing)
    cv2.createTrackbar('Reset', 'Trackbars', 0, 1, nothing)

def reset_trackbar():
    cv2.setTrackbarPos('H_min', 'Trackbars', 0)
    cv2.setTrackbarPos('H_max', 'Trackbars', 179)
    cv2.setTrackbarPos('S_min', 'Trackbars', 0)
    cv2.setTrackbarPos('S_max', 'Trackbars', 255)
    cv2.setTrackbarPos('V_min', 'Trackbars', 0)
    cv2.setTrackbarPos('V_max', 'Trackbars', 255)
    cv2.setTrackbarPos('Reset', 'Trackbars', 0)

def nothing(x):
    pass



setup()
path = '/home/fanuc-i3d-robot/Pictures/Webcam/2025-03-24-185349.jpg'
src = cv2.imread(path)

while True:
    # Capture frame-by-frame

    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV) 

    # Get trackbar positions
    h_min = cv2.getTrackbarPos('H_min', 'Trackbars')
    h_max = cv2.getTrackbarPos('H_max', 'Trackbars')
    s_min = cv2.getTrackbarPos('S_min', 'Trackbars')
    s_max = cv2.getTrackbarPos('S_max', 'Trackbars')
    v_min = cv2.getTrackbarPos('V_min', 'Trackbars')
    v_max = cv2.getTrackbarPos('V_max', 'Trackbars')
    reset = cv2.getTrackbarPos('Reset', 'Trackbars')

    if reset == 1:
        reset_trackbar()

    # Create HSV range
    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])
    # blue_lower_bound = np.array([90, 145, 100])
    # blue_upper_bound = np.array([115, 255, 255])

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

    # Apply mask
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(src, src, mask=mask)

    # Show result
    cv2.imshow('Original', src)
    cv2.imshow('Mask', mask)
    cv2.imshow('Filtered', result)

    # # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # Display the resulting frame
    # cv2.imshow('frame', gray)
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()