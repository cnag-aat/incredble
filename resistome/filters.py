import django_filters
from django_filters  import FilterSet
from django_filters  import ChoiceFilter
from resistome.models import Sample
from resistome.models import Scaffold
from resistome.models import Annotation
from resistome.models import Rgi
from resistome.models import AMRF
from resistome.models import Assembly
from resistome.models import MLST
from resistome.models import AmrfClass
from resistome.models import AmrfElementType
from resistome.models import ResistanceMechanism
from resistome.models import Species
from resistome.models import Carbapenemase
from django import forms
from django.db.models import Q

class DynamicChoiceMixin(object):

    @property
    def field(self):
        queryset = self.parent.queryset
        field = super(DynamicChoiceMixin, self).field

        choices = list()
        have = list()
        # iterate through the queryset and pull out the values for the field name
        for item in queryset:
            name = getattr(item, self.field_name)
            if name in have:
                continue
            have.append(name)
            choices.append((name, name))
        field.choices.choices = choices
        return field


class DynamicChoiceFilter(DynamicChoiceMixin, django_filters.ChoiceFilter):
    pass

class ScaffoldFilter(django_filters.FilterSet):
    st = django_filters.CharFilter(field_name='assembly__mlst__st',label='Sequence Type')
    #minscafflength = django_filters.NumberFilter(field_name='scaffold_length',label='Minimum scaffold length')
    #maxscafflength = django_filters.NumberFilter(field_name='scaffold_length',label='Maximum scaffold length')
    scafflengthrange = django_filters.RangeFilter(field_name='scaffold_length',label='Scaffold length range')
    class Meta:
        model = Scaffold
        fields = {'sample':['exact'],
                  'st':['exact'],
                  'scaffold':['exact'],
                  #'scaffold_length':['gt','lt'],
                  #'minscafflength':['gt'],
                  #'maxscafflength':['lt'],
                  'scafflengthrange':['overlap'],
                  'circular':['exact'],
                  'predicted_mobility':['exact'],
                  'relaxase_type':['exact'],
                  'replicon_type':['exact'],
                  'mpf_type':['exact'],
                  'orit_type':['exact'],
                  'mash_neighbor_cluster':['exact']}

