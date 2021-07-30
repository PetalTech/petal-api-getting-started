#6/27/21 JG
from typing import Any, Dict, List
import random
import requests

METRICS_URL = 'https://metrics-7vjbw6wmkq-uc.a.run.app/metrics'

def request_metrics(
    api_key: str,
    eeg_data: List[List[float]],
    metrics: List[str]
) -> Dict[str, Any]:

    arg_dict = {
        'metrics': metrics,
        'preprocess_steps' : [],
    }

    data = {'data': eeg_data, 'options' : arg_dict}
##    headers = { 'X-API-KEY': api_key }
    headers = {'Auth-Key': "WmPFfy1pAtkX6t_KuSCxOV9xH4TEmp25RK9mWFANkZQ"}
    resp_json = requests.post(METRICS_URL, json=data, headers=headers).json()
    if 'error' in resp_json:
        raise RuntimeError(resp_json['error'])
    processed_metrics = {}
    calculations = resp_json['calculations']
    if 'artifact_detect' in metrics:
        processed_metrics['artifact_detect'] = calculations['artifact_detect']
    if 'blink' in metrics:
        processed_metrics['blink'] = calculations['blink']
    if 'eye' in metrics:
        processed_metrics['eye'] = calculations['eye']
    if 'bandpower' in metrics:
        processed_metrics['bandpower'] = calculations['bandpower']
##        processed_metrics['band_ranges'] = resp_json['options']['band_ranges']
    return processed_metrics


