# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import os
import argparse
import imutils
import time
import dlib
import cv2
import math
import pickle


PATH_TO_LANDMARK_DETECTOR = "./trained_models/shape_predictor_68_face_landmarks.dat"
TEST_NAME = "test_run"
FOLDER_NAME = "./trained_models/"+TEST_NAME

if not os.path.exists(FOLDER_NAME):
	os.makedirs(FOLDER_NAME)

n = 3
def calc_geometric_distance(x1, y1, x2, y2):
	# return pow(((x2-x1)**n + (y2-y1)**n),1.0/n)			# Minkowski Distance	
	return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )			# Eucledian Distance
	# return (abs(x1 - x2) + abs(y1 - y2))					# Manhattan Distance

def alignFace(frame, gray, rect, aligner):
	(x, y, w, h) = face_utils.rect_to_bb(rect)
	faceOrig = imutils.resize(frame[y:y + h, x:x + w], width = 512)
	faceAligned = aligner.align(frame, gray, rect)
	return faceOrig, faceAligned


# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
LM = dict({
	"mouth_outer": (48, 59),
	"mouth_inner": (60, 67),
	"mouth": (48, 68),
	"right_eyebrow": (17, 22),
	"left_eyebrow": (22, 27),
	"right_eye": (36, 42),
	"left_eye": (42, 48),
	"nose": (27, 35),
	"jaw": (0, 17)
})

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PATH_TO_LANDMARK_DETECTOR)

aligner = face_utils.FaceAligner(predictor, desiredFaceWidth=256)

cap = cv2.VideoCapture('speech.avi')	# Replace the filename
ret,frame = cap.read()

frame_number = -1
global_mouth_feature_list = []

# loop over the frames from the video stream
while True:
	frame_number += 1
	current_mouth_features = []
	# frame = vs.read()
	ret,frame = cap.read()

	if ret == True:
		frame = imutils.resize(frame)
		frame = cv2.flip(frame, flipCode=1)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	 
		# detect faces in the grayscale frame
		rects = detector(gray, 0)
		
		if len(rects) > 0:
			rect = rects[0]

			faceOrig, faceAligned = alignFace(frame, gray, rect, aligner)
			alignedGray = cv2.cvtColor(faceOrig, cv2.COLOR_BGR2GRAY)
			alignedRect = detector(alignedGray, 0)
			
			if len(alignedRect) > 0:
				alignedRect = alignedRect[0]

				shape = predictor(alignedGray, alignedRect)
				shape = face_utils.shape_to_np(shape)

				for j in range(LM["mouth_outer"][0], LM["mouth_outer"][1]):
					current_mouth_features.append(calc_geometric_distance(shape[j][0], shape[j][1], shape[j+1][0], shape[j+1][1]))

					if j == LM["mouth_outer"][1]-1:
						current_mouth_features.append(calc_geometric_distance( shape[j+1][0], shape[j+1][1], shape[ LM["mouth_outer"][0] ][0], shape[ LM["mouth_outer"][0] ][1] ))


				for j in range(LM["mouth_inner"][0], LM["mouth_inner"][1]+1):
					for k in range(LM["mouth_inner"][0], LM["mouth_inner"][1]+1):
						current_mouth_features.append(calc_geometric_distance( shape[j][0], shape[j][1], shape[k][0], shape[k][1] ))

				global_mouth_feature_list.append((current_mouth_features, frame_number))

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

print(len(global_mouth_feature_list))
pickle.dump(global_mouth_feature_list, open( os.path.join(FOLDER_NAME, TEST_NAME+'.p'), "wb" ))
# do a bit of cleanup
cap.release()
cv2.destroyAllWindows()