# Imports
import mediaoioe as mp
import cv2

# Define tools for drawing and solution model
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


IMAGE_FILES = []
BGCOLOR = (192, 192, 192)  # gray


with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5
) as pose:
    for idx, file in enumerate(IMAGE_FILES):
        ## Load image
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape

        ## Convert the BGR image to RGB before processing
        results = pose.Process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            continue
        nose = mp_pose.PoseLandmark.Nose
        print(
            f'Noe Coordinates: ('
            f'{results.pose_landmarks.landmark[nose].x  * image_width}'
            f'{results.pose_landmarks.landmark[nose].y  * image_height}'
        )

        ## Draw segmentation on the image
        annotated_image = image.copy()

        ### To improve segmentation around boundaries, consider applying
        ### a joint bilateral filter to "results.segmentation_mask" with 
        ### "image".
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        annotated_image = np.where(condition, annotated_image, bg_image)

        ### Draw pose landmarks on the image.
        mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )
        cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

        ## Plot pose world landmarks
        mp_drawing.plot_landmarks(
            results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS
        )
