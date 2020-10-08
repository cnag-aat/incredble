
# Load initial Resistom data from excel into the database

import csv
import argparse
import django
django.setup()

from resistome.models import *

parser = argparse.ArgumentParser(
    description='Add records to inCREDBle assembly table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    for row in csvreader:
        if row['assembly'] or None:
            print(row['assembly'] or None)


            try:
                sampleobj = Sample.objects.get(barcode=row['sample_barcode'])
            except Sample.DoesNotExist:
                sampleobj = None

            if sampleobj:
                print(sampleobj.name)
                qs = Assembly.objects.filter(sample=sampleobj).delete()
                obj = Assembly()
                obj.sample = sampleobj
                obj.assembly = row['assembly']
                obj.total_scaffolds = row['total_scaffolds']
                obj.circular_scaffolds = row['circular_scaffolds']
                obj.circularity_ratio = row['circularity_ratio']
                obj.scaffolds_2kb_or_shorter = row['scaffolds_2kb_or_shorter']
                obj.assembly_length = row['assembly_length']
                obj.max_scaffold_length = row['max_scaffold_length']
                obj.assembler = row['assembler']
                obj.save()

print("Finished OK")
