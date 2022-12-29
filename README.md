# shredder_machine

# Problem Statement

As many of us may have come across the accidents in the newspapers about the shredder-machine that several workers got their hands chopped off due to carelessness or whatever may be the reason. This is why i took this problem and tried to built a solution for it. Those who do not know what is a shredder-machine just find the images attached below:-

![shredder machine1](https://user-images.githubusercontent.com/53949585/209928577-1744208b-d6d8-4350-ab86-bdf8d6513fc8.jpg) 
![shredder machine2](https://user-images.githubusercontent.com/53949585/209928602-bbc72730-822f-4b5f-b623-2afd4811b01c.jpg)

# Solution
I have designed an AI solution using the Computer Vision which includes the following functionality:-

 --> I am collecting the live feed from the cameras installed it can be any camera, we just need to configure it in our code using the RTSP protocol (using OpenCV)
--> Built a hand detection model to detect hands in the frame captured by the live feed from the camera.
--> experimented with several models like Faster RCNNs, SSDs but at last i selected SSD model because it giving good performance on hand detection as well as good processing speed.
--> Collected good no. of images of the hands variations and then performed the data augmentation on top of it to make it more robust more every possible lighting condition. --> Labelled the images with two classes i.e

1. Closed hand(fist) as Gloved Hand
2. Normal Hand image

--> Then i created two border lines with respect to the frame with the help of distance formula that we were capturing.

1. Safety Border line (Which will give us the alert alarm if our hand passes that line)
2. Machine Borderline, if the hand is close to it then our code will pass a signal to the shredder-machine and it will switch off automatically in order to avoid any accident.
3. With respect to that lines i am also calculating the distance of the hand from Sefty border line.

![Hand_pic1](https://user-images.githubusercontent.com/53949585/209933274-d3806b27-65bc-439f-b935-fa85a163d33c.jpg)
![Hand_pic2](https://user-images.githubusercontent.com/53949585/209933302-1acf22bf-1a31-468e-ab0a-c049344d8f91.jpg)
