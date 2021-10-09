/**
 * This script demonstrates how to receive an LSL stream and call the Petal API
 * in an endless loop. It currently gets bandpower and artifacts and logs to
 * console.
 *
 * Usage: node api_lsl_call_loop.js -n PetalStream_eeg -k $API_KEY
 */
const lsl = require('node-lsl');
const { Command } = require('commander');
const { requestMetrics } = require('./api');

const main = async (eegStreamName, apiKey) => {
  const streams = lsl.resolve_byprop('name', eegStreamName);
  if (streams.length === 0) {
    throw new Error(`Unable to find a LSL stream with name ${eegStreamName}`);
  }
  streamInlet = new lsl.StreamInlet(streams[0]);
  streamInlet.on('closed', () => console.log('LSL inlet closed'));

  while (true) {
    const chunk = streamInlet.pullChunk(5.0, 256);
    const samples = chunk.samples;
    // construct the call based on the received sample chunk
    // lsl chunks group 4-channel samples in a 1D array as follows:
    //   samples: [ch1, ch2, ch3, ch4, ch1, ch2, ch3, ch4, ...]
    // the timestamp array corresponds to each received 4-channel grouping:
    //   timestamps: [ts1, ts2, ...]
    let EEGArray = Array(4);
    for (let i = 0; i < 4; i++) {
      EEGArray[i] = new Array(256);
      for (let j = 0; j < samples.length / 4; j++) {
        EEGArray[i][j] = samples[j * 4 + i];
      }
    }
    const calculations = await requestMetrics(
      apiKey, EEGArray, ['eye', 'blink', 'bandpower', 'artifact_detect']
    );
    console.log(calculations);
  }
}

// read and validate command line args
const program = new Command();
program
  .requiredOption('-n, --eeg-stream-name <name>', 'name of LSL stream to get')
  .requiredOption('-k, --api-key <key>', 'Petal Metrics API key');
program.parse(process.argv);
const { eegStreamName, apiKey } = program;
main(eegStreamName, apiKey)
  .catch(error => {
    console.error(error);
    process.exit(1);
});
