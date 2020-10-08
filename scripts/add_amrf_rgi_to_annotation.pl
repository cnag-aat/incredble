#!/usr/bin/env perl
use strict;


#dataTable($list);

#for i in `cut -f 1 new_data.rotated.v1.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v1/$i/02_Assembly/tables/$i.v1.assembly.tbl >> assembly.tbl; done
#sed -i '2,${/^assembly/d}' assembly.tbl
#sed -i '2,${s/v1/v5/}' assembly.tbl
#for i in `cut -f 1 new_data.rotated.v1.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v1/$i/02_Assembly/tables/$i.v1.scaffolds.tbl >> scaffold.tbl; done
#sed -i '2,${/^assembly/d}' scaffold.tbl
#sed -i '2,${s/v1/v5/}' scaffold.tbl
#for i in `cut -f 1 new_data.rotated.v1.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v1/$i/02_Assembly/tables/$i.v1.mlst.tbl >> mlst.tbl; done
#sed -i '2,${/^assembly/d}' mlst.tbl
#sed -i '2,${s/v1/v5/}' mlst.tbl
#for i in `cut -f 1 new_data.rotated.v1.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v1/$i/02_Assembly/centrifuge/$i.v1.tbl >> centrifuge.tbl; done
#sed -i '2,${/^scaffold/d}' centrifuge.tbl
#sed -i '2,${s/v1/v5/}' centrifuge.tbl
#for i in `cut -f 1 new_data.rotated.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v5/$i/03_Annotation/*annot.tbl >> annotation.tbl; done
#sed -i '2,${/^scaffold/d}' annotation.tbl
#for i in `cut -f 1 new_data.rotated.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v5/$i/03_Annotation/*.amrfinder.tsv >> armf.tbl; done
#sed -i '2,${/^gene/d}' amrf.tbl
#for i in `cut -f 1 new_data.rotated.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v5/$i/03_Annotation/*.rgi.tbl >> rgi.tbl; done
#sed -i '2,${/^gene/d}' rgi.tbl

my %rgigenes={};
my %amrfgenes={};
open(ANN, "<annotation.tbl") or die "Couldn't open annotation.tbl!\n";
open(RGI, "<rgi.tbl") or die "Couldn't open rgi.tbl!\n";
open(AMRF, "<amrf.tbl") or die "Couldn't open amrf.tbl!\n";
open(UPDATE, ">annotation_updated_rgi_amrf.tbl") or die "Couldn't open annotation_updated_rgi_amrf.tbl for writing!\n";;

my $skipheader = <AMRF>;
while(<AMRF>){
  my @f = split("\t",$_);
  $amrfgenes{$f[0]}=1;
}
close AMRF;

open(RGI, "<rgi.tbl");
$skipheader = <RGI>;
while(<RGI>){
  my @f = split("\t",$_);
  $rgigenes{$f[0]}=1;
}
close RGI;

my $header = <ANN>;
chomp $header;
my @hf = split("\t",$header);
if (scalar @hf < 12){push @hf, 'AMRF';}

print UPDATE join("\t",@hf),"\n";
while(<ANN>){
  chomp;
  my @f = split("\t",$_);
  if (scalar @f < 12){push @f, 'No';}
  if (exists $rgigenes{$f[4]}){$f[6]='Yes';}else{$f[6]='No';}
  if (exists $amrfgenes{$f[4]}){$f[12]='Yes';}else{$f[12]='No';}
  print UPDATE join("\t",@f),"\n";
}
close ANN;
close UPDATE;
