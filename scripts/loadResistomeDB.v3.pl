#!/usr/bin/env perl
use lib '/home/devel/talioto/perl5/lib/perl5/';
use REST::Client;
use MIME::Base64;
use JSON::PP;
use Data::Dumper;
use Getopt::Long;
#my $path='/scratch/devel/talioto/denovo_assemblies/CRE';
my $path='/Users/talioto/mount/scratch/denovo_assemblies/CRE/';

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

my $usage = "usage: $0 -bc <sample_barcode> -v <assembly_version>\n";
GetOptions(
	   'bc:s'      => \$bc,
	   'v:s'  => \$version
	  );
die $usage if !($bc && $version);
my $updateAnnotation = 0;
my $assembly_data;
my $mlst_data;
my $speciesverification_data;
my $scaffolds_data;
my $annotation_data;
my $rgi_data;

die "No assembly data" unless $assembly_data=(loadTbl("$path/$version/$bc/02_Assembly/tables/$bc.$version.assembly.tbl",$assembly_data));
die "No mlst data" unless $mlst_data=(loadTbl("$path/$version/$bc/02_Assembly/tables/$bc.$version.mlst.tbl",$mlst_data));
die "No species verification data" unless $speciesverification_data=(loadTbl("$path/$version/$bc/01_preprocessing/$bc.species_verification.out",$speciesverification_data));
die "No scaffolds data" unless $scaffolds_data=(loadTbl("$path/$version/$bc/02_Assembly/tables/$bc.$version.scaffolds.tbl",$scaffolds_data));
die "No annotation data" unless $annotation_data=(loadTbl("$path/$version/$bc/03_Annotation/$bc"."$version.annot.tbl",$annotation_data));
die "No rgi data" unless $rgi_data=(loadTbl("$path/$version/$bc/03_Annotation/$bc"."$version.rgi.tbl",$rgi_data));

print STDERR "Parsed data files... ready to add to ResistomeDB.\n";
print STDERR "Adding assembly data...\n"; #print STDERR Data::Dumper->Dump($assembly_data),"\n" and exit;
die "Failed adding assembly!\n" unless add_assembly();
print STDERR "Adding mlst data...\n";
die "Failed adding mlst!\n" unless add_mlst();
print STDERR "Adding species verification data...\n";
die "Failed adding species verification!\n" unless add_speciesverification();
print STDERR "Adding scaffolds data...\n";
die "Failed adding scaffolds!\n" unless add_scaffolds();
print STDERR "Adding annotation data...\n";
die "Failed adding annotation!\n" unless add_annotation();
print STDERR "Adding RGI annotation data...\n";
die "Failed adding RGI annotation!\n" unless add_rgi();


sub add_assembly{
  my $rounded = sprintf("%.2f",$assembly_data->[0]->{circularity_ratio});
  $assembly_data->[0]->{circularity_ratio} = $rounded;
  $client->GET("$url/assembly/?assembly=". $assembly_data->[0]->{assembly});
  my $response1 = decode_json $client->responseContent();
  print STDERR $assembly_data->[0]->{sample},"\n";
  $client->GET("$url/sample/?barcode=". $assembly_data->[0]->{sample});
  my $response2 = decode_json $client->responseContent();
  if ($response2->{count} == 1) {
    $assembly_data->[0]->{sample}=$response2->{results}->[0]->{url};
  } else {
    print STDERR "Sample $bc could not be found in the samples table. Please add sample first.\n",encode_json($response2),"\n";
    return;
  }
  if ($response1->{count} == 1) {
    print STDERR $assembly_data->[0]->{assembly}," is already in database:\n",encode_json($response1),"\nWill update with new data..\n";
    my $insert = encode_json $assembly_data->[0];
    my $record_to_update = $response1->{results}->[0]->{url}; #the URL;
    print STDERR "Deleting $record_to_update\n"; # and exit;
    $client->DELETE($record_to_update);
    print STDERR "Deleted record:\n",$client->responseContent(),"\n";
    my $insert = encode_json $assembly_data->[0];
    $client->POST("$url/assembly/", $insert);
    print STDERR "Inserted new record:\n",$client->responseContent(),"\n";
    return 1;
  } elsif ($response1->{count} > 1) {
    print STDERR "Multiple records match ", $assembly_data->[0]->{assembly},":\n";
    foreach my $r (@{$response1->{results}}) {
      print STDERR $r->{url},"\n";
      die "Exiting.\n";
    }
  } else {
    my $insert = encode_json $assembly_data->[0];
    $client->POST("$url/assembly/", $insert);
    print STDERR "Inserted:\n",$client->responseContent(),"\n";
    return 1;
  }
}

