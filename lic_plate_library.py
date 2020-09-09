import cv2
import numpy as np
import pytesseract

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    for x in range(0,rows):
        for y in range(0,len(imgArray[x])):
            if len(imgArray[x][y].shape)==2:
                imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
            if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0,0), fx=scale, fy=scale)
            else:
                imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), fx=scale, fy=scale)
            if y == 0:
                horiz = imgArray[x][y]
            else:
                horiz = np.hstack((horiz, imgArray[x][y]))
        if len(imgArray[x]) < cols and y < len(imgArray[x]):
            blank = np.zeros((imgArray[0][0].shape[0], imgArray[0][0].shape[1], 3), np.uint8)
            for i in range(0, cols - len(imgArray[x])):
                horiz = np.hstack((horiz, blank))
        if x == 0:
            vertic = horiz
        else:
            vertic = np.vstack((vertic, horiz))

    return vertic


def printLicensePlate(imgname):
    img = cv2.imread(imgname)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = pytesseract.image_to_string(imgRGB)
    return res