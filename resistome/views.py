from django.shortcuts import render
import django_filters
from django.views.generic import ListView
from resistome.models import *
from django.views.generic import TemplateView
#from resistome.models import Assembly
from django_tables2 import SingleTableView
from django_tables2 import RequestConfig
from resistome.tables import SampleTable
from resistome.tables import ResistanceTable
from resistome.tables import ClinicalTable
from resistome.tables import ScaffoldsTable
from resistome.tables import ScaffoldListTable
from resistome.tables import AnnotationTable
from resistome.tables import AnnotationListTable
from resistome.tables import GeneFiltTable
from resistome.tables import RgiTable
from resistome.tables import SingleScaffoldTable
from resistome.tables import CentrifugeTable
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from resistome.filters import SampleFilter
from resistome.filters import ScaffoldFilter
from resistome.filters import GeneFilter
from resistome.filters import AnnotationFilter
import plotly.graph_objects as go
import pandas as pd
from plotly.offline import plot
from django.utils.safestring import mark_safe
from math import log
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.db.models import Q
# Create your views here.
# def sample_index(request):
#    samples = Sample.objects.all()
#    context = {"samples": samples}
#    return render(request, "sample_index.html", context)
# def index(request):
#    return render(request, 'index.html')

def charts(request):
    species_labels = []
    species_data = []
    speciesdict = {}
    queryset = Species.objects.annotate(num_samples=Count('sample'))
    for species in queryset:
        speciesdict[species.name]=species.num_samples
    sort_speciesdict = sorted(speciesdict.items(), key=lambda x: x[1], reverse=True)
    for i in sort_speciesdict:
        species_labels.append(i[0])
        species_data.append(i[1])

    community_labels = []
    community_data = []
    comdict = {}
    communities = IsolationLocation.objects.order_by().values('community').distinct()
    for com in communities:
        qs = Sample.objects.filter(isolation_location__community=com['community'])
        comdict[com['community']]=qs.count()
    sort_comdict = sorted(comdict.items(), key=lambda x: x[1], reverse=True)
    for i in sort_comdict:
        community_labels.append(i[0])
        community_data.append(i[1])

    species_qs = Species.objects.filter(name='Klebsiella pneumoniae')
    kp_labels = []
    kp_data = []
    kpdict={}
    sequence_types = Sample.objects.filter(species=species_qs[0].pk).order_by().values('assembly__mlst__st').distinct()
    for seqtype in sequence_types:
        qs = Sample.objects.filter(species=species_qs[0].pk).filter(assembly__mlst__st=seqtype['assembly__mlst__st'])
        #kp_labels.append(seqtype['assembly__mlst__st'])
        #kp_data.append(qs.count())
        kpdict[seqtype['assembly__mlst__st']]=qs.count()

    sort_kpdict = sorted(kpdict.items(), key=lambda x: x[1], reverse=True)
    for i in sort_kpdict:
        kp_labels.append(i[0])
        kp_data.append(i[1])

    species_qs = Species.objects.filter(name='Enterobacter cloacae complex')
    enterobacter_labels = []
    enterobacter_data = []
    enterobacterdict={}
    sequence_types = Sample.objects.filter(species=species_qs[0].pk).order_by().values('assembly__mlst__st').distinct()
    for seqtype in sequence_types:
        qs = Sample.objects.filter(species=species_qs[0].pk).filter(assembly__mlst__st=seqtype['assembly__mlst__st'])
        enterobacterdict[seqtype['assembly__mlst__st']]=qs.count()

    sort_enterobacterdict = sorted(enterobacterdict.items(), key=lambda x: x[1], reverse=True)
    for i in sort_enterobacterdict:
        enterobacter_labels.append(i[0])
        enterobacter_data.append(i[1])

    species_qs = Species.objects.filter(name='Escherichia coli')
    ecoli_labels = []
    ecoli_data = []
    ecolidict={}
    sequence_types = Sample.objects.filter(species=species_qs[0].pk).order_by().values('assembly__mlst__st').distinct()
    for seqtype in sequence_types:
        qs = Sample.objects.filter(species=species_qs[0].pk).filter(assembly__mlst__st=seqtype['assembly__mlst__st'])
        #kp_labels.append(seqtype['assembly__mlst__st'])
        #kp_data.append(qs.count())
        ecolidict[seqtype['assembly__mlst__st']]=qs.count()

    sort_ecolidict = sorted(ecolidict.items(), key=lambda x: x[1], reverse=True)
    for i in sort_ecolidict:
        ecoli_labels.append(i[0])
        ecoli_data.append(i[1])

    return render(request, 'charts.html', {
        'species_labels': species_labels,
        'species_data': species_data,
        'community_labels': community_labels,
        'community_data': community_data,
        'kp_labels': kp_labels,
        'kp_data': kp_data,
        'enterobacter_labels': enterobacter_labels,
        'enterobacter_data': enterobacter_data,
        'ecoli_labels': ecoli_labels,
        'ecoli_data': ecoli_data,
    })

