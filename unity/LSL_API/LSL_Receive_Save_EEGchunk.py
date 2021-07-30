    #6/27/21 JG
"""Example program to show how to read a multi-channel time series from LSL."""
from pylsl import StreamInlet, resolve_stream
from datetime import datetime
import numpy as np

print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
fileNameEEG = datetime.now().strftime('%Y-%m-%d%H%M%S') + "_eegData.txt"

chunkLength = 256

#Populate Header with metadata
f=open(fileNameEEG,"a")
f.write(datetime.now().strftime('%Y-%m-%d%H%M%S') + "_eegData_chunkLength:" + str(chunkLength) + ".txt")
f.write(", ")
f.write('\n')
f.close()

print('now collecting data...')

while True:
    sample, timestamp = inlet.pull_chunk(timeout=2, max_samples = chunkLength)
    sample = np.asarray(sample).T

    f=open(fileNameEEG,"a")
    for writeSample in range(0, chunkLength):
        f.write(str(timestamp[writeSample]) + ", ")
        for channel in range(0, len(sample)):
            f.write(str(sample[channel][writeSample]) + ", ")
        f.write('\n')
    f.close()

f.close()
