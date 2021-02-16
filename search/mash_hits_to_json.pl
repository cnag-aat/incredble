#!/usr/bin/env perl
use strict;
#use Math::BigFloat;
#Math::BigFloat->precision(-6);
use JSON::PP;
my $json = JSON::PP->new;
$json = $json->canonical->pretty;
my %sample_score=();
my %topscaffolds =();
my $top_sample_score = 0; #Math::BigFloat->new(0.000000);
my $top_sample = 'none';
# AH0325_v1_c1	AI2801_v1_c1	0.0114865	0	647/1000
# AH0325_v1_c2	AI2801_v1_c1	1	1	0/1000
# AH0325_v1_c3	AI2801_v1_c1	1	1	0/1000
# AH0325_v1_c4	AI2801_v1_c1	1	1	0/1000
# AH0325_v1_c5	AI2801_v1_c1	1	1	0/1000
# AH0325_v1_c6	AI2801_v1_c1	1	1	0/1000
# AH0325_v1_c7	AI2801_v1_c1	1	1	0/1000
# AH0326_v1_c1	AI2801_v1_c1	0.0114865	0	647/1000
# AH0326_v1_c2	AI2801_v1_c1	0.295981	7.34872e-05	1/1000
# AH0326_v1_c3	AI2801_v1_c1	1	1	0/1000
my %result;
#slurp in data, store in hash of hashes
my %uniqseqs = ();
my $seqs_seen=0;
while(my $line = <>){
	my @F=split "\t",$line;
	my $hit = $F[0];
	my $hitsample = $hit;
	if($hit =~/(\S+)_v\d+_c\d+$/){$hitsample = $1;}
	my $q = $F[1];
	my $querysample = $q;
	if($q =~/(\S+)_v\d+_c\d+$/){$querysample = $1;}
	next if $hitsample eq $querysample; #this is only for internal CNAG samples
	if (!exists($uniqseqs{$q})){
		$seqs_seen++;
		$uniqseqs{$q}++;
	}
	last if $seqs_seen > 100;
	my $dist = $F[2];
	my $pval = $F[3];
	my $shared_hashes = $F[4];
	next if $dist > 0.5;
	my $score = 1-$dist;
	push @{$result{$hitsample}},{score=>$score,hit=>$hit,query_seq=>$q};
	if(exists $topscaffolds{$hit}){
		if ($score > $topscaffolds{$q}->{score}){
			$topscaffolds{$q}->{score} = $score;
			$topscaffolds{$q}->{hit} = $hit;
			$topscaffolds{$q}->{query_seq} = $q;
		}
	}else{
			$topscaffolds{$q}->{score} = $score;
			$topscaffolds{$q}->{hit} = $hit;
	}
	$sample_score{$hitsample}+=$score;
	if($sample_score{$hitsample} > $top_sample_score){
		$top_sample_score = $sample_score{$hitsample};
		$top_sample = $hitsample;
	}
}
print $json->encode({top_sample=>$top_sample,
						top_sample_score=>$top_sample_score,
						top_sample_scaffolds=>$result{$top_sample},
						top_scaffolds=>\%topscaffolds});
