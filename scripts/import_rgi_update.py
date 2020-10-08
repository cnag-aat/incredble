import sys
import csv
import argparse
import django
django.setup()

from resistome.models import *

# class Rgi(models.Model):
#     annotation = models.OneToOneField(
#         Annotation, on_delete=models.CASCADE,
#         related_name='rgi_set', related_query_name="rgi_set")
#     gene = models.CharField(unique=True, max_length=20)
#     complete = models.NullBooleanField(blank=True, null=True)
#     start_type = models.CharField(max_length=4, blank=True, null=True, choices=RGI_START_TYPE)
#     rbs_motif = models.CharField(max_length=20, blank=True, null=True)
#     rbs_spacer = models.CharField(max_length=20, blank=True, null=True)
#     gc_cont = models.DecimalField(max_digits=5, decimal_places=3)
#     cut_off = models.CharField(max_length=7, blank=True, null=True, choices=CUT_OFF_TYPE)
#     pass_bitscore = models.PositiveIntegerField(null=True, blank=True)
#     best_hit_bitscore = models.DecimalField(max_digits=8, decimal_places=3)
#     best_hit_aro = models.TextField(blank=True, null=True)
#     best_identities = models.DecimalField(max_digits=7, decimal_places=3)
#     aro = models.PositiveIntegerField(null=True, blank=True)
#     model_type = models.CharField(max_length=40, blank=True, null=True)
#     snps_in_best_hit_aro = models.CharField(max_length=200, blank=True, null=True)
#     other_snps = models.CharField(max_length=200, blank=True, null=True)
#     drug_class = models.CharField(max_length=500, blank=True, null=True)
#     resistance_mechanism = models.CharField(max_length=500, blank=True, null=True)
#     amr_gene_family = models.CharField(max_length=500, blank=True, null=True)
#     predicted_dna = models.TextField(blank=True, null=True)
#     predicted_protein = models.TextField(blank=True, null=True)
#     card_protein_sequence = models.TextField(blank=True, null=True)
#     percentage_length_of_reference_sequence = models.DecimalField(max_digits=5, decimal_places=2)

#gene,complete,start_type,rbs_motif,rbs_spacer,gc_cont,cut_off,pass_bitscore,best_hit_bitscore,best_hit_aro,best_identities,aro,model_type,snps_in_best_hit_aro,other_snps,drug_class,resistance_mechanism,amr_gene_family,predicted_dna,predicted_protein,card_protein_sequence,percentage_length_of_reference_sequence

parser = argparse.ArgumentParser(
    description='Add records to inCREDBle RGI table.')
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
                    rgi_obj = Rgi.objects.get(gene=row['gene'])
                except Rgi.DoesNotExist:
                    rgi_obj = None
                if rgi_obj:
                    rgi_obj.annotation = annotation_obj
                    rgi_obj.gene = row['gene']
                    rgi_obj.complete = row['complete']
                    rgi_obj.start_type = row['start_type']
                    rgi_obj.rbs_motif = row['rbs_motif']
                    rgi_obj.rbs_spacer = row['rbs_spacer']
                    rgi_obj.gc_cont = row['gc_cont']
                    rgi_obj.cut_off = row['cut_off']
                    rgi_obj.pass_bitscore = row['pass_bitscore']
                    rgi_obj.best_hit_bitscore = row['best_hit_bitscore']
                    rgi_obj.best_hit_aro = row['best_hit_aro']
                    rgi_obj.best_identities = row['best_identities']
                    rgi_obj.aro = row['aro']
                    rgi_obj.model_type = row['model_type']
                    rgi_obj.snps_in_best_hit_aro = row['snps_in_best_hit_aro']
                    rgi_obj.other_snps = row['other_snps']
                    rgi_obj.drug_class = row['drug_class']
                    rgi_obj.resistance_mechanism = row['resistance_mechanism']
                    rgi_obj.amr_gene_family = row['amr_gene_family']
                    rgi_obj.predicted_dna = row['predicted_dna']
                    rgi_obj.predicted_protein = row['predicted_protein']
                    rgi_obj.card_protein_sequence = row['card_protein_sequence']
                    rgi_obj.percentage_length_of_reference_sequence = row['percentage_length_of_reference_sequence']
                    print('saving rgi for ' + row['gene'])
                    rgi_obj.save()
                else:
                    obj = Rgi()
                    obj.annotation = annotation_obj
                    obj.gene = row['gene']
                    obj.complete = row['complete']
                    obj.start_type = row['start_type']
                    obj.rbs_motif = row['rbs_motif']
                    obj.rbs_spacer = row['rbs_spacer']
                    obj.gc_cont = row['gc_cont']
                    obj.cut_off = row['cut_off']
                    obj.pass_bitscore = row['pass_bitscore']
                    obj.best_hit_bitscore = row['best_hit_bitscore']
                    obj.best_hit_aro = row['best_hit_aro']
                    obj.best_identities = row['best_identities']
                    obj.aro = row['aro']
                    obj.model_type = row['model_type']
                    obj.snps_in_best_hit_aro = row['snps_in_best_hit_aro']
                    obj.other_snps = row['other_snps']
                    obj.drug_class = row['drug_class']
                    obj.resistance_mechanism = row['resistance_mechanism']
                    obj.amr_gene_family = row['amr_gene_family']
                    obj.predicted_dna = row['predicted_dna']
                    obj.predicted_protein = row['predicted_protein']
                    obj.card_protein_sequence = row['card_protein_sequence']
                    obj.percentage_length_of_reference_sequence = row['percentage_length_of_reference_sequence']
                    print('saving rgi for ' + row['gene'])
                    obj.save()


print("Finished OK")
