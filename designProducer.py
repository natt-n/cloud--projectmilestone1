from google.cloud import pubsub_v1      # pip install google-cloud-pubsub  ##to install
import glob                             # for searching for json file 
import json
import os 
import csv

# Search the current directory for the JSON file (including the service account key) 
# to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
files=glob.glob("*.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=files[0];

# Set the project_id with your project ID
project_id="";
topic_name = "designTopic";   # change it for your topic name if needed

# create a publisher and get the topic path for the publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
print(f"Published messages with ordering keys to {topic_path}.")

#read Labels.csv
keysSaved = False
rowDict = {}
keys = []

with open('Labels.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:

        #save the keys
        if(not keysSaved):
            keys = row
            keysSaved = True
            continue

        #save row into a dictionary
        i = 0
        message = ''
        for key in keys:
            rowDict[key] = row[i]
            i += 1
            message += (key + ":" + rowDict[key] + " ")

        #serialize dictionary
        message = str(message).encode('utf-8')

        # send the value
        print("Producing a record: {}".format(message))    
        future = publisher.publish(topic_path, message)
    
        #ensure that the publishing has been completed successfully
        future.result()
        
