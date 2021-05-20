print("start")

#
# import zxing
# reader = zxing.BarCodeReader()
# barcode = reader.decode("test_images/IMG_1321.JPG")
# print(barcode)
# # BarCode(raw='This should be QR_CODE', parsed='This should be QR_CODE', format='QR_CODE', type='TEXT', points=[(15.0, 87.0), (15.0, 15.0), (87.0, 15.0), (75.0, 75.0)])
#


# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ret3,image = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# find the barcodes in the image and decode each of the barcodes
barcodes = pyzbar.decode(image)
print(barcodes)



# loop over the detected barcodes
for barcode in barcodes:
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
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)



print("end")
