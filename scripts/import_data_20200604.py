
# Load initial Resistom data from excel into the database
import django
django.setup()

from resistome.models import *
import csv


with open('DB_23052020_fix.csv') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        if row['Genomes'] or None:
            print(row)
            print(row['Genomes'] or None)

            #if row['with_data'] != '1':
            #    print('with_data:' + row['with_data'])
            #    print("Skipped")
            #    continue

            species = None
            if row['Species_Final']:
                species, _ = Species.objects.get_or_create(
                    name=row['Species_Final'],
                )

            type_of_carbapenemase = None
            if row['Carba_final']:
                type_of_carbapenemase, _ = TypeOfCarbapenemase.objects.get_or_create(
                    name=row['Carba_final'],
                )

            biological_sample_of_isolation = None
            if row['Sample of isolation']:
                biological_sample_of_isolation, _ = BiologicalSampleOfIsolation.objects.get_or_create(
                    name=row['Sample of isolation'],
                )

            hospital_admission_unit = None
            if row['Hospital admission unit']:
                hospital_admission_unit, _ = HospitalAdmissionUnit.objects.get_or_create(
                    name=row['Hospital admission unit'],
                )

            isolation_location = None
            if row['Hospital/City where strain was isolated']:
                isolation_location, _ = IsolationLocation.objects.get_or_create(
                    name=row['Hospital/City where strain was isolated'],
                )

            try:
                sample = Sample.objects.get(barcode=row['Genomes'])
            except Sample.DoesNotExist:
                sample, _ = Sample.objects.get_or_create(
                    barcode=row['Genomes'])
            #sample.coruna_code = row['coruna_code'] or None
            sample.species = species
            sample.type_of_carbapenemase = type_of_carbapenemase
            sample.biological_sample_of_isolation = biological_sample_of_isolation
            sample.infection_or_colonization = row['Infection/Colonization'] or None
            sample.hospital_admission_unit = hospital_admission_unit
            sample.isolation_location = isolation_location
            sample.acquisition = row['Community/Hospital/LTCF acquisition'] or None
            #sample.type_of_infection = row['type_of_infection'] or None
            #sample.outbreak = row['outbreak'] or None
            sample.patient_data_sex = row['Sex'] or None
            sample.patient_data_age = row['Age'] or None
            sample.pt = row['P/T'] or None
            sample.ctx = row['CTX'] or None
            sample.caz = row['CAZ'] or None
            sample.caz_avi = row['CAZ-AVI'] or None
            sample.cef = row['CEF'] or None
            sample.azt = row['AZT'] or None
            sample.ert = row['ERT'] or None
            sample.mem = row['MEM'] or None
            sample.imi = row['IMI'] or None
            sample.imi_rele = row['IMI-RELE'] or None
            sample.amk = row['AMK'] or None
            sample.cip = row['CIP'] or None
            sample.colis = row['COLIS'] or None
            sample.fosfo_nueva = row['FOSFO'] or None
            sample.genta = row['GENTA'] or None
            sample.tobra = row['TOBRA'] or None
            sample.save()

            try:
                clsi = CLSI.objects.get(sample=sample)
            except CLSI.DoesNotExist:
                clsi, _ = CLSI.objects.get_or_create(sample=sample)

            clsi.piper = row['P_CLSI'] or None
            clsi.pt = row['P/T_CLSI'] or None
            clsi.ctx = row['CTX_CLSI'] or None
            clsi.caz = row['CAZ_CLSI'] or None
            clsi.caz_avi = row['CAZ-AVI_CLSI'] or None
            clsi.cef = row['CEF_CLSI'] or None
            clsi.azt = row['AZT_CLSI'] or None
            clsi.mem = row['MEM_CLSI'] or None
            clsi.imi = row['IMI_CLSI'] or None
            clsi.imi_rele = row['IMI-RELE_CLSI'] or None
            clsi.ert = row['ERT_CLSI'] or None
            clsi.fosfo = row['FOSFO_CLSI'] or None
            clsi.genta = row['GENTA_CLSI'] or None
            clsi.tobra = row['TOBRA_CLSI'] or None
            clsi.amk = row['AMK_CLSI'] or None
            clsi.cip = row['CIP_CLSI'] or None
            clsi.colis = row['COLI_CLSI'] or None
            clsi.save()

            try:
                eucast = EUCAST.objects.get(sample=sample)
            except EUCAST.DoesNotExist:
                eucast, _ = EUCAST.objects.get_or_create(sample=sample)

            eucast.piper = row['P_EUCAST'] or None
            eucast.pt = row['P/T_EUCAST'] or None
            eucast.ctx = row['CTX_EUCAST'] or None
            eucast.caz = row['CAZ_EUCAST'] or None
            eucast.caz_avi = row['CAZ-AVI_EUCAST'] or None
            eucast.cef = row['CEF_EUCAST'] or None
            eucast.azt = row['AZT_EUCAST'] or None
            eucast.mem = row['MEM_EUCAST'] or None
            eucast.imi = row['IMI_EUCAST'] or None
            eucast.imi_rele = row['IMI-RELE_EUCAST'] or None
            eucast.ert = row['ERT_EUCAST'] or None
            eucast.fosfo = row['FOSFO_EUCAST'] or None
            eucast.genta = row['GENTA_EUCAST'] or None
            eucast.tobra = row['TOBRA_EUCAST'] or None
            eucast.amk = row['AMK_EUCAST'] or None
            eucast.cip = row['CIP_EUCAST'] or None
            eucast.colis = row['COLIS_EUCAST'] or None
            eucast.save()

print("Finished OK")
