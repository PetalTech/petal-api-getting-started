/**
 * This script receives a Petal formatted LSL stream and prints it to the console.
 * 
 * Usage: node osc_receive.js -t /PetalStream/eeg -p 14739 -i localhost
 * valid LSL stream names for use with petal streaming apps:
 *     * /PetalStream/gyroscope
 *     * /PetalStream/ppg
 *     * /PetalStream/telemetry
 *     * /PetalStream/eeg
 *     * /PetalStream/acceleration
 *     * /PetalStream/connection_status
 */
const osc = require('osc');
const { Command } = require('commander');

// read and validate command line args
const program = new Command();
program
.requiredOption('-p, --port <int>', 'topic of OSC stream to log')
.requiredOption('-i, --ip <str>', 'topic of OSC stream to log')
.requiredOption('-t, --topic <str>', 'topic of OSC stream to log')
program.parse(process.argv);
const { port, ip, topic } = program;

// Create an osc.js UDP Port.
console.log(`creating new listening UDP port ${port} on ip ${ip}`);
var udpPort = new osc.UDPPort({
  localAddress: ip,
  localPort: port,
  metadata: true
});

console.log('listening for incoming UDP OSC messages');
udpPort.on('message', function (oscMsg, timeTag, info) {
  if (oscMsg.address === topic) {
    const sample_id = oscMsg.args[0].value;
    const unix_ts = oscMsg.args[1].value + oscMsg.args[2].value;
    const lsl_ts = oscMsg.args[3].value + oscMsg.args[4].value;
    const data = [];
    for (let i = 5; i < oscMsg.args.length; i += 1) {
      data[i - 5] = oscMsg.args[i].value;
    }
    console.log(
      `Received ${topic}, sample_id: ${sample_id} unix_ts: ${unix_ts} ` +
      `lsl_ts: ${lsl_ts}`, data
    );
    console.log("Remote info is: ", info);
  }
});

// Open the socket.
udpPort.open();
