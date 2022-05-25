# unset LANG
# export PYTHONIOENCODING=utf-8
import sys
import csv
import argparse
import django

django.setup()
from resistome.models import *

color = {
    "Comunidad de Madrid":"#fb8072",
    "Cataluña":"#ffed6f",
    "Asturias":"#8dd3c7",
    "Galicia":"#bebada",
    "Castilla-La Mancha":"#ffffb3",
    "Andalucía":"#80b1d3",
    "Comunidad Valenciana":"#fdb462",
    "Cantabria":"#b3de69",
    "Islas Baleares":"#fccde5",
    "Castilla y León":"#d9d9d9",
    "Navarra":"#bc80bd",
    "Aragón":"#ccebc5",
    "Ceuta":"#232323"
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
        qs = Sample.objects.filter(barcode=row[0])
        for samp in qs:
            chartcolor = grey
            community = "Unknown"
            if (samp.isolation_location is not None):
                community = samp.isolation_location.community
                chartcolor = color[samp.isolation_location.community] if samp.isolation_location.community in color else grey
            print(",".join([row[0],chartcolor,community]))
