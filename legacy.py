#!/usr/bin/env python3

import argparse
import datetime
from pathlib import Path
import re
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="This script will check how many plots were created with a specific date timestamp")
    parser.add_argument("-p", "--plot", help="Path to the plots directory to search (we will look recursively)",
                        default=Path("/mnt/plots/"), type=Path)
    parser.add_argument("-f", "--folder", type=str, default="legacy")

    try:
        args = parser.parse_args()
    except Exception as e:
        parser.print_help()
        raise e

    return args

if __name__ == "__main__":
    args = parse_args()
    count = 0
    for folder in sorted(os.listdir(args.plot)):
        legacy = str(args.plot) + "/" + folder + "/legacy/"
        if Path(legacy).exists():
            num = len(os.listdir(legacy))
            count = count + num
            print(f"{folder}:\t{num} remaining")
        
    print(f"There are a total of {count} legacy plots remaining")

