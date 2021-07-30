#6/27/21 JG
from typing import Any, Dict, List
import requests
import argparse
import pprint
import time
import math
import numpy as np
from apiHelper import request_metrics
from pylsl import StreamInlet, StreamOutlet, resolve_stream, local_clock, StreamInfo

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

info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'myuidw43536')
outlet = StreamOutlet(info)

print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

artifactList = ['0', '0', '0', '0']
bandpowerList = ['0', '0', '0', '0']

print("now sending markers...")

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
    
##    pprint.pprint(apiOutput)

    if apiOutput['bandpower']['channel1']['0'] != apiOutput['bandpower']['channel2']['0']:
        bandpowerList = [str(apiOutput['bandpower']['channel1']['2']), str(apiOutput['bandpower']['channel2']['2']), str(apiOutput['bandpower']['channel3']['2']), str(apiOutput['bandpower']['channel4']['2'])]
        artifactList = [str(apiOutput['artifact_detect']['channel1']), str(apiOutput['artifact_detect']['channel1']), str(apiOutput['artifact_detect']['channel2']), str(apiOutput['artifact_detect']['channel3'])]
        if 'eye' in apiOutput['artifact_detect']['channel1'] or 'eye' in apiOutput['artifact_detect']['channel2'] or 'eye' in apiOutput['artifact_detect']['channel3'] or 'eye' in apiOutput['artifact_detect']['channel4']:
            heogCount = 5
        else:
            heogCount = 0
    else:
        artifactList = ['5', '5', '5', '5']
        bandpowerList = ['0', '0', '0', '0']
        heogCount = 0

    for artifact in range(0, len(artifactList)):
        if artifactList[artifact] == 'good':
            artifactList[artifact] = '0'
        else:
            artifactList[artifact] = '5'

    if 'True' in str(apiOutput['blink']):
        artifactList = ['5', '0', '0', '5']

    bandpowerStringPlusArtifact = str(bandpowerList[0])+', '+str(bandpowerList[1])+', '+str(bandpowerList[2])+', '+str(bandpowerList[3])+', '+str(artifactList[0])+', '+str(artifactList[1])+', '+str(artifactList[2])+', '+str(artifactList[3]) + ', '+str(heogCount)

    outletSample = str(bandpowerStringPlusArtifact)
    #NOTE: This has the bandpower values for channels 1-4 in the first 4 positions, then artifact counts for channels 1-4 in the next 5-8 positions, then HEOG total artifacts in position 9
    outlet.push_sample([outletSample])




    
