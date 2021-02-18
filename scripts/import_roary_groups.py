import sys
import csv
import argparse
import django
django.setup()
from resistome.models import *

# argument: Ecoli_genes_classified_prefixed.txt
parser = argparse.ArgumentParser(
    description='Add roary groups to inCREDBle RoaryGroup table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    for row in csvreader:
        try:
            sampleobj = Sample.objects.get(barcode=row['barcode'])
        except Sample.DoesNotExist:
            sampleobj = None
        try:
            rgobj = RoaryGroup.objects.get(roary_gene=row['roary_gene'])
        except RoaryGroup.DoesNotExist:
            rgobj, _ = RoaryGroup.objects.get_or_create(
                roary_gene=row['roary_gene'])
        rgobj.species = sampleobj.species
        rgobj.roary_core = row['roary_core']
        print('saving ' + row['roary_gene'])
        rgobj.save()

print("Finished OK")
