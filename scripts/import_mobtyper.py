
# Load initial Resistom data from excel into the database
import django
django.setup()

from resistome.models import *
import csv
import argparse


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
        if row['scaffold'] or None:
            print(row['scaffold'] or None)

            try:
                scaffold_obj = Scaffold.objects.get(
                    scaffold=row['scaffold'])
            except Scaffold.DoesNotExist:
                scaffold_obj = None
            if scaffold_obj:
                for rep in row['replicon_type'].split(','):
                    replicon = None
                    replicon, _ = RepliconType.objects.get_or_create(name=rep)
                    scaffold_obj.replicon_type.add(replicon)
                for rel in row['relaxase_type'].split(','):
                    relaxase = None
                    relaxase, _ = RelaxaseType.objects.get_or_create(name=rel)
                    scaffold_obj.relaxase_type.add(relaxase)
                scaffold_obj.mash_neighbor_cluster = row['mash_neighbor_cluster']
                scaffold_obj.save()

print("Finished OK")
