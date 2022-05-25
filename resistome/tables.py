# tables.py
import django_tables2 as tables
from django_tables2.utils import A
from .models import Sample
from .models import Assembly
from .models import Scaffold
from .models import Annotation
from .models import Centrifuge
from .models import Rgi
import re
from django.utils.safestring import mark_safe
#import html

class SampleTable(tables.Table):
    name = tables.LinkColumn("sample_detail", kwargs={
                             "pk": tables.A("pk")}, empty_values=())
    barcode = tables.LinkColumn("sample_detail", kwargs={
                                "pk": tables.A("pk")}, empty_values=())
    #assembly = tables.Column(accessor='assembly.assembly')
    st = tables.Column(accessor='assembly.mlst.st')
    #verified = tables.RelatedLinkColumn(accessor="speciesverification.verified")

    class Meta:
        attrs={"class": "table table-striped table-responsive-sm"}
        model = Sample
        template_name = "django_tables2/bootstrap4.html"
        paginate = {"per_page": 15}
        #attrs = {"class": "table-sm"}
        fields = ('name', 'barcode', 'coruna_code', 'species',
                  'carbapenemase', 'st', 'isolation_location')
        #fields = ("name", )
        #id = tables.Column(linkify=True)

class AssemblyTable(tables.Table):
    sample = tables.Column(linkify=True,verbose_name='Sample name')
    barcode = tables.Column(verbose_name='Sample barcode',accessor='sample__barcode')
    st = tables.Column(accessor='mlst.st')
    carbapenemase = tables.Column(verbose_name='Carbapenemase',accessor='sample__carb_names',orderable=False)
    ont_coverage = tables.Column(verbose_name='ONT coverage')
    ont_n50 = tables.Column(verbose_name='ONT read N50')
    class Meta:
        attrs={"class": "table table-striped table-responsive-sm"}
        model = Assembly
        template_name = "django_tables2/bootstrap4.html"
        paginate = {"per_page": 15}
        # leave out the assembler unless we add a new one. They're all the same.
        fields = ('sample', 'barcode', 'st', 'carbapenemase', 'total_scaffolds',
                  'circular_scaffolds', 'circularity_ratio', 'assembly_length',
                   'max_scaffold_length','illumina_coverage','ont_coverage','ont_n50')
        #fields = ("name", )
        #id = tables.Column(linkify=True)



class GeneFiltTable(tables.Table):
    gene = tables.LinkColumn("gene_detail", kwargs={
                             "pk": tables.A("pk")}, empty_values=())
    best_hit_aro = tables.Column(accessor='rgi.best_hit_aro')
    model_type = tables.Column(accessor='rgi.model_type')
    drug_class = tables.Column(accessor='rgi.drug_class')
    resistance_mechanism = tables.Column(accessor='rgi.resistance_mechanism')
    amr_gene_family = tables.Column(accessor='rgi.amr_gene_family')

    class Meta:
        model = Annotation
        template_name = "django_tables2/bootstrap4.html"
        paginate = {"per_page": 15}
        fields = ('gene', 'gene_name', 'product', 'best_hit_aro', 'model_type',
                  'drug_class', 'resistance_mechanism', 'amr_gene_family')
        #fields = ("name", )
        #id = tables.Column(linkify=True)


class ResistanceTable(tables.Table):
    Agent = tables.Column()
    MIC = tables.Column()
    CLSI = tables.Column()
    EUCAST = tables.Column()

    class Meta:
        template = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-responsive'}


class ClinicalTable(tables.Table):
    Name = tables.Column()
    Value = tables.Column()

    class Meta:
        template = 'django_tables2/bootstrap4.html'
        show_header = False
        attrs = {'class': 'table table-striped table-responsive'}


class CentrifugeSeqTemplateColumn(tables.TemplateColumn):
    def render(self, record, table, value, bound_column, **kwargs):
        if record.centrifuge_seq == "species":
            return ''

        if record.centrifuge_seq == "-":
            return ''

        return super(CentrifugeSeqTemplateColumn, self).render(record, table, value, bound_column, **kwargs)

