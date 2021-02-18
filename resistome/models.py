from django.db import models
import os
from django.conf import settings

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)
INFECTION_CHOICES = (
    ('I', 'Infection'),
    ('C', 'Colonization'),
)

class Species(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'species'

    def __str__(self):
        return self.name


# class TypeOfCarbapenemase(models.Model):
#     name = models.CharField(max_length=200, blank=True, null=True)
#
#     class Meta:
#         verbose_name_plural = 'types of carbapenemase'
#
#     def __str__(self):
#         return self.name


class BiologicalSampleOfIsolation(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'biological samples of isolation'

    def __str__(self):
        return self.name


class HospitalAdmissionUnit(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class AmrfClass(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

class AmrfElementType(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

class ResistanceMechanism(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name

class IsolationLocation(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    def __str__(self):
        return self.name

ACQUISITION_TYPE = (
    ("Community", "Community"),
    ("Hospital", "Hospital"),
    ("LTCF", "LTCF"))

COLLECTION_CHOICES = (
    ("SERGAS", "SERGAS"),
    ("CNM", "CNM"))

class Carbapenemase(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'carbapenemase_types'

    def __str__(self):
        return self.name

class Sample(models.Model):
    barcode = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=20, db_index=True,verbose_name="Sample name")
    coruna_code = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name="Other names")
    species = models.ForeignKey(Species, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Genus/species")
    #type_of_carbapenemase = models.ForeignKey(TypeOfCarbapenemase, blank=True, null=True, on_delete=models.CASCADE)
    carbapenemase = models.ManyToManyField(Carbapenemase, blank=True)
    #other_resistance_mechanisms = models.CharField(max_length=200, blank=True, null=True)
    #sequence_type = models.CharField(max_length=200, blank=True, null=True, verbose_name='sequence type (ST)')
    biological_sample_of_isolation = models.ForeignKey(BiologicalSampleOfIsolation, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Biological sample")
    infection_or_colonization = models.CharField(max_length=1, blank=True, null=True, choices=INFECTION_CHOICES)
    hospital_admission_unit = models.ForeignKey(HospitalAdmissionUnit, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    isolation_location = models.ForeignKey(IsolationLocation, max_length=200, blank=True, null=True, on_delete=models.CASCADE, help_text='Hospital/City where strain was isolated')
    isolation_year = models.IntegerField(null=True, blank=True)
    collection = models.CharField(max_length=10, blank=True, null=True, help_text='Collection organization', choices=COLLECTION_CHOICES)
    acquisition = models.CharField(max_length=10, blank=True, null=True, help_text='Community/Hospital/LTCF acquisition', choices=ACQUISITION_TYPE)
    type_of_infection = models.CharField(max_length=200, blank=True, null=True)
    outbreak = models.NullBooleanField(blank=True, null=True)
    patient_data_sex = models.CharField(max_length=1, blank=True, null=True, choices=SEX_CHOICES, verbose_name="Patient sex")
    patient_data_age = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Patient age")
    piper = models.CharField(max_length=20, blank=True, null=True, verbose_name="PIPER")
    pt = models.CharField(max_length=20, blank=True, null=True, verbose_name="P/T")
    ctx = models.CharField(max_length=20, blank=True, null=True, verbose_name="CTX")
    caz = models.CharField(max_length=20, blank=True, null=True, verbose_name= "CAZ ")
    caz_avi = models.CharField(max_length=20, blank=True, null=True, verbose_name="CAZ-AVI")
    cef = models.CharField(max_length=20, blank=True, null=True, verbose_name="CEF")
    azt = models.CharField(max_length=20, blank=True, null=True, verbose_name="AZT")
    ert = models.CharField(max_length=20, blank=True, null=True, verbose_name="ERT")
    mem = models.CharField(max_length=20, blank=True, null=True, verbose_name="MEM")
    imi = models.CharField(max_length=20, blank=True, null=True, verbose_name="IMI")
    imi_rele = models.CharField(max_length=20, blank=True, null=True, verbose_name="IMI-RELE")
    amk = models.CharField(max_length=20, blank=True, null=True, verbose_name="AMK")
    cip = models.CharField(max_length=20, blank=True, null=True, verbose_name="CIP")
    colis = models.CharField(max_length=20, blank=True, null=True, verbose_name="COLIS")
    fosfo_nueva = models.CharField(max_length=20, blank=True, null=True, verbose_name="FOSFO NUEVA")
    genta = models.CharField(max_length=20, blank=True, null=True, verbose_name="GENTA")
    tobra = models.CharField(max_length=20, blank=True, null=True, verbose_name="TOBRA")
    edta_assay = models.CharField(max_length=200, blank=True, null=True, verbose_name="EDTA Assay Result")
    pcr = models.CharField(max_length=200, blank=True, null=True, verbose_name="PCR Result")
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('sample_detail', args=[str(self.id)])


class CLSI(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    piper = models.CharField(max_length=3, blank=True, null=True, verbose_name="PIPER")
    pt = models.CharField(max_length=3, blank=True, null=True, verbose_name="P/T")
    ctx = models.CharField(max_length=3, blank=True, null=True, verbose_name="CTX")
    caz = models.CharField(max_length=3, blank=True, null=True, verbose_name="CAZ")
    caz_avi = models.CharField(max_length=3, blank=True, null=True, verbose_name="CAZ-AVI")
    cef = models.CharField(max_length=3, blank=True, null=True, verbose_name="CEF")
    azt = models.CharField(max_length=3, blank=True, null=True, verbose_name="AZT")
    mem = models.CharField(max_length=3, blank=True, null=True, verbose_name="MEM")
    imi = models.CharField(max_length=3, blank=True, null=True, verbose_name="IMI")
    imi_rele = models.CharField(max_length=3, blank=True, null=True, verbose_name="IMI-RELE")
    ert = models.CharField(max_length=3, blank=True, null=True, verbose_name="ERT")
    fosfo = models.CharField(max_length=3, blank=True, null=True, verbose_name="FOSFO")
    genta = models.CharField(max_length=3, blank=True, null=True, verbose_name="GENTA")
    tobra = models.CharField(max_length=3, blank=True, null=True, verbose_name="TOBRA")
    amk = models.CharField(max_length=3, blank=True, null=True, verbose_name="AMK")
    cip = models.CharField(max_length=3, blank=True, null=True, verbose_name="CIP")
    colis = models.CharField(max_length=3, blank=True, null=True, verbose_name="COLIS")

    class Meta:
        verbose_name_plural = 'CLSI'

    def __str__(self):
        return 'CLSI for %s' % self.sample_id


class EUCAST(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    piper = models.CharField(max_length=3, blank=True, null=True, verbose_name="PIPER")
    pt = models.CharField(max_length=3, blank=True, null=True, verbose_name="P/T")
    ctx = models.CharField(max_length=3, blank=True, null=True, verbose_name="CTX")
    caz = models.CharField(max_length=3, blank=True, null=True, verbose_name="CAZ")
    caz_avi = models.CharField(max_length=3, blank=True, null=True, verbose_name="CAZ-AVI")
    cef = models.CharField(max_length=3, blank=True, null=True, verbose_name="CEF")
    azt = models.CharField(max_length=3, blank=True, null=True, verbose_name="AZT")
    mem = models.CharField(max_length=3, blank=True, null=True, verbose_name="MEM")
    imi = models.CharField(max_length=3, blank=True, null=True, verbose_name="IMI")
    imi_rele = models.CharField(max_length=3, blank=True, null=True, verbose_name="IMI-RELE")
    ert = models.CharField(max_length=3, blank=True, null=True, verbose_name="ERT")
    fosfo = models.CharField(max_length=3, blank=True, null=True, verbose_name="FOSFO")
    genta = models.CharField(max_length=3, blank=True, null=True, verbose_name="GENTA")
    tobra = models.CharField(max_length=3, blank=True, null=True, verbose_name="TOBRA")
    amk = models.CharField(max_length=3, blank=True, null=True, verbose_name="AMK")
    cip = models.CharField(max_length=3, blank=True, null=True, verbose_name="CIP")
    colis = models.CharField(max_length=3, blank=True, null=True, verbose_name="COLIS")

    class Meta:
        verbose_name_plural = 'EUCAST'

    def __str__(self):
        return 'EUCAST for %s' % self.sample_id


# Pipeline models

class Assembly(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE,related_name='assembly')
    assembly = models.CharField(max_length=20, unique=True, db_index=True)
    total_scaffolds = models.PositiveIntegerField(null=True, blank=True)
    circular_scaffolds = models.PositiveIntegerField(null=True, blank=True)
    circularity_ratio = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    scaffolds_2kb_or_shorter = models.PositiveIntegerField(null=True, blank=True)
    assembly_length = models.PositiveIntegerField(null=True, blank=True)
    max_scaffold_length = models.PositiveIntegerField(null=True, blank=True)
    assembler = models.CharField(max_length=40, null=True, blank=True)
    image = models.ImageField(upload_to='img',null=True, blank=True)
    illumina_coverage = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    ont_coverage = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    ont_n50 = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Assemblies'

    def __str__(self):
        return self.assembly

def assembly_fasta_path():
    return os.path.join(settings.MEDIA_ROOT, 'assemblyFASTA')

def annotation_path():
    return os.path.join(settings.MEDIA_ROOT, 'annotationDATA')

class DataFiles(models.Model):
    assembly = models.OneToOneField(Assembly, on_delete=models.CASCADE)
    assembly_fasta = models.FileField(upload_to='assemblyFASTA')
    annotation_protein_fasta = models.FileField(upload_to='annotationDATA')
    annotation_transcript_fasta = models.FileField(upload_to='annotationDATA')
    annotation_gff = models.FileField(upload_to='annotationDATA')

    class Meta:
        verbose_name_plural = 'Data files'

    def __str__(self):
        return '%s data files' % self.assembly

class RelaxaseType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'relaxase_types'

    def __str__(self):
        return self.name

class RelaxaseTypeAccession(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'relaxase_type_accessions'

    def __str__(self):
        return self.name

class RepliconType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'replicon_types'

    def __str__(self):
        return self.name

class RepliconTypeAccession(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'replicon_type_accessions'

    def __str__(self):
        return self.name

class MpfType(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'MPF types'

    def __str__(self):
        return self.name

class MpfTypeAccession(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'MPF type accessions'

    def __str__(self):
        return self.name

class OritType(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'OriT types'

    def __str__(self):
        return self.name

class OritAccession(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'OriT accessions'

    def __str__(self):
        return self.name

class PredictedMobility(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Predicted mobilities'

    def __str__(self):
        return self.name

class Scaffold(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    assembly = models.ForeignKey(Assembly, blank=True, null=True, on_delete=models.CASCADE)
    scaffold = models.CharField(max_length=20, unique=True, db_index=True)
    jbrowse_link = models.URLField(max_length=1000, blank=True, null=True, verbose_name="Jbrowse")
    scaffold_length = models.PositiveIntegerField(blank=True, null=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Est. Copy Number")
    circular = models.NullBooleanField(blank=True, null=True)
    # centrifuge_species = models.CharField(max_length=200, blank=True, null=True, verbose_name="Centrifuge classification")
    # centrifuge_seq = models.CharField(max_length=20, blank=True, null=True)
    gc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="GC content")
    relaxase_type = models.ManyToManyField(RelaxaseType, blank=True)
    relaxase_type_accession = models.ManyToManyField(RelaxaseTypeAccession, blank=True)
    replicon_type = models.ManyToManyField(RepliconType, blank=True)
    replicon_type_accession = models.ManyToManyField(RepliconTypeAccession, blank=True)
    mpf_type = models.ForeignKey(MpfType, blank=True, null=True, verbose_name="MPF type", on_delete=models.CASCADE)
    mpf_type_accession = models.ManyToManyField(MpfTypeAccession, blank=True)
    orit_type = models.ManyToManyField(OritType, blank=True, verbose_name="OriT type")
    orit_accession = models.ManyToManyField(OritAccession, blank=True, verbose_name="OriT accession")
    predicted_mobility = models.ForeignKey(PredictedMobility, blank=True, null=True, verbose_name="Mobility", on_delete=models.CASCADE)
    mash_nearest_neighbor = models.CharField(max_length=20, blank=True, null=True, verbose_name="MASH nearest neighbor")
    mash_neighbor_distance = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True, verbose_name="MASH neighbor distance")
    mash_neighbor_cluster = models.CharField(max_length=20, blank=True, null=True, verbose_name="MASH neighbor cluster")

    def __str__(self):
        return self.scaffold

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('scaffold_detail', args=[str(self.scaffold)])

class Centrifuge(models.Model):
    scaffold = models.ForeignKey(Scaffold, on_delete=models.CASCADE)
    centrifuge_species = models.CharField(max_length=200, blank=True, null=True, verbose_name="Centrifuge classification")
    centrifuge_seq = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '%s' % self.centrifuge_species

CORE_CHOICES = (
    ("core", "core"),
    ("soft_core", "soft core"),
    ("shell","shell"),
    ("cloud","cloud"))

class Annotation(models.Model):
    scaffold = models.ForeignKey(Scaffold, on_delete=models.CASCADE,
        related_name='gene_set', related_query_name="gene_set", db_index=True)
    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    orientation = models.CharField(max_length=1, blank=True, null=True, choices=(('+', '+'), ('-', '-')))
    gene = models.CharField(max_length=20, unique=True, blank=True, null=True)
    gene_name = models.CharField(max_length=20, blank=True, null=True, db_index=True )
    rgi = models.CharField(max_length=3, blank=True, null=True, db_index=True, choices=(('Yes', 'Yes'),))
    amrf = models.CharField(max_length=3, blank=True, null=True, db_index=True, choices=(('Yes', 'Yes'),))
    ec_number = models.CharField(max_length=20, blank=True, null=True)
    product = models.TextField(blank=True, null=True)
    inference = models.TextField(blank=True, null=True)
    jbrowse_link = models.URLField(max_length=1000, blank=True, null=True)
    protein_sequence = models.TextField(blank=True, null=True)
    orthogroup = models.CharField(max_length=10, blank=True, null=True, db_index=True, verbose_name="OrthoGroup")
    roary_gene = models.CharField(max_length=25, blank=True, null=True, db_index=True, verbose_name="RoaryGroup")
    roary_core = models.CharField(max_length=15, blank=True, null=True, db_index=True, verbose_name="Core classification", choices=CORE_CHOICES)
    prokka_id = models.CharField(max_length=15, blank=True, null=True, verbose_name="Prokka ID")

    class Meta:
        indexes = (
            models.Index(fields=['rgi','amrf']),
        )
    def __str__(self):
        return '%s %s:%s' % (self.scaffold, self.start, self.end)

class RoaryGroup(models.Model):
    roary_gene = models.CharField(max_length=25, blank=True, null=True, db_index=True, verbose_name="RoaryGroup")
    roary_core = models.CharField(max_length=15, blank=True, null=True, db_index=True, verbose_name="Core classification", choices=CORE_CHOICES)
    species = models.ForeignKey(Species, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Genus/species")

    class Meta:
        indexes = (
            models.Index(fields=['roary_gene','species','roary_core']),
        )
    def __str__(self):
        return '%s' % (self.roary_gene)


RGI_START_TYPE = (
    ("ATG", "ATG"),
    ("GTG", "GTG"),
    ("TTG", "TTG"),
    ("Edge", "Edge"))


CUT_OFF_TYPE = (
    ("strict", "strict"),
    ("perfect", "perfect"),
    ("loose", "loose"))


class Rgi(models.Model):
    annotation = models.OneToOneField(
        Annotation, on_delete=models.CASCADE,
        related_name='rgi_set', related_query_name="rgi_set")
    gene = models.CharField(unique=True, max_length=20)
    complete = models.NullBooleanField(blank=True, null=True)
    start_type = models.CharField(max_length=4, blank=True, null=True, choices=RGI_START_TYPE)
    rbs_motif = models.CharField(max_length=20, blank=True, null=True)
    rbs_spacer = models.CharField(max_length=20, blank=True, null=True)
    gc_cont = models.DecimalField(max_digits=5, decimal_places=3)
    cut_off = models.CharField(max_length=7, blank=True, null=True, choices=CUT_OFF_TYPE)
    pass_bitscore = models.PositiveIntegerField(null=True, blank=True)
    best_hit_bitscore = models.DecimalField(max_digits=8, decimal_places=3)
    best_hit_aro = models.TextField(blank=True, null=True)
    best_identities = models.DecimalField(max_digits=7, decimal_places=3)
    aro = models.PositiveIntegerField(null=True, blank=True)
    model_type = models.CharField(max_length=40, blank=True, null=True)
    snps_in_best_hit_aro = models.CharField(max_length=200, blank=True, null=True)
    other_snps = models.CharField(max_length=200, blank=True, null=True)
    drug_class = models.CharField(max_length=500, blank=True, null=True)
    resistance_mechanism = models.CharField(max_length=500, blank=True, null=True)
    rgi_resistance_mechanism = models.ForeignKey(ResistanceMechanism, max_length=200, blank=True, null=True, on_delete=models.CASCADE,verbose_name="Resistance mechanism")
    amr_gene_family = models.CharField(max_length=500, blank=True, null=True)
    predicted_dna = models.TextField(blank=True, null=True)
    predicted_protein = models.TextField(blank=True, null=True)
    card_protein_sequence = models.TextField(blank=True, null=True)
    percentage_length_of_reference_sequence = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.gene


class MLST(models.Model):
    assembly = models.OneToOneField(Assembly, blank=True, null=True, on_delete=models.CASCADE, related_name='mlst')
    pubmlst = models.CharField(max_length=200, blank=True, null=True, verbose_name='PubMLST')
    st = models.IntegerField(verbose_name='ST', db_index=True)
    alleles = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'MLST'

    def __str__(self):
        return '%s:%s' % (self.assembly, self.st)


class SpeciesVerification(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    illumina_sp = models.CharField(max_length=200, blank=True, null=True)
    ont_sp = models.CharField(max_length=200, blank=True, null=True)
    lims_sp = models.CharField(max_length=200, blank=True, null=True)
    seq_agreement = models.NullBooleanField(blank=True, null=True)
    verified = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return '%s' % (self.sample, )

#gene,gene_symbol,sequence_name,scope,element_type,element_subtype,class,subclass,method,target_length,reference_sequence_length,pct_coverage_of_reference_sequence,pct_identity_to_reference_sequence,alignment_length,accession_of_closest_sequence,name_of_closest_sequence,hmm_id,hmm_description
class AMRF(models.Model):
    annotation = models.OneToOneField(
        Annotation, on_delete=models.CASCADE,
        related_name='amrf_set', related_query_name="amrf_set")
    gene = models.CharField(unique=True, max_length=20)
    gene_symbol = models.CharField(max_length=20)
    sequence_name = models.CharField(max_length=200, blank=True, null=True)
    scope = models.CharField(max_length=20)
    element_type = models.CharField(max_length=20)
    amrf_element_type = models.ForeignKey(AmrfElementType, max_length=50, blank=True, null=True, on_delete=models.CASCADE)
    element_subtype = models.CharField(max_length=20)
    amrf_class = models.CharField(max_length=50)
    amrfclass = models.ForeignKey(AmrfClass, max_length=100, blank=True, null=True, on_delete=models.CASCADE)
    amrf_subclass = models.CharField(max_length=50)
    method = models.CharField(max_length=20)
    target_length = models.PositiveIntegerField(null=True, blank=True)
    reference_sequence_length = models.PositiveIntegerField(null=True, blank=True)
    pct_coverage_of_reference_sequence = models.DecimalField(null=True, blank=True,max_digits=5, decimal_places=2)
    pct_identity_to_reference_sequence = models.DecimalField(null=True, blank=True,max_digits=5, decimal_places=2)
    alignment_length = models.PositiveIntegerField(null=True, blank=True)
    accession_of_closest_sequence = models.CharField(null=True, blank=True, max_length=20)
    name_of_closest_sequence = models.CharField(max_length=200, blank=True, null=True)
    hmm_id = models.CharField(null=True, blank=True, max_length=20)
    hmm_description = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return self.gene

class GenomeUpload(models.Model):
    description = models.CharField(max_length=255, blank=True)
    fasta = models.FileField(upload_to='uploaded_genomes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=10000, blank=True)
