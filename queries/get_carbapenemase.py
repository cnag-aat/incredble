# unset LANG
# export PYTHONIOENCODING=utf-8
import sys
import csv
import argparse
import django
import re
django.setup()
from resistome.models import *


parser = argparse.ArgumentParser(
    description='Get ST for each sample from sample list file.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    print(",".join(["sample","OXA-48","KPC-2/3","VIM-1","NDM","IMP","GES-6"]))
    for row in csvreader:
        qs = Sample.objects.filter(barcode=row[0])
        for samp in qs:
            #chartcolor = stcolor[str(m.st)] if str(m.st) in stcolor else grey
            carbs = samp.carbapenemase.all()
            oxa="0"
            vim="0"
            imp="0"
            kpc="0"
            ndm="0"
            ges="0"
            for c in carbs:
                if(re.match("OXA",c.name)):
                    oxa = "1"
                if(re.match("IMP",c.name)):
                    imp = "1"
                if(re.match("VIM",c.name)):
                    vim = "1"
                if(re.match("KPC",c.name)):
                    kpc = "1"
                if(re.match("NDM",c.name)):
                    ndm = "1"
                if(re.match("GES",c.name)):
                    ges = "1"
            print(",".join([row[0],oxa,kpc,vim,ndm,imp,ges]))
