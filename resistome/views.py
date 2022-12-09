from django.shortcuts import render, redirect
import django_filters
from django.views.generic import ListView
from resistome.models import *
from django.views.generic import TemplateView
from django_tables2 import SingleTableView
from django_tables2 import RequestConfig
from resistome.tables import SampleTable
from resistome.tables import AssemblyTable
from resistome.tables import ResistanceTable
from resistome.tables import ClinicalTable
from resistome.tables import ScaffoldsTable
# from resistome.tables import ScaffoldListTable
from resistome.tables import AnnotationTable
from resistome.tables import AnnotationListTable
from resistome.tables import AnnotationCoordsTable
from resistome.tables import GeneFiltTable
from resistome.tables import RgiTable
# from resistome.tables import SingleScaffoldTable
from resistome.tables import CentrifugeTable
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from resistome.filters import SampleFilter
from resistome.filters import AssemblyFilter
from resistome.filters import ScaffoldFilter
from resistome.filters import GeneFilter
from resistome.filters import AnnotationFilter
from resistome.forms import GenomeUploadForm
import plotly.graph_objects as go
import plotly.express as px
from itertools import cycle
import pandas as pd
import re
from plotly.offline import plot
from django.utils.safestring import mark_safe
from math import log
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.db.models import Q
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import subprocess
import json
import os, time, sys
import scipy.stats as stats
import networkx as nx
from timeit import default_timer as timer
from datetime import timedelta
import pickle
import logging
from django.contrib import messages
# Get an instance of a logger
logger = logging.getLogger(__name__)


