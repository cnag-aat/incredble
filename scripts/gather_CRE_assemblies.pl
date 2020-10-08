#!/usr/bin/env perl
use strict;

my $list = $ARGV[0];

dataTable($list);

#for i in `cut -f 1 new_data.rotated.v1.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v1/$i/02_Assembly/tables/$i.v1.assembly.tbl >> assembly.tbl; done
#sed -i '2,${/^assembly/d}' assembly.tbl
#for i in `cut -f 1 new_data.rotated.v1.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v1/$i/02_Assembly/tables/$i.v1.scaffolds.tbl >> scaffold.tbl; done
#sed -i '2,${/^assembly/d}' scaffold.tbl
#for i in `cut -f 1 new_data.rotated.v1.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v1/$i/02_Assembly/tables/$i.v1.mlst.tbl >> mlst.tbl; done
#sed -i '2,${/^assembly/d}' mlst.tbl
#for i in `cut -f 1 new_data.rotated.v1.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v1/$i/02_Assembly/centrifuge/$i.v1.tbl >> centrifuge.tbl; done
#sed -i '2,${/^scaffold/d}' centrifuge.tbl
#for i in `cut -f 1 new_data.rotated.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v5/$i/03_Annotation/*annot.tbl >> annotation.tbl; done
#sed -i '2,${/^scaffold/d}' annotation.tbl
#for i in `cut -f 1 new_data.rotated.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v5/$i/03_Annotation/*.amrfinder.tsv >> armf.tbl; done
#sed -i '2,${/^gene/d}' amrf.tbl
#for i in `cut -f 1 new_data.rotated.txt`; do echo $i; cat /scratch/devel/talioto/denovo_assemblies/CRE/v5/$i/03_Annotation/*.rgi.tbl >> rgi.tbl; done
#sed -i '2,${/^gene/d}' rgi.tbl




sub dataTable {
    my $list = shift;
    open( IN, "<$list" );
    `mkdir -p assemblyFASTA`;
    `mkdir -p annotationDATA`;
    open( DATA, ">datafiles.txt" );
    print DATA join( "\t",
        qw(assembly assembly_fasta annotation_protein_fasta annotation_transcript_fasta annotation_gff)
      ),
      "\n";

    while ( my $line = <IN> ) {
        next if $line =~ m/Genome/;
        print STDERR "processing $line";
        chomp $line;
        my ( $barcode, $version ) = split "\t", $line;
        my $dir = "/scratch/devel/talioto/denovo_assemblies/CRE/$version/$barcode";
        if ( !-e "$dir/02_Assembly/$barcode.$version.assembly.fasta" ) {
            print STDERR "$dir/02_Assembly/$barcode.$version.assembly.fasta does not exist. Skipping..."
              and next;
        }
        `cp $dir/02_Assembly/$barcode.$version.assembly.fasta assemblyFASTA/$barcode.$version.assembly.fasta`;
        my $annotation = $barcode . $version;
        `cp $dir/03_Annotation/$annotation.annot.4jb.gff3 annotationDATA/$barcode.$version.annotation.gff3`;
        `CDS2seqCRE.pl -f assemblyFASTA/$barcode.$version.assembly.fasta -i annotationDATA/$barcode.$version.annotation.gff3`;
        `mv $barcode.$version.annotation.pep.fa annotationDATA/$barcode.$version.protein.fasta`;
        `mv $barcode.$version.annotation.cds.fa annotationDATA/$barcode.$version.CDS.fasta`;
        `gzip assemblyFASTA/$barcode.$version.assembly.fasta`;
        `gzip annotationDATA/$barcode.$version.annotation.gff3`;
        `gzip annotationDATA/$barcode.$version.protein.fasta`;
        `gzip annotationDATA/$barcode.$version.CDS.fasta`;
        my $pa       = "/home/talioto/datafiles/assemblyFASTA";
        my $pan      = "/home/talioto/datafiles/annotationDATA";
        my $ass      = $barcode . "_" . $version;
        my $assfasta = "$barcode.$version.assembly.fasta.gz";
        my $apa      = "$barcode.$version.protein.fasta.gz";
        my $atf      = "$barcode.$version.CDS.fasta.gz";
        my $gff      = "$barcode.$version.annotation.gff3.gz";
        print DATA join( "\t",
            ( $ass, "$pa/$assfasta", "$pan/$apa", "$pan/$atf", "$pan/$gff" ) ),
          "\n";
    }
}
