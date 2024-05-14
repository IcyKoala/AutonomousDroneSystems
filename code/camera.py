import cv2
import numpy as np
import math
class CameraDetector:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture('https://145.137.76.228:8080/video')

    def release(self):
        self.cap.release()

    def checkDrone(image):
        #function that takes a image as input.
        #Returns a list of all the drones in the image.
        #This list contains information about the color, position and orientation
        pass

    def detectTriangle(self, frame):
        '''
        takes video stream
        returns a list of all triangles and there corners
        '''

        if frame is None:
            return None

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5,5),np.uint8)
        gray_scale = cv2.morphologyEx(gray_frame, cv2.MORPH_OPEN, kernel)


        _, threshold = cv2.threshold(gray_scale, 175, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # List to store points of triangles
        triangle_points = []


        for contour in contours:
            if cv2.contourArea(contour) < 50:  # Area filtering
                continue
            # Approximate contour
            approx = cv2.approxPolyDP(contour, 0.2 * cv2.arcLength(contour, True), True)


            # Filter only triangles (3 vertices)
            if len(approx) == 3:
                # Check if contour is convex
                if not cv2.isContourConvex(approx):
                    continue

                triangle_points.append(approx)
                cv2.drawContours(frame, [contour], 0, (0, 0, 255), 5)

                center = self.getCenter(approx)
                cv2.circle(frame, center, 5, (0, 255, 0), -1)
                cv2.putText(frame, 'Triangle', center, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                orientation_vector = self.checkOrientation(center, approx)
                endpoint = (center[0] + orientation_vector[0], center[1] + orientation_vector[1])
                cv2.line(frame, center, endpoint, (255, 0, 0), 2)
                print(self.checkColor(frame, center))



        # Display the frame
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        pass

    def checkColor(self, frame, centerPoint):
        """
        Function to check the color at a specific point in the frame.
        Returns:
            tuple: BGR color value at the specified point.
        """

        # Sample color at the center point
        color = frame[centerPoint[1], centerPoint[0]]

        return color

    def getCenter(self, trianglePoints):
        """
        Calculate the center of a triangle given its three points.

        Returns:
            tuple: Coordinates of the center of the triangle.
        """

        # Unpack the points of the triangle
        p1, p2, p3 = trianglePoints

        # Calculate the average x-coordinate
        center_x = (p1[0][0] + p2[0][0] + p3[0][0]) // 3

        # Calculate the average y-coordinate
        center_y = (p1[0][1] + p2[0][1] + p3[0][1]) // 3

        return (center_x, center_y)


    def checkOrientation(self, centerPoint, trianglePoints):
        """
        Function to check the orientation of the drone.

        Returns:
            tuple: Vector from center to the topmost point of the triangle.
        """
        p1, p2, p3 = trianglePoints

        distances = [
            np.sqrt((centerPoint[0] - p[0][0])**2 + (centerPoint[1] - p[0][1])**2)
            for p in [p1, p2, p3]
        ]

        top_index = np.argmax(distances)

        top_point = trianglePoints[top_index][0]

        orientation_vector = (top_point[0] - centerPoint[0], top_point[1] - centerPoint[1])

        return orientation_vector

    def showStream(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        # cv2.imshow('frame', frame)
        cv2.waitKey(1)
        return frame

detector = CameraDetector()

while True:
    frame = detector.showStream()

    frame_with_triangles = detector.detectTriangle(frame)

    if frame is None:
        break



detector.release()
cv2.destroyAllWindows()