sub add_mlst{
  $client->GET("$url/assembly/?assembly=". $mlst_data->[0]->{assembly});
  my $response2 = decode_json $client->responseContent();
  if ($response2->{count} == 1) {
    $mlst_data->[0]->{assembly}=$response2->{results}->[0]->{url};
  } else {
    print STDERR $mlst_data->[0]->{assembly}," could not be found in the assembly table. Please add assembly first.\n",encode_json($response2),"\n";
    return;
  }
  if ($mlst_data->[0]->{st} eq '-') {
    $mlst_data->[0]->{st}=0;
  }
  my $insert = encode_json $mlst_data->[0];
  $client->POST("$url/mlst/", $insert);
  print STDERR $client->responseContent(),"\n";
  return 1;
}

sub add_speciesverification{
  $client->GET("$url/sample/?barcode=$bc");
  my $response2 = decode_json $client->responseContent();
  if ($response2->{count} == 1) {
    $speciesverification_data->[0]->{sample}=$response2->{results}->[0]->{url};
  } else {
    print STDERR "Sample $bc could not be found in the samples table. Please add sample first.\n",encode_json($response2),"\n";
    return;
  }
  my $insert = encode_json $speciesverification_data->[0];
  $client->POST("$url/speciesverification/", $insert);
  print STDERR $client->responseContent(),"\n";
  return 1;
}

sub add_scaffolds{
  my $assemblyURL=0;
  my $sampleURL=0;
  $client->GET("$url/assembly/?assembly=". $scaffolds_data->[0]->{assembly});
  my $response2 = decode_json $client->responseContent();
  if ($response2->{count} == 1) {
    $assemblyURL=$response2->{results}->[0]->{url};
  } else {
    print STDERR $scaffolds_data->[0]->{assembly}," could not be found in the assembly table. Please add assembly first.\n",encode_json($response2),"\n";
    return 0;
  }

  $client->GET("$url/sample/?barcode=". $bc);
  my $responseSample = decode_json $client->responseContent();
  if ($responseSample->{count} == 1) {
    $sampleURL=$responseSample->{results}->[0]->{url};
  } else {
    print STDERR "Sample $bc could not be found in the samples table. Please add sample first.\n",encode_json($responseSample),"\n";
    return 0;
  }
  foreach my $record (@$scaffolds_data) {
    $record->{assembly}=$assemblyURL;
    $record->{sample}=$sampleURL;
    $client->GET("$url/scaffold/?scaffold=". $record->{scaffold});
    my $response1 = decode_json $client->responseContent();
    if ($response1->{count} == 1) {
      print STDERR $record->{scaffold}," is already in database:\n",encode_json($response1),"\nRelying on cascade resulting from assembly record deletion. Delete assembly record first to remove scaffold records.\n";
      # print STDERR $record->{scaffold}," is already in database:\n",encode_json($response1),"\nWill update with new data..\n";
      # my $insert = encode_json $record;
      # my  $record_to_update = $response1->{results}->[0]->{url}; #the URL;
      # print STDERR "Updating $record_to_update\n"; # and exit;
      # $client->PATCH($record_to_update,$insert);
      # print STDERR "Updated record:\n",$client->responseContent(),"\n";
    } elsif ($response1->{count} > 1) {
      print STDERR "Multiple records match ", $record->{scaffold},":\n";
      foreach my $r (@{$response1->{results}}) {
	print STDERR $r->{url},"\n";
	die "Exiting.\n";
      }
    } else {

      my $insert = encode_json $record;
      $client->POST("$url/scaffold/", $insert);
      print STDERR "Inserted:\n",$client->responseContent(),"\n";
    }
  }
  return 1;
}

