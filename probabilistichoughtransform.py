def hough_transform(image):
    """
    Determine and cut the region of interest in the input image.
    Parameter:
        image: grayscale image which should be an output from the edge detector
    """
    # Distance resolution of the accumulator in pixels.
    rho = 1              
    # Angle resolution of the accumulator in radians.
    theta = np.pi/180    
    # Only lines that are greater than threshold will be returned.
    threshold = 20       
    # Line segments shorter than that are rejected.
    minLineLength = 20   
    # Maximum allowed gap between points on the same line to link them
    maxLineGap = 500     
    # function returns an array containing dimensions of straight lines 
    # appearing in the input image
    return cv2.HoughLinesP(image, rho = rho, theta = theta, threshold = threshold,
                           minLineLength = minLineLength, maxLineGap = maxLineGap)
