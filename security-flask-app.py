import boto3, json
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template

AWS_KEY="xxxxx"
AWS_SECRET="xxxxx"
REGION="xxxxx"
BUCKET = "bucket-name"
human_PREFIX = "human-folder-name/"
false_PREFIX = "false-positive-folder-name/"

#Connect to s3 bucket
s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET)
                           
# list_objects_v2 will return a max of 1000 items
# get list of all pictures in human folder (if under 1000)
human_response = s3.list_objects_v2(
	Bucket = BUCKET,
	Prefix = human_PREFIX #folder path
	)

# get list of all pictures in false positive folder (if under 1000)
false_response = s3.list_objects_v2(
	Bucket = BUCKET,
	Prefix = false_PREFIX #folder path
	)

#start at -1 because folder name is automatically included in count
human_count = human_response['KeyCount'] - 1	
false_count = false_response['KeyCount'] - 1

# If there are 999 or more pictures in a folder, use "list_objects_v2" until all pics have been accounted for
# in the human folder

if(human_response['KeyCount'] == 1000):
	try:
		#"StartAfter" key only exists if there are more than 1000 items 
		start_after = human_response['StartAfter']
		more = True
		while(more == True):
			add_response = s3.list_objects_v2(
				Bucket = BUCKET,
				Prefix = human_PREFIX,
				StartAfter = start_after
			)
			human_count += add_response['KeyCount']
			try:
				start_after = add_response['StartAfter']
			except:
				more = False
				pass
	except:
		#There are exactly 999 pics in folder 
		pass

# If there are 999 or more pictures in a folder, use "list_objects_v2" until all pics have been accounted for
# in the animal folder
if(false_response['KeyCount'] == 1000):
	try:
		start_after = false_response['StartAfter']
		more = True
		while(more == True):
			add_response = s3.list_objects_v2(
				Bucket = BUCKET,
				Prefix = false_PREFIX,
				StartAfter = start_after
			)
			false_count += add_response['KeyCount']
			try:
				start_after = add_response['StartAfter']
			except:
				more = False
				pass
	except:
		#There are exactly 999 pics in folder 
		pass

# # print out each count
# print human_count
# print false_count
                           

app = Flask(__name__)
 
@app.route("/")
def chart():
    
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]

    labels2 = ["January","February","March","April","May","June","July","August"]
    values2 = [10,9,8,7,6,4,7,8]

    labels3 = ["People Spotted","False Alarm"]
    values3 = [human_count,false_count]

    labels4 = ["January","February","March","April","May","June","July","August"]
    values4 = [10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=labels,values2=values2, labels2=labels2,
    	values3=values3, labels3=labels3, values4=values4, labels4=labels4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)