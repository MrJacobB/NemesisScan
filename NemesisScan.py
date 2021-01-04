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

#Instantiates nmap
nmap = nmap3.Nmap()


def main():
    args: Dict[str, str] = read_args()

    print(args)
    print(args["size"])
    print(args["target"])

    nmap_scan(args)



def nmap_scan(args):
    if args["size"] == 1:
        print("Small scan")
        scanport=10
    elif args["size"] == 2:
        scanport=1000
        print("Medium scan")
    elif args["size"] == 3:
        scanport=65389
        print("Large scan")

    # Scans with nmap for top ports - (ip , top_ports)
    results = nmap.scan_top_ports(args["target"], scanport)
    #temp dump json to file for analysis
    result_dump1 = json.dump(results, open("nmap_top_ports.json", "w"), indent=4)

    os_results = nmap.nmap_os_detection(args["target"]) # MOST BE ROOT
    #temp dump json to file for analysis
    result_dump2 = json.dump(os_results, open("nmap_os_detection.json", "w"), indent=4)
    
    service_results = nmap.nmap_version_detection(args["target"]) # MOST BE ROOT
    #temp dump json to file for analysis
    result_dump3 = json.dump(service_results, open("nmap_version_detection.json", "w"), indent=4)

    list_results = nmap.nmap_list_scan(args["target"])
    #temp dump json to file for analysis
    result_dump4 = json.dump(list_results, open("nmap_list.json", "w"), indent=4)


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
        # size.set_defaults(medium=True)
        
        #for debug:
        size.set_defaults(small=True)
        
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
        if args.small:
            my_dict = {"size": 1, "target": args.target_list}
        elif args.medium:
            my_dict = {"size": 2, "target": args.target_list}
        elif args.large:
            my_dict = {"size": 3, "target": args.target_list}

    # return dictionary
    return my_dict



if __name__ == "__main__":
    main()