# @permission_required("resistome.view_sample", login_url='access_denied')
def model_form_upload(request):
    if request.method == 'POST':
        form = GenomeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_query=form.save()
            process = subprocess.run('/home/www/resistome.cnag.cat/incredible/search/mash dist -i /home/www/resistome.cnag.cat/incredible/search/incredble.release7.fasta.msh /home/www/resistome.cnag.cat/incredible/deployment/data/'+ new_query.fasta.name +' | /home/www/resistome.cnag.cat/incredible/search/mash_hits_to_json.pl', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            output = process.stdout
            new_query.result = output
            new_query.save()
            #myupload=GenomeUpload.objects.get(pk=new_query.pk)
            #clean up upload directory
            path = r"/home/www/resistome.cnag.cat/incredible/deployment/data/uploaded_genomes/"
            now = time.time()
            for f in os.listdir(path):
                f = os.path.join(path, f)
                if os.stat(f).st_mtime < now - 7 * 86400:
                    if os.path.isfile(f):
                        os.remove(f)
            return redirect('/incredble/result/'+ str(new_query.pk) +'/')
    else:
        form = GenomeUploadForm()
    return render(request, 'upload.html', {
        'form': form
    })

# @permission_required("resistome.view_sample", login_url='access_denied')
def mash_result(request, pk=None):
    context = {"result": "No hits"}
    if pk:
        genome = GenomeUpload.objects.get(pk=pk)
        #process = subprocess.run('/home/www/resistome.cnag.cat/incredible/search/mash dist -i /home/www/resistome.cnag.cat/incredible/search/incredble.release7.fasta.msh /home/www/resistome.cnag.cat/incredible/deployment/data/'+ genome.fasta.name +' | /home/www/resistome.cnag.cat/incredible/search/mash_hits_to_json.pl', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        #output = process.stdout
        #parsed = json.loads(output)
        parsed = json.loads(genome.result)

        if parsed['top_sample'] != 'none':
            context = { "genome": genome,
                        "top_sample": parsed['top_sample'],
                            "top_sample_score": parsed['top_sample_score'],
                                "top_sample_scaffolds": parsed['top_sample_scaffolds'],
                                    "top_scaffolds":parsed['top_scaffolds']
                                    }
            response = render(request, "mash_result.html", context)
            response.set_cookie(key='CRE', value='uq4QeBPJRR9wRUV4')
            return response
        else:
            response = render(request, "no_hits.html", context)
            response.set_cookie(key='CRE', value='uq4QeBPJRR9wRUV4')
            return response

    response = render(request, "mash_result.html", context)
    response.set_cookie(key='CRE', value='uq4QeBPJRR9wRUV4')
    return response


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


# class BlastView(PermissionRequiredMixin, TemplateView):
class BlastView(TemplateView):
    # permission_required = "resistome.view_sample"
    # login_url = "access_denied"
    template_name = 'blast.html'

    def render_to_response(self, context, **response_kwargs):
        response = super(BlastView, self).render_to_response(
            context, **response_kwargs)
        response.set_cookie(key='CRE', value='uq4QeBPJRR9wRUV4')
        return response


# class TreeView(PermissionRequiredMixin, TemplateView):
class TreeView(TemplateView):
    # permission_required = "resistome.view_sample"
    # login_url = "access_denied"
    template_name = 'tree.html'


class AccessDeniedView(TemplateView):
    template_name = 'denied.html'

# @permission_required("resistome.view_sample", login_url='access_denied')
def ani_networks(request):

    # messages.info(request, 'Rendering tANI networks. Please be patient. This can take up to 1 minute...')
    t1= timer()
    f = ScaffoldFilter(request.GET, queryset=Scaffold.objects.all())
    filtered_set = f.qs
    filtered_scaffs = filtered_set.values_list('scaffold', flat=True)
    t2= timer()
    plasmid_info_MOB = pd.read_csv("/home/www/resistome.cnag.cat/incredible/ani/AF_ANI_rel07_nodes.MOBTYPE.tsv", sep="\t")
    t3= timer()
    #ani = pd.read_csv("/home/www/resistome.cnag.cat/incredible/ani/AF_ANI_rel07.filtered.tsv", sep="\t")
    #scaff = Scaffold.objects.filter(scaffold=scaffold).annotate(num_genes=Count('gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))),all_genes=Count('gene_set'))

    #ani["ANI_tw"] = ani["ANI_tw"].astype(float)
    #ani["AF"] = ani["AF"].astype(float)

    #ani_filt = ani.loc[(ani['AF'] > 99.9) & (ani['ANI_tw'] > 99.9)]
    my_edges = ANI.objects.filter(tANI__lte=0.05)
    t4= timer()
    debug=''
    ##Now we built the graph
    # edges = {}
    # nodes = {}
    G = nx.Graph()
    if os.path.isfile('/home/talioto/pickles/ani.pickle'):
        with open('/home/talioto/pickles/ani.pickle', 'rb') as anifile:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
            G = pickle.load(anifile)
    else:
        for e in my_edges:
            na = e.node_a.scaffold
            nb = e.node_b.scaffold
            if na != nb:
                G.add_edge(na, nb, weight=float(0.06) - float(e.tANI))
            # if not na in edges.keys():
            #     edges[na] = {}
            # if not na in nodes.keys():
            #     nodes[na] = 0
            # if not nb in nodes.keys():
            #     nodes[nb] = 0
            # edges[na][nb] = ''
            # nodes[na] += 1
            # nodes[nb] += 1
        with open('/home/talioto/pickles/ani.pickle', 'wb') as anifile:
        # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(G, anifile, pickle.HIGHEST_PROTOCOL)
    relationships = G.subgraph(filtered_scaffs)
    t5= timer()
    ##Now we make groups according to certain feature

    ##for relaxase type (we could add a filter depending on the feature that is being filtered).Something like:
    #if feat == "MOBtype":
    groups_relaxase = pd.DataFrame()
    for node in relationships.nodes:
        scaffs = Scaffold.objects.filter(scaffold=node)
        list1=[]
        for rt in scaffs[0].relaxase_type.all():
            list1.append(rt.name)
        s = ","
        s = s.join(list1)
        #r = plasmid_info_MOB[plasmid_info_MOB['file_id'] == node]['relaxase_type'].iloc[0]
        r = s
        if r == "MOBP" or r=="MOBP,MOBP":
            group = 0
        elif (r == 'MOBF'):
            group = 1
        elif (r == 'MOBH'):
            group = 2
        elif (r=="MOBQ"):
            group= 3
        elif (r=="MOBC"):
            group = 4
        elif (r=="MOBV"):
            group = 5
        elif (r=="MOBF,MOBP" or r=="MOBP,MOBF" or r=="MOBP,MOBF,MOBP"):
            group = 6
        elif (r=="MOBH,MOBF" or r=="MOBF,MOBH"):
            group = 7
        elif (r=="MOBC,MOBF" or r=="MOBF,MOBC"):
            group = 8
        elif (r=="MOBH,MOBP" or r=="MOBP,MOBH"):
            group = 9
        elif (r=="MOBC,MOBP" or r=="MOBP,MOBC"):
            group = 10
        else:
            group = 11
        groups_relaxase.loc[node, 'group'] = group

    ##for reptype
    #elif feat == "rep_type":
    groups_Inc = pd.DataFrame()
    for node in relationships.nodes:
        r = plasmid_info_MOB[plasmid_info_MOB['file_id'] == node]['rep_type'].iloc[0]
        #species[species['Genomes'] == ids[0]]['Species_Final'].iloc[0]
       # print (r)
        if re.match("IncL", r):
            group = 0
        elif re.match("ColRNAI_rep_cluster_1987", r):
            group = 1
        elif re.match("ColRNAI_rep_cluster_1857", r):
            group= 2
        elif re.match('IncFIB', r):
            group = 3
        elif re.match('IncR', r):
            group = 4
        elif re.match('IncFII', r):
            group = 5
        elif re.match('IncF', r):
            group = 6
        elif re.match('Inc', r):
            group=7
        elif re.match('ColRNAI', r):
            group = 8
        elif r== "rep_cluster_1150":
            group = 9
        elif r=="rep_cluster_1":
            groups=10
        else:
            group=11
        groups_Inc.loc[node, 'group'] = group

    ##for community
    #elif feat == "Community":
    communities = pd.read_csv("/home/www/resistome.cnag.cat/incredible/ani/samples_community.txt", sep="\t") # we should get this from the database instead
    groups_communities = pd.DataFrame()
    for node in relationships.nodes:
        ids = node.split('_')
        r = communities[communities['Genomes'] == ids[0]]['Community'].iloc[0]
        #print (r)
        if r == "Andalucía":
            group = 0
        elif r == "Aragón":
            group = 1
        elif r=="Asturias":
            group= 2
        elif r=="Cantabria":
            group = 3
        elif r == "Castilla y León":
            group = 4
        elif r == "Castilla-La Mancha":
            group = 5
        elif r == "Cataluña":
            group = 6
        elif r == "Ceuta":
            group = 7
        elif r == "Comunidad Valenciana":
            group = 8
        elif r == "Comunidad de Madrid":
            group = 9
        elif r == "Galicia":
            group = 10
        elif r == "Islas Baleares":
            group = 11
        elif r == "Navarra":
            group = 12
        else:
            group=13
        groups_communities.loc[node, 'group'] = group

    ##for mlst
    #elif feat == "mlst":
    species = pd.read_csv("/home/www/resistome.cnag.cat/incredible/ani/rel7_species.txt", sep="\t") ##we should get this from the db instead
    mlst = pd.read_csv("/home/www/resistome.cnag.cat/incredible/ani/rel7.mlst_final.txt", sep="\t") ## we should get this from the db instead
    groups_mlst = pd.DataFrame()
    for node in relationships.nodes:
        ids = node.split('_')
        #print (ids[0])
        spp = species[species['Genomes'] == ids[0]]['Species_Final'].iloc[0]
        r = mlst[mlst['Genomes'] == ids[0]]['MLST_Final'].iloc[0]
        #print (r)
        if spp == "Klebsiella pneumoniae":
            group_spp = 0
            if r == 11:
                group = 0
            elif r==307:
                group=1
            elif r == 147:
                group = 2
            elif r==392:
                group=3
            elif r== 15:
                group=4
            elif r==512:
                group = 5
            elif r==405:
                group=6
            elif r==5000:
                group = 7
            elif r==1961:
                group = 8
            elif r == 101:
                group =9
            elif r==326:
                group = 10
            else:
                group = 11
        elif re.match("Enterobacter", spp):
            group_spp = 1
            if r == 78:
                group = 12
            elif r==171:
                group=13
            else:
                group=14
        elif (spp=="Escherichia coli"):
            group_spp= 2
            if r==131:
                group=15
            else:
                group=16
        elif re.match('Citrobacter',spp):
            group = 17
        elif re.match('Klebsiella', spp):
            group = 18
        else:
            group=19
        groups_mlst.loc[node, 'group'] = group

    ##for carbapenemases
    #elif feat == "carbapenemase":
    carbapenemases = pd.read_csv("/home/www/resistome.cnag.cat/incredible/ani/plasmids_with_carbapenemases.txt", sep="\t") ## we should get this from the db instead
    groups_carbapenemases = pd.DataFrame()
    for node in relationships.nodes:
        if node in carbapenemases.values:
            r = carbapenemases[carbapenemases['Plasmid'] == node]['carbapenemase'].iloc[0]
            if r == 'OXA-48':
                group = 0
            elif r == 'KPC':
                group = 1
            elif r == 'VIM':
                group= 2
            elif r == 'NDM':
                group = 3
            elif r == 'IMP':
                group = 4
            elif r == 'GES':
                group = 5
        else:
            group=6
        groups_carbapenemases.loc[node, 'group'] = group

    ## now we built color maps per feature:
    val_map_relaxase = {'MOBP':0,
               'MOBF':1,
               'MOBH':2,
               'MOBQ':3,
               'MOBC':4,
               'MOBV':5,
               'MOBF,MOBP':6,
               'MOBF,MOBH':7,
               'MOBF,MOBC':8,
               'MOBP,MOBH':9,
               'MOBC,MOBP':10,
               'No MOB':11}
    reverse_map_relaxase = {v:k for k,v in val_map_relaxase.items()}

    val_map_reptype = {'IncL/M':0,
               'ColRNAI_rep_cluster_1987':1,
               'ColRNAI_rep_cluster_1857':2,
               'IncFIB':3,
               'IncR':4,
               'IncFII':5,
               'Other IncF':6,
               'Other Inc': 7,
               'Other ColRNAI' : 8,
               'rep_cluster_1150':9,
               'rep_cluster_1': 10,
               'Other rep_cluster':11}
    reverse_map_reptype = {v:k for k,v in val_map_reptype.items()}

    val_map_community = {'Andalucía':0,
               'Aragón':1,
               'Asturias':2,
               'Cantabria':3,
               'Castilla y León':4,
               'Castilla-La Mancha':5,
               'Cataluña':6,
               'Ceuta': 7,
               'Comunidad Valenciana' : 8,
               'Comunidad de Madrid':9,
               'Galicia':10,
               'Islas Baleares': 11,
               'Navarra':12,
               'Unknown':13}
    reverse_map_community = {v:k for k,v in val_map_community.items()}

    val_map_mlst = {'K.pneumoniae ST11':0,
                    'K.pneumoniae ST307':1,
                    'K.pneumoniae ST147':2,
                    'K.pneumoniae ST392':3,
                    'K.pneumoniae ST15':4,
                    'K.pneumoniae ST512':5,
                    'K.pneumoniae ST405':6,
                    'K.pneumoniae ST5000':7,
                    'K.pneumoniae ST1961':8,
                    'K.pneumoniae ST101':9,
                    'K.pneumoniae ST326':10,
                    'K.pneumoniae other':11,
                    'E.cloacae ST78':12,
                    'E.cloacae ST171':13,
                    'E.cloacae other':14,
                    'E.coli ST131':15,
                    'E.coli other':16,
                    'Citrobacter':17,
                    'Other Klebsiella':18,
                    'Other':19}
    reverse_map_mlst = {v:k for k,v in val_map_mlst.items()}

    val_map_carb = {'OXA-48':0,
                    'KPC':1,
                    'VIM':2,
                    'NDM':3,
                    'IMP':4,
                    'GES':5,
                    'None':6}
    reverse_map_carb = {v:k for k,v in val_map_carb.items()}
    t6= timer()
    # colors
    mycolors = ['grey'] + list(px.colors.qualitative.Light24)
    #palette = cycle(mycolors.append(px.colors.qualitative.Light24))
    palette = cycle(mycolors)
    edge_x = []
    edge_y = []
    #myweight=nx.get_edge_attributes(relationships,'weight')
    pos = nx.spring_layout(relationships,weight='weight',seed=107361)
    t7= timer()
    for edge in relationships.edges():
        # edge_x+=[pos[edge[0]][0],pos[edge[1]][0], None]
        # edge_y+=[pos[edge[0]][1],pos[edge[1]][1], None]
        edge_x+=[pos[edge[0]][0],pos[edge[1]][0],None]
        edge_y+=[pos[edge[0]][1],pos[edge[1]][1],None]


    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        showlegend=False,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    #Now loop through each figure

    #fig = go.Figure(data=[edge_trace, node_trace],
    right_margin = 340
    fig = go.Figure(data=[edge_trace],
            layout=go.Layout(
                legend_title='Relaxase Type',
                showlegend=True,
                hovermode='closest',
                height=700,
                margin=go.layout.Margin(b=5,l=5,r=right_margin,t=5,pad=4, autoexpand=False),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    relaxasegroups = list(reverse_map_relaxase.keys())
    relaxasegroups.reverse()
    for grp in relaxasegroups:
        node_x = []
        node_y = []
        node_text = []
        label = ''
        for node in relationships.nodes():
            if groups_relaxase.loc[node, 'group'] == grp:
                x = pos[node][0]
                y = pos[node][1]
                node_x.append(x)
                node_y.append(y)
                label = reverse_map_relaxase[groups_relaxase.loc[node]["group"]]
                node_text.append(node+":"+label)

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            # colorscale=colorscale,
            mode='markers',
            text=node_text,
            hoverinfo='text',
            showlegend=True,
            name=label,
            marker=dict(
                # colorscale='Rainbow',
                # reversescale=True,
                color=next(palette),
                size=10,
                line_width=2)))
    fig.update_layout(font=dict(size=20))
    plot_div_relaxase = plot(fig, output_type='div', include_plotlyjs=False)


#############
    palette = cycle(mycolors)
    fig2 = go.Figure(data=[edge_trace],
             layout=go.Layout(
                legend_title='Replicon',
                showlegend=True,
                hovermode='closest',
                height=700,
                margin=go.layout.Margin(b=5,l=5,r=right_margin,t=5,pad=4, autoexpand=False),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    reptypegroups = list(reverse_map_reptype.keys())
    reptypegroups.reverse()
    for grp in reptypegroups:
        node_x = []
        node_y = []
        node_text = []
        label = ''
        for node in relationships.nodes():
            if groups_Inc.loc[node, 'group'] == grp:
                x = pos[node][0]
                y = pos[node][1]
                node_x.append(x)
                node_y.append(y)
                label = reverse_map_reptype[groups_Inc.loc[node]["group"]]
                node_text.append(node+":"+label)

        fig2.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            text=node_text,
            hoverinfo='text',
            showlegend=True,
            name=label,
            marker=dict(
                # colorscale='Rainbow',
                # reversescale=True,
                color=next(palette),
                size=10,
                line_width=2)))
    fig2.update_layout(font=dict(size=20))
    plot_div_reptype = plot(fig2, output_type='div', include_plotlyjs=False)

#############
    palette = cycle(mycolors)
    fig3 = go.Figure(data=[edge_trace],
             layout=go.Layout(
                legend_title='Community',
                showlegend=True,
                hovermode='closest',
                height=700,
                margin=go.layout.Margin(b=5,l=5,r=right_margin,t=5,pad=4, autoexpand=False),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    communitygroups = list(reverse_map_community.keys())
    communitygroups.reverse()
    for grp in communitygroups:
        node_x = []
        node_y = []
        node_text = []
        label = ''
        for node in relationships.nodes():
            if groups_communities.loc[node, 'group'] == grp:
                x = pos[node][0]
                y = pos[node][1]
                node_x.append(x)
                node_y.append(y)
                label = reverse_map_community[groups_communities.loc[node]["group"]]
                node_text.append(node+":"+label)

        fig3.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            text=node_text,
            hoverinfo='text',
            showlegend=True,
            name=label,
            marker=dict(
                # colorscale='Rainbow',
                # reversescale=True,
                color=next(palette),
                size=10,
                line_width=2)))
    fig3.update_layout(font=dict(size=20))
    plot_div_communities = plot(fig3, output_type='div', include_plotlyjs=False)

#############
    palette = cycle(mycolors)
    fig4 = go.Figure(data=[edge_trace],
             layout=go.Layout(
                legend_title='Sequence Type',
                showlegend=True,
                hovermode='closest',
                height=700,
                margin=go.layout.Margin(b=5,l=5,r=right_margin,t=5,pad=4, autoexpand=False),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    mlstgroups = list(reverse_map_mlst.keys())
    mlstgroups.reverse()
    for grp in mlstgroups:
        node_x = []
        node_y = []
        node_text = []
        label = ''
        for node in relationships.nodes():
            if groups_mlst.loc[node, 'group'] == grp:
                x = pos[node][0]
                y = pos[node][1]
                node_x.append(x)
                node_y.append(y)
                label = reverse_map_mlst[groups_mlst.loc[node]["group"]]
                node_text.append(node+":"+label)

        fig4.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            text=node_text,
            hoverinfo='text',
            showlegend=True,
            name=label,
            marker=dict(
                # colorscale='Rainbow',
                # reversescale=True,
                color=next(palette),
                size=10,
                line_width=2)))
    fig4.update_layout(font=dict(size=20))
    plot_div_mlst = plot(fig4, output_type='div', include_plotlyjs=False)

#############
    palette = cycle(mycolors)
    fig5 = go.Figure(data=[edge_trace],
             layout=go.Layout(
                legend_title='Carbapenemase',
                showlegend=True,
                hovermode='closest',
                height=700,
                margin=go.layout.Margin(b=5,l=5,r=right_margin,t=5,pad=4, autoexpand=False),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    carbgroups = list(reverse_map_carb.keys())
    carbgroups.reverse()
    for grp in carbgroups:
        node_x = []
        node_y = []
        node_text = []
        label = ''
        for node in relationships.nodes():
            if groups_carbapenemases.loc[node, 'group'] == grp:
                x = pos[node][0]
                y = pos[node][1]
                node_x.append(x)
                node_y.append(y)
                label = reverse_map_carb[groups_carbapenemases.loc[node]["group"]]
                node_text.append(node+":"+label)

        fig5.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            text=node_text,
            hoverinfo='text',
            showlegend=True,
            name=label,
            marker=dict(
                # colorscale='Rainbow',
                # reversescale=True,
                color=next(palette),
                size=10,
                line_width=2)))
    fig5.update_layout(font=dict(size=20))
    plot_div_carb = plot(fig5, output_type='div', include_plotlyjs=False)
    t8= timer()
    debug = debug + str(timedelta(seconds=t2-t1)) + "\n"
    debug = debug + str(timedelta(seconds=t3-t2)) + "\n"
    debug = debug + str(timedelta(seconds=t4-t3)) + "\n"
    debug = debug + str(timedelta(seconds=t5-t4)) + "\n"
    debug = debug + str(timedelta(seconds=t6-t5)) + "\n"
    debug = debug + str(timedelta(seconds=t7-t6)) + "\n"
    debug = debug + str(timedelta(seconds=t8-t7)) + "\n"
    #scaffolds_table = ScaffoldsTable(filtered_set)
    context = { "plot_div_relaxase": plot_div_relaxase,
                "plot_div_reptype": plot_div_reptype,
                "plot_div_communities": plot_div_communities,
                "plot_div_mlst": plot_div_mlst,
                "plot_div_carb": plot_div_carb,
                'filter': f,
                #'table': scaffolds_table,
                'debug':debug
               }
    return render(request, "ani.html", context)

# @permission_required("resistome.view_sample", login_url='access_denied')
def spain_map_filter(request):

    colors = ['rgb(189,189,189)', 'rgb(218, 30, 55)', 'rgb(189, 31, 54)', 'rgb(167, 30, 52)', 'rgb(133, 24, 42)', 'rgb(100, 18, 32)',
              'rgb(55, 119, 255)', 'rgb(251, 139, 36)', 'rgb(42, 157, 143)', 'rgb(102, 46, 155)', 'rgb(147, 129, 255)', 'rgb(255, 216, 190)']
    species = {0: 'All', 1: 'Klebsiella pneumoniae', 2: 'Klebsiella oxytoca', 3: 'Klebsiella variicola', 4: 'Klebsiella aerogenes', 5: 'Klebsiella quasipneumoniae',
               6: 'Enterobacter cloacae complex', 7: 'Serratia marcescens', 8: 'Escherichia coli', 9: 'Citrobacter freundii', 10: 'Citrobacter koseri', 11: 'Raoultella ornithinolytica'}

    fig = go.Figure(go.Scattergeo())
    columns = ['Location', 'Lat', 'Lon', 'Species', 'Value']
    rows = []
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
                # text = '<a href="https://denovo.cnag.cat:8080/samples/">' + df_spec['Location'] + ": " + df_spec['Value'].map('{:.0f}'.format).astype(str) + '</a>',
                text=df_spec['Location'] + ": " + df_spec['Value'].map('{:.0f}'.format).astype(str), hoverinfo='location + name + text',
                name=species[i],
                marker=dict(
                    size=(df_spec['Value'] * 100),
                    sizemode='area',
                    color=colors[i],
                    line_width=0.5,
                    opacity=0.75
                )))

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
        legend_itemsizing='trace',
        height=600,
        width=800
    )


    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #context['plot'] = plot_div
    sample_table = SampleTable(filtered_set)
    context = {"plot": plot_div,
               'filter': f,
               'table': sample_table
               }
    return render(request, "map_filter.html", context)


