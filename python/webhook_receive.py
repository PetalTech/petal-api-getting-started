'''
This script listens on a webhook URL for messages and prints it to the console.
The root path '/' will listen for all events. Example payload for 'metricsJson':
{
    'action': {
        'value': {
            'artifact_detect': {
                'channel1': 'artifact',
                'channel2': 'artifact',
                'channel3': 'artifact',
                'channel4': 'artifact'
            },
            bandpower: {
                channel1: {
                '0': 20.88662778423314,
                '1': 47.681796906634396,
                '2': 52.49722928091861,
                '3': 80.58513408010214
                },
                channel2: {
                '0': 10.954671304955088,
                '1': 27.76331742324538,
                '2': 36.1206198231319,
                '3': 35.02804073557742
                },
                channel3: {
                '0': 38.02791333015509,
                '1': 85.29277913777635,
                '2': 83.80068133441219,
                '3': 156.39622267856817
                },
                channel4: {
                '0': 20.88662778423314,
                '1': 47.681796906634396,
                '2': 52.49722928091861,
                '3': 80.58513408010214
                }
            },
            'blink': {'blink': 0},
            'eye': {'eye': 0}
        },
        'time': 1214.697467542195
    },
    'type': 'metricsJson'
}

Usage: python webhook_receive.py -i localhost -p 14739
'''
import argparse
from flask import Flask, request, Response
from waitress import serve

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int,
                    default=14739, help='the port of petal configured webhooks')
parser.add_argument('-i', '--ip', type=int,
                    default='0.0.0.0', help='the IP of petal configured webhooks')
args = parser.parse_args()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def myendpoint():
    print('received data\n')
    print(request.json)
    return Response(status=200)

print(f'waiting for petal data on port {args.ip}:{args.port}')

serve(app, host=args.ip, port=args.port, threads=1)
