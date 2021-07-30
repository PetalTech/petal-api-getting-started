#6/27/21 JG
"""Example program to show how to read a multi-channel time series from LSL."""
from pylsl import StreamInlet, resolve_stream
from datetime import datetime

print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
fileNameEEG = datetime.now().strftime('%Y-%m-%d%H%M%S') + "_eegData.txt"

#Populate Header with metadata
f=open(fileNameEEG,"a")
f.write(datetime.now().strftime('%Y-%m-%d%H%M%S') + "_eegData.txt")
f.write(", ")
f.write('\n')
f.close()

print('now collecting data...')

while True:
    sample, timestamp = inlet.pull_sample()
    print(timestamp, sample)
    f=open(fileNameEEG,"a")
    f.write(str(timestamp))
    f.write(", ")
    f.write(str(sample))
    f.write(", ")
    f.write('\n')
    f.close()

f.close()
