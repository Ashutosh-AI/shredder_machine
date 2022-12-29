import cv2
import argparse
import datetime
from datetime import date
from imutils.video import VideoStream

import orien_lines
from utils import detector_utils
from utils.save_results import save_data


ap = argparse.ArgumentParser()
ap.add_argument('-d', '--display', dest='display', type=int,
                        default=1, help='Display the detected images using OpenCV. This reduces FPS')
args = vars(ap.parse_args())


detection_graph, sess = detector_utils.load_inference_graph()

lst1 = []
if __name__ == "__main__":
    # Detection confidence threshold to draw bbox
    score_thresh = 0.80

    vs = VideoStream(0).start()

    # Orientation of Machine
    Orientation = "bt"    # hand moving Direction, Enter the orientation of hand progression lr,rl,bt,tb
    # For Machine
    # Percent of Screen the line of Machine
    Line_perc1 = float(15)
    # For Safety
    # Percent of Screen for the line of safety
    Line_perc2 = float(30)

    num_hands_detect = 2

    start_time = datetime.datetime.now()
    num_frames = 0

    cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)


    def count_no_of_times(lst):
        x=y=cnt=0
        for i in lst:
            x=y
            y=i
            if x==0 and y==1:
                cnt += 1
        return cnt

    try:
        while True:
            frame = vs.read()
            im_height, im_width = frame.shape[:2]

            # Convert image to RGB, opencv reads BGR formats
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                print("Error Converting to RGB Format")

            # Run image through tensorflow graph
            boxes, score, classes = detector_utils.detect_objects(
                frame, detection_graph,sess)

            Line_Position2 = orien_lines.drawsafelines(frame, Orientation, Line_perc1, Line_perc2)

            # Draw bbox and text
            a = detector_utils.draw_box_on_image(num_hands_detect, score_thresh, score, boxes, classes, im_width, im_height, frame, Line_Position2, Orientation)

            lst1.append(a)
            # Calculate Frames per second (FPS)
            num_frames +=1
            elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
            fps = num_frames/elapsed_time

            if args["display"]:

                # Display FPS on frame
                detector_utils.draw_text_on_image(fps, frame)
                cv2.imshow("Detection", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                if cv2.waitKey(25) & 0xFF == ("q"):
                    cv2.destroyAllWindows()
                    vs.stop()
                    break

        no_of_time_hand_crossed = count_no_of_times(lst1)
        print(no_of_time_hand_crossed)
        today = date.today()
        save_data(no_of_time_hand_crossed)
        print("Average FPS: ", str("{0:.2f}".format(fps)))

    except KeyboardInterrupt:
        no_of_time_hand_crossed = count_no_of_times(lst1)
        print(no_of_time_hand_crossed)
        today = date.today()
        save_data(no_of_time_hand_crossed)
        print("Average FPS: ", str("{0:.2f}".format(fps)))
