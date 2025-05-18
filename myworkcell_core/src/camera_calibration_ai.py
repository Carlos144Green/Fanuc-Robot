import cv2
import numpy as np

def calibrate_camera(image_paths, grid_size=(9, 6), square_size=1.0):
    """
    Calibrates the camera using a set of chessboard images.

    :param image_paths: List of file paths to chessboard images.
    :param grid_size: Tuple indicating the number of inner corners per chessboard row and column (rows, cols).
    :param square_size: Size of a square in the chessboard (in any unit, e.g., meters or millimeters).
    :return: Camera matrix, distortion coefficients, rotation vectors, and translation vectors.
    """
    # Prepare object points (3D points in real-world space)
    objp = np.zeros((grid_size[0] * grid_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:grid_size[1], 0:grid_size[0]].T.reshape(-1, 2)
    objp *= square_size

    # Arrays to store object points and image points
    objpoints = []  # 3D points in real-world space
    imgpoints = []  # 2D points in image plane

    for image_path in image_paths:
        # Read the image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, grid_size, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Refine corner locations
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1),
                criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            )
            imgpoints[-1] = corners2

    # Perform camera calibration
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    if not ret:
        raise ValueError("Camera calibration failed. Ensure that the images are valid and the chessboard is visible.")

    return camera_matrix, dist_coeffs, rvecs, tvecs