class HomeView(TemplateView):
    template_name = 'index.html'


class SideBar(TemplateView):
    template_name = 'sidebar.html'

# class JbrowseView(TemplateView):
#    template_name = 'browse/index.html'


class BlastView(PermissionRequiredMixin, TemplateView):
    permission_required = "resistome.view_sample"
    login_url = "access_denied"
    template_name = 'blast.html'

    def render_to_response(self, context, **response_kwargs):
        response = super(BlastView, self).render_to_response(
            context, **response_kwargs)
        response.set_cookie(key='CRE', value='uq4QeBPJRR9wRUV4')
        return response


class TreeView(PermissionRequiredMixin, TemplateView):
    permission_required = "resistome.view_sample"
    login_url = "access_denied"
    template_name = 'tree.html'


class AccessDeniedView(TemplateView):
    template_name = 'denied.html'



@permission_required("resistome.view_sample", login_url='access_denied')
def spain_map_filter(request):

    #    df = pd.read_csv('/Users/talioto/Documents/projects/CRE/server-dev/incredible/incredible/static/isolation_locations_test.csv')
    #    df.head()

    colors = ['rgb(189,189,189)', 'rgb(218, 30, 55)', 'rgb(189, 31, 54)', 'rgb(167, 30, 52)', 'rgb(133, 24, 42)', 'rgb(100, 18, 32)',
              'rgb(55, 119, 255)', 'rgb(251, 139, 36)', 'rgb(42, 157, 143)', 'rgb(102, 46, 155)', 'rgb(147, 129, 255)', 'rgb(255, 216, 190)']
    species = {0: 'All', 1: 'Klebsiella pneumoniae', 2: 'Klebsiella oxytoca', 3: 'Klebsiella variicola', 4: 'Klebsiella aerogenes', 5: 'Klebsiella quasipneumoniae',
               6: 'Enterobacter cloacae complex', 7: 'Serratia marcescens', 8: 'Escherichia coli', 9: 'Citrobacter freundii', 10: 'Citrobacter koseri', 11: 'Raoultella ornithinolytica'}

    fig = go.Figure(go.Scattergeo())
    columns = ['Location', 'Lat', 'Lon', 'Species', 'Value']
    rows = []
    #all_samples_set = Sample.objects.all()
    f = SampleFilter(request.GET, queryset=Sample.objects.all())
    filtered_set = f.qs
    location_set = IsolationLocation.objects.all()
    for loc in location_set:
        samplecount = filtered_set.filter(isolation_location=loc).count()
        if samplecount:
            row = [loc.name, loc.latitude, loc.longitude, 'All', samplecount]
            rows.append(row)
    for i in range(11):
        species_id = Species.objects.get(name=species[i + 1])
        for loc in location_set:
            samplecount = filtered_set.filter(
                isolation_location=loc, species=species_id).count()
            if samplecount:
                row = [loc.name, loc.latitude, loc.longitude,
                       species[i + 1], samplecount]
                rows.append(row)

    if len(rows):
        df = pd.DataFrame(rows, columns=columns)
        for i in range(12):
            df_spec = df.query('Species == "%s"' % species[i])
            fig.add_trace(go.Scattergeo(
                lon=df_spec['Lon'],
                lat=df_spec['Lat'],
                #text = '<a href="https://denovo.cnag.cat:8080/samples/">' + df_spec['Location'] + ": " + df_spec['Value'].map('{:.0f}'.format).astype(str) + '</a>',
                text=df_spec['Location'] + ": " + df_spec['Value'].map('{:.0f}'.format).astype(str), hoverinfo='location + name + text',
                name=species[i],
                marker=dict(
                    size=(df_spec['Value'] * 100),
                    sizemode='area',
                    color=colors[i],
                    line_width=0.5,
                    opacity=0.75
                )))

    #df_all = df.query('Species == "All"')
    # fig['data'][0].update(mode='markers+text', textposition='bottom center',
    #              text=df_all['Location'] + ": " + df_all['Value'].map('{:.0f}'.format).astype(str)) #+' '+ df_all['Location']
    fig.update_layout(
        #title=go.layout.Title(
        #    text='CRE samples collected and sequenced in Spain by CNAG in 2019'),
        geo=go.layout.Geo(
            resolution=50,
            scope='europe',
            showframe=True,
            showcoastlines=True,
            landcolor="rgb(229, 229, 229)",
            countrycolor="white",
            coastlinecolor="white",
            projection_type='mercator',
            showocean=True, oceancolor="LightBlue",
            lonaxis_range=[-12.0, 6],
            lataxis_range=[35.0, 45.0],
            domain=dict(x=[0, 1], y=[0, 1])
        ),
        #legend_traceorder = 'reversed',
        legend_itemsizing='trace',
        height=600,
        width=800
    )

    # def do_click(trace, points, state):
    #     if points.point_inds:
    #         ind = points.point_inds[0]
    #         url = 'https://denovo.cnag.cat:8080/samples/' # df.link.iloc[ind]
    #         webbrowser.open_new_tab(url)

    # fig.on_click(do_click)

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #context['plot'] = plot_div
    sample_table = SampleTable(filtered_set)
    context = {"plot": plot_div,
               'filter': f,
               'table': sample_table
               }
    return render(request, "map_filter.html", context)


