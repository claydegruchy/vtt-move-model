#!/usr/bin/env python
import cv2
import numpy as np
import requests
import time
from pyzbar import pyzbar
import imutils
from shapedetector import ShapeDetector



def detect_barcode(image):
    print("detect_barcode")
    # image = cv2.imread(args["image"])
    # find the barcodes in the image and decode each of the barcodes

# make black and white
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 6, 255, cv2.THRESH_BINARY)[1]
    # blur = cv2.GaussianBlur(image,(5,5),0)
    # add an adaptive threshhold
    ret3,image = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


    # image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


# look for barcodes
    barcodes = pyzbar.decode(image)



    # loop over the detected barcodes
    for barcode in barcodes:
        # print(barcode)
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 2)
        # print the barcode type and data to the terminal
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    return image



# def detect_shape(image):
#     # doesnt work
#     print("detect_shape")
#         # convert the resized image to grayscale, blur it slightly,
#     # and threshold it
#     ratio = 1
#
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
#
#     # find contours in the thresholded image and initialize the
#     # shape detector
#     cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#         cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#     sd = ShapeDetector()
#
#     # loop over the contours
#     for c in cnts:
#         # compute the center of the contour, then detect the name of the
#         # shape using only the contour
#         c.astype('int8')
#
#         M = cv2.moments(c)
#         cX = int((M["m10"] / M["m00"]) * ratio)
#         cY = int((M["m01"] / M["m00"]) * ratio)
#         shape = sd.detect(c)
#
#         # multiply the contour (x, y)-coordinates by the resize ratio,
#         # then draw the contours and the name of the shape on the image
#         c = c.astype("float")
#         c *= ratio
#         c = c.astype("int")
#         cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
#         cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
#             0.5, (255, 255, 255), 2)
#
#     # return image

while True:

    print("start")

    # get the imamge
    url = r'http://192.168.1.248:8080/live.jpg'
    resp = requests.get(url, stream=True).raw
    # convert it for use
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)


    # pass into the processor
    image = detect_barcode(image)
    # detect_shape(image)


    # for testing
    cv2.imshow('image',image)
    # cv2.waitKey(33)
    # if k==27:    # Esc key to stop
    #     break
    cv2.waitKey(5)
    # cv2.destroyAllWindows()

    print("done, sleeping")
    time.sleep(0.2)