sub add_annotation{
  my %scaffoldsURL=();	 #store seen scaffold URLs to minimize lookups
  my @modified=();
  my $count=0;
  foreach my $record (@$annotation_data) {
    $count++;
    my $scaffoldURL=0;
    next if $record->{rgi} ne 'Yes';
    if (exists($scaffoldURL{$record->{scaffold}})) {
      $scaffoldURL = $scaffoldURL{$record->{scaffold}};
      $record->{scaffold}=$scaffoldURL;
    } else {
      $client->GET("$url/scaffold/?scaffold=". $record->{scaffold});
      my $responseScaffold = decode_json $client->responseContent();
      if ($responseScaffold->{count} == 1) {
	$scaffoldURL=$responseScaffold->{results}->[0]->{url};
      } else {
	print STDERR $record->{scaffold}," could not be found in the scaffold table. Please add scaffold first.\n",encode_json($responseScaffold),"\n";
	return 0;
      }
      $scaffoldURL{$record->{scaffold}}=$scaffoldURL;
      $record->{scaffold}=$scaffoldURL;
    }
    if ($updateAnnotation) { #not going to update. need to delete assembly to cascade deletion of scaffolds and annotation records first.
      # $client->GET("$url/annotation/?gene=". $record->{gene});
      # my $response1 = decode_json $client->responseContent();
      # if ($response1->{count} == 1) {
      # 	print STDERR $record->{gene}," is already in database:\n",encode_json($response1),"\nWill update with new data..\n";
      # 	my $insert = encode_json $record;
      # 	my $record_to_update = $response1->{results}->[0]->{url}; #the URL;
      # 	print STDERR "Updating $record_to_update\n"; # and exit;
      # 	$client->PATCH($record_to_update,$insert);
      # 	print STDERR "Updated record:\n",$client->responseContent(),"\n";
      # } elsif ($response1->{count} > 1) {
      # 	print STDERR "Multiple records match ", $record->{gene},":\n";
      # 	foreach my $r (@{$response1->{results}}) {
      # 	  print STDERR $r->{url},"\n";
      # 	  die "Exiting.\n";
      # 	}
      # } else {

      # 	#my $insert = encode_json $record;
      # 	#$client->POST("$url/annotation/", $insert);
      # 	push @modified, $record;
      # 	#print STDERR "Inserted:\n",$client->responseContent(),"\n";
      # }
    } else {
      #my $insert = encode_json $record;
      #$client->POST("$url/annotation/", $insert);
      push @modified, $record;
      #print STDERR "Inserted:\n",$client->responseContent(),"\n";
    }
    if ($count % 10 == 0) {	#only add batches of 100

      if (scalar @modified > 0) {
	print STDERR "Inserting annotation records in bulk...\n";
	my $insert = encode_json \@modified;
	print STDERR "$insert\n\n";
	$client->POST("$url/annotation/", $insert);
	print STDERR $client->responseContent(),"\n";
	@modified=();
      }
    }
  }
  if (scalar @modified > 0) {
    print STDERR "Inserting annotation records in bulk...\n";
    my $insert = encode_json \@modified;
    $client->POST("$url/annotation/", $insert);
    print STDERR $client->responseContent(),"\n";
  }
  return 1;
}

sub add_rgi{
  my @modified=();
  foreach my $record (@$rgi_data) {
    my $annotationURL=0;
    $client->GET("$url/annotation/?gene=". $record->{gene});
    my $responseAnnotation= decode_json $client->responseContent();
    if ($responseAnnotation->{count} == 1) {
      $annotationURL=$responseAnnotation->{results}->[0]->{url};
    } else {
      print STDERR $record->{gene}," could not be found in the annotation table. Please add gene annotations first.\n",encode_json($responseAnnotation),"\n";
      return 0;
    }
    $record->{cut_off}=lc($record->{cut_off});
    my $rounded = sprintf("%.2f",$record->{best_hit_bitscore});
    $record->{best_hit_bitscore} = $rounded;
    $record->{annotation}=$annotationURL;
    $client->GET("$url/rgi/?gene=". $record->{gene});
    my $response1 = decode_json $client->responseContent();
    if ($response1->{count} == 1) {
      if ($updateAnnotation) { #again, will not updaate, rely on cascading delete starting with assembly record deletion
	# print STDERR $record->{gene}," is already in database:\n",encode_json($response1),"\nWill update with new data..\n";
	# my $insert = encode_json $record;
	# my $record_to_update = $response1->{results}->[0]->{url}; #the URL;
	# print STDERR "Updating $record_to_update\n"; # and exit;
	# $client->PATCH($record_to_update,$insert);
	# print STDERR "Updated record:\n",$client->responseContent(),"\n";
      }
    } elsif ($response1->{count} > 1) {
      print STDERR "Multiple records match ", $record->{gene},":\n";
      foreach my $r (@{$response1->{results}}) {
	print STDERR $r->{url},"\n";
	die "Exiting.\n";
      }
    } else {
      push @modified, $record;
      # my $insert = encode_json $record;
      # $client->POST("$url/rgi/", $insert);
      # print STDERR "Inserted:\n",$client->responseContent(),"\n";

    }
  }
  if (scalar @modified > 0) {
    my $insert = encode_json \@modified;
    $client->POST("$url/rgi/", $insert);
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
