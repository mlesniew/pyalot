#!/usr/bin/env python

import argparse
import os
import sys
import platform

import requests

from .pyalot import pyalot

DEFAULT_TOKEN_PATH = '~/.pushalot-token'

def main():
    try:
        parser = argparse.ArgumentParser(
            description='Send push notifications to devices')

        parser.add_argument('--title')
        parser.add_argument('--link')
        parser.add_argument('--link-title')
        parser.add_argument('--source', default=platform.node())
        parser.add_argument('--image')
        parser.add_argument('--ttl', type=int)
        parser.add_argument('--silent', action='store_true')
        parser.add_argument('--important', action='store_true')
        parser.add_argument('--token')
        parser.add_argument('--token-path', default=DEFAULT_TOKEN_PATH)
        parser.add_argument('--pipe', action='store_true')
        parser.add_argument('body', nargs='*')

        args = parser.parse_args()

        if args.token:
            token = args.token
        else:
            try:
                with open(os.path.expanduser(args.token_path)) as f:
                    token = f.read().strip()
            except Exception as e:
                print 'Error loading token:', e
                return 1

        if args.pipe:
            # read body from stdin
            body = '\n'.join(line for line in sys.stdin)
        else:
            # read body from arguments
            body = ' '.join(args.body)

        try:
            pyalot(body=body,
                    title=args.title, source=args.source,
                    link=args.link, link_title=args.link_title,
                    image=args.image,
                    silent=args.silent, important=args.important,
                    ttl=args.ttl,
                    token=token)
        except ValueError as e:
            print e
            return 1
        except requests.exceptions.RequestException as e:
            print 'Request error:', e
            return 1
        except requests.ConnectionError as e:
            print 'Connection error:', e
            return 1

    except KeyboardInterrupt:
        return 1


if __name__ == '__main__':
    main()
