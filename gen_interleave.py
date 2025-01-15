#!/usr/bin/env python3
# Most code taken from HMSDK gen_migpol.py script

import argparse
import json
import os
import subprocess as sp
import sys

import yaml

# Common options
monitoring_intervals = "--monitoring_intervals 100ms 2s 20s"
monitoring_nr_regions_range = "--monitoring_nr_regions_range 10 100000"

# Common damos options
# We want a range to be big enough to interleave, so have it be at least 200MB (100 huge pages)
damos_sz_region = "--damos_sz_region 214748364800 max"
damos_filter = "--damos_filter memcg nomatching /cipp"

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--pid",
        dest="pid",
        default=None,
        type=int,
        help="The PID of the process to track."
    )
    parser.add_argument(
        "-v",
        "--virt",
        dest="virt",
        action="store_true"
    )
    parser.add_argument("-w", dest="wmark", action='store_true')
    parser.add_argument(
        "-o", "--output", dest="output", default=None, help="Set the output json file."
    )

    return parser.parse_args()

def run_command(cmd):
    with sp.Popen(cmd.split(), stdout=sp.PIPE, stderr=sp.PIPE) as p:
        stdout,stderr = p.communicate()
        stdout_lines = stdout.decode(errors="ignore")
        stderr_lines = stderr.decode(errors="ignore")
        if len(stderr_lines) > 0:
            print(stderr_lines)
        return stdout_lines

def parent_dir_of_file(filename):
    return os.path.dirname(os.path.abspath(filename))

def main():
    args = parse_argument()

    if os.geteuid() != 0:
        print("error: Run as root")
        sys.exit(1)

    damo = parent_dir_of_file(__file__) + "/damo"
    node_jsons = []

    common_opts = f"{monitoring_intervals} {monitoring_nr_regions_range}"
    common_damos_opts = f"{damos_sz_region}"

    damos_action = "--damos_action interleave"
    if args.virt:
        ops = "--ops vaddr"
    else:
        ops = "--ops paddr"
    if args.pid is not None:
        pid = f"--target_pid {args.pid}"
    else:
        pid = ""
    damos_access_rate = "--damos_access_rate 15% 100%"
    damos_age = "--damos_age 0 max"
    damos_quotas = "--damos_quotas 2s 50G 10s 0 0 1%"
    if args.wmark:
        damos_wmark = "--damos_wmarks sysfs 2s 100 95 90"
    else:
        damos_wmark = ""
    cmd = (
        f"{damo} args damon --format json {common_opts} {damos_action} "
        f"{ops} {pid} {damos_access_rate} {damos_age} {damos_quotas} {damos_wmark}"
    )
    json_str = run_command(cmd)
    node_json = json.loads(json_str)

    config = yaml.dump(node_json, default_flow_style=False, sort_keys=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(config + "\n")
    else:
        print(config)

    return 0

if __name__ == "__main__":
    sys.exit(main())
