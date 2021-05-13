import cv2 as cv
import numpy as np
import base64

List = [ [ ] ]
cList = [[]]
isDrawing = False

def nothing(x):
	pass
	pass

def render_lines(x, y):
	global List, cList
	b,g,r = (0, 0, 0)
	List[-1].append([x, y])
	cList[-1].append([int(b),int(g),int(r)])

def clear(event, x, y, flags, params):
	global List, cList
	if event == cv.EVENT_FLAG_LBUTTON:
		List = [[]]
		cList = [[]]


def calibration(frameO):
	global cap

	cv.namedWindow("calibration")
	cv.createTrackbar('hue lower', 'calibration', 50, 179, nothing)
	cv.createTrackbar('hue upper', 'calibration', 130, 179, nothing)
	cv.createTrackbar('sat lower', 'calibration', 90,255,nothing)
	cv.createTrackbar('sat upper', 'calibration', 255,255,nothing)
	cv.createTrackbar('vib lower', 'calibration', 60, 255, nothing)
	cv.createTrackbar('vib upper', 'calibration', 189, 255, nothing)
	cv.createTrackbar('start app', 'calibration', 0, 1, nothing)

	_, frameO = cap.read()
	frame = cv.flip(frameO, 1)
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	hl = cv.getTrackbarPos('hue lower', 'calibration')
	hu = cv.getTrackbarPos('hue upper', 'calibration')
	sl = cv.getTrackbarPos('sat lower', 'calibration')
	su = cv.getTrackbarPos('sat upper', 'calibration')
	vl = cv.getTrackbarPos('vib lower', 'calibration')
	vu = cv.getTrackbarPos('vib upper', 'calibration')

	lower = np.array([hl,sl,vl])
	range = np.array([hu,su,vu])

	rows,cols,chan = frame.shape
	temp = frame[20:rows-20, 20:cols-20]
	mask = cv.inRange(hsv, lower, range)
	
	tempmask = mask[20:rows-20, 20:cols-20]
	tempres = cv.bitwise_and(temp, temp, mask=tempmask)
	res = cv.copyMakeBorder(tempres, 20,20,20, 20, cv.BORDER_CONSTANT, value=[0,0,0])

	return (hl, hu, sl, su, vl, vu)

def canvas(raw_frame):

	global cap, List, cList , isDrawing
	hl, hu, sl, su, vl, vu = [50,130,90,255,60,189]

	frame = cv.flip(raw_frame, 1)
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	lower = np.array([hl,sl,vl])
	ranges = np.array([hu,su,vu])

	rows,cols,chan = frame.shape
	temp = frame[20:rows-20, 20:cols-20]
	mask = cv.inRange(hsv, lower, ranges)
	
	tempmask =  mask[20:rows-20, 20:cols-20]
	tempres = cv.bitwise_and(temp, temp, mask=tempmask)
	res = cv.copyMakeBorder(tempres, 20,20,20, 20, cv.BORDER_CONSTANT, value=[0,0,0])
	
	# cv.imshow("calibration", res)
	
	res2gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
	median = cv.medianBlur(res2gray, 23)

	contours, hierarchy = cv.findContours(median, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	if (len(contours) > 0) and (contours is not None) :
		cnt = contours[0]
		(a, b), r = cv.minEnclosingCircle(cnt)
		center = (int(a), int(b))
		radius = int(r)
		cv.circle(frame, center, radius, (0, 128 ,128), 4)

		render_lines(center[0], center[1])
		isDrawing = True
	else:
		if isDrawing:
			List.append([])
			cList.append([])
		isDrawing = False

	# white_arr = np.zeros(frame.shape, np.uint8)
	# white_arr += 255
	
	for i,j in zip(List,cList):
		if j !=[]:
			r,g,b = j[0]
			cv.polylines(frame,[np.array(i, dtype=np.int32)], False, (r,g,b), 2, cv.LINE_AA)
			
			# cv.polylines(white_arr,[np.array(i, dtype=np.int32)], False, (r,g,b), 2, cv.LINE_AA)

	# disp_arr = np.vstack((white_arr, frame))
	return frame

def convert_uri(uri):
	encoded = uri.split(',')[1]
	nparray = np.fromstring(base64.b64decode(encoded), np.uint8)
	img = cv.imdecode(nparray, cv.IMREAD_COLOR)
	return img

def convert_img(img):
	_, im_arr = cv.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
	im_bytes = im_arr.tobytes()
	b = base64.b64encode(im_bytes)
	b =b.decode()
	b = "data:image/jpeg;base64," + b
	return b
