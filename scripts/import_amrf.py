import sys
import csv
import argparse
import django
django.setup()

from resistome.models import *

#gene,gene_symbol,sequence_name,scope,element_type,element_subtype,class,subclass,method,target_length,reference_sequence_length,pct_coverage_of_reference_sequence,pct_identity_to_reference_sequence,alignment_length,accession_of_closest_sequence,name_of_closest_sequence,hmm_id,hmm_description

# class AMRF(models.Model):
#     annotation = models.OneToOneField(
#         Annotation, on_delete=models.CASCADE,
#         related_name='amrf_set', related_query_name="amrf_set")
#     gene = models.CharField(unique=True, max_length=20)
#     gene_symbol = models.CharField(unique=True, max_length=20)
#     sequence_name = models.CharField(max_length=200, blank=True, null=True)
#     scope = models.CharField(unique=True, max_length=20)
#     element_type = models.CharField(unique=True, max_length=20)
#     element_subtype = models.CharField(unique=True, max_length=20)
#     amrf_class = models.CharField(unique=True, max_length=50)
#     amrf_subclass = models.CharField(unique=True, max_length=50)
#     method = models.CharField(unique=True, max_length=20)
#     target_length = models.PositiveIntegerField(null=True, blank=True)
#     reference_sequence_length = models.PositiveIntegerField(null=True, blank=True)
#     pct_coverage_of_reference_sequence = models.DecimalField(max_digits=5, decimal_places=2)
#     pct_identity_to_reference_sequence = models.DecimalField(max_digits=5, decimal_places=2)
#     alignment_length = models.PositiveIntegerField(null=True, blank=True)
#     accession_of_closest_sequence = models.CharField(unique=True, max_length=20)
#     name_of_closest_sequence = models.CharField(max_length=200, blank=True, null=True)
#     hmm_id = models.CharField(unique=True, max_length=20)
#     hmm_description = models.CharField(max_length=200, blank=True, null=True)

parser = argparse.ArgumentParser(
    description='Add records to inCREDBle AMRF table.')
parser.add_argument('csv_file', metavar='csv',
                    help='a CSV formatted file')
args = parser.parse_args()
with open(args.csv_file) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    for row in csvreader:
        if row['gene'] or None:
            try:
                annotation_obj = Annotation.objects.get(gene=row['gene'])
            except Annotation.DoesNotExist:
                annotation_obj = None
                sys.exit(row['gene'] + " doesn't exist. Please create it in Annotation table first")
            if annotation_obj:
                try:
                    amrf_obj = AMRF.objects.get(gene=row['gene'])
                except AMRF.DoesNotExist:
                    amrf_obj = None
                if amrf_obj:
                    ac, created = AmrfClass.objects.get_or_create(name=row['class'])
                    amrf_obj.annotation = annotation_obj
                    amrf_obj.gene = row['gene']
                    amrf_obj.gene_symbol = row['gene_symbol']
                    amrf_obj.sequence_name = row['sequence_name']
                    amrf_obj.scope = row['scope']
                    amrf_obj.element_type = row['element_type']
                    amrf_obj.element_subtype = row['element_subtype']
                    amrf_obj.amrfclass = ac
                    amrf_obj.amrf_subclass = row['subclass']
                    amrf_obj.method = row['method']
                    amrf_obj.target_length = row['target_length'] #shirt = 'white' if game_type == 'home' else 'green'
                    amrf_obj.reference_sequence_length = row['reference_sequence_length'] if row['reference_sequence_length'] != 'NA' else None
                    amrf_obj.pct_coverage_of_reference_sequence = row['pct_coverage_of_reference_sequence'] if row['pct_coverage_of_reference_sequence'] != 'NA' else None
                    amrf_obj.pct_identity_to_reference_sequence = row['pct_identity_to_reference_sequence'] if row['pct_identity_to_reference_sequence'] != 'NA' else None
                    amrf_obj.alignment_length = row['alignment_length'] if row['alignment_length'] != 'NA' else None
                    amrf_obj.accession_of_closest_sequence = row['accession_of_closest_sequence'] if row['accession_of_closest_sequence'] != 'NA' else None
                    amrf_obj.name_of_closest_sequence = row['name_of_closest_sequence'] if row['name_of_closest_sequence'] != 'NA' else None
                    amrf_obj.hmm_id = row['hmm_id'] if row['hmm_id'] != 'NA' else None
                    amrf_obj.hmm_description = row['hmm_description'] if row['hmm_description'] != 'NA' else None
                    print('saving amrf for ' + row['gene'])
                    amrf_obj.save()
                else:
                    obj = AMRF()
                    ac, created = AmrfClass.objects.get_or_create(name=row['class'])
                    obj.annotation = annotation_obj
                    obj.gene = row['gene']
                    obj.gene_symbol = row['gene_symbol']
                    obj.sequence_name = row['sequence_name']
                    obj.scope = row['scope']
                    obj.element_type = row['element_type']
                    obj.element_subtype = row['element_subtype']
                    obj.amrfclass = ac
                    obj.amrf_subclass = row['subclass']
                    obj.method = row['method']
                    obj.target_length = row['target_length']
                    obj.reference_sequence_length = row['reference_sequence_length'] if row['reference_sequence_length'] != 'NA' else None
                    obj.pct_coverage_of_reference_sequence = row['pct_coverage_of_reference_sequence'] if row['pct_coverage_of_reference_sequence'] != 'NA' else None
                    obj.pct_identity_to_reference_sequence = row['pct_identity_to_reference_sequence'] if row['pct_identity_to_reference_sequence'] != 'NA' else None
                    obj.alignment_length = row['alignment_length'] if row['alignment_length'] != 'NA' else None
                    obj.accession_of_closest_sequence = row['accession_of_closest_sequence'] if row['accession_of_closest_sequence'] != 'NA' else None
                    obj.name_of_closest_sequence = row['name_of_closest_sequence'] if row['name_of_closest_sequence'] != 'NA' else None
                    obj.hmm_id = row['hmm_id'] if row['hmm_id'] != 'NA' else None
                    obj.hmm_description = row['hmm_description'] if row['hmm_description'] != 'NA' else None
                    print('saving amrf for ' + row['gene'])
                    obj.save()

print("Finished OK")
