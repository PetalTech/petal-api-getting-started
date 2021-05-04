/**
 * This script receives a Petal formatted LSL stream and prints it to the console.
 * 
 * Usage: node lsl_receive.js -n PetalStream_eeg
 * valid LSL stream names for use with petal streaming apps:
 *     * PetalStream_gyroscope
 *     * PetalStream_ppg
 *     * PetalStream_telemetry
 *     * PetalStream_eeg
 *     * PetalStream_acceleration
 *     * PetalStream_connection_status
 */
const lsl = require('node-lsl');
const { Command } = require('commander');

// read and validate command line args
const program = new Command();
program
  .requiredOption('-n, --eeg-stream-name <name>', 'name of LSL stream to get')
program.parse(process.argv);
const { eegStreamName } = program;

// init the LSL inlet
const streams = lsl.resolve_byprop('name', eegStreamName);
if (streams.length === 0) {
  throw new Error(`Unable to find a LSL stream with name ${eegStreamName}`);
}
streamInlet = new lsl.StreamInlet(streams[0]);
streamInlet.on('closed', () => console.log('LSL inlet closed'));

// receive data forever
while (true) {
  const chunk = streamInlet.pullChunk(5.0, 1);
  const samples = chunk.samples;
  const timestamp = chunk.timestamps[0];
  if (timestamp === 0) {
    console.log('found no samples');
  }
  console.log(timestamp, samples);
}
