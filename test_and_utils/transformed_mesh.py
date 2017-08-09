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
import numpy as np

# Custom libs
import affine_transform

PATH_TO_LANDMARK_DETECTOR = "../trained_models/shape_predictor_68_face_landmarks.dat"


def calc_geometric_distance(x1, y1, x2, y2):
	return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )


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

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PATH_TO_LANDMARK_DETECTOR)

# initialize the face aligner
aligner = face_utils.FaceAligner(predictor, desiredFaceWidth=256)

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
cap = cv2.VideoCapture(0)
ret,frame = cap.read()

mesh = np.zeros((512, 512, 3), np.uint8)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	# frame = vs.read()
	ret,frame = cap.read()

	cv2.imshow("mesh", mesh)

	if ret == True:
		frame = imutils.resize(frame)
		frame = cv2.flip(frame, flipCode=1)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\
	 
		# detect faces in the grayscale frame
		rects = detector(gray, 0)
		
		if len(rects) > 0:
			rect = rects[0]

			faceOrig, faceAligned = affine_transform.alignFace(frame, gray, rect, aligner)
			alignedGray = cv2.cvtColor(faceOrig, cv2.COLOR_BGR2GRAY)
			alignedRect = detector(alignedGray, 0)

			if len(alignedRect) > 0:
				alignedRect = alignedRect[0]

				# determine the facial landmarks for the face region, then
				# convert the facial landmark (x, y)-coordinates to a NumPy
				# array
				shape = predictor(alignedGray, alignedRect)
				shape = face_utils.shape_to_np(shape)
				mesh = np.zeros((512, 512, 3), np.uint8)

				# left_eye_mesh = []
				# for (x, y) in shape[LM["left_eye"][0]:LM["left_eye"][1]]:
				# 	left_eye_mesh.append([x+128, y+128])
				# left_eye_mesh = np.array(left_eye_mesh)

				face_mesh = []
				for (x, y) in shape[LM["jaw"][0]:LM["jaw"][1]]:
					face_mesh.append([x+128, y+128])
				for (x, y) in shape[LM["left_eyebrow"][1]-1:LM["left_eyebrow"][0]-1:-1]:
					face_mesh.append([x+128, y+100])
				for (x, y) in shape[LM["right_eyebrow"][1]-1:LM["right_eyebrow"][0]-1:-1]:
					face_mesh.append([x+128, y+100])
				face_mesh = np.array(face_mesh)
				cv2.fillConvexPoly(mesh, face_mesh, (255, 255, 255))

				left_eyebrow_mesh = []
				for (x, y) in shape[LM["left_eyebrow"][0]:LM["left_eyebrow"][1]]:
					left_eyebrow_mesh.append([x+128, y+128])
				left_eyebrow_mesh = np.array(left_eyebrow_mesh)
				cv2.polylines(mesh, [left_eyebrow_mesh], False, (255, 0, 0), 3)

				right_eyebrow_mesh = []
				for (x, y) in shape[LM["right_eyebrow"][0]:LM["right_eyebrow"][1]]:
					right_eyebrow_mesh.append([x+128, y+128])
				right_eyebrow_mesh = np.array(right_eyebrow_mesh)
				cv2.polylines(mesh, [right_eyebrow_mesh], False, (255, 0, 0), 3)

				right_eye_mesh = []
				for (x, y) in shape[LM["right_eye"][0]:LM["right_eye"][1]]:
					right_eye_mesh.append([x+128, y+128])
				right_eye_mesh = np.array(right_eye_mesh)
				cv2.fillConvexPoly(mesh, right_eye_mesh, (0, 255, 0))

				left_eye_mesh = []
				for (x, y) in shape[LM["left_eye"][0]:LM["left_eye"][1]]:
					left_eye_mesh.append([x+128, y+128])
				left_eye_mesh = np.array(left_eye_mesh)
				cv2.fillConvexPoly(mesh, left_eye_mesh, (0, 255, 0))

				mouth_outer_mesh = []
				for (x, y) in shape[LM["mouth_outer"][0]:LM["mouth_outer"][1]]:
					mouth_outer_mesh.append([x+128, y+128])
				mouth_outer_mesh = np.array(mouth_outer_mesh)
				cv2.fillConvexPoly(mesh, mouth_outer_mesh, (0, 0, 255))

				mouth_inner_mesh = []
				for (x, y) in shape[LM["mouth_inner"][0]:LM["mouth_inner"][1]]:
					mouth_inner_mesh.append([x+128, y+128])
				mouth_inner_mesh = np.array(mouth_inner_mesh)
				cv2.fillConvexPoly(mesh, mouth_inner_mesh, (0, 0, 0))
				# for (x, y) in shape[LM["right_eyebrow"][1]-1:LM["right_eyebrow"][0]-1:-1]:
				# 	face_mesh.append([x+128, y+128])



				

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
cv2.destroyAllWindows()