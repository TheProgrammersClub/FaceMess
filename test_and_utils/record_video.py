# import the necessary packages
import imutils
import datetime
import os
import argparse
import cv2


TEST_NAME = "test_run"
FOLDER_NAME = "../trained_models/"+TEST_NAME


if not os.path.exists(FOLDER_NAME):
	os.makedirs(FOLDER_NAME)


# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
cap = cv2.VideoCapture(0)
	
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
ret,frame = cap.read()
height,width,_ = frame.shape
# height, width = 256, 256

out = cv2.VideoWriter(os.path.join(FOLDER_NAME, TEST_NAME+'.avi'),fourcc, 20.0,(width,height))

# loop over the frames from the video stream
while True:

	ret,frame = cap.read()

	if ret == True:
		frame = imutils.resize(frame)
		frame = cv2.flip(frame, flipCode=1)
		
		out.write(frame)

		# show the frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	 	
		if key == ord(" "):
	 		cv2.imwrite("snapshot.png", frame)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	else:
		break


# do a bit of cleanup
cap.release()
out.release()
cv2.destroyAllWindows()