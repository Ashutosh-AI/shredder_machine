# Utilities for object detector.

import numpy as np
import tensorflow as tf
import os
import cv2
from utils import label_map_util
from utils import alertcheck


TRAINED_MODEL_DIR = "./frozen_graphs"
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = TRAINED_MODEL_DIR + "/ssd5_optimized_inference_graph.pb"
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = TRAINED_MODEL_DIR + "/Glove_label_map.pbtxt"
NUM_CLASSES = 2

# load label map using utils provided by tensorflow object detection api
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)

categories = label_map_util.convert_label_map_to_categories(
    label_map=label_map, max_num_classes=NUM_CLASSES, use_display_name=True)

# Creates dictionary of COCO compatible categories keyed by category id
category_index = label_map_util.create_category_index(categories)

a = 0

# Load a frozen infrerence graph into memory
def load_inference_graph():
    # load frozen tensorflow model into memory

    print("> ====== Loading frozen graph into memory")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    print(">  ====== Inference graph loaded.")
    return detection_graph, sess


# Actual detection .. generate scores and bounding boxes given an image
def detect_objects(image_np, detection_graph, sess):
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name(
        'detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name(
        'detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name(
        'num_detections:0')

    image_np_expanded = np.expand_dims(image_np, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores,
            detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    return np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes)


def draw_box_on_image(num_hands_detect, score_thresh, scores, boxes, classes, im_width, im_height, image_np, Line_Position2, Orientation):
    # Determined using a piece of paper of known length, code can be found in distance to camera
    focalLength = 875
    # The average width of a human hand (inches) http://www.theaveragebody.com/average_hand_size.php
    # added an inch since thumb is not included
    avg_width = 4.0
    # To more easily differetiate distances and detected bboxes

    global a
    color0 = (255,0,0)
    color1 = (0,0,255)

    for i in range(num_hands_detect):

        if (scores[i]>score_thresh):

            if classes[i] == 1:
                id = "hand"

            if classes[i] == 2:
                id = "gloved_hand"
                avg_width = 3.0 # To compensate bbox size change

            if i==0: color = color0
            else: color = color1

            y_min, x_min, y_max, x_max = (boxes[i][0]*im_height, boxes[i][1]*im_width,
                                         boxes[i][2]*im_height, boxes[i][3]*im_width)
            left, right, top, bottom = (x_min, x_max, y_min, y_max)

            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            cv2.rectangle(image_np, p1,p2, color)

            cv2.putText(image_np, "hand" + str(i) + ": " + id, (int(left), int(top)-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            cv2.putText(image_np, "Confidence" + str("{0:.2f}".format(scores[i])), (int(left), int(top)-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            a = alertcheck.draw_box_to_safeline(image_np, p1, p2, Line_Position2, Orientation)
    return a


# Show fps value on image
def draw_text_on_image(fps, image_np):
    cv2.putText(image_np, "FPS : " + str("{0:.2f}".format(fps)),
                (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (77,255,9), 2)

