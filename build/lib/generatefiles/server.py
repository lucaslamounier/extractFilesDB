# -*- encoding: utf-8 -*-
__author__ = 'lucas'

import argparse
from bottledaemon import daemon_run

def server():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'stop'], help='action')
    parser.add_argument('-host', default='localhost')
    parser.add_argument('-port', default='8888')
    args = parser.parse_args()

    if args.action == 'start':
        print ('Started server %s:%s ' %(args.host, args.port))
    else:
        print ('Stopped')

    daemon_run(args.host, args.port)