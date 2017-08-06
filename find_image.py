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

def eucledian_distance(x1,y1,x2,y2):
	return math.sqrt( (x1-x2)**2+(y1-y2)**2)

PATH_TO_LANDMARK_DETECTOR = "./shape_predictor_68_face_landmarks.dat"
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PATH_TO_LANDMARK_DETECTOR)

with open('face_coordinates.pkl', 'rb') as f:
	array = pickle.load(f)

img = cv2.imread("images.jpg")
img = imutils.resize(img, width=480)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	 
rects = detector(gray, 0)
distances = []

for rect in rects:
	curr_array = []
	shape = predictor(gray, rect)
	shape = face_utils.shape_to_np(shape)		

	for idx, (x, y) in enumerate(shape):
		curr_array.append((x,y))
	
	distances = []
	for coord in curr_array:
		x1,y1 = coord[0],coord[1]
		for curr in curr_array:
			x2,y2 = curr[0],curr[1]
			value = eucledian_distance(x1, y1, x2, y2)
			distances.append(value)

for i in array:
	if i == distances:
		print("Yes")