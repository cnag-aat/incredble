import django
django.setup()

from resistome.models import *

header=['name','sample','hospital','species','st']
print(','.join(header))
for sample in Sample.objects.all():
    location = sample.isolation_location
    location='Unknown'
    try:
        location = sample.isolation_location.name
    except:
        location='Unknown'
    ass = Assembly.objects.get(sample=sample.pk)
    try:
        mlst = MLST.objects.get(assembly=ass.pk)
        info=[str(sample.barcode),sample.name,sample.isolation_location.name,mlst.pubmlst,str(mlst.st)]
    except:
        pubmlst=sample.species.name
        st=str(0)
        info=[str(sample.barcode),sample.name,location,pubmlst,st]
    print(','.join(info))
