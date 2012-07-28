#!/usr/bin/env python

import argparse
import asyncore

import rwi.defaults as D
from rwi.server.asyn import AsynServer

def main():
    p = argparse.ArgumentParser(description='The rwi server.')
    p.add_argument('host', metavar='HOST', type=str, default=D.HOST, nargs='?',
            help='the host name to bind to (default: empty)')
    p.add_argument('-p', '--port', metavar='PORT', type=int, default=D.PORT,
            help='port to listen on (default: %(default)s)')
    args = p.parse_args()

    server = AsynServer(args.host, args.port)
    asyncore.loop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nCaught interrupt signal; quitting')
