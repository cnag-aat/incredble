#!/bin/env perl
print "assembly,assembly_fasta,annotation_protein_fasta,annotation_transcript_fasta,annotation_gff\n";
while (<>){
	chomp;
	my($barcode, $version)=split;
  	my $pa="/home/talioto/datafiles/assemblyFASTA";
  	my $pan="/home/talioto/datafiles/annotationDATA";
  	my $ass=$barcode."_".$version;
  	my $assfasta="$barcode.$version.assembly.fasta.gz";
  	my $apa="$barcode.$version.protein.fasta.gz";
  	my $atf="$barcode.$version.CDS.fasta.gz";
  	my $gff="$barcode.$version.annotation.gff3.gz";
  	print  "$ass,$pa/$assfasta,$pan/$apa,$pan/$afa,$pan/$atf,$pan/$gff\n";
}
