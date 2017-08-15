# Importing libraries
import numpy as np
import cv2
import pickle
from PIL import Image

# Recording video
cap = cv2.VideoCapture(0)
frames = []
while True:
	ret,frame = cap.read()
	h,w,_ = frame.shape

	image = {
	'pixels': frame.tobytes(),
	'size': (h,w),
	'mode': "BGR;16",
	}
	frames.append(image)

	cv2.imshow("Video",frame)
	key = cv2.waitKey(1)
	if key == ord('q'):
		break

# Cleaning Up
print(len(frames))
cap.release()
cv2.destroyAllWindows()

# Dumping the frames onto a pickle file
with open('frames.pkl','wb') as file:
	pickle.dump(frames,file)

# Loading frames from the pickle file
frames = []
with open('frames.pkl','rb') as file:
	frames = pickle.load(file)

for frame in frames:
	img = Image.frombytes(frame['mode'],frame['size'],frame['pixels'])
	img.show()