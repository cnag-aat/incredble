# unset LANG
# export PYTHONIOENCODING=utf-8
import sys
import csv
import argparse
import django

django.setup()
from resistome.models import *

stcolor = {
    "131":"#A6CEE3",
    "10":"#1F78B4",
    "127":"#B2DF8A",
    "624":"#33A02C",
    "410":"#FB9A99",
    "648":"#E31A1C",
    "602":"#FDBF6F",
    "362":"#FF7F00",
    "538":"#CAB2D6",
    "58":"#6A3D9A",
    "68":"#F0E68C",
    "162":"#BDB76B",
    "23":"#b15928",
    "11106":"#654321"
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
