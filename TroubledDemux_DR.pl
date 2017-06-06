#!/usr/bin/perl -w

#USAGE = TroubledDemux_DR.pl TEMP.fastq

$inputfile     = $ARGV[0];
open(FDR, "gzip -dc $inputfile |");

my $count=0;


while(( my @lines = map $_ = <FDR>, 1 .. 4 )[0]) {
  chomp($lines[0]);
  chomp($lines[1]);
  chomp($lines[2]);
  chomp($lines[3]);
  
  if ($lines[1] =~ /^$ARGV[1]/g) {
    $count++; 
    print $lines[0]."\n".$lines[1]."\n".$lines[2]."\n".$lines[3]."\n";
    
    }
    
}
