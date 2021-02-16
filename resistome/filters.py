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
    class Meta:
        model = Scaffold
        fields = {'sample':['exact'],
                  'st':['exact'],
                  'scaffold':['exact'],
                  'scaffold_length':['gt','lt'],
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
    class Meta:
        model = Sample
        fields = {'name':['exact'],'barcode':['exact'],'species':['exact'], 'carbapenemase':['exact'],'biological_sample_of_isolation':['exact'],'collection':['exact'],'isolation_location':['exact'],'acquisition':['exact'],'st':['exact'],'amrf_set_gene_symbol':['icontains'],'gene_symbol':['icontains'],'patient_data_age':['gt','lt'],'patient_data_sex':['exact']}

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
