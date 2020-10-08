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


#scaffold,start,end,orientation,gene,gene_name,rgi,ec_number,product,inference,jbrowse_link,protein_sequence

parser = argparse.ArgumentParser(
    description='Add records to inCREDBle annotation table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        if row['gene'] or None:
            try:
                scaffold_obj = Scaffold.objects.get(scaffold=row['scaffold'])
            except Scaffold.DoesNotExist:
                scaffold_obj = None
                sys.exit(row['scaffold'] + " doesn't exist. Please create it first")
            if scaffold_obj:
                try:
                    annotation_obj = Annotation.objects.get(gene=row['gene'])
                except Annotation.DoesNotExist:
                    annotation_obj = None
                if annotation_obj:
                    annotation_obj.scaffold = scaffold_obj
                    annotation_obj.start = row['start']
                    annotation_obj.end = row['end']
                    annotation_obj.orientation = row['orientation']
                    annotation_obj.gene = row['gene']
                    annotation_obj.gene_name = row['gene_name']
                    annotation_obj.rgi = row['rgi']
                    annotation_obj.amrf = row['amrf']
                    annotation_obj.ec_number = row['ec_number']
                    annotation_obj.product = row['product']
                    annotation_obj.inference = row['inference']
                    annotation_obj.jbrowse_link = "https://denovo.cnag.cat/genomes/cre/browse/?loc=" + row['scaffold'] + '%3A' + row['start'] + '..' + row['end']
                    annotation_obj.protein_sequence = row['protein_sequence']
                    print('saving ' + row['gene'])
                    annotation_obj.save()
                else:
                    obj = Annotation()
                    obj.scaffold = scaffold_obj
                    obj.start = row['start']
                    obj.end = row['end']
                    obj.orientation = row['orientation']
                    obj.gene = row['gene']
                    obj.gene_name = row['gene_name']
                    obj.rgi = row['rgi']
                    obj.amrf = row['amrf']
                    obj.ec_number = row['ec_number']
                    obj.product = row['product']
                    obj.inference = row['inference']
                    obj.jbrowse_link = "https://denovo.cnag.cat/genomes/cre/browse/?loc=" + row['scaffold'] + '%3A' + row['start'] + '..' + row['end']
                    obj.protein_sequence = row['protein_sequence']
                    print('saving ' + row['gene'])
                    obj.save()

print("Finished OK")
