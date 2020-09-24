# Overview

Scripts written in Node.js for EEG and Petal API testing.

## Recommended Installation

We use Node.js 10.15.3, but any later version will probably also work.

Install the dependencies:

```
npm install
```

Run a script. Examples:

```
node api_lsl_call_loop.js -n SimulatedEEGStream -k $API_KEY
node api_preprocess.js -k $API_KEY
node lsl_receive.js -n SimulatedEEGStream
node lsl_stream.js -s 256
```

## API Overview

There is a single endpoint used to access the metrics API. The `api.js` file contains a function that will streamline this call, and all other api scripts make use of this function to log the output of that request to the console.

### api.js

This file provides a function to make Petal Metrics API calls.

### api_all_metrics.js

This script contains an example of a Petal Metrics API call for all metrics at once. You will need a valid developer API key to access.

Usage: node api_all_metrics.js -k $API_KEY

### api_artifacts.js

This script contains an example of checking channels for artifacts in a Petal Metrics API call. You will need a valid developer API key to access.

Usage: node api_artifacts.js -k $API_KEY

### api_bandpower.js

This script contains an example of a bandpower Petal Metrics API call. You will need a valid developer API key to access.

Usage: `node api_bandpower.js -k $API_KEY`

### api_preprocess.js

This script contains an example of a preprocessed EEG data Petal Metrics API call. You will need a valid developer API key to access.

Usage: `node api_preprocess.js -k $API_KEY`

### api_lsl_call_loop.js

This script demonstrates how to receive an LSL stream and call the Petal API in an endless loop. It currently gets bandpower and artifacts and logs to console.

Usage: `node api_lsl_call_loop.js -n SimulatedEEGStream -k $API_KEY`

## LSL Script Overviews

LSL, or lab streaming layer is a research focused EEG and marker streaming system that provides high resolution timestamps in addition to high frequency EEG streaming. It's not necessary to use this to stream or ingest data in order to access the API, but it can be used to stream device EEG data or simulate input/output from a device.

### lsl_receive.js

This script receives a 4 channel LSL EEG stream and prints it to console

Usage: `node lsl_receive.js -n SimulatedEEGStream`

### lsl_stream.js

This script streams 4 channels of EEG data at a selected sample rate. It can
stream randomly generated data, or from a CSV file with any header where the
first 4 columns represent channels 1-4.

Usage:
  * random EEG data at 256Hz: `node lsl_stream.js -s 256`
  * from a CSV file at 256Hz: `node lsl_stream.js -s 256 -f ../example_data.csv`
