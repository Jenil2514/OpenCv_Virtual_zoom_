# Import necessary libraries
from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np

# Set up video capture with specified dimensions
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize hand detector with a detection confidence of 1
detector = HandDetector(detectionCon=1)

# Initialize variables for scaling and image position
startDist = None
scale = 0
cx, cy = 550, 550  # Initial position for placing the image

# Main loop for video processing
while True:
    # Read a frame from the camera
    success, img = cap.read()

    # Detect hands in the frame
    hands = detector.findHands(img, draw=False)

    # Load an image to be manipulated
    img1 = cv2.imread("earth1.png")

    # Check if exactly two hands with specific finger configurations are detected
    if len(hands) == 2 and detector.fingersUp(hands[0]) == [1, 1, 1, 0, 0] and detector.fingersUp(hands[1]) == [1, 1, 1, 0, 0]:
        lmlist1 = hands[0]["lmList"]
        lmlist2 = hands[1]["lmList"]

        # Calculate the distance between hand centers for scaling
        if startDist is None:
            length, info = detector.findDistance(hands[0]["center"], hands[1]["center"])
            startDist = length

        length, info = detector.findDistance(hands[0]["center"], hands[1]["center"])
        scale = int((length - startDist) // 2)
        cx, cy = info[4:]
        print(scale)
    else:
        startDist = None

    try:
        # Resize the image based on the calculated scale and position it on the frame
        h1, w1, _ = img1.shape
        newH, newW = ((h1 + scale) // 2) * 2, ((w1 + scale) // 2) * 2
        img1 = cv2.resize(img1, (newW, newH))
        img[cy - newH // 2:cy + newH // 2, cx - newW // 2:cx + newW // 2] = img1
    except:
        pass

    # Display the modified frame
    cv2.imshow('img', img)

    # Wait for a key event to break out of the loop
    cv2.waitKey(1)
