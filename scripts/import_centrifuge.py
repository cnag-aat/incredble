import django
django.setup()

import csv
import sys
import argparse

from resistome.models import *

parser = argparse.ArgumentParser(
    description='Add records to inCREDBle datafiles table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    for row in csvreader:
        if row['scaffold'] or None:
            print(row['scaffold'] or None)


##            species = None
##            created = False
##            if row['centrifuge_sp']:
##                spec,created = Species.objects.get_or_create(
##                    name=row['centrifuge_sp'],
##                )

            try:
                scaff = Scaffold.objects.get(scaffold=row['scaffold'])
            except:
                scaff = None
            if scaff:
                try:
                    cent = Centrifuge.objects.get(scaffold=row['scaffold'],centrifuge_species=row['centrifuge_sp'],centrifuge_seq=row['seqID'])
                except:
                    cent = Centrifuge()
                    cent.scaffold=scaff
                    cent.centrifuge_species=row['centrifuge_sp']
                    cent.centrifuge_seq=row['seqID']
                    cent.save()


print("Finished OK")
