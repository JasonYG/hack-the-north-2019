import config as keys

from picamera import PiCamera
from time import sleep
import requests

import boto3
from facebook import Facebook

camera = PiCamera()
camera.start_preview()

COLLECTION = "htn2019collection"

rekognition = boto3.client(
    "rekognition",
    "us-east-1",
    aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
)

# Rekognition functions
def index_faces(bytes, collection_id, image_id=None, attributes=()):
	response = rekognition.index_faces(
		Image={
			"Bytes": bytes
		},
		CollectionId=collection_id,
		ExternalImageId=image_id,
	    DetectionAttributes=attributes,
	)
	return response['FaceRecords']

def search_faces_by_image(bytes, collection_id, threshold=80):
	response = rekognition.search_faces_by_image(
		Image={
			"Bytes": bytes
		},
		CollectionId=collection_id,
		FaceMatchThreshold=threshold,
	)
	return response['FaceMatches']

# Taking pictures
print("capturing...")
camera.capture('/home/pi/Desktop/image.jpg')
print("retrieving file...")
files = {'file': open('/home/pi/Desktop/image.jpg', 'rb')}
print("searching in collection...")

for record in search_faces_by_image(files, COLLECTION):
	face = record['Face']
	print "Matched Face ({}%)".format(record['Similarity'])
	print "  FaceId : {}".format(face['FaceId'])
	print "  ImageId : {}".format(face['ExternalImageId'])
#r = requests.post('https://2adc0fc4.ngrok.io/upload/1', files=files)
#r.text
sleep(1)


camera.stop_preview()