@permission_required("resistome.view_sample", login_url='access_denied')
def sample_detail(request, pk=None, barcode=None):
    if pk:
        sample = Sample.objects.get(pk=pk)
    else:
        sample = Sample.objects.get(barcode=barcode)
        pk = sample.pk
    ass = Assembly.objects.get(sample=pk)

    eucast = EUCAST.objects.get(sample=pk)
    clsi = CLSI.objects.get(sample=pk)
    try:
        df = DataFiles.objects.get(assembly=ass.pk)
    except DataFiles.DoesNotExist:
        df = None
    scaffolds = Scaffold.objects.filter(assembly=ass.pk).annotate(num_genes=Count(
        'gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
    hosp = None
    maploc = " "
    age = " "
    if sample.isolation_location:
        hosp = IsolationLocation.objects.get(name=sample.isolation_location)
        maploc = mark_safe("<a target='_blank' href='http://www.google.com/maps/place/" + str(
            hosp.latitude) + "," + str(hosp.longitude) + "'>" + str(sample.isolation_location) + "</a>")
    age = str(int(sample.patient_data_age))
    try:
        mlst = MLST.objects.get(assembly=ass.pk)
        clinical_data = [  # {'Agent': 'piper', 'CLSI': str(clsi.piper), 'EUCAST': str(eucast.piper)},
            {'Name': 'Collection', 'Value': sample.collection},
            {'Name': 'Isolation Year', 'Value': sample.isolation_year},
            {'Name': 'Isolation Location', 'Value': maploc},
            {'Name': 'Hospital Admission Unit', 'Value': str(
                sample.hospital_admission_unit)},
            {'Name': 'Patient Sex', 'Value': str(sample.patient_data_sex)},
            {'Name': 'Patient Age', 'Value': age},
            {'Name': 'Community/Hospital/LTCF acquisition',
                'Value': str(sample.acquisition)},
            {'Name': 'Biological Sample of Isolation', 'Value': str(
                sample.biological_sample_of_isolation)},
            {'Name': 'Infection or Colonization', 'Value': str(
                sample.infection_or_colonization)},
            {'Name': 'Outbreak', 'Value': str(sample.outbreak)},
            {'Name': 'Genus/Species', 'Value': mark_safe(
                "<div style='font-style:italic;'}>" + str(sample.species) + "</div>")},
            {'Name': 'Carbapenamase type(s)', 'Value': ', '.join(b.name for b in sample.carbapenemase.all())},
            {'Name': 'MLST', 'Value': str(mlst.st) + ":" + str(mlst.alleles)},
            {'Name': 'EDTA Assay (if any)', 'Value': str(sample.edta_assay)},
            {'Name': 'PCR Result (if any)', 'Value': str(sample.pcr)},
            #{'Name': 'MLST', 'Value': str(mlst.pubmlst) + ":" + str(mlst.st) + " " + str(mlst.alleles)},
        ]
    except:
        mlst = None
        clinical_data = [  # {'Agent': 'piper', 'CLSI': str(clsi.piper), 'EUCAST': str(eucast.piper)},
            {'Name': 'Collection', 'Value': sample.collection},
            {'Name': 'Isolation Year', 'Value': sample.isolation_year},
            {'Name': 'Isolation Location', 'Value': maploc},
            {'Name': 'Hospital Admission Unit', 'Value': str(
                sample.hospital_admission_unit)},
            {'Name': 'Patient Sex', 'Value': str(sample.patient_data_sex)},
            {'Name': 'Patient Age', 'Value': str(
                int(sample.patient_data_age))},
            {'Name': 'Community/Hospital/LTCF acquisition',
                'Value': str(sample.acquisition)},
            {'Name': 'Biological Sample of Isolation', 'Value': str(
                sample.biological_sample_of_isolation)},
            {'Name': 'Infection or Colonization', 'Value': str(
                sample.infection_or_colonization)},
            {'Name': 'Outbreak', 'Value': str(sample.outbreak)},
            {'Name': 'Genus/Species', 'Value': mark_safe(
                "<div style='font-style:italic;'}>" + str(sample.species) + "</div>")},
            {'Name': 'Carbapenamase type(s)', 'Value': ', '.join(b.name for b in sample.carbapenemase.all())},
            {'Name': 'EDTA Assay (if any)', 'Value': str(sample.edta_assay)},
            {'Name': 'PCR Result (if any)', 'Value': str(sample.pcr)},
        ]

    clinical_table = ClinicalTable(clinical_data)

    clsi_eucast_data = [
                        {'Agent': 'Piper', 'MIC': str(sample.piper).replace(">=", "≥").replace("<=", "≤"), 'CLSI': str(clsi.piper),        'EUCAST': str(eucast.piper)},
                        {'Agent': 'P/T', 'MIC': str(sample.pt).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.pt), 'EUCAST': str(eucast.pt)},
                        {'Agent': 'CTX', 'MIC': str(sample.ctx).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.ctx), 'EUCAST': str(eucast.ctx)},
                        {'Agent': 'CAZ', 'MIC': str(sample.caz).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.caz), 'EUCAST': str(eucast.caz)},
                        {'Agent': 'CAZ-AVI', 'MIC': str(sample.caz_avi).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.caz_avi), 'EUCAST': str(eucast.caz_avi)},
                        {'Agent': 'CEF', 'MIC': str(sample.cef).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.cef), 'EUCAST': str(eucast.cef)},
                        {'Agent': 'AZT', 'MIC': str(sample.azt).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.azt), 'EUCAST': str(eucast.azt)},
                        {'Agent': 'MEM', 'MIC': str(sample.mem).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.mem), 'EUCAST': str(eucast.mem)},
                        {'Agent': 'IMI', 'MIC': str(sample.imi).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.imi), 'EUCAST': str(eucast.imi)},
                        {'Agent': 'IMI-RELE', 'MIC': str(sample.imi_rele).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.imi_rele), 'EUCAST': str(eucast.imi_rele)},
                        {'Agent': 'ERT', 'MIC': str(sample.ert).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.ert), 'EUCAST': str(eucast.ert)},
                        {'Agent': 'FOSFO', 'MIC': str(sample.fosfo_nueva).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.fosfo), 'EUCAST': str(eucast.fosfo)},
                        {'Agent': 'GENTA', 'MIC': str(sample.genta).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.genta), 'EUCAST': str(eucast.genta)},
                        {'Agent': 'TOBRA', 'MIC': str(sample.tobra).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.tobra), 'EUCAST': str(eucast.tobra)},
                        {'Agent': 'AMK', 'MIC': str(sample.amk).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.amk), 'EUCAST': str(eucast.amk)},
                        {'Agent': 'CIP', 'MIC': str(sample.cip).replace(">=", "≥").replace(
                            "<=", "≤"), 'CLSI': str(clsi.cip), 'EUCAST': str(eucast.cip)},
                        {'Agent': 'COLIS', 'MIC': str(sample.colis).replace(">=", "≥").replace("<=", "≤"), 'CLSI': str(clsi.colis), 'EUCAST': str(eucast.colis)}]

    clsi_eucast_table = ResistanceTable(clsi_eucast_data)
    scaffolds_table = ScaffoldsTable(scaffolds)
    context = {"sample": sample,
               "ass": ass,
               "eucast": eucast,
               "clsi": clsi,
               "df": df,
               "scaffolds": scaffolds,
               "scaffolds_table": scaffolds_table,
               "clsi_eucast_table": clsi_eucast_table,
               "clinical_table": clinical_table
               }
    response = render(request, "sample_detail.html", context)
    response.set_cookie(key='CRE', value='uq4QeBPJRR9wRUV4')
    return response


