#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse

import _damo_fmt_str
import _damon

def update_pr_schemes_stats(raw_nr):
    if _damon.any_kdamond_running():
        for name in _damon.current_kdamond_names():
            err = _damon.update_schemes_stats(name)
            if err != None:
                print('update schemes stat fail:', err)
                exit(1)
    content = _damon.read_damon_fs()
    kdamonds = _damon.current_kdamonds()
    
    print('# <kdamond> <context> <scheme> <field> <value>')
    for kdamond in kdamonds:
        for ctx in kdamond.contexts:
            for scheme in ctx.schemes:
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'nr_tried', _damo_fmt_str.format_nr(
                        scheme.stats.nr_tried, raw_nr)))
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'sz_tried', _damo_fmt_str.format_sz(
                        scheme.stats.sz_tried, raw_nr)))
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'nr_applied', _damo_fmt_str.format_nr(
                        scheme.stats.nr_applied, raw_nr)))
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'sz_applied', _damo_fmt_str.format_sz(
                        scheme.stats.sz_applied, raw_nr)))
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'qt_exceeds', _damo_fmt_str.format_nr(
                        scheme.stats.qt_exceeds, raw_nr)))

def set_argparser(parser):
    parser.add_argument('--delay', metavar='<secs>', default=3, type=float,
            help='delay between repeated status prints')
    parser.add_argument('--count', metavar='<count>', default=1, type=int,
            help='number of repeated status prints')
    parser.add_argument('--raw', action='store_true',
            help='print number in mchine friendly raw form')

def main(args=None):
    if not args:
        parser = argparse.ArgumentParser()
        set_argparser(parser)
        args = parser.parse_args()

    # Require root permission
    _damon.ensure_root_permission()
    _damon.ensure_initialized(args)

    for i in range(args.count):
        update_pr_schemes_stats(args.raw)
        if i != args.count - 1:
            time.sleep(args.delay)

if __name__ == '__main__':
    main()
