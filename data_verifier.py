import numpy as np
import cv2
import pickle

FILE_NAME = "recorded_mouth_features"

cap = cv2.VideoCapture(FILE_NAME+".avi")
all_features_list = pickle.load(open(FILE_NAME+".p"), "rb")

while True:

	ret, frame = cap.read()

	if ret == True:
		cv2.imshow("frame", frame)
		key = cv2.waitKey(1) & 0xFF
	 
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
	else:
		break

cap.release()
cv2.destroyAllWindows()