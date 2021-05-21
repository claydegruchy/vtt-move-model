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
    # image = cv2.GaussianBlur(image,(5,5),0)
    # add an adaptive threshhold
    ret3, image = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    image = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


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
        barcodeText = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeText, barcodeType)
        cv2.putText(image, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # print the barcode type and data to the terminal

        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeText))
    return [image, barcodes]


barcodes_history = {}
barcodes_locations = {}

offline = False


test_images = [
    './test_images/live (1).jpg',
    './test_images/live (2).jpg',
    './test_images/live (3).jpg'
]

cycle = 0

while True:

    print("starting detection cycle")
    if offline:
        image = cv2.imread(test_images[cycle])
        cycle += 1
        if cycle > 2:
            cycle = 0
    else:
        # get the imamge
        try:
            url = r'http://192.168.1.248:8080/live.jpg'
            resp = requests.get(url, stream=True).raw
            # convert it for use
            image = np.asarray(bytearray(resp.read()), dtype="uint8")

            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        except Exception as e:
            print("could not contact server")
            continue

    original = image
# FISHEYE PREVENTION
    # from defisheye import Defisheye
    #
    # dtype = 'stereographic'
    # format = 'fullframe'
    # fov = 85
    # pfov = 80
    #
    #
    # obj = Defisheye(image, dtype=dtype, format=format, fov=fov, pfov=pfov)
    # image = obj.convert("img_out")
    # # break

    # pass into the processor
    image, barcodes = detect_barcode(image)

    # process eacch barcode
    for barcode in barcodes:
        # decode
        barcodeText = barcode.data.decode("utf-8")

        # get the rect
        (x, y, w, h) = barcode.rect

        # find the centre of the current snapshot
        centre = (x + w // 2,  y + h // 2)

    # if the code is not in the dict, add it
        if barcodeText not in barcodes_history:
            barcodes_history[barcodeText] = {"locations": [], "info": {}}
        barcodes_history[barcodeText]["info"]["failures"] = 0
        barcodes_history[barcodeText]["info"]["updated"] = True
        # insert the centre of the current snapshot
        # print(barcodes_history[barcodeText])
        barcodes_history[barcodeText]["locations"].insert(0, centre)
    # limit the size of the dict to 5
        barcodes_history[barcodeText]["locations"] = barcodes_history[barcodeText]["locations"][:5]




    for barcode in list (barcodes_history.keys()):
        # checks to see if this is an outdated location
        if not barcodes_history[barcode]["info"]["updated"]:
            print("looks like", barcode, "could not be found")
            barcodes_history[barcode]["info"]["failures"] += 1

        barcodes_history[barcode]["info"]["updated"] = False

        if barcodes_history[barcode]["info"]["failures"] > 5:
            print("looks like", barcode,
                  "has been missing a while, clearing its oldest location")
            barcodes_history[barcode]["locations"] = barcodes_history[barcode]["locations"][:-1]
            barcodes_history[barcode]["info"]["failures"] = 0

        if not barcodes_history[barcode]["locations"]:
            print(barcode, "has no locations, removing")
            del barcodes_history[barcode]
            continue

        # get the average of the centres, put it into the accessible locations
        barcodes_locations[barcode] = tuple(
            [int(sum(ele) / len(barcodes_history[barcode]["locations"])) for ele in zip(*barcodes_history[barcode]["locations"])])
        if not barcodes_locations[barcode]:
            print(barcode, "has no location. FIXME")
            continue
        # highlight that location in the GUI
        cv2.circle(original, barcodes_locations[barcode], 30, (0, 0, 255), 2)

# draw boundry
    if "top" in barcodes_locations and "bottom" in barcodes_locations:

        cv2.rectangle(
            original, barcodes_locations["top"], barcodes_locations["bottom"], (0, 0, 255), 10)
    # for testing
    cv2.imshow('original ', original)
    cv2.waitKey(33)
    # if k==27:    # Esc key to stop
    #     break
    # cv2.waitKey(5)
    # cv2.destroyAllWindows()
    print("posting to endpoint")
    r = requests.post('http://127.0.0.1:5000/api/update.json',
                      json=barcodes_locations)

    print("done, sleeping")
    time.sleep(0.5)
