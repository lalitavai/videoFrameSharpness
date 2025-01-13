# Import modules
import cv2
import matplotlib.pyplot as plt

import numpy as np


def var_abs_laplacian(image):
    """
    Calculate the Variance of Absolute Values of the Laplacian (VAVOL) for a given image.

    This function computes the Laplacian of an image, takes the absolute values
    of the result, and then determines the variance of these absolute values.
    The VAVOL metric can be used to estimate the sharpness or focus of an image.

    :param image: The input image for which the Variance of Absolute Values of
        the Laplacian (VAVOL) is to be computed. It can be either a grayscale
        image or a color image as a NumPy array.
    :type image: numpy.ndarray

    :return: The computed Variance of Absolute Values of the Laplacian (VAVOL)
        of the input image as a floating-point number.
    :rtype: float
    """
    # Ensure the image is grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Laplacian of the image
    laplacian = cv2.Laplacian(gray, cv2.CV_32F)

    # absolute values of the Laplacian
    abs_laplacian = np.abs(laplacian)

    # Variance of Absolute Values of the Laplacian
    vavol = np.var(abs_laplacian)

    return vavol


def sum_modified_laplacian(im):
    """
    Compute the sum of the modified Laplacian (SML) for a given image.

    This function calculates the SML by computing horizontal and vertical
    second-order derivatives of the input image using pre-defined kernels.
    The modified Laplacian emphasizes regions of high intensity variation,
    which is often used in tasks such as focus measure computations in image
    processing pipelines.

    :param im: Input image, which can be in grayscale or color (RGB/BGR) format.
               If the image is in color, it is converted to grayscale before
               processing.
    :type im: numpy.ndarray
    :return: The sum of the modified Laplacian (SML), represented as a float.
    :rtype: float
    """
    # Ensure the image is grayscale
    if len(im.shape) == 3:
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    else:
        gray = im


    # kernels for horizontal and vertical second-order derivatives
    kernel_x = np.array([[0, -1, 0],
                         [0, 2, 0],
                         [0, -1, 0]], dtype=np.float32)

    kernel_y = np.array([[0, 0, 0],
                         [-1, 2, -1],
                         [0, 0, 0]], dtype=np.float32)

    #get derivatives using cv2.filter2D
    laplacian_x = cv2.filter2D(gray, cv2.CV_32F, kernel_x)
    laplacian_y = cv2.filter2D(gray, cv2.CV_32F, kernel_y)

    # absolute values of the derivatives
    abs_laplacian_x = np.abs(laplacian_x)
    abs_laplacian_y = np.abs(laplacian_y)

    # Sum the absolute values
    modified_laplacian = abs_laplacian_x + abs_laplacian_y

    # sum of the Modified Laplacian
    sml = np.sum(modified_laplacian)

    return sml


#Read input video filename
filename = 'focus-test.mp4'

# Create a VideoCapture object
cap = cv2.VideoCapture(filename)

# Read first frame from the video
ret, frame = cap.read()

# Display total number of frames in the video
print("Total number of frames : {}".format(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

maxV1 = 0
maxV2 = 0

# Frame with maximum measure of focus
# Obtained using methods 1 and 2
bestFrame1 = 0
bestFrame2 = 0

# Frame ID of frame with maximum measure
# of focus
# Obtained using methods 1 and 2
bestFrameId1 = 0
bestFrameId2 = 0

# Get measures of focus from both methods
val1 = var_abs_laplacian(frame)
val2 = sum_modified_laplacian(frame)

# Specify the ROI for flower in the frame
# UPDATE THE VALUES BELOW
top = 0
left = 0
bottom = frame.shape[0]
right = frame.shape[1]

# Iterate over all the frames present in the video
while (ret):
    # Crop the flower region out of the frame
    flower = frame[top:bottom, left:right]
    # Get measures of focus from both methods
    val1 = var_abs_laplacian(flower)
    val2 = sum_modified_laplacian(flower)
    print("Frame: ", val1, val2, " Flower: ", var_abs_laplacian(flower), sum_modified_laplacian(flower))

    # If the current measure of focus is greater
    # than the current maximum
    if val1 > maxV1:
        # Revise the current maximum
        maxV1 = val1
        # Get frame ID of the new best frame
        bestFrameId1 = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        # Revise the new best frame
        bestFrame1 = frame.copy()
        print("Frame ID of the best frame [Method 1]: {}".format(bestFrameId1))

    # If the current measure of focus is greater
    # than the current maximum
    if val2 > maxV2:
        # Revise the current maximum
        maxV2 = val2
        # Get frame ID of the new best frame
        bestFrameId2 = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        # Revise the new best frame
        bestFrame2 = frame.copy()
        print("Frame ID of the best frame [Method 2]: {}".format(bestFrameId2))

    # Read a new frame
    ret, frame = cap.read()

print("================================================")
# Print the Frame ID of the best frame
print("Frame ID of the best frame [Method 1]: {}".format(bestFrameId1))
print("Frame ID of the best frame [Method 2]: {}".format(bestFrameId2))

# Release the VideoCapture object
cap.release()

# Stack the best frames obtained using both methods
out = np.hstack((bestFrame1, bestFrame2))

# Display the stacked frames

cv2.imshow("Laplacian", out)

c = cv2.waitKey(0)
cv2.destroyAllWindows()
