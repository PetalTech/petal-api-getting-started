/**
 * This file provides a function to make Petal Metrics API calls.
 * 
 * Example response (replace 'bad_data' with a number): {
 *  artifact_detect: {
 *    channel1: 'artifact',
 *    channel2: 'good',
 *    channel3: 'artifact',
 *    channel4: 'artifact'
 *  },
 *  bandpower: {
 *    channel1: {
 *      '0': 15.966456958134767,
 *      '1': 38.07424640852407,
 *      '2': 60.4062953043204,
 *      '3': 65.69193669664433
 *    },
 *    channel2: {
 *      '0': 'bad_data',
 *      '1': 'bad_data',
 *      '2': 'bad_data',
 *      '3': 'bad_data'
 *    },
 *    channel3: {
 *      '0': 'bad_data',
 *      '1': 'bad_data',
 *      '2': 'bad_data',
 *      '3': 'bad_data'
 *    },
 *    channel4: {
 *      '0': 'bad_data',
 *      '1': 'bad_data',
 *      '2': 'bad_data',
 *      '3': 'bad_data'
 *    }
 *  },
 *  blink: { blink: 'False' },
 *  eye: { eye: 'False' }
 */
const request = require('request');

const API_HOST = 'https://app.petal.dev';


/**
* Request nicely formatted metrics from the Petal Metrics API
* @param {string} token - Petal Metrics dev API key
* @param {Array<Array<number>>} EEGData - 2D array of 4-channel EEG data
* @param {Array<str>} metrics - array of desired metrics results, options:
*  'bandpower', 'preprocessed_data'
* @return object containing all requested properties based on metrics params
*/
const requestMetrics = (token, EEGData, metrics) => {
  return new Promise((resolve, reject) => {
    const baseURL = `${API_HOST}/api/v1`
    const auth = token;
    const url = `${baseURL}/app/metrics`;
    // const url = `${baseURL}/metrics`;
    const args = {
      band_ranges: {
        alpha: [8, 13],
        beta: [13, 30],	
        delta: [1, 3],
        theta: [3, 8]
      },
      metrics: metrics,
      preprocess_steps: [],
    };
    const metricData = {
      data: EEGData,
      options: args,
    };
    const metricDetails = {
      url,
      method: 'POST',
      json: metricData,
      headers: {
        Authorization: `Bearer ${auth}`,
        'Content-Type': 'application/json',
      },
    }
    const unixCallTs = new Date() / 1000;
    // make the API request and log the bandpower result, or error info if it failed
    request(metricDetails, (...args) => {
      // console.log(args);
      const [ error, response, body ] = args;
      // console.log('received request response, processing');
      // console.log(response);
      if (error) {
        console.error(error);
        console.error(body);
        reject(new Error('failed request'));
      }
      if (body && body.calculations) {
        // provide the metrics calculations, the call ts and return ts
        resolve({
          metrics: body.calculations,
          unixCallTs,
          unixRecvTs: new Date() / 1000
        });
      } else {
        console.error(error);
        console.error(body);
        console.error(response);
        reject(new Error('no calculations in body'));
      }
    });
  });
};

module.exports.requestMetrics = requestMetrics;
