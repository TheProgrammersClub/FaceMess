# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import os
import argparse
import imutils
import time
import dlib
import cv2
import math
import pickle

PATH_TO_LANDMARK_DETECTOR = "../trained_models/shape_predictor_68_face_landmarks.dat"


def calc_geometric_distance(x1, y1, x2, y2):
	return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )




def alignFace(frame, gray, rect, aligner):
	(x, y, w, h) = face_utils.rect_to_bb(rect)
	faceOrig = imutils.resize(frame[y:y + h, x:x + w], width=256)
	faceAligned = aligner.align(frame, gray, rect)

	return faceOrig, faceAligned


def main():
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
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	ret,frame = cap.read()


	# loop over the frames from the video stream
	while True:

		ret,frame = cap.read()

		if ret == True:
			frame = imutils.resize(frame, width=800)
			frame = cv2.flip(frame, flipCode=1)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		 
			# detect faces in the grayscale frame
			rects = detector(gray, 0)
			
			for rect in rects:

				faceOrig, faceAligned = alignFace(frame, gray, rect, aligner)

				shape = predictor(gray, rect)
				shape = face_utils.shape_to_np(shape)

				for (x, y) in shape:
					cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)



				# show the frame
				cv2.imshow("FaceOriginal", frame)
				cv2.imshow("FaceAligned", faceAligned)


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

if __name__ == "__main__":
	main()