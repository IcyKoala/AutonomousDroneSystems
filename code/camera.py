import cv2
import numpy as np
import threading
import imutils
import pathPlanning

def gridToCamera(x,y):
    return (int(x/100*1000), int(y/100*600))


class CameraDetector:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture('https://145.24.238.36:8080///video')
        self.frame = None
        self.resizedFrame = None
        self.lock = threading.Lock()
        self.running = True

        # # Define color ranges for red and green triangles (BGR format)
        # self.red_lower = np.array([30, 30, 130])
        # self.red_upper = np.array([140, 140, 256])
        # self.green_lower = np.array([70, 150, 0])
        # self.green_upper = np.array([150, 255, 150])

        # Define color ranges for red and green triangles (BGR format) values WD.01.019
        self.red_lower = np.array([30, 30, 100])
        self.red_upper = np.array([100, 100, 206])
        self.green_lower = np.array([70, 120, 35])
        self.green_upper = np.array([150, 205, 150])

        # Start the video capture thread
        self.capture_thread = threading.Thread(target=self.update_frame, daemon=True)
        self.capture_thread.start()

    def update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame

    def release(self):
        self.running = False
        self.capture_thread.join()
        self.cap.release()

    def detectTriangle(self, frame):
        '''
        Takes video stream frame
        Returns the centers and orientation vectors of red and green triangles
        '''

        if frame is None:
            return None, None, frame

   


        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(self.resizedFrame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        # Apply adaptive thresholding
        threshold = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Find contours
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        displayframe = self.resizedFrame.copy()
        self.drawGrid(displayframe)

        red_center = None
        red_orientation_vector = None
        green_center = None
        green_orientation_vector = None

        found_red = False
        found_green = False

        for contour in contours:
            if found_red and found_green:
                break

            area = cv2.contourArea(contour)
            if area < 100 or area > 10000:  # Area filtering to ignore small contours
                continue

            # Approximate contour
            epsilon = 0.2 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Filter only triangles (3 vertices)
            if len(approx) == 3:
                # Check if contour is convex
                if not cv2.isContourConvex(approx):
                    continue
                center = self.getCenter(approx)
                color = self.checkColor(self.resizedFrame, center)

                # Check if the color is within the specified range for red
                if not found_red and self.isColorInRange(color, self.red_lower, self.red_upper):
                    print('RED ' + str(color))
                    red_center = center
                    red_orientation_vector = self.checkOrientation(center, approx)
                    cv2.drawContours(displayframe, [approx], 0, (0, 0, 255), 2)
                    cv2.circle(displayframe, center, 5, (0, 255, 0), -1)
                    cv2.putText(displayframe, 'Red Triangle', center, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    endpoint = (center[0] + red_orientation_vector[0], center[1] + red_orientation_vector[1])
                    cv2.line(displayframe, center, endpoint, (255, 0, 0), 2)
                    found_red = True

                # Check if the color is within the specified range for green
                elif not found_green and self.isColorInRange(color, self.green_lower, self.green_upper):
                    print('GREEN ' + str(color))
                    green_center = center
                    green_orientation_vector = self.checkOrientation(center, approx)
                    cv2.drawContours(displayframe, [approx], 0, (0, 255, 0), 2)
                    cv2.circle(displayframe, center, 5, (255, 0, 0), -1)
                    cv2.putText(displayframe, 'Green Triangle', center, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                    endpoint = (center[0] + green_orientation_vector[0], center[1] + green_orientation_vector[1])
                    cv2.line(displayframe, center, endpoint, (0, 255, 0), 2)
                    found_green = True
        return red_center, red_orientation_vector, displayframe ,green_center, green_orientation_vector



    def isColorInRange(self, color, lower, upper):
        """
        Check if a given BGR color is within the specified range.
        """
        return np.all(lower <= color) and np.all(color <= upper)

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

    def drawGrid(self, frame):
        for i in range(5):
            cv2.rectangle(frame, (0, 0), (i * 200, i * 200), (0, 0, 0), 2)


    def get_frame(self):
        with self.lock:
            if self.frame is not None:
                self.resizedFrame = imutils.resize(self.frame, width=1080, height=1920)
                return self.resizedFrame
                
            return None

if __name__ == '__main__':
    detector = CameraDetector()
    pathplanning = pathPlanning.PathPlanning()

    while True:
        frame = detector.get_frame()
        if frame is None:
            continue

      
        center,orientation_vector, frame_with_triangles, a,b = detector.detectTriangle(frame)

        targets = pathplanning.RotateCircleFormation(5, 30, (50,50), 180)
        for target in targets:
            pos = gridToCamera(target[0], target[1])
            cv2.rectangle(frame_with_triangles, pos, pos, (0, 0, 255), 10)


        if frame_with_triangles is not None:
            cv2.imshow('frame', frame_with_triangles)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    detector.release()
    cv2.destroyAllWindows()