# @permission_required("resistome.view_sample", login_url='access_denied')
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
    scaffolds = Scaffold.objects.filter(assembly=ass.pk).annotate(all_genes=Count('gene_set'),num_genes=Count(
        'gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
    hosp = None
    maploc = " "
    age = " "
    if sample.isolation_location:
        hosp = IsolationLocation.objects.get(name=sample.isolation_location)
        maploc = mark_safe("<a target='_blank' href='http://www.google.com/maps/place/" + str(
            hosp.latitude) + "," + str(hosp.longitude) + "'>" + str(sample.isolation_location) + "</a>")
    age = str(int(sample.patient_data_age))
    carbapenemase_list = mark_safe(', '.join(b.name if ("Negative" in b.name or "Conflict" in b.name or "Broken" in b.name) else "<a href='/incredble/genes/?sample_barcode=" + sample.barcode + '&amrf_set__gene_symbol=' + b.name.replace("Broken ","") + "'>" + b.name + "</a>"  for b in sample.carbapenemase.all()))

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
            {'Name': 'Carbapenamase type(s)', 'Value': carbapenemase_list},
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

# class SampleListView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
class SampleListView(ExportMixin, SingleTableMixin, FilterView):
    # permission_required = "resistome.view_sample"
    # login_url = "access_denied"
    model = Sample
    table_class = SampleTable
    template_name = 'samples.html'
    filterset_class = SampleFilter
    table_pagination = {"per_page": 15}
    def render_to_response(self, context, **response_kwargs):
        response = super(SampleListView, self).render_to_response(context, **response_kwargs)
        response.set_cookie('CRE', 'uq4QeBPJRR9wRUV4')
        return response

# class AssemblyListView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
class AssemblyListView(ExportMixin, SingleTableMixin, FilterView):
    # permission_required = "resistome.view_sample"
    # login_url = "access_denied"
    model = Assembly
    table_class = AssemblyTable
    template_name = 'assemblies.html'
    filterset_class = AssemblyFilter
    table_pagination = {"per_page": 15}

    def render_to_response(self, context, **response_kwargs):
        response = super(AssemblyListView, self).render_to_response(context, **response_kwargs)
        response.set_cookie('CRE', 'uq4QeBPJRR9wRUV4')
        return response

# @permission_required("resistome.view_scaffold", login_url='access_denied')
def ScaffoldView(request, scaffold):
    scaff = Scaffold.objects.filter(scaffold=scaffold).annotate(num_genes=Count('gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))),all_genes=Count('gene_set'))
    sample = scaff[0].sample
    scaff_table = ScaffoldsTable(scaff)
    centrifuge = Centrifuge.objects.filter(scaffold=scaff[0].pk)
    centrifuge_table = CentrifugeTable(centrifuge)
    context = {"sample": sample,
               "scaffold_table": scaff_table,
               "centrifuge_table": centrifuge_table,
               "scaffold": scaff[0],
               }
    response = render(request, "scaffold.html", context)
    return render(request, "scaffold.html", context)

# class ScaffoldListView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
class ScaffoldListView(ExportMixin, SingleTableMixin, FilterView):
    # permission_required = "resistome.view_scaffold"
    # login_url = "access_denied"
    model = Scaffold
    table_class = ScaffoldsTable
    template_name = 'scaffold_list.html'
    filterset_class = ScaffoldFilter
    table_pagination = {"per_page": 50}
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(num_genes=Count('gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))),all_genes=Count('gene_set'))
        #return qs.annotate(num_genes=Count(
        #    'gene_set', filter=(Q(gene_set__rgi='Yes') | Q(gene_set__amrf='Yes'))))
    def render_to_response(self, context, **response_kwargs):
        response = super(ScaffoldListView, self).render_to_response(context, **response_kwargs)
        response.set_cookie('CRE', 'uq4QeBPJRR9wRUV4')
        return response

# class AnnotationListView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
class AnnotationListView(ExportMixin, SingleTableMixin, FilterView):
    # permission_required = "resistome.view_annotation"
    # login_url = "access_denied"
    model = Annotation
    table_class = AnnotationListTable
    template_name = 'annotation.html'
    filterset_class = AnnotationFilter
    table_pagination = {"per_page": 50}

    def render_to_response(self, context, **response_kwargs):
        response = super(AnnotationListView, self).render_to_response(context, **response_kwargs)
        response.set_cookie('CRE', 'uq4QeBPJRR9wRUV4')
        return response

# class AnnotationCoordsView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
class AnnotationCoordsView(ExportMixin, SingleTableMixin, FilterView):
    # permission_required = "resistome.view_annotation"
    # login_url = "access_denied"
    model = Annotation
    table_class = AnnotationCoordsTable
    template_name = 'coords.html'
    filterset_class = AnnotationFilter
    table_pagination = {"per_page": 50}

    def render_to_response(self, context, **response_kwargs):
        response = super(AnnotationCoordsView, self).render_to_response(context, **response_kwargs)
        response.set_cookie('CRE', 'uq4QeBPJRR9wRUV4')
        return response


# @permission_required("resistome.view_sample", login_url='access_denied')
def AnnotationFastaView(request):
    genes = Annotation.objects.all()
    for filter_field in request.GET.keys():
        if request.GET.get(filter_field):
            ff = filter_field
            if (ff == 'st'):
                ff = 'scaffold__assembly__mlst__st'
                genes = genes.filter(**{ff: request.GET.get(filter_field)})
            elif (ff == 'scaffold'):
                ff = 'scaffold__scaffold'
                genes = genes.filter(**{ff: request.GET.get(filter_field)})
            elif (ff == 'resistance'):
                genes = genes.filter(Q(rgi='Yes') | Q(amrf='Yes'))
            elif (ff == 'page'):
                pass
            elif (ff == 'sort'):
                pass
            else:
                genes = genes.filter(**{ff: request.GET.get(filter_field)})
    fasta = ''
    count = 1
    def insert_newlines(string, every=80):
        return '\n'.join(string[i:i+every] for i in range(0, len(string), every))
    def xstr(s):
        if s is None:
            return ''
        return str(s)

    for g in genes[:10000]:
        mlst = MLST.objects.filter(assembly=g.scaffold.assembly)
        seq = insert_newlines(g.protein_sequence)
        fasta += ">"+g.gene +"|"+ xstr(g.gene_name) +"|"+ xstr(g.roary_gene) +"|ST"+ xstr(mlst[0].st) +"\n" + seq + "\n"
        count+=1
        if count>10000:
            break

    return HttpResponse(fasta, content_type="text/plain")

# @permission_required("resistome.view_sample", login_url='access_denied')
def AnnotationCoordView(request):
    genes = Annotation.objects.all()
    for filter_field in request.GET.keys():
        if request.GET.get(filter_field):
            ff = filter_field
            if (ff == 'st'):
                ff = 'scaffold__assembly__mlst__st'
                genes = genes.filter(**{ff: request.GET.get(filter_field)})
            elif (ff == 'scaffold'):
                ff = 'scaffold__scaffold'
                genes = genes.filter(**{ff: request.GET.get(filter_field)})
            elif (ff == 'resistance'):
                genes = genes.filter(Q(rgi='Yes') | Q(amrf='Yes'))
            elif (ff == 'page'):
                pass
            elif (ff == 'sort'):
                pass
            else:
                genes = genes.filter(**{ff: request.GET.get(filter_field)})
    tsv = ''

    def xstr(s):
        if s is None:
            return ''
        return str(s)

    for g in genes:
        mlst = MLST.objects.filter(assembly=g.scaffold.assembly)
        separator = '\t'
        tsv += separator.join([g.scaffold.scaffold,str(g.start),str(g.end),g.orientation,xstr(g.roary_gene),xstr(g.scaffold.sample.barcode),xstr(mlst[0].st)]) +"\n"


    return HttpResponse(tsv, content_type="text/plain")

# @permission_required("resistome.view_annotation", login_url='access_denied')
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
        {'Name': 'Browse', 'Value': mark_safe('<a href="https://genomes.cnag.cat/genomes/cre/browse/?loc=' + location_string + \
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
        {'Name': 'Roary Gene Group', 'Value': mark_safe('<a href="/incredble/genes/?roary_gene=' + str(
            annotation.roary_gene) + '">' + str(annotation.roary_gene) + '</a>')},
        {'Name': 'Roary Core Annotation', 'Value': str(
            annotation.roary_core)},

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

def EnrichmentView(request, sequence_type=None, species=None):

    try:
        species_qs = Species.objects.filter(name='Klebsiella pneumoniae')
        speciesobj = species_qs[0]
    except Species.DoesNotExist:
        speciesobj = None
    try:
        mlst_qs = MLST.objects.filter(st='15')
        mlstobj = mlst_qs[0]
    except Species.DoesNotExist:
        mlstobj  = None

    test_total = Sample.objects.filter(species=speciesobj,assembly__mlst__st=mlstobj.st).count()
    control_total = Sample.objects.filter(species=speciesobj).exclude(assembly__mlst__st=mlstobj.st).count()
    return_text = ''
    roary_groups = RoaryGroup.objects.filter(species=speciesobj)
    myTuple = ('ST','roary_gene', 'ST_positive','ST_total','ST_proportion','rest_positive','rest_total','rest_proportion','Fisher_exact_pvalue_two-sided')
    return_text += ("\t".join(myTuple) + "\n")

    for rg in roary_groups:
        test_pos = Annotation.objects.filter(roary_gene=rg.roary_gene,scaffold__assembly__mlst__st=mlstobj.st).values('scaffold__assembly').distinct().count()
        control_pos = Annotation.objects.filter(roary_gene=rg.roary_gene).exclude(scaffold__assembly__mlst__st=mlstobj.st).values('scaffold__assembly').distinct().count()
        test_neg = test_total - test_pos
        control_neg = control_total - control_pos
        if ((test_pos/test_total > 0.8) and (control_pos/control_total < 0.2)):
            oddsratio, pvalue = stats.fisher_exact([[test_pos, control_pos], [test_neg, control_neg]],alternative='two-sided')
            if (pvalue < 0.05):
                myTuple = (str(mlstobj.st),rg.roary_gene, str(test_pos),str(test_total),str(test_pos/test_total),str(control_pos),str(control_total),str(control_pos/control_total),str(pvalue))
                return_text += ("\t".join(myTuple) + "\n")


    return HttpResponse(return_text, content_type="text/plain")
