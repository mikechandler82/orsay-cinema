#!/usr/bin/env python3
"""Serve installation files only. Not needed after the TV app is installed."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bind', default='127.0.0.1', help='Use 0.0.0.0 to serve to your TV on a trusted LAN')
    parser.add_argument('--port', type=int, default=80)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent / 'dist'
    if not (directory / 'widgetlist.xml').exists():
        parser.error('Run build.py with --server-url first')
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    print('Installation server only; stop it after syncing the TV.')
    ThreadingHTTPServer((args.bind, args.port), handler).serve_forever()
