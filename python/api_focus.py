'''
Script for api calls and average alpha calculation ("focus").
Uses random data, no device connection required.
To use with real data, see api_lsl_call_loop.py to use LSL and loop api calls
To call, use python api_focus.py -k <api-key>
'''

import argparse
import math
import random
from typing import Any, Dict, List

import numpy as np
import requests

import api


parser = argparse.ArgumentParser()
parser.add_argument('-k', '--api_key', type=str, required=True,
                    help='API key for the Petal Metrics API')
args = parser.parse_args()

random_eeg_data = [
    [random.randint(0,100) / 100 for i in range(150)]
    for num in range(4)
]

calculations = api.request_metrics(
    api_key=args.api_key,
    eeg_data=random_eeg_data,
    metrics=['preprocessed_data', 'artifact_count', 'bandpower'],
)

# parse api result and get bandpower
bandpower = calculations["bandpower"]
alphaAverage = 0
for channel in bandpower:
    print(f'channel {channel} alpha: {bandpower[channel]["alpha"]}')
    alphaAverage += bandpower[channel]['alpha']

# calculate average alpha and print
alphaAverage = alphaAverage/4
print(f'alpha average: {alphaAverage}')
