# Libraries Import
import numpy as np
import cv2
import dlib
import imutils
import pickle
from imutils import face_utils
import math
import glob

def eucledian_distance(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# Initialization
global_array = []
PATH_TO_LANDMARK_DETECTOR = "../shape_predictor_68_face_landmarks.dat"
LM = dict({
	"mouth_outer" : (48,59),
	"mouth_inner" : (60,67)
	})
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PATH_TO_LANDMARK_DETECTOR)

# Save frames from the video
cap = cv2.VideoCapture(0)
count = 0
while True:
	ret,frame = cap.read()
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	key = cv2.waitKey(1)
	if key == ord(' '):
		cv2.imwrite('snap_'+str(count)+'.png',frame)
		count += 1
	elif key == ord('q'):
		break
	cv2.imshow("Frame",frame)

# Read all the images & find the distance between keypoints
images = []
for img in glob.glob("./*.png"):
	temp = cv2.imread(img)
	images.append(temp)

for img in images:
	frame = imutils.resize(img,width = 360)
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	rects = detector(gray,0)

	for rect in rects:
		array = []
		shape = predictor(gray,rect)
		shape = face_utils.shape_to_np(shape)

		for i in range(LM["mouth_inner"][0], LM["mouth_inner"][1]+1):
			for j in range(LM["mouth_inner"][0], LM["mouth_inner"][1]+1):
				array.append(eucledian_distance( shape[i][0], shape[i][1], shape[j][0], shape[j][1] ))

	global_array.append(array)

length = 0
for i in global_array:
	length += len(i)
print(length,np.shape(global_array))

# display = np.zeros((480,640,3),np.uint8)
print("Difference between the distances between keypoints for the inner_mouth")
for idx_i,i in enumerate(global_array):
	for idx_j,j in enumerate(global_array):
		diff = np.array(i) - np.array(j)
		print(diff)
		# cv2.putText(display, str(diff), (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1)
		cv2.imshow("Images",np.hstack([images[idx_i],images[idx_j]]))
		# cv2.imshow("Difference",display)
		cv2.waitKey(0)	

cv2.destroyAllWindows()