"""
Qt Uses the Model-View Paragigm

Models
"""

# Imports
import mediapipe as mp
import numpy as np
import cv2


class Camera:
    """
    Class to set up camera access
    """

    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.last_frame = np.zeros((1,1))
        self.drawing = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles
        self.pose = mp.solutions.pose


    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num, cv2.CAP_DSHOW)


    def get_frame(self):
        self.success, last_frame = self.cap.read()
        self.last_frame = cv2.flip(last_frame, 1)
        return self.success, self.last_frame


    def acquire_movie(self, num_frames):
        
        movie = []

        with self.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as pose:
            for _ in range(num_frames):
                success, image = self.get_frame()
                if not success:
                    print("Ignoring empty camera frame")
                    continue

                # Process the image with the pose model
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)

                # Draw the pose annotation
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                self.drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    self.pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.drawing_styles.get_default_pose_landmarks_style()
                )

                self.last_frame = image

                movie.append(self.last_frame)

        return movie


    def close_camera(self):
        self.cap.release()


    def __str__(self):
        return f"OpenCV Camera {self.cam_num}"


if __name__ == '__main__':
    cam = Camera(1)
    cam.initialize()
    print(cam)

    _, frame = cam.get_frame()
    print(frame)

    cam.close_camera()
