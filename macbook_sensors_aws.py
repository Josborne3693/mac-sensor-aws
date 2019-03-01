#!/usr/bin/env python
# coding: utf-8

# In[14]:


import subprocess
import time
import json
import csv
import os

try:
    import boto3
except:
    print("AWS Python SDK 'boto3' not installed")


# In[ ]:





# In[32]:


def getTime(verbose=True):
    currentTime = time.time()
    if verbose == True: 
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(currentTime)))
    return currentTime


# In[5]:


def getCPUtemp():
    cpuTemp = 0.0
    
    cpuBashCommand = "istats cpu --value-only"
    process = subprocess.Popen(cpuBashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if error == None:
        cpuTemp = float(output.decode('UTF-8').strip())
    else:
        print("Error getting cpu temperature")
        
    return cpuTemp


# In[6]:


def getFanSpeeds():
    fanSpeedsData = []
    fanSpeeds = []
    
    cpuBashCommand = "istats fan --value-only"
    process = subprocess.Popen(cpuBashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if error == None:
        fanSpeedsData = output.decode('UTF-8').strip().split('\n')
        for i, value in enumerate(fanSpeedsData):
            fanSpeedsData[i] = value.strip()
        numFans = int(fanSpeedsData[0])
        for i in range(numFans):
            fanSpeeds.append(int(fanSpeedsData[i+1]))
        
        # print("Num fans: " + str(numFans))
    else:
        print("Error getting fan 1 speed")
        
    return fanSpeeds


# In[31]:


def gatherData():
    """Gathers time, cpuTemp, and fanSpeed data"""
    data = {
        "timestamp": 0,
        "cpuTemp": 0,
        "fan1speed": 0,
        "fan2speed": 0
    }
    
    currentTime = getTime(verbose=True)
    cpuTemp = getCPUtemp()
    fanSpeeds = getFanSpeeds()
    
    data['timestamp'] = currentTime
    data['cpuTemp'] = cpuTemp
    data['fan1speed'] = fanSpeeds[0]
    data['fan2speed'] = fanSpeeds[1]
    
    return data


# In[8]:


def sendData(client, data):
    message = {
        'messageId': "j_macbook",
        'payload': str.encode(json.dumps(data))
    }
    response = client.batch_put_message(
        channelName="macbook_sensors_channel",
        messages=[message]
    )
    print(response)


# In[25]:


def writeDictToCSV(csv_file, dict_data):
    csv_columns = list(dict_data.keys())
    
    # if file exists and is not empty, append, else write
    if os.path.isfile(csv_file): # file exists
        if os.stat(csv_file).st_size > 0: # file is not empty
            writeMethod = 'a'
        else:
            writeMethod = 'w'
    else:
        writeMethod = 'w'
        
    try:
        with open(csv_file, writeMethod) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            if writeMethod == 'w':
                writer.writeheader()
            writer.writerow(dict_data)
    except IOError:
        print("I/O error") 


# In[45]:


def collectData(
    seconds,
    frequency,
    sendToIoTAnalytics=False,
    saveToCSV=False,
    csv_file=None,
    verbose=False
):
    
    client = boto3.client('iotanalytics')
    
    sleepTime = 1.0/frequency
    iterations = int(seconds/sleepTime)
    
    starttime=time.time()
    
    for i in range(iterations):
        data = gatherData()
        
        if sendToIoTAnalytics == True:
            sendData(client=client, data=data)
        
        if saveToCSV == True:
            if csv_file == None:
                csv_file = "data_log_" + time.strftime('%Y-%m-%d--%H-%M-%S', time.localtime(time.time())) + ".csv"
 
            writeDictToCSV(
                csv_file=csv_file,
                dict_data=data
            )
        
        if verbose == True:
            print(json.dumps(data, indent=2))
            
        time.sleep(sleepTime - ((time.time() - starttime) % sleepTime))


# In[56]:


#csv_file = "data_log_2019-02-28--11-31-40.csv"
csv_file = None

collectData(
    seconds=60,
    frequency=2,
    sendToIoTAnalytics=False,
    saveToCSV=True,
    csv_file=csv_file,
    verbose=True
)

