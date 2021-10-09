'''
This file provides a function to make Petal Metrics API calls.
'''
import json
from typing import Any, Dict, List
import random

import requests


API_HOST = 'https://app.petal.dev'


def request_metrics(
    api_key: str,
    eeg_data: List[List[float]],
    metrics: List[str]
) -> Dict[str, Any]:
    '''
    Request nicely formatted metrics from the Petal Metrics API.

    Args:
        api_key: Petal Metrics dev API key
        eeg_data: 2D list of 4-channel EEG data
        metrics: list of desired metrics results, options:
            'bandpower', 'preprocessed_data'

    Returns:
        dict containing all requested properties based on metrics param
         - metrics param: resulting property:
           - bandpower: bandpower and bandRanges
           - preprocessed_data: data
    '''
    args = {
      'band_ranges': {
        'alpha': [8, 13],
        'beta': [13, 30],	
        'delta': [1, 3],
        'theta': [3, 8]
      },
      'metrics': metrics,
      'preprocess_steps': [],
    }
    data = {'data': eeg_data, 'options' : args}
    headers = { 'Authorization': f'Bearer {api_key}' }
    base_url = f'{API_HOST}/api/v1'
    call_url = f'{base_url}/app/metrics'
    resp = requests.post(call_url, json=data, headers=headers)
    print(f'status: {resp.status_code}')
    try:
        resp_json = resp.json()
    except json.decoder.JSONDecodeError:
        print(resp.text)
        raise RuntimeError('failed to parse response')
    if 'error' in resp_json:
        raise RuntimeError(resp_json['error'])
    elif 'calculations' not in resp_json:
        raise ValueError(f'could not find calculations in {resp_json}')
    return resp_json['calculations']
