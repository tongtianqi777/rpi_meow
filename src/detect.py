"""Main script to run the object detection routine."""
import argparse
import sys
import time
from typing import List

import cv2
from detector.object_detector import ObjectDetector, Detection
from detector.object_detector import ObjectDetectorOptions
import detector.utils as utils
from db import DB

from redis_handle import RedisHandle
from commons import SAW_CAT_EVENT, SAW_CAT, LAST_TIME_SAW_CAT
from config import LAST_TIME_SAW_CAT_IMG

DETECT_FREQUENCY = 1  # every 1 second. limiting the detect frequency cause CPU and GPU may get too hot

CAT_LABEL = "cat"  # assuming there's only this label that represents cats
SCORE_THRESHOLD = 0.5  # only when it's above this value do we consider a trustworthy detection

ONE_MIN = 60  # 60s


def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool, visualize: bool) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
      model: Name of the TFLite object detection model.
      camera_id: The camera id to be passed to OpenCV.
      width: The width of the frame captured from the camera.
      height: The height of the frame captured from the camera.
      num_threads: The number of CPU threads to run the model.
      enable_edgetpu: True/False whether the model is a EdgeTPU model.
    """
    redis_handle = RedisHandle()
    db = DB()

    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    last_time_saw_cat = time.time() - ONE_MIN  # so that we can catch it if cat shows up right after launch

    # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=num_threads,
        score_threshold=0.5,
        max_results=3,  # there can be a couple of things in the view
        enable_edgetpu=enable_edgetpu)
    detector = ObjectDetector(model_path=model, options=options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        counter += 1
        image = cv2.flip(image, 0)  # flip image vertically
        image = cv2.flip(image, 1)  # flip image horizontally

        # Run object detection estimation using the model.
        detections = detector.detect(image)

        if saw_cat(detections):
            curr_time = time.time()
            redis_handle.set(SAW_CAT, 'true')
            redis_handle.set(LAST_TIME_SAW_CAT, str(curr_time))

            if curr_time - last_time_saw_cat > ONE_MIN:
                # keep a record only when it has been more than 1 min (to reduce DB size)
                db.add_event_history(SAW_CAT_EVENT)  # log to DB
                cv2.imwrite(LAST_TIME_SAW_CAT_IMG, image)  # write the current shot as image to disk
                last_time_saw_cat = curr_time
        else:
            redis_handle.set(SAW_CAT, 'false')

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()
            counter = 0
            redis_handle.set('fps', fps)  # for monitoring

        if visualize:
            # Draw keypoints and edges on input image
            image = utils.visualize(image, detections)

            # Show the FPS
            fps_text = 'FPS = {:.1f}'.format(fps)
            text_location = (left_margin, row_size)
            cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        font_size, text_color, font_thickness)

            cv2.imshow('object_detector', image)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break

        time.sleep(DETECT_FREQUENCY)

    cap.release()
    cv2.destroyAllWindows()


def saw_cat(detections: List[Detection]) -> bool:
    """
    see if there's cat in all the detection results
    :param detections: a list of detections
    :return: a boolean val
    """
    # there can a couple of object detected
    for detection in detections:

        # there can be a couple of categories for each object
        for category in detection.categories:
            if category.label == CAT_LABEL and category.score >= SCORE_THRESHOLD:
                return True

    return False


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        default='detector/efficientdet_lite0.tflite')
    parser.add_argument(
        '--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=480)
    parser.add_argument(
        '--numThreads',
        help='Number of CPU threads to run the model.',
        required=False,
        type=int,
        default=4)
    parser.add_argument(
        '--enableEdgeTPU',
        help='Whether to run the model on EdgeTPU.',
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        '--visualize',
        help='Whether to visualize the object detection in a separate window for debugging',
        action='store_true',
        required=False,
        default=False)
    args = parser.parse_args()

    run(
        args.model,
        int(args.cameraId),
        args.frameWidth,
        args.frameHeight,
        int(args.numThreads),
        bool(args.enableEdgeTPU),
        args.visualize
    )


if __name__ == '__main__':
    main()
