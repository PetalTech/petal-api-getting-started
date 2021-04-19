'''
This script receives a Petal formatted OSC stream and prints it to the console.

Usage: python osc_receive.py -t /PetalStream/eeg

valid OSC topics for use with petal streaming apps:
    * /PetalStream/gyroscope
    * /PetalStream/ppg
    * /PetalStream/telemetry
    * /PetalStream/eeg
    * /PetalStream/acceleration
    * /PetalStream/connection_status
'''
import argparse
import math

import pythonosc.dispatcher
import pythonosc.osc_server


def print_petal_stream_handler(unused_addr, *args):
    '''
    Every stream is preceded by these data points:
        * int: sample ID
        * int: unix timestamp (whole number)
        * float: unix timestamp (decimal)
        * int: LSL timestamp (whole number)
        * float: LSL timestamp (decimal)

    The next set of data in the transmission follow these formats:
    telemetry:
        * float: battery level
        * float: temperature
        * float: fuel gauge voltage
    EEG:
        * float: channel 1
        * float: channel 2
        * float: channel 3
        * float: channel 4
    acceleration and gyroscope:
        * float: x
        * float: y
        * float: z
    ppg:
        * float: ambient
        * float: IR
        * float: red
    connection_status:
        * int: connected (0 or 1)
    '''
    sample_id = args[0]
    unix_ts = args[1] + args[2]
    lsl_ts = args[3] + args[4]
    data = args[5:]
    print(
        f'sample_id: {sample_id}, unix_ts: {unix_ts}, '
        f'lsl_ts: {lsl_ts}, data: {data}'
    )


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ip', type=str, required=False,
                    default="127.0.0.1", help="The ip to listen on")
parser.add_argument('-p', '--udp_port', type=str, required=False, default=14739,
                    help="The UDP port to listen on")
parser.add_argument('-t', '--topic', type=str, required=False,
                    default='/PetalStream/eeg', help="The topic to print")
args = parser.parse_args()

dispatcher = pythonosc.dispatcher.Dispatcher()
dispatcher.map(args.topic, print_petal_stream_handler)

server = pythonosc.osc_server.ThreadingOSCUDPServer(
    (args.ip, args.udp_port),
    dispatcher
)
print("Serving on {}".format(server.server_address))
server.serve_forever()