class SampleFilter(django_filters.FilterSet):
    st = django_filters.CharFilter(field_name='assembly__mlst__st',label='Sequence Type')
    gene_symbol = django_filters.CharFilter(field_name='assembly__scaffold__gene_set__gene_name',label='RGI gene Symbol')
    amrf_set_gene_symbol = django_filters.CharFilter(field_name='assembly__scaffold__gene_set__amrf_set__gene_symbol',label='AMRF gene symbol',lookup_expr='icontains')
    RESISTANCE_CHOICES = (
        ('PIPER', 'PIPER'),
        ('PT', 'P/T'),
        ('CTX', 'CTX'),
        ('CAZ', 'CAZ'),
        ('CAZ_AVI', 'CAZ-AVI'),
        ('CEF', 'CEF'),
        ('AZT', 'AZT'),
        ('MEM', 'MEM'),
        ('IMI', 'IMI'),
        ('IMI_RELE', 'IMI-RELE'),
        ('ERT', 'ERT'),
        ('FOSFO', 'FOSFO'),
        ('GENTA', 'GENTA'),
        ('TOBRA', 'TOBRA'),
        ('AMK', 'AMK'),
        ('CIP', 'CIP'),
        ('COLIS', 'COLIS'),
    )
    date_range = django_filters.RangeFilter(field_name='isolation_year',label='Date range')
    resistance = django_filters.MultipleChoiceFilter(field_name='resistance',label='Resistant to',method='drug_resistance_filter',choices=RESISTANCE_CHOICES,null_label=None)
    class Meta:
        model = Sample
        fields = {'name':['exact'],'barcode':['exact'],'species':['exact'], 'carbapenemase':['exact'],'resistance':['exact'],'biological_sample_of_isolation':['exact'],'collection':['exact'],'isolation_location':['exact'],'date_range':['overlap'],'acquisition':['exact'],'st':['exact'],'amrf_set_gene_symbol':['icontains'],'gene_symbol':['icontains'],'patient_data_age':['gt','lt'],'patient_data_sex':['exact']}
    def drug_resistance_filter(self, queryset, name, value):
        for drug in value:
            if drug=='PIPER':
                queryset = queryset.filter(
                    Q(eucast__piper='R')
                )
            if drug=='PT':
                queryset = queryset.filter(
                    Q(eucast__pt='R')
                )
            if drug=='CTX':
                queryset = queryset.filter(
                    Q(eucast__ctx='R')
                )
            if drug=='CAZ':
                queryset = queryset.filter(
                    Q(eucast__caz='R')
                )
            if drug=='CAZ_AVI':
                queryset = queryset.filter(
                    Q(eucast__caz_avi='R')
                )
            if drug=='CEF':
                queryset = queryset.filter(
                    Q(eucast__cef='R')
                )
            if drug=='AZT':
                queryset = queryset.filter(
                    Q(eucast__azt='R')
                )
            if drug=='MEM':
                queryset = queryset.filter(
                    Q(eucast__mem='R')
                )
            if drug=='IMI':
                queryset = queryset.filter(
                    Q(eucast__imi='R')
                )
            if drug=='IMI_RELE':
                queryset = queryset.filter(
                    Q(eucast__imi_rele='R')
                )
            if drug=='ERT':
                queryset = queryset.filter(
                    Q(eucast__ert='R')
                )
            if drug=='FOSFO':
                queryset = queryset.filter(
                    Q(eucast__fosfo='R')
                )
            if drug=='TOBRA':
                queryset = queryset.filter(
                    Q(eucast__tobra='R')
                )
            if drug=='AMK':
                queryset = queryset.filter(
                    Q(eucast__amk='R')
                )
            if drug=='CIP':
                queryset = queryset.filter(
                    Q(eucast__cip='R')
                )
            if drug=='COLIS':
                queryset = queryset.filter(
                    Q(eucast__colis='R')
                )
        return queryset

class AssemblyFilter(django_filters.FilterSet):
    st = django_filters.CharFilter(field_name='mlst__st',label='Sequence Type')
    #carbapenemase = django_filters.CharFilter(field_name='sample__carbapenemase__name',label='Carbapenemase')
    sample__carbapenemase__name = django_filters.ModelChoiceFilter(label='Carbapenemase type',queryset=Carbapenemase.objects.all())

    total_scaffolds_range = django_filters.RangeFilter(field_name='total_scaffolds',label='Number of scaffolds')
    circular_scaffolds_range = django_filters.RangeFilter(field_name='circular_scaffolds',label='Number of circular scaffolds')
    circularity_ratio_range = django_filters.RangeFilter(field_name='circularity_ratio',label='Circularity ratio')
    assembly_length_range = django_filters.RangeFilter(field_name='assembly_length',label='Assembly length')
    max_scaffold_length_range = django_filters.RangeFilter(field_name='max_scaffold_length',label='Largest scaffold length')
    illumina_coverage_range = django_filters.RangeFilter(field_name='illumina_coverage',label='Illumina coverage')
    ont_coverage_range = django_filters.RangeFilter(field_name='ont_coverage',label='ONT coverage')
    ont_n50_range = django_filters.RangeFilter(field_name='ont_n50',label='ONT N50')

    class Meta:
        model = Assembly
        fields = {'sample':['exact'],
                    'st':['exact'],
                    'sample__carbapenemase__name':['exact'],
                    'total_scaffolds_range':['overlap'],
                    'circular_scaffolds_range':['overlap'],
                    'circularity_ratio_range':['overlap'],
                    'assembly_length_range':['overlap'],
                    'max_scaffold_length_range':['overlap'],
                    'assembler':['icontains'],
                    'illumina_coverage_range':['overlap'],
                    'ont_coverage_range':['overlap'],
                    'ont_n50_range':['overlap']}

