import sys
import csv
import argparse
import django
django.setup()
from resistome.models import *


# class Annotation(models.Model):
#     scaffold = models.ForeignKey(Scaffold, on_delete=models.CASCADE,
#         related_name='gene_set', related_query_name="gene_set")
#     start = models.PositiveIntegerField(null=True, blank=True)
#     end = models.PositiveIntegerField(null=True, blank=True)
#     orientation = models.CharField(max_length=1, blank=True, null=True, choices=(('+', '+'), ('-', '-')))
#     gene = models.CharField(max_length=20, unique=True, blank=True, null=True)
#     gene_name = models.CharField(max_length=20, blank=True, null=True)
#     rgi = models.CharField(max_length=3, blank=True, null=True, choices=(('Yes', 'Yes'),))
#     ec_number = models.CharField(max_length=20, blank=True, null=True)
#     product = models.TextField(blank=True, null=True)
#     inference = models.TextField(blank=True, null=True)
#     jbrowse_link = models.URLField(max_length=1000, blank=True, null=True)
#     protein_sequence = models.TextField(blank=True, null=True)


# scaffold,start,end,orientation,gene,gene_name,rgi,ec_number,product,inference,jbrowse_link,protein_sequence

parser = argparse.ArgumentParser(
    description='Add orthogroup to inCREDBle annotation table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    for row in csvreader:
        if row['gene'] or None:
            print(row['gene'])
            try:
                obj = Annotation.objects.get(gene=row['gene'])
            except Annotation.DoesNotExist:
                obj = None
            if obj:
                obj.orthogroup = row['orthogroup']
                obj.save()

print("Finished OK")
