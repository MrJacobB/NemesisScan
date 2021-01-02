#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
import json
import argparse
import concurrent.futures
import nmap3
from datetime import datetime
from typing import Dict


def main():
    args: Dict[str, str] = read_args()

    print(args)
    print(args["size"])
    print(args["target"])

    #Instantiates nmap
    nmap = nmap3.Nmap()

    # Scans with nmap for top ports - (ip , top_ports)
    # results = nmap.scan_top_ports("127.0.0.1", 10)
    results = nmap.scan_top_ports("192.168.1.1", 10)
    # Dumps json result to file for manual analyzes
    result_dump = json.dump(results, open("nmap_top_ports.json", "w"), indent=4)

    # os_results = nmap.nmap_os_detection("127.0.0.1") # MOST BE ROOT
    # os_results = nmap.nmap_os_detection("192.168.1.1") # MOST BE ROOT
    # result_dump = json.dump(os_results, open("nmap_os_detection.json", "w"), indent=4)


    # for key, value in results.items():
    #     print(key, value)
    #     print("break")
    #     for key1, value1 in value.items():
    #         print(key1, value1)
    # print("break")
    # print(results)

    # data = json.loads(results.get())
    # print(data)
    # print(results.keys())
    # print(results["127.0.0.1"].items())


def read_args() -> Dict[str, str]:
    # Check for valid CLI arguments
    parser = argparse.ArgumentParser()
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--target", type=str, metavar="", help="Small scale scanning")
    target.add_argument(
        "--target_list", type=str, metavar="", help="Medium scale scanning"
    )
    size = parser.add_mutually_exclusive_group()
    size.add_argument("-s", "--small", action="store_true", help="Small scale scanning")
    size.add_argument(
        "-m", "--medium", action="store_true", help="Medium scale scanning"
    )
    size.add_argument("-l", "--large", action="store_true", help="Large scale scanning")
    args = parser.parse_args()
    if args.small == False and args.medium == False and args.large == False:
        # Dumb way of making a default - possible TODO: parser defaults?
        size.set_defaults(medium=True)
        args = parser.parse_args()

    if args.target:
        # If target is true, deterimine scan size
        if args.small:
            my_dict = {"size": 1, "target": args.target}
        elif args.medium:
            my_dict = {"size": 2, "target": args.target}
        elif args.large:
            my_dict = {"size": 3, "target": args.target}
    elif args.target_list:
        # If target_list is true, deterimine scan size
        # TODO:
        # Split list into json/xml/object?
        if args.small:
            my_dict = {"size": 1, "target": args.target_list}
        elif args.medium:
            my_dict = {"size": 2, "target": args.target_list}
        elif args.large:
            my_dict = {"size": 3, "target": args.target_list}

    # return dictionary
    return my_dict


def scan():
    return {}
    # TODO
    # Enum:

    # nmap

    # nabuu

    # TODO
    # Service detection:

    # nmap --script

    # nuclei

    # TODO
    # Web analyzing:

    # subfinder

    # nslookup

    # webanalyzer

    # gohead


if __name__ == "__main__":
    main()