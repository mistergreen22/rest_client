#  Version 1.1

#!/usr/bin/python
# ToDo add config
# ToDo add logging
# ToDo replace json schemes
# ToDo replace error message

import argparse
import http
import socketserver
import json

from collections import deque
from http.server import CGIHTTPRequestHandler
from urllib import parse

URL = 'http://localhost'

METHOD_GET = 'get'
METHOD_POST = 'post'
METHOD_PUT = 'put'
METHOD_DELETE = 'delete'

DEFAULT_ALIAS = 0

LIMIT_ALIAS = 10000
SUPPORTED_LIMIT_QUEUE = 100
SUPPORTED_LIMIT_MESSAGE = 100

DEFAULT_PORT = 8888
RAGE_PORT = (1024, 49152)

NO_MESSAGES = 'no messages'
MESSAGE_DONE = 'Done'



queues = {}


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


class BaseServer(http.server.BaseHTTPRequestHandler):
    def _send_header(self, code, status):
        self.send_response(code, status)
        self.send_header('content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        query = parse.parse_qs(parse.urlparse(self.path).query)
        alias = int(query['queue'][0]) if len(query) else DEFAULT_ALIAS

        if 0 < alias > LIMIT_ALIAS:
            self._send_header(400, 'Unsupported alias')
            return
        else:
            queue = queues.get(alias)
            if queue is None or len(queue) == 0:
                message = NO_MESSAGES
            else:
                # Alias an empty queue is not remove
                message = queue.popleft()

        self._send_header(200, 'Ok')
        self.wfile.write(
            json.dumps({'message': message}).encode(encoding='utf_8'))

    def do_POST(self):
        data_len = int(self.headers.get('content-length'))
        raw_json_data = self.rfile.readline(data_len).decode(encoding='utf_8')
        # magic!!! need to convert twice
        # ToDo investigate it
        json_data = json.loads(raw_json_data)

        alias = json_data.get('queue', DEFAULT_ALIAS)
        message = json_data.get('message', '')

        if message == '':
            self._send_header(400, 'Message is empty')
            return

        if 0 < alias > LIMIT_ALIAS:
            self._send_header(400, 'Queue must be <= {}'.format(LIMIT_ALIAS))
            return

        queue = queues.get(alias)
        if queue is None:
            if len(queues) < SUPPORTED_LIMIT_QUEUE:
                queue = deque()
                queue.append(message)
                queues.update({alias: queue})
            else:
                # ToDo need to specify requirements
                # self._send_header(400, 'Server supports only 100 queues')
                # return
                pass
        elif len(queue) == SUPPORTED_LIMIT_MESSAGE:
            # ToDo need to specify requirements
            # self._send_header(
            #     400, 'Queue is full, support only 100 messages')
            # return
            pass
        else:
            queue.append(message)

        self._send_header(201, 'Ok')

    def do_DELETE(self):
        query = parse.parse_qs(parse.urlparse(self.path).query)
        alias = int(query['queue'][0]) if len(query) else DEFAULT_ALIAS

        if 0 < alias > LIMIT_ALIAS:
            self._send_header(400, 'Unsupported alias')
            return
        else:
            queue = queues.get(alias)
            if queue is None or len(queue) == 0:
                self._send_header(404, 'Not Found')
            else:
                # Alias an empty queue is not remove
                queue.popleft()
                self._send_header(204, 'Ok')
        return

    def do_PUT(self):
        data_len = int(self.headers.get('content-length'))
        raw_json_data = self.rfile.readline(data_len).decode(encoding='utf_8')
        # magic!!! need to convert twice
        # ToDo investigate it
        json_data = (json.loads(raw_json_data))

        alias = json_data.get('queue', DEFAULT_ALIAS)
        message = json_data.get('message', '')

        if alias > LIMIT_ALIAS:
            self._send_header(400, 'Unsupported alias')
            return
        else:
            queue = queues.get(alias)
            if queue is None or len(queue) == 0:
                self._send_header(404, 'Not Found')
            else:
                queue.popleft()
                queue.append(message)
                self._send_header(205, 'No Content')
                return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p', dest='PORT', type=int, default=DEFAULT_PORT, action='store',
        help='Server port, [rage: {}, [default: {}]'.format(
            RAGE_PORT, DEFAULT_PORT))

    args = parser.parse_args()

    # Validation of parameters
    if args.PORT not in range(*RAGE_PORT):
        print('Invalid choice range: "{}", "{}"'.format(args.PORT, RAGE_PORT))
        exit()

    server = ThreadedHTTPServer(('localhost', args.PORT), BaseServer)
    print('Start server. Port: "{}"'.format(args.PORT))
    server.serve_forever()
