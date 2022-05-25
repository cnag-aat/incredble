
# Load initial Resistom data from excel into the database

import django
django.setup()

import csv
from resistome.models import *

with open('database_20190123_import.csv') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        if row['barcode'] or None:
            print(row['barcode'], row['lims_name'] or None)

            if not row['name'] or row['name'] == '#N/A':
                print("Skipped")
                continue

            species = None
            if row['species']:
                species, _ = Species.objects.get_or_create(
                    name=row['species'],
                )
            type_of_carbapenemase = None
            if row['type_of_carbapenemase']:
                type_of_carbapenemase, _ = TypeOfCarbapenemase.objects.get_or_create(
                    name=row['type_of_carbapenemase'],
                )
            biological_sample_of_isolation = None
            if row['biological_sample_of_isolation']:
                biological_sample_of_isolation, _ = BiologicalSampleOfIsolation.objects.get_or_create(
                    name=row['biological_sample_of_isolation'],
                )
            hospital_admission_unit = None
            if row['hospital_admission_unit']:
                hospital_admission_unit, _ = HospitalAdmissionUnit.objects.get_or_create(
                    name=row['hospital_admission_unit'],
                )
            isolation_location = None
            if row['isolation_location']:
                isolation_location, _ = IsolationLocation.objects.get_or_create(
                    name=row['isolation_location'],
                )

            sample, _ = Sample.objects.get_or_create(
                barcode=row['barcode'] or None,
                name=row['lims_name'] or None,
                coruna_code=row['coruna_code'] or None,
                species=species,
                type_of_carbapenemase=type_of_carbapenemase,
                other_resistance_mechanisms=row['other_resistance_mechanisms'] or None,
                sequence_type=row['sequence_type'] or None,
                biological_sample_of_isolation=biological_sample_of_isolation,
                infection_or_colonization=row['infection_or_colonization'] or None,
                hospital_admission_unit=hospital_admission_unit,
                isolation_location=isolation_location,
                acquisition=row['acquisition'] or None,
                type_of_infection=row['type_of_infection'] or None,
                outbreak=row['outbreak'] or None,
                patient_data_sex=row['patient_data_sex'] or None,
                patient_data_age=row['patient_data_age'] or None or None,
                pt=row['pt'] or None,
                ctx=row['ctx'] or None,
                caz=row['caz'] or None,
                caz_avi=row['caz_avi'] or None,
                cef=row['cef'] or None,
                azt=row['azt'] or None,
                ert=row['ert'] or None,
                mem=row['mem'] or None,
                imi=row['imi'] or None,
                imi_rele=row['imi_rele'] or None,
                amk=row['amk'] or None,
                cip=row['cip'] or None,
                colis=row['colis'] or None,
                fosfo_nueva=row['fosfo_nueva'] or None,
                genta=row['genta'] or None,
                tobra=row['tobra'] or None,
            )

            clsi, _ = CLSI.objects.get_or_create(
                sample=sample,
                piper=row['clsi__piper'] or None,
                pt=row['clsi__pt'] or None,
                ctx=row['clsi__ctx'] or None,
                caz=row['clsi__caz'] or None,
                caz_avi=row['clsi__caz_avi'] or None,
                cef=row['clsi__cef'] or None,
                azt=row['clsi__azt'] or None,
                mem=row['clsi__mem'] or None,
                imi=row['clsi__imi'] or None,
                imi_rele=row['clsi__imi_rele'] or None,
                ert=row['clsi__ert'] or None,
                fosfo=row['clsi__fosfo'] or None,
                genta=row['clsi__genta'] or None,
                tobra=row['clsi__tobra'] or None,
                amk=row['clsi__amk'] or None,
                cip=row['clsi__cip'] or None,
                colis=row['clsi__colis'] or None,
            )

            eucast, _ = EUCAST.objects.get_or_create(
                sample=sample,
                piper=row['eucast__piper'] or None,
                pt=row['eucast__pt'] or None,
                ctx=row['eucast__ctx'] or None,
                caz=row['eucast__caz'] or None,
                caz_avi=row['eucast__caz_avi'] or None,
                cef=row['eucast__cef'] or None,
                azt=row['eucast__azt'] or None,
                mem=row['eucast__mem'] or None,
                imi=row['eucast__imi'] or None,
                imi_rele=row['eucast__imi_rele'] or None,
                ert=row['eucast__ert'] or None,
                fosfo=row['eucast__fosfo'] or None,
                genta=row['eucast__genta'] or None,
                tobra=row['eucast__tobra'] or None,
                amk=row['eucast__amk'] or None,
                cip=row['eucast__cip'] or None,
                colis=row['eucast__colis'] or None,
            )

print("Finished OK")
