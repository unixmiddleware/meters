# import the necessary packages
from shapes import ShapeDetector
import argparse
import imutils
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
print('Initial size', image.size)
print('Initial shape', image.shape)
resized = cv2.resize(image, (320,240))
print('Resized size', resized.size)
print('Resized shape', resized.shape)
cv2.imshow('Resized',resized)
cv2.moveWindow('Resized',0,0)

ratio = resized.shape[0] / float(resized.shape[0])
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray',gray)
cv2.moveWindow('Gray',340,0)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow('Blurred',blurred)
cv2.moveWindow('Blurred',680,0)

blurred = gray

thresh = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY)[1]
# find contours in the thresholded image and initialize the
# shape detector
contours,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('Number of Contours',len(contours))
contours = [x for x in contours if cv2.contourArea(x) > 10]
print('Number of big Contours',len(contours))
contours = sorted(contours, key=lambda x: cv2.contourArea(x),reverse=True)

sd = ShapeDetector()
# loop over the contours
cnum=0
for c in contours:
	(x,y,w,h) = cv2.boundingRect(c)
	shape = sd.detect(c)
	print('Shape{} {} x={}, y={}, w={}, h={}'.format(cnum,shape,x,y,w,h))
	cnum += 1
	r1 = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
	cv2.rectangle(r1,(185,15),(280,35),(0,255,0),3)
	if shape == 'circle':
		cv2.circle(r1,(x+(x//2),y-(y//2)),3,(0,0,255),-1)
	else:
		cv2.rectangle(r1,(x,y),(x+w,y+h),(255,0,0),3)
	win = '{}: {} ({},{})'.format(cnum,shape,x,y)
	cv2.imshow(win, r1)
	cv2.moveWindow(win,0+(cnum*100),440+(cnum*40))
	cv2.waitKey(0)

#	# multiply the contour (x, y)-coordinates by the resize ratio,
#	# then draw the contours and the name of the shape on the image
#	c = c.astype("float")
#	c *= ratio
#	c = c.astype("int")
#	r1 = resized
#	cv2.drawContours(r1, [c], -1, (255, 0, 0), 2)
#	cv2.putText(r1, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#	# show the output r1
