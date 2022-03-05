import cv2
import yaml
import time
import tensorflow as tf

from depth_estimator import DepthEstimator
from custom_video_capture import CustomVideoCapture
from aruco_detector.aruco_detector import findArucoMarkers, arucoIndex
from pose_estimator import PoseEstimator

with open("config.yaml") as file:
    config = yaml.full_load(file)

cap = CustomVideoCapture(0)
depth_estimator = DepthEstimator()
pose_estimator = PoseEstimator(use_poseviz=config["pose_estimation"]["poseviz"])

frame_number = 0
tic = 0
while True:
    if config['print_fps']:
        fps = 1 / (time.time() - tic)
        tic = time.time()
        print("FPS: {}".format(fps))

    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find aruco markers
    arucoFound = findArucoMarkers(frame, frame_number)

    # Estimate depth
    if config["depth_estimation"]["enable"]:
        disparity_map, scaled_disparity_map = depth_estimator.predict(rgb_frame)

    # Pose estimation
    if config["pose_estimation"]["enable"]:
        pred_poses = pose_estimator.predict(rgb_frame)

    

    #Draw Aruco
    if len(arucoFound[0]) != 0:
        for bbox, id in zip(arucoFound[0], arucoFound[1]):
            frame = arucoIndex(bbox, id, frame)

    cv2.imshow("Frame", frame)

    if config["depth_estimation"]["show_depth_window"]:
        cv2.imshow("Depth estimation", scaled_disparity_map)
    
    key = cv2.waitKey(1)
    if not ret or key == ord('q'):
        break
    
    frame_number += 1

cap.release()
cv2.destroyAllWindows()