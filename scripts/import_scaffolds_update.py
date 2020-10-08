
# Load initial Resistom data from excel into the database

import csv
import argparse
import django
django.setup()

from resistome.models import *


    # sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    # assembly = models.ForeignKey(Assembly, blank=True, null=True, on_delete=models.CASCADE)
    # scaffold = models.CharField(max_length=20, unique=True, db_index=True)
    # jbrowse_link = models.URLField(max_length=1000, blank=True, null=True, verbose_name="Jbrowse")
    # scaffold_length = models.PositiveIntegerField(blank=True, null=True)
    # depth = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Est. Copy Number")
    # circular = models.NullBooleanField(blank=True, null=True)
    # centrifuge_species = models.CharField(max_length=200, blank=True, null=True, verbose_name="Centrifuge classification")
    # centrifuge_seq = models.CharField(max_length=20, blank=True, null=True)

parser = argparse.ArgumentParser(
    description='Add records to inCREDBle scaffold table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    for row in csvreader:
        if row['assembly'] or None:
            print(row['assembly'] or None)
            bcv = row['assembly'].split("_")
            sample=bcv[0]
            try:
                assembly_obj = Assembly.objects.get(assembly=row['assembly'])
            except Assembly.DoesNotExist:
                assembly_obj = None
            try:
                sample_obj = Sample.objects.get(barcode=sample)
            except Sample.DoesNotExist:
                sample_obj = None

            if assembly_obj and sample_obj:
                try:
                    scaffold_obj = Scaffold.objects.get(scaffold=row['scaffold'])
                except Scaffold.DoesNotExist:
                    scaffold_obj = None
                if scaffold_obj:
                    scaffold_obj.assembly = assembly_obj
                    scaffold_obj.sample = sample_obj
                    scaffold_obj.scaffold = row['scaffold']
                    scaffold_obj.jbrowse_link = "https://resistome.cnag.cat/genomes/cre/browse/?loc=" + row['scaffold']
                    scaffold_obj.scaffold_length = row['scaffold_length']
                    scaffold_obj.depth = row['depth']
                    scaffold_obj.circular = row['circular']
                    scaffold_obj.save()
                else:
                    obj = Scaffold()
                    obj.assembly = assembly_obj
                    obj.sample = sample_obj
                    obj.scaffold = row['scaffold']
                    obj.jbrowse_link = "https://resistome.cnag.cat/genomes/cre/browse/?loc=" + row['scaffold']
                    obj.scaffold_length = row['scaffold_length']
                    if (row['depth']):
                        obj.depth = row['depth']
                    else:
                        obj.depth = 1
                    obj.circular = row['circular']
                    obj.save()

print("Finished OK")
