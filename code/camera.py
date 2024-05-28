import cv2
import numpy as np
import threading

class CameraDetector:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture('https://145.137.78.29:8080//video')
        self.frame = None
        self.lock = threading.Lock()
        self.running = True

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
        Returns a list of all triangles and their corners
        '''

        if frame is None:
            return None

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        # Apply adaptive thresholding
        threshold = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Find contours
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # List to store points of triangles
        triangle_points = []

        displayframe = frame.copy()
        center = (0, 0)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 200 or area > 10000:  # Area filtering to ignore small contours
                continue

            # Approximate contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Filter only triangles (3 vertices)
            if len(approx) == 3:
                # Check if contour is convex
                if not cv2.isContourConvex(approx):
                    continue
                center = self.getCenter(approx)
                color = self.checkColor(frame, center)

                print(color)

                if color[2] < 200 or color[0] > 100 or color[1] > 100:
                    continue

                triangle_points.append(approx)

                cv2.drawContours(displayframe, [approx], 0, (0, 0, 255), 2)

                cv2.circle(displayframe, center, 5, (0, 255, 0), -1)
                cv2.putText(displayframe, 'Triangle', center, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                orientation_vector = self.checkOrientation(center, approx)
                endpoint = (center[0] + orientation_vector[0], center[1] + orientation_vector[1])
                cv2.line(displayframe, center, endpoint, (255, 0, 0), 2)

        return displayframe

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

    def get_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

if __name__ == '__main__':
    detector = CameraDetector()

    while True:
        frame = detector.get_frame()
        if frame is None:
            continue

        frame_with_triangles = detector.detectTriangle(frame)

        if frame_with_triangles is not None:
            cv2.imshow('frame', frame_with_triangles)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    detector.release()
    cv2.destroyAllWindows()
