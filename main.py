import cv2
import numpy as np
import mouse


def image_resize(image, width = None, height = None):
    dim = None
    (h, w) = image.shape[:2]

    r = width / float(w)
    dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = cv2.INTER_LINEAR_EXACT)

    return resized

cap = cv2.VideoCapture(0)


while True:
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lneon = np.array([20, 144, 121])
	uneon = np.array([93, 255, 255])
	mask_neon = cv2.inRange(hsv, lneon, uneon)

	contoursneon, _ = cv2.findContours(mask_neon, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in contoursneon :
		if cv2.contourArea(c) <= 50 :
			continue
		x, y, _, _ = cv2.boundingRect(c)
		#print(x)
		mouse.move(x, y, absolute=True, duration=0.1)
		cv2.drawContours(frame, contoursneon, -1, (0, 255, 0), 3)
	
	frame = image_resize(frame, width = 500)  
	cv2.imshow("frame", frame)
	
	key = cv2.waitKey(1)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()