"""
=====================================================
🚗 Lane Detection using OpenCV
Author: Ayush Kumar
License: Ayush Kumar Open Source License (v1.0, 2025)
=====================================================
"""

import cv2
import numpy as np

# --------------------------
# Step 1: Define helper functions
# --------------------------

def canny_edge_detector(image):
    """Applies Canny edge detection after grayscale + blur."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges

def region_of_interest(image):
    """Applies a triangular mask to focus on the road region."""
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def display_lines(image, lines):
    """Draws lines on the image."""
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if line is None:
                continue
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 8)
    return line_image

def make_coordinates(image, line_parameters):
    """Generates coordinates for the line segment."""
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    """Averages left and right lane lines."""
    left_fit = []
    right_fit = []
    if lines is None:
        return None
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope, intercept = parameters[0], parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_line = right_line = None
    if left_fit:
        left_fit_avg = np.average(left_fit, axis=0)
        left_line = make_coordinates(image, left_fit_avg)
    if right_fit:
        right_fit_avg = np.average(right_fit, axis=0)
        right_line = make_coordinates(image, right_fit_avg)
    return np.array([left_line, right_line])

# --------------------------
# Step 2: Read video or webcam
# --------------------------

# To use your own video: replace 0 with 'test_road.mp4'
cap = cv2.VideoCapture('test_road.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Step 3: Detect edges
    edges = canny_edge_detector(frame)

    # Step 4: Apply region of interest
    cropped_edges = region_of_interest(edges)

    # Step 5: Detect lines
    lines = cv2.HoughLinesP(cropped_edges, 2, np.pi / 180, 100,
                            np.array([]), minLineLength=40, maxLineGap=5)

    # Step 6: Average and display lines
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)

    # Step 7: Overlay lane lines on original frame
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    # Step 8: Display the result
    cv2.imshow("Lane Detection - Ayush Kumar", combo_image)

    # Exit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