# ExportMixin, SingleTableView,
class SampleListView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = "resistome.view_sample"
    login_url = "access_denied"
    model = Sample
    table_class = SampleTable
    template_name = 'samples.html'
    filterset_class = SampleFilter
    table_pagination = {"per_page": 15}
    def render_to_response(self, context, **response_kwargs):
        response = super(SampleListView, self).render_to_response(context, **response_kwargs)
        response.set_cookie('CRE', 'uq4QeBPJRR9wRUV4')
        return response


@permission_required("resistome.view_annotation", login_url='access_denied')
def gene_list_filtScaffold(request, scaffold):
    #geneset = Annotation.objects.filter(scaffold=scaffold)
    scaff = Scaffold.objects.get(scaffold=scaffold)
    #query = Q(scaffold=scaff)
    #query.add(Q(rgi='Yes'), Q.AND)
    #query.add(Q(amrf='Yes'), Q.OR)
    filteredgenes = Annotation.objects.filter(Q(scaffold=scaff) & (
        Q(rgi='Yes') | Q(amrf='Yes')))  # this is where get_related would work
    # sample=Scaffold.objects.get(scaffold=scaffold).sample
    gene_table = AnnotationListTable(filteredgenes)
    #f = GeneFilter
    context = {"scaffold": scaff,
               "table": gene_table,
               # "filter": f
               }
    return render(request, "filteredgenes.html", context)