# class ScaffoldListTable(tables.Table):
#     scaffold = tables.Column(linkify=True)
#     # queryset=queryset.annotate(num_genes=Count(
#     #     'gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
#
#     num_genes = tables.TemplateColumn('<a href="{% url \'gene_list\' %}?scaffold={{record.scaffold}}&resistance=Yes">{{record.num_genes}}</a>',empty_values=(), verbose_name='Resistance Genes')
#     all_genes = tables.TemplateColumn('<a href="{% url \'gene_list\' %}?scaffold={{record.scaffold}}">{{record.all_genes}}</a>',empty_values=(), verbose_name='Resistance Genes')
#
#     #sample = tables.Column(accessor='sample',linkify=True)
#     #scaffold = tables.LinkColumn(verbose_name= 'RGI Genes' )
#     jbrowse_link = tables.Column(verbose_name='Browse Genome')
#     jbrowse_link = tables.TemplateColumn(
#         '<a href="https://resistome.cnag.cat/genomes/cre/browse/?loc={{record.scaffold}}&tracks=DNA%2CAnnotation%2CRGI-Annotation%2CAMRFinder-Annotation%2CResfinder&highlight=" target="_blank">Browse</a>')
#
#     species = tables.Column(empty_values=(),
#                           verbose_name='Species')
#
#     def render_species(self, record):
#         if record.centrifuge_set.exists():
#             uniqueList = []
#             for cent in record.centrifuge_set.all():
#                 if cent.centrifuge_species not in uniqueList:
#                     uniqueList.append(cent.centrifuge_species)
#             return mark_safe("<div style='font-style:italic;'}>" + ', '.join(species for species in uniqueList) + "</div>")
#             # return ', '.join(cent.centrifuge_species for cent in record.centrifuge_set.all())
#
#     class Meta:
#         model = Scaffold
#         template_name = "django_tables2/bootstrap4.html"
#         attrs = {'class': 'table table-striped table-responsive'}
#         paginate = {"per_page": 10}
#         fields = ('scaffold', 'sample','jbrowse_link', 'num_genes', 'all_genes','scaffold_length',
#                   'circular', 'depth','species','gc','predicted_mobility','replicon_type','replicon_type_accession',
#                   'relaxase_type','relaxase_type_accession','mpf_type','mpf_type_accession',
#                   'orit_type','orit_accession','mash_nearest_neighbor','mash_neighbor_distance','mash_neighbor_cluster')