class GeneFilter(django_filters.FilterSet):
    amr_gene_family = django_filters.CharFilter(lookup_expr='icontains')
    gene = django_filters.CharFilter(lookup_expr='icontains')
    resistance_mechanism = django_filters.CharFilter(lookup_expr='icontains')
    best_hit_aro = django_filters.CharFilter(lookup_expr='icontains')
    model_type = django_filters.CharFilter(lookup_expr='icontains')
    drug_class = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Rgi
        fields = ['gene',
                  'best_hit_aro',
                  'model_type',
                  'drug_class',
                  'resistance_mechanism',
                  'amr_gene_family']

class AnnotationFilter(django_filters.FilterSet):
    AMR_gene_family = django_filters.CharFilter(field_name='rgi_set__amr_gene_family',label='AMR gene family',lookup_expr='icontains')
    sample = django_filters.CharFilter(field_name='scaffold__sample__name',label='Sample name',lookup_expr='exact')
    sample_barcode = django_filters.CharFilter(field_name='scaffold__sample__barcode',label='Sample barcode',lookup_expr='exact')
    scaffold = django_filters.CharFilter(field_name='scaffold__scaffold',label='Scaffold',lookup_expr='exact')
    gene = django_filters.CharFilter(label='Gene ID',lookup_expr='icontains')
    gene_name = django_filters.CharFilter(label='Gene name',lookup_expr='icontains')
    product = django_filters.CharFilter(label='Product',lookup_expr='icontains')
    rgi_set__rgi_resistance_mechanism = django_filters.ModelChoiceFilter(label='Resistance mechanism',queryset=ResistanceMechanism.objects.all())
    Drug_class = django_filters.CharFilter(field_name='rgi_set__drug_class',label='Drug class',lookup_expr='icontains')
    amrf_set__amrf_element_type = django_filters.ModelChoiceFilter(label='AMRF element type',queryset=AmrfElementType.objects.all())
    amrf_set__amrfclass = django_filters.ModelChoiceFilter(label='AMRF Class',queryset=AmrfClass.objects.all())
    rgi_set__best_hit_aro = django_filters.CharFilter(field_name='rgi_set__best_hit_aro',label='Best hit ARO',lookup_expr='icontains')
    amrf_set__gene_symbol = django_filters.CharFilter(field_name='amrf_set__gene_symbol',label='AMRF gene symbol',lookup_expr='icontains')
    st = django_filters.CharFilter(field_name='scaffold__assembly__mlst__st',label='ST',lookup_expr='exact')
    scaffold__sample__species = django_filters.ModelChoiceFilter(label='Species',queryset=Species.objects.all())
    RESISTANCE_CHOICES = (
        ('Yes', 'Yes'),
    )
    resistance = django_filters.ChoiceFilter(field_name='resistance',label='Resistance genes only',method='resistance_filter',choices=RESISTANCE_CHOICES,null_label=None)
    class Meta:
        model = Annotation
        fields = ['sample',
                  'sample_barcode',
                  'scaffold',
                  'gene',
                  'gene_name',
                  'rgi_set__best_hit_aro',
                  'product',
                  'Drug_class',
                  'rgi_set__rgi_resistance_mechanism',
                  'AMR_gene_family',
                  'amrf_set__gene_symbol',
                  'amrf_set__amrf_element_type',
                  'amrf_set__amrfclass',
                  'rgi',
                  'amrf',
                  'orthogroup',
                  'roary_core',
                  'roary_gene',
                  'st',
                  'scaffold__sample__species',
                  'resistance'
                  ]
    def resistance_filter(self, queryset, name, value):
        if value=='Yes':
            return queryset.filter(
                Q(rgi='Yes') | Q(amrf='Yes')
            )
