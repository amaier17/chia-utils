#!/usr/bin/env python3

import argparse
import datetime
from pathlib import Path
import re
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="This script will check how many plots were created with a specific date timestamp")
    parser.add_argument("-p", "--plot", help="Path to the plots directory to search (we will look recursively)",
                        default=Path("/mnt/plots/"), type=Path)
    parser.add_argument("-d", "--date", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), default=datetime.datetime.today())

    try:
        args = parser.parse_args()
    except Exception as e:
        parser.print_help()
        raise e

    return args

if __name__ == "__main__":
    args = parse_args()
    print(f"Checking for all plots with the date {args.date.strftime('%Y-%m-%d')}")
    count = 0
    for plot in args.plot.rglob("*.plot"):
        plot_search = re.compile(r"plot-k\d{2}-(\d{4})-(\d{2})-(\d{2}).*")
        res = plot_search.match(str(plot).split("/")[-1])
        year = int(res.group(1))
        month = int(res.group(2))
        day = int(res.group(3))
        if year == args.date.year and month == args.date.month and day == args.date.day:
            count=count+1

    print(f"I found a total of {count} plots on {args.date.strftime('%Y-%m-%d')}")
