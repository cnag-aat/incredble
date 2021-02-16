#!/usr/bin/env perl
use strict;
use Math::BigFloat;
Math::BigFloat->precision(-6);


my %sample_score=();
my %topscaffolds =();
my $top_sample_score = Math::BigFloat->new(0.000000);
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
while(my $line = <>){
	my $hitsample = 'none';
	my $querysample = 'none';
	my @F=split "\t",$line;
	my $hit = $F[0];
	if($hit =~/(\S+)_v\d+_c\d+$/){$hitsample = $1;}
	my $q = $F[1];
	if($q =~/(\S+)_v\d+_c\d+$/){$querysample = $1;}
	next if $hitsample eq $querysample;
	my $dist = $F[2];
	my $pval = $F[3];
	my $shared_hashes = $F[4];
	next if $dist > 0.02;
	push @{$result{$hitsample}},$line;
	my $score = Math::BigFloat->new(1-$dist);
	if(exists $topscaffolds{$hit}){
		if ($score > $topscaffolds{$q}->{score}){
			$topscaffolds{$q}->{score} = $score;
			$topscaffolds{$q}->{hit} = $hit;
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

print "Top scaffold matches:\n";
foreach my $qscaff (sort keys %topscaffolds ){ #i is a counter
	print "$qscaff\t$topscaffolds{$qscaff}->{hit}\t$topscaffolds{$qscaff}->{score}\n";
}
printf("Best sample match:\n%s\t%.6f\n",$top_sample,$top_sample_score) ;
foreach my $r (@{$result{$top_sample}}){
		print $r;
}
#print new line character
