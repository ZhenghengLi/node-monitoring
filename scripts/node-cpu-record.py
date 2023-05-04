#!/usr/bin/env python3

import argparse
import time
import logging
import threading
from signal import signal, SIGINT
import json
import psutil
import csv

parser = argparse.ArgumentParser(description='desc')
parser.add_argument("csvfile")
parser.add_argument("-i", dest="interval", type=int, default=1)
parser.add_argument("-m", dest="maxrec", type=int, default=10000)
args = parser.parse_args()

psutil.cpu_times_percent()

attr_list = ['user', 'system', 'idle', 'iowait',
             'irq', 'softirq', 'steal', 'guest']

csv_fields = ['unixtime'] + attr_list + ['memory']

csv_values = {}

stop_event = threading.Event()


def handler(signal_received, frame):
    stop_event.set()
    print("\nstop recording and close file ...")


signal(SIGINT, handler)


def do_the_record(csvfile):
    print('start recording to file', csvfile)
    with open(args.csvfile, 'x') as fout:
        writer = csv.DictWriter(fout, fieldnames=csv_fields)
        writer.writeheader()
        for x in range(args.maxrec):
            time.sleep(args.interval)
            if stop_event.is_set():
                break
            csv_values['unixtime'] = "%.2f" % time.time()
            ctp = psutil.cpu_times_percent()
            for attr in attr_list:
                csv_values[attr] = getattr(ctp, attr)
            svm = psutil.virtual_memory()
            csv_values['memory'] = svm.percent
            print(csv_values)
            writer.writerow(csv_values)
    print('recording stopped.')


thread1 = threading.Thread(target=do_the_record, args=(args.csvfile,))
thread1.start()
thread1.join()

print('done.')
