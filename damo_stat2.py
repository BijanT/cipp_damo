#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse

import damo_stat_kdamonds_summary
import damo_stat_schemes_stats

import _damon_args

def set_argparser(parser):
    subparsers = parser.add_subparsers(title='stat type', dest='stat_type',
            metavar='<stat type>', help='the type of the stat to show')
    subparsers.required = True

    parser_kdamonds_summary = subparsers.add_parser('kdamonds_summary',
            help='summary of kdamonds')
    damo_stat_kdamonds_summary.set_argparser(parser_kdamonds_summary)

    parser_schemes_stats = subparsers.add_parser('schemes_stats',
            help='schemes apply stats')
    damo_stat_schemes_stats.set_argparser(parser_schemes_stats)

    _damon_args.set_common_argparser(parser)

def main(args=None):
    if not args:
        parser = argparse.ArgumentParser()
        set_argparser(parser)
        args = parser.parse_args()

    if args.stat_type == 'kdamonds_summary':
        damo_stat_kdamonds_summary.main(args)
    elif args.stat_type == 'schemes_stats':
        damo_stat_schemes_stats.main(args)

if __name__ == '__main__':
    main()
