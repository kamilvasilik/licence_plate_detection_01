# License Plate Detection

import cv2
import pytesseract
from lic_plate_library import stackImages, printLicensePlate


def LPDetection():
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    cam.set(10, 100)

    licPlateClassifier = cv2.CascadeClassifier('Resources/haarcascades/haarcascade_russian_plate_number.xml')

    count = 0
    while True:
        success, imgWeb = cam.read()
        imgGray = cv2.cvtColor(imgWeb, cv2.COLOR_BGR2GRAY)
        licensePlate = licPlateClassifier.detectMultiScale(imgGray, 1.1, 10)
        for (x, y, w, h) in licensePlate:
            area = w*h
            if area > 500:
                cv2.rectangle(imgWeb, (x,y), (x+w, y+h), (255, 0, 255), 2)
                cv2.putText(imgWeb, 'License Plate', (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                imgROI = imgWeb[y:y+h, x:x+w]
                imgROIstack = stackImages(3, [[imgROI]])
                cv2.imshow('License Plate', imgROIstack)

        imgStack = stackImages(.8, [[imgWeb]])
        cv2.imshow('WebCam', imgStack)

        keypressed = cv2.waitKey(1)
        if keypressed == ord('s'):
            imgwritename = 'Resources/LicPLate_' + str(count) + '.jpg'
            cv2.imwrite(imgwritename, imgROI)
            plp = printLicensePlate(imgwritename)
            if plp == "":
                print('Not clear')
            else:
                print(plp)
                cv2.rectangle(imgWeb, (0,200), (640, 300), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgWeb, 'Scan Saved', (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
                cv2.imshow('WebCam', imgWeb)
                cv2.waitKey(500)
                count += 1
        elif keypressed == ord('q'):
            break


if __name__ == '__main__':
    LPDetection()