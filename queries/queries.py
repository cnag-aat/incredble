# unset LANG
# export PYTHONIOENCODING=utf-8
import sys
import csv
import argparse
import django
from django.db.models import Count
from django.db.models import Q
from django.core import serializers
django.setup()
from resistome.models import *
def xstr(s):
    if s is None:
        return ''
    return str(s)

a_set = Annotation.objects.all().filter(scaffold__sample__species__name = 'Klebsiella pneumoniae',roary_core='core')
separator = '\t'
for g in a_set:
    mlst = MLST.objects.filter(assembly=g.scaffold.assembly)
    print(separator.join([g.scaffold.scaffold,str(g.start),str(g.end),g.orientation,xstr(g.roary_gene),xstr(g.gene),xstr(mlst[0].st)]) +"\n")

IncLscaffs = Scaffold.objects.all().filter(replicon_type__name='IncL/M')
for s in IncLscaffs:
    print(s.scaffold,s.sample.barcode,s.sample.id,s.sample.isolation_location.city,s.sample.isolation_location.community,",".join(list(s.sample.carbapenemase.all().values_list('name', flat=True))),s.sample.species, sep='\t')

scaffolds_qs = Scaffold.objects.all().annotate(num_genes=Count('gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
for s in scaffolds_qs:
    print(s.scaffold,s.num_genes,s.sample.barcode,s.sample.id,",".join(list(s.sample.carbapenemase.all().values_list('name', flat=True))),s.sample.species, sep='\t')

sample_qs = Sample.objects.all()
for samp in sample_qs:
    num = 0
    scaffolds_qs = Scaffold.objects.all().filter(sample=samp.id).annotate(num_genes=Count('gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
    for s in scaffolds_qs:
        num+=s.num_genes
    resistance=0
    if(samp.eucast.piper == 'R'):
        resistance+=1

    if(samp.eucast.pt == 'R'):
        resistance+=1

    if(samp.eucast.ctx == 'R'):
        resistance+=1

    if(samp.eucast.caz == 'R'):
        resistance+=1

    if(samp.eucast.caz_avi == 'R'):
        resistance+=1

    if(samp.eucast.cef == 'R'):
        resistance+=1

    if(samp.eucast.azt == 'R'):
        resistance+=1

    if(samp.eucast.mem == 'R'):
        resistance+=1

    if(samp.eucast.imi == 'R'):
        resistance+=1

    if(samp.eucast.imi_rele == 'R'):
        resistance+=1

    if(samp.eucast.ERT == 'R'):
        resistance+=1

    if(samp.eucast.fosfo == 'R'):
        resistance+=1

    if(samp.eucast.genta == 'R'):
        resistance+=1

    if(samp.eucast.tobra == 'R'):
        resistance+=1

    if(samp.eucast.amk == 'R'):
        resistance+=1

    if(samp.eucast.cip == 'R'):
        resistance+=1

    if(samp.eucast.colis == 'R'):
        resistance+=1

    print(samp.barcode,samp.name,num,resistance)
