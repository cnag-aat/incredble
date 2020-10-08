#!/usr/bin/env perl
use lib '/home/devel/talioto/perl5/lib/perl5/';
use REST::Client;
use MIME::Base64;
use JSON::PP;
use Data::Dumper;
use Getopt::Long;
#my $path='/scratch/devel/talioto/denovo_assemblies/CRE';
my $path='/Users/talioto/Documents/projects/CRE/server-dev/incredible/data';

my $version ='v1';
my $bc = 0;
my $client = REST::Client->new();
$client->addHeader('Content-Type', 'application/json');
$client->addHeader('charset', 'UTF-8');
$client->addHeader('Accept', 'application/json');
$client->addHeader('Authorization' => 'Basic '.encode_base64('test:pz37G2n7'));
#my $url="http://172.16.10.45/resistome/api";
my $url="http://127.0.0.1:8000/api";
#### EXAMPLE TABLES ####
#v1/$bc/01_preprocessing/$bc.species_verification.out
#Illumina_sp	ONT_sp	LIMS_sp	Seq_Agreement	Verified

#v1/AH0311/02_Assembly/tables/AH0311.v1.assembly.tbl
#sample_barcode	assembly	total_scaffolds	circular_scaffolds	circularity_ratio	scaffolds_2kb_or_shorter	assembly_length	max_scaffold_length	assembler
  
#v1/AH0311/02_Assembly/tables/AH0311.v1.scaffolds.tbl
#assembly	scaffold	scaffold_length	depth	circular
  
#v1/AH0311/02_Assembly/tables/AH0311.v1.mlst.tbl
#assembly	PubMLST	ST	alleles
  
#v1/AH0311/03_Annotation/AH0311v1.annot.tbl
#scaffold	start	end	orientation	gene	gene_name	rgi	ec_number	product	inference	jbrowse_link	protein_sequence

#v1/AH0311/03_Annotation/AH0311v1.rgi.tbl
#gene	complete	start_type	rbs_motif	rbs_spacer	gc_cont	cut_off	pass_bitscore	best_hit_bitscore	best_hit_aro	best_identities	aro	model_type	snps_in_best_hit_aro	other_snps	drug_class	resistance_mechanism	amr_gene_family	predicted_dna	predicted_protein	card_protein_sequence	percentage_length_of_reference_sequence

my $usage = "usage: $0 -tbl <datafiles.tbl>\n";
my $tbl = "$path/datafiles.tbl";
GetOptions(
	   'tbl:s'      => \$tbl
	  );
die $usage if !($tbl);
my $updateAnnotation = 0;
my $data_files;

die "data files" unless $data_files=(loadTbl($tbl,$data_files));

print STDERR "Parsed data files... ready to add to ResistomeDB.\n";
print STDERR "Adding data files...\n"; #print STDERR Data::Dumper->Dump($assembly_data),"\n" and exit;
die "Failed adding data files!\n" unless add_data_files();

sub add_data_files{
  my %assemblyURL=();	 #store seen scaffold URLs to minimize lookups
  foreach my $record (@$data_files) {
    if (exists($assemblyURL{$record->{assembly}})) {
      $assemblyURL = $assemblyURL{$record->{assembly}};
      $record->{assembly}=$assemblyURL;
    } else {
      $client->GET("$url/assembly/?assembly=". $record->{assembly});
      my $responseAssembly = decode_json $client->responseContent();
      if ($responseAssembly->{count} == 1) {
	$assemblyURL=$responseAssembly->{results}->[0]->{url};
      } else {
	print STDERR $record->{assembly}," could not be found in the assembly table. Please add assembly first.\n",encode_json($responseAssembly),"\n";
	return 0;
      }
      $assemblyURL{$record->{assembly}}=$assemblyURL;
      $record->{assembly}=$assemblyURL;
    }
   
    print STDERR "Inserting data file record...\n";
    my $insert = encode_json $record;
    print STDERR "$insert\n\n";
    $client->POST("$url/datafiles/", $insert);
    print STDERR $client->responseContent(),"\n";
  }
  return 1;
}

sub loadTbl {
  my $file =  shift;
  my $arrayref = shift;
  open TAB, "<$file" or die "couldn't open $file\n";
  my $head = <TAB>;
  chomp $head;
  my @h = split "\t",$head;
  my $count=0;
  while (my $record = <TAB>) {
    chomp $record;
    my @r = split "\t",$record;
  
    for (my $i=0;$i<@h; $i++) {
      $h[$i]=~s/sample_barcode/sample/; #fix some field names on the fly. later we should fix the flatfiles.
      $arrayref->[$count]->{lc($h[$i])}=($r[$i]);
    }
    $count++;
  }
  close TAB;
  return $count?$arrayref:0;
}
