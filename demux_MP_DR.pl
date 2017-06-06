#! /usr/bin/perl -w
# AUTHOR: KPWILLI, some portions added by DEBJIT
# Date: 3/20/2015
# USAGE: Go into the RUN folder and execute: nohup ../demux_MP_DR.pl NexteraFilePath &

use strict;
use Cwd;

#die "Usage: $0 [full]\nmakes simple file names like S1_R1.fq.gz unless you add 'full' option\nrun in a folder containing one NextSeq folder" if $ARGV[0] and $ARGV[0] =~ /^-h/;
my $group = 20458;
my $dir = cwd();
my $full;
opendir(my $dh, $dir) or die "Can't opendir $dir: $!\n";
my $SStest;
for (grep {-d "$dir/$_" && ! /^\.{1,2}$/} readdir $dh) {
 if (-f "$dir/$_/SampleSheet.csv" and not -l "$dir/$_/SampleSheet.csv") {
  print "$_\n"; 
  $SStest = $_;
 }
}
die "No SampleSheet.csv file found\n" unless $SStest;
mkdir "demux";
chown -1, $group, 'demux';
die "Couldn't work in directory $dir; permissions problem?\n" unless -d "$dir/demux";
system "ln -s $dir/$SStest/SampleSheet.csv $dir/demux/"; # symbolic link to SampleSheet, for convenience
chdir $SStest;
#system "/usr/local/bin/bcl2fastq -o ../demux &> ../demux/demux.log"; # demultiplex with Illumina script, put results in demux directory [changed by DEBJIT]
chdir '../demux';
system "scp -r $ARGV[0]/demux/unconcat/Undetermined* .";#[changed by DEBJIT]

#######################################################
# SEGMENT FOR MP added by DEBJIT
#######################################################
system "gunzip Undetermined_*";
#system "rm -r *fastq.gz";
system "echo `perl ../../MPFinder_DR.pl SampleSheet.csv Undetermined_S0_L001_R1_001.fastq 0.Stats_L001_R1.txt`";
system "echo `perl ../../MPFinder_DR.pl SampleSheet.csv Undetermined_S0_L001_R2_001.fastq 0.Stats_L001_R2.txt`";
system "echo `perl ../../MPFinder_DR.pl SampleSheet.csv Undetermined_S0_L002_R1_001.fastq 0.Stats_L002_R1.txt`";
system "echo `perl ../../MPFinder_DR.pl SampleSheet.csv Undetermined_S0_L002_R2_001.fastq 0.Stats_L002_R2.txt`";
system "echo `perl ../../MPFinder_DR.pl SampleSheet.csv Undetermined_S0_L003_R1_001.fastq 0.Stats_L003_R1.txt`";
system "echo `perl ../../MPFinder_DR.pl SampleSheet.csv Undetermined_S0_L003_R2_001.fastq 0.Stats_L003_R2.txt`";
system "echo `perl ../../MPFinder_DR.pl SampleSheet.csv Undetermined_S0_L004_R1_001.fastq 0.Stats_L004_R1.txt`";
system "echo `perl ../../MPFinder_DR.pl SampleSheet.csv Undetermined_S0_L004_R2_001.fastq 0.Stats_L004_R2.txt`";
mkdir "RAW";
system "mv Undetermined_* RAW/";
system "gzip *.fastq";

#######################################################
my @files = glob "*fastq.gz";
my (%concats, %names);
for (@files) {
 unless (/^(.*)_S(\d+)_(L\d+)_(R\d+)_001.fastq.gz$/) {warn "Can't parse file $_\n"; next}
 $concats{$2}{$4}{$3} = $_;
 $names{$2} = $1;
}

open OUT, ">readCounts.txt";
for my $sample (sort {$a <=> $b} keys %concats) {
 for my $read (sort keys %{$concats{$sample}}) {
  my $outfile = "S${sample}_$read.fq";
  $outfile = "$names{$sample}_$outfile" if $full;
  my $files = '';
  for my $lane (sort keys %{$concats{$sample}{$read}}) {
   $files .= " $concats{$sample}{$read}{$lane}";
   chown -1, $group, $concats{$sample}{$read}{$lane};
  }
  if ($sample eq 0) { # Undetermined
   my $readct = `zcat $files | wc -l`;
   $readct /= 4;
   print OUT "S${sample}_$read (Undetermined)\t$readct\treads\n";
   next;
  }
  system "zcat $files > $outfile";
  my $readct = `wc -l < $outfile`;
  $readct /= 4;
  print OUT $outfile;
  print OUT " ($names{$sample})" unless $full;
  print OUT "\t$readct\treads\n"; 
  system "gzip $outfile";
  chown -1, $group, $outfile;
 }
}
close OUT;
chown -1, $group, 'readCounts.txt', 'demux.log';
mkdir "unconcat";
chown -1, $group, 'unconcat';
system "mv *fastq.gz unconcat";
