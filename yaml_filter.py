#!/usr/bin/env python3

"""
yaml_filter [-i type,type] [-o type,type]

Takes stdin, selects only objects in the 'in_filter', discards
objects in the 'out_filter', and writes the result to stdout.

The use case is with e.g. Kubernetes, you have a YAML file
which has CRD, webhook, and objects using these.

Apply the same YAML 3 times:

cat foo.yaml | yaml_filter -i CustomResourceDefinition | kubectl apply -f -
cat foo.yaml | yaml_filter -i ValidatingWebhookConfiguration | kubectl apply -f -
cat foo.yaml | kubectl apply -f -

on the last run you could choose

 -o CustomResourceDefinition,ValidatingWebhookConfiguration

but its a bit moot since Kubernetes will properly apply the unchanged
CRD and WebHook

"""

import sys
import argparse
import yaml
import csv

parser = argparse.ArgumentParser(description='Filter kubernetes objects')
parser.add_argument('-i', '--in_filter',
                    help='Print only objects in this comma-sep list',
                    default=[])
parser.add_argument('-o', '--out_filter',
                    help='Print only objects not this comma-sep list',
                    default=[])
args = parser.parse_args()

if args.in_filter:
    args.in_filter = args.in_filter.split(',')
if args.out_filter:
    args.out_filter = args.out_filter.split(',')

for x in yaml.load_all(sys.stdin):
    if not args.in_filter or x['kind'] in args.in_filter:
        if not args.out_filter or x['kind'] not in args.out_filter:
            print("---")
            print(yaml.dump(x))
