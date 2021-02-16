# unset LANG
# export PYTHONIOENCODING=utf-8
import sys
import csv
import argparse
import django

django.setup()
from resistome.models import *

stcolor = {
    "11":"#A6CEE3",
    "307":"#1F78B4",
    "147":"#B2DF8A",
    "392":"#33A02C",
    "512":"#FB9A99",
    "15":"#E31A1C",
    "405":"#FDBF6F",
    "5000":"#FF7F00",
    "101":"#CAB2D6",
    "1961":"#6A3D9A",
    "326":"#FFFF99",
    "258":"#B15928",
    "437":"#7A4E4E"
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
