# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2


PATH_TO_LANDMARK_DETECTOR = "./trained_models/shape_predictor_68_face_landmarks.dat"

# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
FACIAL_LANDMARKS = dict({
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

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
# vs = VideoStream(0).start()
cap = cv2.VideoCapture(0)
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	# frame = vs.read()
	ret,frame = cap.read()
	frame = imutils.resize(frame, width=720)
	frame = cv2.flip(frame, flipCode=1)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
	# detect faces in the grayscale frame
	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		
		# shape = shape[FACIAL_LANDMARKS["mouth"][0]:FACIAL_LANDMARKS["mouth"][1]]
 
		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		for idx, (x, y) in enumerate(shape):
			cv2.putText(frame, str(idx), (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255))
			cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

		for j in range(FACIAL_LANDMARKS["mouth_outer"][0], FACIAL_LANDMARKS["mouth_outer"][1]):
			cv2.line(frame, (shape[j][0], shape[j][1]), (shape[j+1][0], shape[j+1][1]), (255,255,255))
		cv2.line(frame, (shape[59][0], shape[59][1]), (shape[48][0], shape[48][1]), (255,255,255))

		# cv2.line(frame, (shape[48][0], shape[48][1]), (shape[60][0], shape[60][1]), (255,255,255))
	  
	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()