/**
 * This file provides a function to make Petal Metrics API calls.
 */
const request = require('request');


const metricsUrl = 'https://app.petal.dev/api/v1/metrics';


/**
 * Request nicely formatted metrics from the Petal Metrics API
 * @param {string} apiKey - Petal Metrics dev API key
 * @param {Array<Array<number>>} EEGData - 2D array of 4-channel EEG data
 * @param {Array<str>} metrics - array of desired metrics results, options:
 *  'bandpower', 'preprocessed_data'
 * @return object containing all requested properties based on metrics params
 */
requestMetrics = (apiKey, EEGData, metrics) => new Promise(
  resolve => {
    // set up the API call args with EEG preprocessing settings and bandpower
    var args = {
      'nperseg': 25,
      'nfft': 75,
      'sample_rate': 256,
      'filter_multiplier': 8,
      'filter_order': 2,
      'bandpass_lowcut': 0.01,
      'bandpass_highcut': 30,
      'lowpass_cutoff': 30,
      'highpass_cutoff': .01,
      'normalize_mode': 'by_channel',
      'band_ranges': {
        'alpha': [8, 13],
        'beta': [13, 30],	
        'delta': [1, 3],
        'theta': [3, 8]
      },
      'metrics': metrics,
      'preprocess_steps' : ['bandpass','interpolate_data'],
    }
    var metricData = {
      data: EEGData,
      options: args,
    };
    var metricDetails = {
      url: metricsUrl,
      method: 'POST',
      json: metricData,
      headers: { 'X-API-KEY': apiKey },
    };

    // make the API request and log the bandpower result, or error info if it failed
    request({ ...metricDetails },
      function (error, response, body) {
        if (body === undefined) {
          console.log(response.toJSON());
          throw new Error('request failed');
        }
        if (body.calculations) {
          resolve(body.calculations);
        } else {
          console.error(error);
          console.error(body);
          throw new Error('failed request');
        }
      }
    );
  }
)

module.exports.requestMetrics = requestMetrics;
