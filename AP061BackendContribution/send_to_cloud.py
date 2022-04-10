from unicodedata import name
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json
import cv2
import base64

connect_str = "DefaultEndpointsProtocol=https;AccountName=ifpgastorshafan;AccountKey=fYIE/xL//fN9CRUByd24GrdWlGGJJFcPClVmTK1QNkQUTLvgbN/fAU7T3CzpuFAye40Q2P5QMibJPCteW3K6QA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def sendData(speed,direction,DF,DB,DL,DR,path):

	container = "readingdata"

	containerClient = blob_service_client.get_container_client(container=container)

	f = open('sensor_data.json', 'r+')
	j = json.load(f)
	f.close()

	j['speed'] = speed
	j['direction'] = direction
	j['distance']['Front'] = DF
	j['distance']['Back'] = DB
	j['distance']['Left'] = DL
	j['distance']['Right'] = DR
	j['image'] = convertImg(path)

	f = open('sensor_data.json','w+')
	f.write(j)
	f.close()


	try:
		with open('sensor_data.json', 'rb') as json:
			containerClient.upload_blob(data=json, name='sensors.json',overwrite=True)
		print("Success")

	except Exception as e:
		print(e)
		print("Ignoring duplicate filenames")


def convertImg(path):
	img = cv2.imread(path)

	_,en = cv2.imencode(".jpeg",img)

	encoded = base64.b64encode(en)
	encoded = encoded.decode('utf-8')

	data = "data:image/jpeg;base64,"

	finalData = data+encoded
	
	return finalData
	
def checkSafeReturn():
	container = "readingdata"
	containerClient = blob_service_client.get_container_client(container=container)
	try:
		blob = containerClient.get_blob_client(blob="a.txt")
		stream = blob.download_blob()
		data = stream.readall()
		return data.decode('utf-8')
	except ResourceNotFoundError:
		print("No blob found.")
		return
	
