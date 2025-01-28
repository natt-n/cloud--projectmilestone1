from google.cloud import pubsub_v1      # pip install google-cloud-pubsub  ##to install
import glob                             # for searching for json file 
import json
import os 
import random
import numpy as np                      # pip install numpy    ##to install
import time
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

#read csv
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
        for key in keys:
            rowDict[str(key)] = str(row[i])
            i += 1
            print(key + ":" + rowDict[key])
        
        message = json.dumps(rowDict).encode('utf-8') # serialize the message
    
        try:    
        
            future = publisher.publish(topic_path, message);
        
            #ensure that the publishing has been completed successfully
            future.result()    
            print("The messages {} has been published successfully".format(rowDict))
        except: 
            print("Failed to publish the message")
    
    time.sleep(.5)   # wait for 0.5 second
        
      