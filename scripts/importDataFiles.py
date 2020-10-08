import django
django.setup()
import os
from django.core.files import File
import sys
import csv
import argparse
from resistome.models import *

# class DataFiles(models.Model):
#     assembly = models.OneToOneField(Assembly, on_delete=models.CASCADE)
#     assembly_fasta = models.FileField(upload_to='assemblyFASTA')
#     annotation_protein_fasta = models.FileField(upload_to='annotationDATA')
#     annotation_transcript_fasta = models.FileField(upload_to='annotationDATA')
#     annotation_gff = models.FileField(upload_to='annotationDATA')

parser = argparse.ArgumentParser(
    description='Add records to inCREDBle datafiles table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    for row in csvreader:
        if row['assembly'] or None:
            print(row['assembly'])
            try:
                assembly_obj = Assembly.objects.get(assembly=row['assembly'])
            except Assembly.DoesNotExist:
                assembly_obj = None
                sys.exit(row['assembly'] + " doesn't exist. Please create it first.")

            assembly = Assembly.objects.get(assembly=row['assembly'])
            assembly_fasta_filename = row['assembly_fasta']
            annotation_protein_fasta_filename = row['annotation_protein_fasta']
            annotation_transcript_fasta_filename = row['annotation_transcript_fasta']
            annotation_gff_filename = row['annotation_gff']
            qs = DataFiles.objects.filter(assembly=assembly).delete()
            df = DataFiles()
            df.assembly = assembly
            assembly_fasta_django_file = open(assembly_fasta_filename, 'rb')
            df.assembly_fasta.save(os.path.basename(assembly_fasta_filename), assembly_fasta_django_file, save=True)
            annotation_protein_fasta_django_file = open(annotation_protein_fasta_filename, 'rb')
            df.annotation_protein_fasta.save(os.path.basename(annotation_protein_fasta_filename), annotation_protein_fasta_django_file, save=True)
            annotation_transcript_fasta_django_file = open(annotation_transcript_fasta_filename, 'rb')
            df.annotation_transcript_fasta.save(os.path.basename(annotation_transcript_fasta_filename), annotation_transcript_fasta_django_file, save=True)
            annotation_gff_django_file = open(annotation_gff_filename, 'rb')
            df.annotation_gff.save(os.path.basename(annotation_gff_filename), annotation_gff_django_file, save=True)
            df.save()
print("Finished OK")
csvfile.close()
