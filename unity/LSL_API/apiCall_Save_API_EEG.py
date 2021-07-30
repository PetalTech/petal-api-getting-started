#6/27/21 JG
from typing import Any, Dict, List
import requests
import argparse
import pprint
import time
import math
import numpy as np
from datetime import datetime
from apiHelper import request_metrics
from pylsl import StreamInlet, StreamOutlet, resolve_stream, local_clock, StreamInfo


metricsCall = ['bandpower', 'eye', 'blink', 'artifact_detect']





# static muse variables
windowLength = 256
chunkLength = 192
samplingRate = 256
numSensors = 4
dataBuffer = np.zeros([numSensors, windowLength])
timeStampBuffer = np.zeros(windowLength)
metaDataString = "metricsCall:" + str(metricsCall) + "_windowLength:" + str(windowLength) + "_chunkLength:" + str(chunkLength)

# api parser
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--api_key', type=str, required=True,
                    help='API key for the Petal Metrics API')
args = parser.parse_args()

print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

#Populate Header with metadata
fileNameAPI = datetime.now().strftime('%Y-%m-%d%H%M%S') + "_apiOutput.txt"
f=open(fileNameAPI,"a")
f.write(datetime.now().strftime('%Y-%m-%d%H%M%S') + "_apiOutput_metaData:" + str(metaDataString) + ".txt")
f.write(", ")
f.write('\n')
f.close()

#Populate Header with metadata
fileNameEEG = datetime.now().strftime('%Y-%m-%d%H%M%S') + "_eegData.txt"
f=open(fileNameEEG,"a")
f.write(datetime.now().strftime('%Y-%m-%d%H%M%S') + "_eegData.txt")
f.write(", ")
f.write('\n')
f.close()

while True:
    sample, timestamp = inlet.pull_chunk(timeout=2, max_samples = chunkLength)
    sample = np.asarray(sample).T
    for channel in range(0, numSensors):
        dataBuffer[channel] = np.roll(dataBuffer[channel], -chunkLength)
        for newSample in range(0, chunkLength):
            dataBuffer[channel][len(dataBuffer[channel])-chunkLength+newSample] = sample[channel][newSample]
    finalDataAPI = np.asarray(dataBuffer).tolist()
    timestampWindow = [timestamp[len(timestamp)-1], timestamp[0]]

    timeStampBuffer = np.roll(timeStampBuffer, -chunkLength)
    for newTime in range(0, chunkLength):
        timeStampBuffer[len(timeStampBuffer)-chunkLength+newTime] = timestamp[newTime]
    
    #call api
    apiOutput = request_metrics(
            api_key=args.api_key,
            eeg_data=finalDataAPI,
            metrics=metricsCall,
    )
    
    pprint.pprint(apiOutput)

    f=open(fileNameAPI,"a")
    f.write(str(timestampWindow))
    f.write(", ")
    f.write(str(apiOutput))
    f.write(", ")
    f.write('\n')
    f.close()
    
    f=open(fileNameEEG,"a")
    for writeSample in range(0, chunkLength):
        f.write(str(timeStampBuffer[writeSample]) + ", ")
        for channel in range(0, numSensors):
            f.write(str(dataBuffer[channel][writeSample]) + ", ")
        f.write('\n')
    f.close()

f.close()


