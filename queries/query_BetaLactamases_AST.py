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

sample_qs = Sample.objects.all()
for samp in sample_qs:
    num = 0
    #scaffolds_qs = Scaffold.objects.all().filter(sample=samp.id).annotate(num_genes=Count('gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
    #for s in scaffolds_qs:
    #    num+=s.num_genes
    scaffolds_qs = Scaffold.objects.all().filter(sample=samp.id).annotate(num_genes=Count('gene_set', filter=(Q(gene_set__amrf='Yes') & Q(gene_set__amrf_set__amrfclass__name='BETA-LACTAM'))))
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
    if(samp.eucast.ert == 'R'):
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
