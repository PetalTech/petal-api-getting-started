/**
 * Call the API with only a key and no muse connection.
 * 
 * Usage: node api_standalone.js -k $API_KEY
 */

const METRICS = ['eye', 'blink', 'bandpower', 'artifact_detect'];
const WINDOW_SIZE = 256;

const { Command } = require('commander');
const { requestMetrics } = require('./api');

/**
   * The eeg data window variable tracks the currently accumulated EEG
   * samples. 
   * @param {number} numChannels the number of channels to initialize
   */
const initEegArray = (numChannels) => {
  // may optionally .fill(0); at this point, but should not be needed
  const eegDataWindow = new Array(numChannels)
  for (let i = 0; i < numChannels; i += 1) {
      console.log( 'init channel array of', i)
      eegDataWindow[i] = new Array(WINDOW_SIZE);
      eegDataWindow[i].fill(1);
  }
  console.log( 'final data window length', eegDataWindow.length);
  return eegDataWindow;
}

// read and validate command line args
const program = new Command();
program
  .requiredOption('-k, --api-key <key>', 'Petal Metrics API key');
program.parse(process.argv);
const { apiKey } = program;

const eegArr = initEegArray(4);
requestMetrics(apiKey, eegArr, METRICS)
  .then(ret => {
    console.log('get return from metrics', ret)
    console.log('SUCCESS')
  })
  .catch(err => {
    console.error(err)
    console.error('FAILURE')
  });
