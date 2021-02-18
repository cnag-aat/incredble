import sys
import csv
import argparse
import scipy.stats as stats
import django
django.setup()
from resistome.models import *

# argument: Ecoli_genes_classified_prefixed.txt
parser = argparse.ArgumentParser(
    description='Add roary groups to inCREDBle RoaryGroup table.')
parser.add_argument('sequence_type', metavar='ST',
                    help='the ST to test for enrichment/depletion')
parser.add_argument('species', metavar='species',
                    help='the species (Klebsiella pneumoniae, Enterobacter cloacae complex, Escherichia coli)')
args = parser.parse_args()

try:
    speciesobj = Species.objects.get(name=args.species)
except Species.DoesNotExist:
    speciesobj = None

test_total = Sample.objects.filter(species=speciesobj,assembly__mlst__st=args.sequence_type).count()
control_total = Sample.objects.filter(species=speciesobj).exclude(assembly__mlst__st=args.sequence_type).count()

roary_groups = RoaryGroup.objects.filter(species=speciesobj)
myTuple = ('ST','roary_gene', 'ST_positive','ST_total','ST_proportion','rest_positive','rest_total','rest_proportion','Fisher_exact_pvalue_two-sided','Fisher_exact_pvalue_greater','Fisher_exact_pvalue_less')
x = "\t".join(myTuple)
print(x)
for rg in roary_groups:
    test_pos = Annotation.objects.filter(roary_gene=rg.roary_gene,scaffold__assembly__mlst__st=args.sequence_type).values('scaffold__assembly').distinct().count()
    control_pos = Annotation.objects.filter(roary_gene=rg.roary_gene).exclude(scaffold__assembly__mlst__st=args.sequence_type).values('scaffold__assembly').distinct().count()
    test_neg = test_total - test_pos
    control_neg = control_total - control_pos
    oddsratio_greater, pvalue_greater = stats.fisher_exact([[test_pos, control_pos], [test_neg, control_neg]],alternative='greater')
    oddsratio_less, pvalue_less = stats.fisher_exact([[test_pos, control_pos], [test_neg, control_neg]],alternative='less')
    oddsratio, pvalue = stats.fisher_exact([[test_pos, control_pos], [test_neg, control_neg]],alternative='two-sided')
    myTuple = (args.sequence_type,rg.roary_gene, str(test_pos),str(test_total),str(test_pos/test_total),str(control_pos),str(control_total),str(control_pos/control_total),str(pvalue),str(pvalue_greater), str(pvalue_less))
    x = "\t".join(myTuple)
    print(x)
