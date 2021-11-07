/**
 * This script receives a Petal formatted LSL stream and prints it to the console.
 * 
 * Usage: node webhook_receive.js -p 14739 -i localhost
 * The root path '/' will listen for all events. Example payload for 'metricsJson':
 * {
 *  'action': {
 *      'value': {
 *          'artifact_detect': {
 *              'channel1': 'artifact',
 *              'channel2': 'artifact',
 *              'channel3': 'artifact',
 *              'channel4': 'artifact'
 *          },
 *          bandpower: {
 *            channel1: {
 *              '0': 20.88662778423314,
 *              '1': 47.681796906634396,
 *              '2': 52.49722928091861,
 *              '3': 80.58513408010214
 *            },
 *            channel2: {
 *              '0': 10.954671304955088,
 *              '1': 27.76331742324538,
 *              '2': 36.1206198231319,
 *              '3': 35.02804073557742
 *            },
 *            channel3: {
 *              '0': 38.02791333015509,
 *              '1': 85.29277913777635,
 *              '2': 83.80068133441219,
 *              '3': 156.39622267856817
 *            },
 *            channel4: {
 *              '0': 20.88662778423314,
 *              '1': 47.681796906634396,
 *              '2': 52.49722928091861,
 *              '3': 80.58513408010214
 *            }
 *          },
 *          'blink': {'blink': 0},
 *          'eye': {'eye': 0}
 *      },
 *      'time': 1214.697467542195
 *   },
 *   'type': 'metricsJson'
 * }
 */
const express = require("express");
const router = express.Router();
const app = express();
const bodyParser = require('body-parser');
const { Command } = require('commander');

app.use(bodyParser.urlencoded());
app.use(bodyParser.json());

const program = new Command();
program
.requiredOption('-p, --port <int>', 'topic of OSC stream to log')
.requiredOption('-i, --ip <str>', 'topic of OSC stream to log')
program.parse(process.argv);
const { port, ip } = program;

app.use("/", router);

app.post('/', (req, res) => {
  console.log(req.body);
  return res.status(200);
});

app.listen(port, ip, () => {
  console.log(`listening for petal webhooks on port ${ip}:${port}`);
});