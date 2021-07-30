import pyautogui
import numpy as np
import requests
import argparse
import pprint
import time
from apiHelper import request_metrics
from pylsl import StreamInlet, StreamOutlet, resolve_stream, local_clock

metricsCall = ['bandpower', 'eye', 'blink', 'artifact_detect']

# static muse variables
windowLength = 256
chunkLength = 192
samplingRate = 256
numSensors = 4
dataBuffer = np.zeros([numSensors, windowLength])

# api parser
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--api_key', type=str, required=True,
                    help='API key for the Petal Metrics API')
args = parser.parse_args()

print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

while True:
    sample, timestamp = inlet.pull_chunk(timeout=2, max_samples = chunkLength)
    sample = np.asarray(sample).T
    for channel in range(0, numSensors):
        dataBuffer[channel] = np.roll(dataBuffer[channel], -chunkLength)
        for newSample in range(0, chunkLength):
            dataBuffer[channel][len(dataBuffer[channel])-chunkLength+newSample] = sample[channel][newSample]
    finalDataAPI = np.asarray(dataBuffer).tolist()
    
    #call api
    apiOutput = request_metrics(
            api_key=args.api_key,
            eeg_data=finalDataAPI,
            metrics=metricsCall,
    )
    
    pprint.pprint(apiOutput)

    #Clicking code! See "README" to edit
    if 'True' in str(apiOutput['blink']):
        pyautogui.click(button='left') #mouse left click
    if 'True' in str(apiOutput['eye']):
        pyautogui.click(button='right') #mouse right click









