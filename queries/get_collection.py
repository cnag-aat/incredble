# unset LANG
# export PYTHONIOENCODING=utf-8
import sys
import csv
import argparse
import django
import re
django.setup()
from resistome.models import *

color = {
    "SERGAS":"#66c2a5",
    "CNM":"#fc8d62"
}
grey="#7A7A7A"
parser = argparse.ArgumentParser(
    description='Get ST for each sample from sample list file.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    print(",".join(["sample","collection","color"]))
    for row in csvreader:
        qs = Sample.objects.filter(barcode=row[0])
        for samp in qs:
            print(",".join([row[0],color[samp.collection],samp.collection]))
