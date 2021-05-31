#!/usr/bin/env python

import argparse
import os
import sys
import time

import MakeCSV
from __init__ import __version__

# __cmd__ = 'mf'
__cmd__ = sys.argv[0]


def check_file(x):
    x = os.path.join(os.getcwd(), x)
    if not os.path.exists(x):
        raise FileNotFoundError("{0} does not exist".format(x))
    else:
        return x


def check_natural(v):
    if int(v) < 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid natural number" % int(v))
    return int(v)


usage = '''usage:
  {0} mice.avi -H -o out.csv # output csv with header
  {0} mice.avi -w            # show window
  {0} mice.avi -i            # show debug info
'''.format(__cmd__)


class Formatter(
        argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):
    pass


def parser(test=None):
    parser = argparse.ArgumentParser(
        prog=__cmd__,
        formatter_class=Formatter,
        description='mice freeze detection',
        epilog=usage)

    parser.add_argument('avi', metavar='path', type=check_file,
                        help='AVI file path to process')
    parser.add_argument('-o', '--out', metavar='path', help='output file path',
                        default='')
    parser.add_argument('-t', '--threshold', type=check_natural,
                        help='threshold', default=30)
    parser.add_argument('-w', '--window', action='store_true',
                        help='show window')
    parser.add_argument('-i', '--info', action='store_true',
                        help='print info')
    parser.add_argument('-H', '--header', action='store_true',
                        help='add header')
    parser.add_argument('-d', '--delimiter', type=str, default=',',
                        help='output delimiter')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if test:
        return parser.parse_args(test)
    else:
        return parser.parse_args()


def main():
    start = time.time()
    args = parser()

    if args.info:
        print('[version: {}]'.format(__version__), file=sys.stderr)
        print('[args: {}]'.format(vars(args)), file=sys.stderr)

    print('[Detecting...]',  end='', file=sys.stderr, flush=True)

    m = MakeCSV.MakeCSV(avi=args.avi, delimiter=args.delimiter,
                        header=args.header, out=args.out,
                        threshold=args.threshold, window=args.window)

    m.make()

    if args.info:
        print('[done: {}s]'.format(time.time()-start), file=sys.stderr)

    print('\033[1K\033[G', end='', file=sys.stderr, flush=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
