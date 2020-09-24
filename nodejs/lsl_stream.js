/**
 * This script streams 4 channels of EEG data at a selected sample rate. It can
 * stream randomly generated data, or from a CSV file with any header where the
 * first 4 columns represent channels 1-4.
 *
 * Usage:
 *   random EEG data at 256Hz: node lsl_stream.js -s 256
 *   from a CSV file at 256Hz: node lsl_stream.js -s 256 -f ../example_data.csv
 */
const fs = require('fs');
const csv = require('csvtojson')
const lsl = require('node-lsl');
const { Command } = require('commander');

/**
 * Async/promise based function for sleeping without blocking the main thread
 * @param {number} milliseconds - n milliseconds to async sleep for
 */
const sleep = (milliseconds) => new Promise(
  resolve => setTimeout(resolve, milliseconds)
);

const main = async (sampleRate, eegCsvFilePath) => {
  // construct the EEG LSL output stream
  const info = lsl.create_streaminfo(
    'SimulatedEEGStream',
    'EEG',
    4,
    sampleRate,
    lsl.channel_format_t.cft_float32,
    'muse'
  );
  const desc = lsl.get_desc(info);
  const channels = lsl.append_child(desc, "channels");
  for (let i = 0; i < 4; i++) {
    const channel = lsl.append_child(channels, 'channel');
    lsl.append_child_value(channel, 'label', `Channel ${i}`);
    lsl.append_child_value(channel, 'unit', 'microvolts');
    lsl.append_child_value(channel, 'type', 'EEG');
  }
  const outlet = lsl.create_outlet(info, 0, 360);
  const startTs = lsl.local_clock();

  /**
   * Stream this sample over the LSL stream and provide simulated time diff
   * @param {Array<number>} EEGSample - 1D 4-channel EEG sample array
   * @param {number} sampleId - current sample ID/index
   * @return {number} the difference in seconds between the LSL clock and the
   *  actual time the sample was streamed
   *    - if negative, you're ahead the expected time by this much seconds
   *    - if positive, you're behind of the expected time by this much seconds
   */
  const streamSample = (EEGSample, sampleId) => {
    const idealTs = startTs + (1 / sampleRate * sampleId);
    lsl.push_sample_ft(
      outlet,
      new lsl.FloatArray(EEGSample),
      idealTs,
    );
    return lsl.local_clock() - idealTs;
  }

  // if streaming from a file, read the file line-by-line and stream each sample
  if (eegCsvFilePath) {
    console.log(`streaming EEG data from ${eegCsvFilePath}`);
    await csv({
      noheader: false,
      headers: ['ch1', 'ch2', 'ch3', 'ch4']
    })
    .fromFile(eegCsvFilePath)
    .subscribe((json, lineNumber) => {
      return new Promise((resolve,reject) => {
        const EEGSample = [json['ch1'], json['ch2'], json['ch3'], json['ch4']];
        const timeDiffSecs = streamSample(EEGSample, lineNumber);
        // if the local clock is ahead of our ideal timestamp, we must wait
        if (timeDiffSecs < 0) {
          sleep(-1000 * timeDiffSecs).then(() => resolve());
        } else {
          resolve();
        }
      });
    });
  } else {
    // if not streaming from a file, stream randomly generated data
    console.log('streaming random data');
    let sampleId = 0;
    while (true) {
      let randomEEGData = Array(4);
      for (let i = 0; i < randomEEGData.length; i++) {
        randomEEGData[i] = Math.floor(Math.random() * 10)
      }
      const timeDiffSecs = streamSample(randomEEGData, sampleId);
      sampleId += 1;
      // if the local clock is ahead of our ideal timestamp, we must wait
      if (timeDiffSecs < 0) {
        await sleep(-1000 * timeDiffSecs)
      }
    }
  }
}

// read and validate command line args
const program = new Command();
program
  .requiredOption('-s, --sample-rate <rate>', 'frequency of stream in Hz')
  .option('-f, --eeg-csv-file-path <path>', 'path to EEG CSV file to stream');
program.parse(process.argv);
const { sampleRate, eegCsvFilePath } = program;
if (eegCsvFilePath) {
  if (!eegCsvFilePath.endsWith('.csv')) {
    throw new Error(`Expected .csv extension on file ${eegCsvFilePath}`);
  }
  if (!fs.existsSync(eegCsvFilePath)) {
    throw new Error(`could not find provided file path ${eegCsvFilePath}`);
  }
}
if (sampleRate <= 0) {
  throw new Error(`Invalid sample rate, must be >= 0: ${sampleRate}`);
}

main(sampleRate, eegCsvFilePath)
  .catch(error => {
  console.error(error);
  process.exit(1);
});
