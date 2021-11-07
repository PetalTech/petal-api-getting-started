'''
Call the API with only a key and no muse connection.

Usage: python api_standalone.py -k $API_KEY
'''
import argparse
import pprint
import time

import pylsl

import api

WINDOW_SIZE = 256
N_CHANNELS = 4

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--api_key', type=str, required=True,
                    help='API key for the Petal Metrics API')
args = parser.parse_args()

eeg_data = [[1] * WINDOW_SIZE for channel in range(N_CHANNELS)]
calculations = api.request_metrics(
    api_key=args.api_key,
    eeg_data=eeg_data,
    metrics=['eye', 'blink', 'bandpower', 'artifact_detect'],
)
pprint.pprint(calculations)
