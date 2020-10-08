#add sample #already done
#import_mlst.py
#add assembly
#add scaffolds

gather_CRE_assemblies.pl #run this on cluster, then copy data to server
cd /home/www/resistome.cnag.cat/incredible/import_scripts_20200812
python3 ./import_assembly.py /home/talioto/tables/assembly.tbl
sed 's/protein.fasta/protein.fa/g;' /home/talioto/tables/datafiles.tbl | sed 's/CDS.fasta/CDS.fa/g;' > /home/talioto/tables/datafiles_fix.tbl
python3 ./importDataFiles.py /home/talioto/tables/datafiles_fix.tbl
for i in `cat /home/talioto/tables/new_data.rotated.txt|cut -f 1|grep -v Gen`; do cp /home/www/resistome.cnag.cat/incredible/deployment/data/img/$i.v1.assembly.png /home/talioto/datafiles/images/$i.v5.assembly.png; done
for i in `cat /home/talioto/tables/new_data.rotated.txt|cut -f 1|grep -v Gen`; do echo -e "$i""_v5""\t/home/talioto/datafiles/images/$i.v5.assembly.png" >> /home/talioto/tables/imageFiles.tbl; done
python3 ./importImageFiles.py /home/talioto/tables/imageFiles.tbl
python3 ./import_scaffolds_replace.py /home/talioto/tables/scaffold.tbl
python3 ./import_centrifuge.py /home/talioto/tables/centrifuge.tbl
import_mobtyper.py
python3 ./import_annotation_allgenes.py /home/talioto/tables/annotation_updated_rgi_amrf.tbl
import_annotation_orthogroups.py #optional and can be done last
python3 ./import_amrf.py /home/talioto/tables/amrf.tbl
python3 ./import_rgi_update.py /home/talioto/tables/rgi.tbl
