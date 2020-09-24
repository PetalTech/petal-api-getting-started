'''
This script receives a 4 channel LSL EEG stream and prints it to console

Usage: python lsl_receive.py -n SimulatedEEGStream
'''
import argparse

import pylsl


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--stream_name', type=str, required=True,
                    help='the name of the LSL stream')
args = parser.parse_args()

# first resolve an EEG stream
print(f'looking for a stream with name {args.stream_name}...')
streams = pylsl.resolve_stream('name', args.stream_name)

# create a new inlet to read from the stream
if len(streams) == 0:
    raise RuntimeError(f'Found no LSL streams with name {args.stream_name}')
inlet = pylsl.StreamInlet(streams[0])

while True:
    sample, timestamp = inlet.pull_sample()
    print(timestamp, sample)
