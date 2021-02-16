# unset LANG
# export PYTHONIOENCODING=utf-8
import sys
import csv
import argparse
import django

django.setup()
from resistome.models import *

stcolor = {
    "78":"#A6CEE3",
    "171":"#1F78B4",
    "114":"#B2DF8A",
    "133":"#33A02C",
    "96":"#FB9A99",
    "1379":"#E31A1C",
    "23":"#FDBF6F",
    "515":"#FF7F00",
    "93":"#CAB2D6",
    "732":"#6A3D9A",
    "66":"#FFFF99",
    "182":"#B15928",
    "24":"#7A4E4E"
}
grey="#7A7A7A"

parser = argparse.ArgumentParser(
    description='Get ST for each sample from sample list file.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')

    for row in csvreader:
        mlst_qs = MLST.objects.filter(assembly__sample__barcode=row[0])
        for m in mlst_qs:
            chartcolor = stcolor[str(m.st)] if str(m.st) in stcolor else grey
            print(",".join([row[0],chartcolor,str(m.st)]))
