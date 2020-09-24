# Overview

Scripts written in Python3 for EEG and Petal API testing.

## Recommended Installation

For python, we use 3.8.5, but any later 3+ version will probably work.

Create a virtualenv:

```
pip install venv
python3 -m venv eeg_venv
# activate the venv according to your OS
# Windows example:
. ./eeg_venv/scripts/Activate
pip install -r requirements.txt
```

Run a script. Examples:

```
python api_lsl_call_loop.py -n SimulatedEEGStream -k $API_KEY
python api_bandpower.py -k $API_KEY
python lsl_stream.py
python lsl_receive.py -n SimulatedEEGStream
```

## File & Script Overviews

## API Overview

There is a single endpoint used to access the metrics API. The `api.py` file contains a function that will streamline this call, and all other api scripts make use of this function to log the output of that request to the console.

### api.py

This file provides a function to make Petal Metrics API calls.

### api_all_metrics.py

This script contains an example of a Petal Metrics API call for all metrics at once. You will need a valid developer API key to access.

Usage: python api_all_metrics.py -k $API_KEY

### api_artifacts.py

This script contains an example of checking channels for artifacts in a Petal Metrics API call. You will need a valid developer API key to access.

Usage: python api_artifacts.py -k $API_KEY

### api_bandpower.py

This script contains an example of a bandpower Petal Metrics API call. You will need a valid developer API key to access.

Usage: `python api_bandpower.py -k $API_KEY`

### api_preprocess.py

This script contains an example of a preprocessed data Petal Metrics API call. You will need a valid developer API key to access.

Usage: `python api_preprocess.py -k $API_KEY`

### api_lsl_call_loop.py

This script demonstrates how to receive an LSL stream and call the Petal API in an endless loop. It currently gets bandpower and artifacts and logs to console.

Usage: `python api_lsl_call_loop.py -n SimulatedEEGStream -k $API_KEY`

## LSL Script Overviews

LSL, or lab streaming layer is a research focused EEG and marker streaming system that provides high resolution timestamps in addition to high frequency EEG streaming. It's not necessary to use this to stream or ingest data in order to access the API, but it can be used to stream device EEG data or simulate input/output from a device.

### lsl_receive.py

This script receives a 4 channel LSL EEG stream and prints it to console

Usage: `python lsl_receive.py -n SimulatedEEGStream`

### lsl_stream.py

This script streams 4 channels of EEG data at a selected sample rate. It can
stream randomly generated data, or from a CSV file with any header where the
first 4 columns represent channels 1-4.

Usage:
  * random EEG data at 256Hz: `python lsl_stream.py -s 256`
  * from a CSV file at 256Hz: `python lsl_stream.py -s 256 -f ../example_data.csv`
