from django.urls import path
from . import views
from resistome.views import SampleListView
# from resistome.views import GeneListView
from resistome.views import AnnotationListView
from resistome.views import ScaffoldListView
from resistome.views import HomeView
from resistome.views import AccessDeniedView
from resistome.views import BlastView
from resistome.views import TreeView
from resistome.views import SideBar
#from resistome.views import JbrowseView
urlpatterns = [
    path("samples/", SampleListView.as_view(), name="sample_list"),
    path("", HomeView.as_view(), name="home"),
    path("<int:pk>/", views.sample_detail, name="sample_detail"),
    path("samples/?barcode=<barcode>", views.sample_detail, name="barcode_detail"),
    # path("genes_old/", GeneListView.as_view(), name="gene_list_old"),
    path("genes/", AnnotationListView.as_view(), name="gene_list"),
    path("genes/scaffold/<scaffold>/", views.gene_list_filtScaffold, name="gene_list_filtScaffold"),
    path("genes/<int:pk>/", views.gene_detail, name="gene_detail"),
    path("genes/<gene>/", views.gene_detail, name="gene_detail"),
    path("scaffold/<scaffold>", views.ScaffoldView, name="scaffold_detail"),
    path("scaffolds/", ScaffoldListView.as_view(), name="scaffold_list"),
    path("map/", views.spain_map_filter, name="spain_map_filter"),
    path('access_denied/', AccessDeniedView.as_view(), name="access_denied"),
    path("blast/", BlastView.as_view(), name="blast"),
    path("tree/", TreeView.as_view(), name="tree"),
    path("sidebar/", SideBar.as_view(), name="sidebar"),
    path('charts/', views.charts, name='charts'),
    #path("genomes/cre/browse/", JbrowseView.as_view(), name="jbrowse"),
]
