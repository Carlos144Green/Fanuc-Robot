import cv2
import numpy as np
import os
import glob
 
# Defining the dimensions of checkerboard
CHECKERBOARD = (6,9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 
 
 
# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None
 
# Extracting path of individual image stored in a given directory
images = glob.glob('/home/fanuc-i3d-robot/catkin_ws/src/myworkcell_core/calibration_imgs1 copy/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
     
    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """
    if ret == True:
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
         
        imgpoints.append(corners2)
 
        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
     
    cv2.imshow('img',img)
    print(fname)
    # cv2.waitKey(0)
 
cv2.destroyAllWindows()
 
 
"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
img = cv2.imread('/home/fanuc-i3d-robot/catkin_ws/src/myworkcell_core/calibration_imgs1/img3.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
print(dst.shape)
print(img.shape)

cv2.imshow('calibresult.png', dst)
cv2.imshow("Differences", img)

cv2.waitKey(0)


# print("Camera matrix : \n")
# print(mtx)
# print("dist : \n")
# print(dist)
# print("rvecs : \n")
# print(rvecs)
# print("tvecs : \n")
# print(tvecs)

gray1 = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Step 3: Compute absolute difference
diff = cv2.absdiff(gray1, gray2)

# Step 4: Threshold the difference
_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

# Show results
cv2.imshow("Diffwerences!", thresh)
cv2.waitKey(0)
# Step 5: Find contours (optional but useful for visualization)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on one of the original images
highlighted = img.copy()
cv2.drawContours(highlighted, contours, -1, (0, 0, 255), 2)

# Show results
cv2.imshow("Differences!", highlighted)
cv2.waitKey(0)
cv2.destroyAllWindows()