class ScaffoldsTable(tables.Table):
    scaffold = tables.Column(linkify=True)
    #num_genes = tables.LinkColumn("gene_list_filtScaffold", kwargs={
    #                                  "scaffold": tables.A("scaffold")}, empty_values=(), verbose_name='Resistance Genes')
    #all_genes = tables.LinkColumn("gene_list_filtScaffoldAll", kwargs={"scaffold": tables.A("scaffold")}, empty_values=(), verbose_name='All Genes')

    num_genes = tables.TemplateColumn('<a href="{% url \'gene_list\' %}?scaffold={{record.scaffold}}&resistance=Yes">{{record.num_genes}}</a>',empty_values=(), verbose_name='Resistance Genes')
    all_genes = tables.TemplateColumn('<a href="{% url \'gene_list\' %}?scaffold={{record.scaffold}}">{{record.all_genes}}</a>',empty_values=(), verbose_name='All Genes')
    mash_neighbor_cluster = tables.TemplateColumn('<a href="{% url \'scaffold_list\' %}?mash_neighbor_cluster={{record.mash_neighbor_cluster}}">{{record.mash_neighbor_cluster}}</a>',empty_values=(), verbose_name='MASH neighbor cluster')
    #AnnotationListView resistance=Yes
    #num_genes = tables.TemplateColumn("gene_list_filtScaffold", kwargs={
    #                                  "scaffold": tables.A("scaffold")}, empty_values=(), verbose_name='Resistance Genes')
    sample = tables.Column(accessor='sample',linkify=True)
    #scaffold = tables.LinkColumn(verbose_name= 'RGI Genes' )
    jbrowse_link = tables.Column(verbose_name='Browse Genome')
    jbrowse_link = tables.TemplateColumn(
        '<a href="https://genomes.cnag.cat/genomes/cre/browse/?loc={{record.scaffold}}&tracks=DNA%2CAnnotation%2CRGI-Annotation%2CAMRFinder-Annotation%2CResfinder&highlight=" target="_blank">Browse</a>')

    species = tables.Column(empty_values=(),
                          verbose_name='Species')
    st = tables.Column(verbose_name="ST",accessor='assembly__mlst__st')
    def render_species(self, record):
        if record.centrifuge_set.exists():
            uniqueList = []
            for cent in record.centrifuge_set.all():
                if cent.centrifuge_species not in uniqueList:
                    uniqueList.append(cent.centrifuge_species)
            return mark_safe("<div style='font-style:italic;'}>" + ', '.join(species for species in uniqueList) + "</div>")
            # return ', '.join(cent.centrifuge_species for cent in record.centrifuge_set.all())

    class Meta:
        model = Scaffold
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-striped table-responsive'}
        paginate = {"per_page": 10}
        fields = ('scaffold', 'sample','st','jbrowse_link', 'num_genes', 'all_genes','scaffold_length',
                  'circular', 'depth','species','gc','predicted_mobility','replicon_type','replicon_type_accession',
                  'relaxase_type','relaxase_type_accession','mpf_type','mpf_type_accession',
                  'orit_type','orit_accession','mash_nearest_neighbor','mash_neighbor_distance','mash_neighbor_cluster')
        #fields = ('scaffold', 'sample','jbrowse_link', 'num_genes', 'all_genes','scaffold_length',
                  #'circular', 'depth','species','predicted_mobility','replicon_type','relaxase_type','mash_neighbor_cluster')

class CentrifugeTable(tables.Table):

    centrifuge_seq = CentrifugeSeqTemplateColumn(
        '<a href="https://www.ncbi.nlm.nih.gov/nuccore/{{record.centrifuge_seq}}" target="_blank">{{record.centrifuge_seq}}</a>')

    class Meta:
        model = Centrifuge
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-responsive'}
        paginate = {"per_page": 10}
        fields = ('centrifuge_species', 'centrifuge_seq')


# class SingleScaffoldTable(tables.Table):
#     num_genes = tables.TemplateColumn('<a href="{% url \'gene_list\' %}?scaffold={{record.scaffold}}&resistance=Yes">{{record.num_genes}}</a>',empty_values=(), verbose_name='Resistance Genes')
#     all_genes = tables.TemplateColumn('<a href="{% url \'gene_list\' %}?scaffold={{record.scaffold}}">{{record.all_genes}}</a>',empty_values=(), verbose_name='Resistance Genes')
#
#     sample = tables.Column(linkify=True)
#     #sample = tables.Column(accessor='sample',linkify=True)
#     #scaffold = tables.LinkColumn(verbose_name= 'RGI Genes' )
#     jbrowse_link = tables.Column(verbose_name='Browse Genome')
#     jbrowse_link = tables.TemplateColumn(
#         '<a href="https://resistome.cnag.cat/genomes/cre/browse/?loc={{record.scaffold}}&tracks=DNA%2CAnnotation%2CRGI-Annotation%2CAMRFinder-Annotation%2CResfinder&highlight=" target="_blank">Browse</a>')
#
#     class Meta:
#         model = Scaffold
#         template_name = "django_tables2/bootstrap4.html"
#         attrs = {'class': 'table table-responsive'}
#         paginate = {"per_page": 10}
#         fields = ('scaffold', 'sample', 'jbrowse_link', 'num_genes', 'all_genes','scaffold_length',
#                             'circular', 'depth','gc','predicted_mobility','replicon_type','replicon_type_accession',
#                             'relaxase_type','relaxase_type_accession','mpf_type','mpf_type_accession',
#                             'orit_type','orit_accession','mash_nearest_neighbor','mash_neighbor_distance','mash_neighbor_cluster')

