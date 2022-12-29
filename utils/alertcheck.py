import cv2
from playsound import playsound


def draw_box_to_safeline(image_np, p1, p2, Line_Position2, Orientation):

    if(Orientation == "bt"):

        bounding_mid = (int((p1[0] + p2[0])/2), int(p1[1]))
        if(bounding_mid):
            cv2.line(image_np, pt1=bounding_mid, pt2=(bounding_mid[0], Line_Position2), color=(255,0,0), thickness=1, lineType=8, shift=0)
            distance_from_line = bounding_mid[1] - Line_Position2

    elif(Orientation == "tb"):

        boundimg_mid = (int((p1[0] + p2[0])/2), p2[1])
        if(boundimg_mid):
            cv2.line(image_np, pt1=boundimg_mid, pt2=(boundimg_mid[0], Line_Position2), color=(255,0,0), thickness=1, lineType=8, shift=0)
            distance_from_line = Line_Position2 - boundimg_mid[1]

    elif (Orientation == "lr"):

        bounding_mid = (int(p2[0]), int((p1[1] + p2[1]) / 2))
        if (bounding_mid):
            cv2.line(img=image_np, pt1=bounding_mid, pt2=(Line_Position2, bounding_mid[1]), color=(255, 0, 0), thickness=1, lineType=8, shift=0)
            distance_from_line = Line_Position2 - bounding_mid[0]

    elif (Orientation == "rl"):

        bounding_mid = (int(p1[0]), int((p1[1] + p2[1]) / 2))
        if (bounding_mid):
            cv2.line(img=image_np, pt1=bounding_mid, pt2=(Line_Position2, bounding_mid[1]), color=(255, 0, 0), thickness=1, lineType=8, shift=0)
            distance_from_line = bounding_mid[1] - Line_Position2


    if (distance_from_line <= 0):

        posii = int(image_np.shape[1]/2)
        cv2.putText(image_np, "ALERT", (posii,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0), thickness=2)
        playsound("utils/alert.wav")
        cv2.rectangle(image_np, pt1=(posii-10,20), pt2=(posii+75,60), color=(255,0,0), thickness=3, lineType=8, shift=0)
        return 1
    else:
        return 0