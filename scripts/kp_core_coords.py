import sys
import django
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