@permission_required("resistome.view_scaffold", login_url='access_denied')
def ScaffoldView(request, scaffold):
    #scaff = Scaffold.objects.filter(scaffold=scaffold)
    #filteredgenes = Annotation.objects.filter(Q(scaffold=scaffold) & (Q(rgi='Yes') | Q(amrf='Yes')))
    scaff = Scaffold.objects.filter(scaffold=scaffold).annotate(num_genes=Count(
        'gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
    sample = scaff[0].sample
    scaff_table = SingleScaffoldTable(scaff)
    centrifuge = Centrifuge.objects.filter(scaffold=scaff[0].pk)
    centrifuge_table = CentrifugeTable(centrifuge)
    context = {"sample": sample,
               "scaffold_table": scaff_table,
               "centrifuge_table": centrifuge_table,
               "scaffold": scaff[0],
               # "filter": f
               }
    response = render(request, "scaffold.html", context)
    return render(request, "scaffold.html", context)

class ScaffoldListView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = "resistome.view_scaffold"
    login_url = "access_denied"
    model = Scaffold
    table_class = ScaffoldListTable
    template_name = 'scaffold_list.html'
    filterset_class = ScaffoldFilter
    table_pagination = {"per_page": 50}
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(num_genes=Count(
            'gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
    def render_to_response(self, context, **response_kwargs):
        response = super(ScaffoldListView, self).render_to_response(context, **response_kwargs)
        response.set_cookie('CRE', 'uq4QeBPJRR9wRUV4')
        return response

# class GeneListView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView): #ExportMixin, SingleTableView,
#     permission_required = "resistome.view_annotation"
#     login_url = "/access_denied"
#     model = Rgi
#     table_class = GeneTable
#     template_name = 'genes.html'
#     filterset_class = GeneFilter
#     table_pagination={"per_page": 50}

# ExportMixin, SingleTableView,
class AnnotationListView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = "resistome.view_annotation"
    login_url = "access_denied"
    model = Annotation
    table_class = AnnotationListTable
    template_name = 'annotation.html'
    filterset_class = AnnotationFilter
    table_pagination = {"per_page": 50}
    def render_to_response(self, context, **response_kwargs):
        response = super(AnnotationListView, self).render_to_response(context, **response_kwargs)
        response.set_cookie('CRE', 'uq4QeBPJRR9wRUV4')
        return response


@permission_required("resistome.view_annotation", login_url='access_denied')
def gene_detail(request, pk=None, gene=None):
    if pk:
        annotation = Annotation.objects.get(pk=pk)
    else:
        annotation = Annotation.objects.get(gene=gene)
        pk = annotation.pk

    rgi = None
    amrf = None
    try:
        rgi = Rgi.objects.get(annotation=pk)
    except Rgi.DoesNotExist as e:
        pass

    try:
        amrf = AMRF.objects.get(annotation=pk)
    except AMRF.DoesNotExist as e:
        pass

    annotation = Annotation.objects.get(pk=pk)
    sample = annotation.scaffold.sample
    location_string = str(annotation.scaffold) + ":" + \
        str(annotation.start) + ".." + str(annotation.end)
    annotation_data = [  # {'Agent': 'piper', 'CLSI': str(clsi.piper), 'EUCAST': str(eucast.piper)},
        {'Name': 'Browse', 'Value': mark_safe('<a href="https://resistome.cnag.cat/genomes/cre/browse/?loc=' + location_string + \
                                              '&tracks=DNA%2CAnnotation%2CRGI-Annotation%2CAMRFinder-Annotation%2CResfinder&highlight=" target="_blank">' + location_string + '</a>')},
        # {'Name': 'Browse', 'Value': mark_safe(str(annotation.jbrowse_link))},#str(annotation.scaffold) + ':' + str(annotation.start) + ".." + str(annotation.end) + str(annotation.orientation)},
        {'Name': 'Gene ID', 'Value': str(annotation.gene)},
        {'Name': 'Gene Name', 'Value': str(
            annotation.gene_name)},
        {'Name': 'EC Number', 'Value': str(
            annotation.ec_number)},
        {'Name': 'Product', 'Value': str(
            annotation.product)},
        {'Name': 'Inference', 'Value': str(
            annotation.inference)},
        {'Name': 'Protein Sequence', 'Value': str(
            annotation.protein_sequence)},
        {'Name': 'Orthologous Group', 'Value': mark_safe('<a href="/incredble/genes/?orthogroup=' + str(
            annotation.orthogroup) + '">' + str(annotation.orthogroup) + '</a>')},

    ]

    annotation_table = AnnotationTable(annotation_data)
    context = {"sample": sample,
               "annotation_table": annotation_table,
               "annotation": annotation,
               }
    if rgi:
        rgi_data = [
            {'Name': 'Drug Class', 'Value': str(rgi.drug_class)},
            {'Name': 'Resistance Mechanism',
             'Value': str(rgi.resistance_mechanism)},
            {'Name': 'AMR Gene Family',
             'Value': str(rgi.amr_gene_family)},
            {'Name': 'Best Hit ARO', 'Value': str(rgi.best_hit_aro)},
            {'Name': 'Best Hit Bitscore',
             'Value': str(rgi.best_hit_bitscore)},
            {'Name': 'Best Identities',
             'Value': str(rgi.best_identities)},
            {'Name': 'ARO', 'Value': str(rgi.aro)},
            {'Name': 'Model Type', 'Value': str(rgi.model_type)},
            {'Name': 'SNPs in Best Hit ARO',
             'Value': str(rgi.snps_in_best_hit_aro)},
            {'Name': 'Other SNPs', 'Value': str(rgi.other_snps)},
            {'Name': 'Complete', 'Value': str(rgi.complete)},
            {'Name': 'Start Type', 'Value': str(rgi.start_type)},
            {'Name': 'RBS Motif', 'Value': str(rgi.rbs_motif)},
            {'Name': 'RBS Spacer', 'Value': str(rgi.rbs_spacer)},
            {'Name': 'GC Content', 'Value': str(rgi.gc_cont)},
            {'Name': 'Cut Off', 'Value': str(rgi.cut_off)},
            {'Name': 'Pass Bitscore', 'Value': str(rgi.pass_bitscore)},
            {'Name': 'Predicted DNA Sequence',
             'Value': str(rgi.predicted_dna)},
            {'Name': 'Predicted Protein Sequence',
             'Value': str(rgi.predicted_protein)},
            {'Name': 'CARD Protein Sequence',
             'Value': str(rgi.card_protein_sequence)},
            {'Name': 'Pct Length of CARD Sequence', 'Value': str(
                rgi.percentage_length_of_reference_sequence)},
        ]
        rgi_table = RgiTable(rgi_data)
        context["rgi_table"] = rgi_table

    if amrf:
        amrf_data = [
            {'Name': 'Gene Symbol', 'Value': str(amrf.gene_symbol)},
            {'Name': 'Sequence Name', 'Value': str(amrf.sequence_name)},
            {'Name': 'Scope', 'Value': str(amrf.scope)},
            {'Name': 'Element Type', 'Value': str(amrf.element_type)},
            {'Name': 'Element Subtype', 'Value': str(amrf.element_subtype)},
            {'Name': 'AMRF Class', 'Value': str(amrf.amrf_class)},
            {'Name': 'AMRF Subclass', 'Value': str(amrf.amrf_subclass)},
            {'Name': 'Method', 'Value': str(amrf.method)},
            {'Name': 'Target Length', 'Value': str(amrf.target_length)},
            {'Name': 'Reference Sequence Length',
                'Value': str(amrf.reference_sequence_length)},
            {'Name': '% Coverage of Reference Sequence', 'Value': str(
                amrf.pct_coverage_of_reference_sequence)},
            {'Name': '% Identity to Reference Sequence', 'Value': str(
                amrf.pct_identity_to_reference_sequence)},
            {'Name': 'Alignment Length', 'Value': str(amrf.alignment_length)},
            {'Name': 'Accession of Closest Sequence',
                'Value': str(amrf.accession_of_closest_sequence)},
            {'Name': 'Name of Closest Sequence',
                'Value': str(amrf.name_of_closest_sequence)},
            {'Name': 'HMM ID', 'Value': str(amrf.hmm_id)},
            {'Name': 'HMM Description', 'Value': str(amrf.hmm_description)},
        ]
        amrf_table = RgiTable(amrf_data)
        context["amrf_table"] = amrf_table

    response = render(request, "gene_detail.html", context)
    response.set_cookie(key='CRE', value='uq4QeBPJRR9wRUV4')
    return response
    # return render(request, "gene_detail.html", context)


@permission_required("resistome.view_annotation", login_url='access_denied')
def gene_detail_old(request, pk):
    rgi = Rgi.objects.get(pk=pk)
    annotation = Annotation.objects.get(rgi_set=pk)
    sample = annotation.scaffold.sample
    annotation_data = [  # {'Agent': 'piper', 'CLSI': str(clsi.piper), 'EUCAST': str(eucast.piper)},
        # str(annotation.scaffold) + ':' + str(annotation.start) + ".." + str(annotation.end) + str(annotation.orientation)},
        {'Name': 'Browse', 'Value': mark_safe(str(annotation.jbrowse_link))},
        {'Name': 'Gene ID', 'Value': str(annotation.gene)},
        {'Name': 'Gene Name', 'Value': str(annotation.gene_name)},
        {'Name': 'EC Number', 'Value': str(annotation.ec_number)},
        {'Name': 'Product', 'Value': str(annotation.product)},
        {'Name': 'Inference', 'Value': str(annotation.inference)},
        {'Name': 'Protein Sequence', 'Value': str(
            annotation.protein_sequence)},
    ]

    annotation_table = AnnotationTable(annotation_data)

    rgi_data = [
        {'Name': 'Drug Class', 'Value': str(rgi.drug_class)},
        {'Name': 'Resistance Mechanism',
         'Value': str(rgi.resistance_mechanism)},
        {'Name': 'AMR Gene Family',
         'Value': str(rgi.amr_gene_family)},
        {'Name': 'Best Hit ARO', 'Value': str(rgi.best_hit_aro)},
        {'Name': 'Best Hit Bitscore',
         'Value': str(rgi.best_hit_bitscore)},
        {'Name': 'Best Identities',
         'Value': str(rgi.best_identities)},
        {'Name': 'ARO', 'Value': str(rgi.aro)},
        {'Name': 'Model Type', 'Value': str(rgi.model_type)},
        {'Name': 'SNPs in Best Hit ARO',
         'Value': str(rgi.snps_in_best_hit_aro)},
        {'Name': 'Other SNPs', 'Value': str(rgi.other_snps)},
        {'Name': 'Complete', 'Value': str(rgi.complete)},
        {'Name': 'Start Type', 'Value': str(rgi.start_type)},
        {'Name': 'RBS Motif', 'Value': str(rgi.rbs_motif)},
        {'Name': 'RBS Spacer', 'Value': str(rgi.rbs_spacer)},
        {'Name': 'GC Content', 'Value': str(rgi.gc_cont)},
        {'Name': 'Cut Off', 'Value': str(rgi.cut_off)},
        {'Name': 'Pass Bitscore', 'Value': str(rgi.pass_bitscore)},
        {'Name': 'Predicted DNA Sequence',
         'Value': str(rgi.predicted_dna)},
        {'Name': 'Predicted Protein Sequence',
         'Value': str(rgi.predicted_protein)},
        {'Name': 'CARD Protein Sequence',
         'Value': str(rgi.card_protein_sequence)},
        {'Name': 'Pct Length of CARD Sequence', 'Value': str(
            rgi.percentage_length_of_reference_sequence)},
    ]

    rgi_table = RgiTable(rgi_data)

    context = {"sample": sample,
               "annotation_table": annotation_table,
               "annotation": annotation,
               "rgi_table": rgi_table,
               }
    response = render(request, "gene_detail.html", context)
    response.set_cookie(key='CRE', value='uq4QeBPJRR9wRUV4')
    return response
    # return render(request, "gene_detail.html", context)