class AnnotationTemplateColumn(tables.TemplateColumn):
    def render(self, record, table, value, bound_column, **kwargs):
        match = re.search('^http.*=([^=]+)',value)
        if match:
            location = match.group(1).replace("%3A", ":")
            return mark_safe('<a href="' + value + '" target="_blank">' + location + '</a>')

        return super(AnnotationTemplateColumn, self).render(record, table, value, bound_column, **kwargs)

class AnnotationTable(tables.Table):
    Name = tables.Column()
    Value = AnnotationTemplateColumn("{{record.Value}}")

    class Meta:
        template = 'django_tables2/bootstrap4.html'
        show_header = False
        attrs = {'class': 'table table-striped table-responsive'}

class AnnotationListTable(tables.Table):
    gene = tables.LinkColumn("gene_detail", kwargs={
                             "pk": tables.A("pk")}, empty_values=())
    scaffold = tables.Column(linkify=True)
    best_hit_aro = tables.Column(accessor='rgi_set.best_hit_aro',verbose_name='Best hit ARO')
    drug_class = tables.Column(accessor='rgi_set.drug_class')
    resistance_mechanism = tables.Column(accessor='rgi_set.rgi_resistance_mechanism')
    amr_gene_family = tables.Column(accessor='rgi_set.amr_gene_family')
    #barcode = tables.Column(accessor='scaffold.sample.barcode', verbose_name='CNAG barcode')
    name = tables.Column(accessor='scaffold.sample',
                         linkify=True, verbose_name='Sample name')
    element_type = tables.Column(verbose_name="AMRF element type",accessor='amrf_set.amrf_element_type')
    amrfclass = tables.Column(verbose_name="AMRF class",accessor='amrf_set.amrfclass')
    amrf_gene_symbol = tables.Column(verbose_name="AMRF gene symbol",accessor='amrf_set.gene_symbol')
    #roary_gene = tables.LinkColumn("gene_list_roary", kwargs={
    #                         "roary_gene": tables.A("roary_gene")}, empty_values=())
    roary_gene = tables.TemplateColumn(
        '<a href="/incredble/genes/?roary_gene={{record.roary_gene}}">{{record.roary_gene}}</a>')
    st = tables.Column(verbose_name="ST",accessor='scaffold__assembly__mlst__st')
    #sample = tables.LinkColumn("barcode_detail", kwargs={"barcode": tables.A("sample")}, empty_values=())
##    best_hit_bitscore = tables.Column(accessor='rgi.best_hit_bitscore')
##    model_type = tables.Column(accessor='rgi.model_type')
##    drug_class = tables.Column(accessor='rgi.drug_class')
##    resistance_mechanism = tables.Column(accessor='rgi.resistance_mechanism')
##    amr_gene_family = tables.Column(accessor='rgi.amr_gene_family')
    #verified = tables.RelatedLinkColumn(accessor="speciesverification.verified")

    class Meta:
        attrs={"class": "table table-striped table-responsive-sm"}
        model = Annotation
        template_name = "django_tables2/bootstrap4.html"
        paginate = {"per_page": 15}
        #attrs = {"class": "table-sm"}
        fields = ('name', 'st','gene', 'scaffold','gene_name', 'product', 'best_hit_aro','drug_class', 'resistance_mechanism', 'amrf_gene_symbol','amr_gene_family','element_type','amrfclass','roary_core','roary_gene')
        #fields = ("name", )
        #id = tables.Column(linkify=True)

class AnnotationCoordsTable(tables.Table):
    st = tables.Column(verbose_name="ST",accessor='scaffold__assembly__mlst__st')
    export_formats = ['csv', 'tsv']
    class Meta:
        model = Annotation
        template_name = "django_tables2/bootstrap4.html"
        paginate = {"per_page": 100}
        #attrs = {"class": "table-sm"}
        fields = ('scaffold','start','end','orientation','roary_gene','gene','st')
        #fields = ("name", )
        #id = tables.Column(linkify=True)



class RgiTable(tables.Table):
    Name = tables.Column()
    Value = tables.Column()

    class Meta:
        template = 'django_tables2/bootstrap4.html'
        show_header = False
        attrs = {'class': 'table table-striped table-responsive'}
