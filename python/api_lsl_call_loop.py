'''
This script demonstrates how to receive an LSL stream and call the Petal API in
an endless loop. It currently gets bandpower and artifacts and logs to console.

Usage: python api_lsl_call_loop.py -n PetalStream_eeg -k $API_KEY
'''
import argparse
import pprint
import time

import pylsl

import api


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--stream_name', type=str, required=True,
                    help='the name of the LSL stream')
parser.add_argument('-k', '--api_key', type=str, required=True,
                    help='API key for the Petal Metrics API')
args = parser.parse_args()

# get the LSL inlet
print(f'looking for a stream with name {args.stream_name}...')
streams = pylsl.resolve_stream('name', args.stream_name)
if len(streams) == 0:
    raise RuntimeError(f'Found no LSL streams with name {args.stream_name}')
inlet = pylsl.StreamInlet(streams[0])

# make API calls in a loop
while True:
    # construct the call based on the received sample chunk
    # lsl chunks group 4-channel samples in a 2D array as follows:
    #   samples: [[ch1, ch2, ch3, ch4], [ch1, ch2, ch3, ch4], ...]
    # the timestamp array corresponds to each received 4-channel grouping:
    #   timestamps: [ts1, ts2, ...]
    chunk, timestamps = inlet.pull_chunk(timeout=5.0, max_samples=256)
    eeg_data = [
        [samples[channel] for samples in chunk] for channel in range(4)
    ]
    calculations = api.request_metrics(
        api_key=args.api_key,
        eeg_data=eeg_data,
        metrics=['eye', 'blink', 'bandpower', 'artifact_detect'],
    )
    pprint.pprint(calculations)
