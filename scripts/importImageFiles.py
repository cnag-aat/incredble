import django
import os
import sys
django.setup()
from django.core.files import File
import argparse

from resistome.models import *
import csv

# assembly  image
# AH0325_v1 /home/talioto/datafiles/images//AH0325.v1.assembly.png
# AH0326_v1 /home/talioto/datafiles/images/AH0326.v1.assembly.png


parser = argparse.ArgumentParser(
    description='Add Bandage images to inCREDBle assembly table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    for row in csvreader:
        if row['assembly'] or None:
            print(row['assembly'])
            try:
                assembly = Assembly.objects.get(assembly=row['assembly'])
            except Assembly.DoesNotExist:
                assembly = None
                sys.exit(row['assembly'] + " does not exist.")
            if assembly:
                image_filename = row['image']
                png_file = open(image_filename, 'rb')
                assembly.image.save(os.path.basename(image_filename), png_file, save=True)
                assembly.save()
print("Finished OK")
csvfile.close()
