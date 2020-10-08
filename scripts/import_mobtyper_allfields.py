
# Load initial Resistom data from excel into the database
import django
django.setup()

from resistome.models import *
import csv
import argparse
from pathlib import Path


#EXAMPLE
#file_id	num_contigs	total_length	gc	rep_type(s)	rep_type_accession(s)	relaxase_type(s)	relaxase_type_accession(s)	mpf_type	mpf_type_accession(s)   orit_type(s)	orit_accession(s)	PredictedMobility	mash_nearest_neighbor	mash_neighbor_distance	mash_neighbor_cluster
#AI2643_v1_c2.fa	1	227132	52.360741771304795	IncFIB,IncFII	000107__CP014778_00094,000124__KP125893_00142	MOBF	NC_021231_00058	MPF_F	NC_021502_00150,NC_019155_00032,NC_019165_00034,NC_021654_00016,NC_011281_00082,NC_022609_00081,NC_014312_00128,NC_021502_00131,NC_019389_00068,NC_023332_00154,NC_014312_00118,NC_014312_00116	-	-	Conjugative	KY271404	0.00243596	770


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
        if row['file_id'] or None:
            scaffold_name = Path(row['file_id']).stem
            print(scaffold_name or None)

            try:
                scaffold_obj = Scaffold.objects.get(
                    scaffold=scaffold_name)
            except Scaffold.DoesNotExist:
                scaffold_obj = None
            if scaffold_obj:
                scaffold_obj.gc = row['gc']
                for rep in row['rep_type(s)'].split(','):
                    replicon = None
                    replicon, _ = RepliconType.objects.get_or_create(name=rep)
                    scaffold_obj.replicon_type.add(replicon)
                for repa in row['rep_type_accession(s)'].split(','):
                    replicon_accession = None
                    replicon_accession, _ = RepliconTypeAccession.objects.get_or_create(name=repa)
                    scaffold_obj.replicon_type_accession.add(replicon_accession)
                for rel in row['relaxase_type(s)'].split(','):
                    relaxase = None
                    relaxase, _ = RelaxaseType.objects.get_or_create(name=rel)
                    scaffold_obj.relaxase_type.add(relaxase)
                for rela in row['relaxase_type_accession(s)'].split(','):
                    relaxase_accession = None
                    relaxase_accession, _ = RelaxaseTypeAccession.objects.get_or_create(name=rela)
                    scaffold_obj.relaxase_type_accession.add(relaxase_accession)
                if row['mpf_type']:
                    mpf_type, _ = MpfType.objects.get_or_create(
                        name=row['mpf_type'],
                    )
                    scaffold_obj.mpf_type = mpf_type

                for mpfa in row['mpf_type_accession(s)'].split(','):
                    mpf_type_accession = None
                    mpf_type_accession, _ = MpfTypeAccession.objects.get_or_create(name=mpfa)
                    scaffold_obj.mpf_type_accession.add(mpf_type_accession)
                for ori in row['orit_type(s)'].split(','):
                    orit = None
                    orit, _ = OritType.objects.get_or_create(name=ori)
                    scaffold_obj.orit_type.add(orit)
                for orita in row['orit_accession(s)'].split(','):
                    orit_accession = None
                    orit_accession, _ = OritAccession.objects.get_or_create(name=orita)
                    scaffold_obj.orit_accession.add(orit_accession)
                if row['PredictedMobility']:
                    predicted_mobility, _ = PredictedMobility.objects.get_or_create(
                        name=row['PredictedMobility'],
                    )
                    scaffold_obj.predicted_mobility = predicted_mobility

                scaffold_obj.mash_nearest_neighbor = row['mash_nearest_neighbor']
                scaffold_obj.mash_neighbor_distance = row['mash_neighbor_distance']
                scaffold_obj.mash_neighbor_cluster = row['mash_neighbor_cluster']
                scaffold_obj.save()

print("Finished OK")
