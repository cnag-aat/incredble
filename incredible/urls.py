"""incredible URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from resistome import api
from django.conf.urls import url


# API Endpoints
router = routers.DefaultRouter()
router.register(r'species', api.SpeciesViewSet)
router.register(r'carbapenemase', api.CarbapenemaseViewSet)
router.register(r'biologicalsampleofisolation', api.BiologicalSampleOfIsolationViewSet)
router.register(r'hospitaladmissionunit', api.HospitalAdmissionUnitViewSet)
router.register(r'isolationlocation', api.IsolationLocationViewSet)
router.register(r'sample', api.SampleViewSet)
router.register(r'clsi', api.CLSIViewSet)
router.register(r'eucast', api.EUCASTViewSet)
router.register(r'assembly', api.AssemblyViewSet)
router.register(r'datafiles', api.DataFilesViewSet)
router.register(r'scaffold', api.ScaffoldViewSet)
router.register(r'annotation', api.AnnotationViewSet)
router.register(r'rgi', api.RgiViewSet)
router.register(r'mlst', api.MLSTViewSet)
router.register(r'speciesverification', api.SpeciesVerificationViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #path("", SampleListView.as_view(), name="home"),
    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include("resistome.urls")),
    url(r'^accounts/', include('allauth.urls')),

    #path('', RedirectView.as_view(url='admin/', permanent=False), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
