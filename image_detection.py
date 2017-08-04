from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import math
import cv2
import pickle

global_array = []

def eucledian_distance(x1,y1,x2,y2):
	return math.sqrt( (x1-x2)**2+(y1-y2)**2)

cap = cv2.VideoCapture(0)
	
PATH_TO_LANDMARK_DETECTOR = "./shape_predictor_68_face_landmarks.dat"
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PATH_TO_LANDMARK_DETECTOR)

while True:
	ret,frame = cap.read()
	frame = imutils.resize(frame, width=480)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	 
	rects = detector(gray, 0)

	for rect in rects:
		array = []
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)		

		# find the keypoints for each face in the frame & store them
		for idx, (x, y) in enumerate(shape):
			array.append((x,y))

		distances = []
		for coord in array:
			x1,y1 = coord[0],coord[1]
			for curr in array:
				x2,y2 = curr[0],curr[1]
				value = eucledian_distance(x1, y1, x2, y2)
				distances.append(value)

		global_array.append(distances)
		cv2.imshow("Live",frame)

	key = cv2.waitKey(1)
	if key == ord(' '):
		cv2.imwrite("snap.png",frame)
	elif key == ord('q'):
		break
cv2.destroyAllWindows()

with open('face_coordinates.pkl', 'wb') as f:
	pickle.dump(global_array, f)