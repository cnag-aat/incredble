
from resistome.models import *
from rest_framework import viewsets
from resistome.serializers import *
from rest_framework_bulk import BulkModelViewSet


class SpeciesViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    filter_fields = '__all__'


class CarbapenemaseViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Carbapenemase.objects.all()
    serializer_class = CarbapenemaseSerializer
    filter_fields = '__all__'


class BiologicalSampleOfIsolationViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = BiologicalSampleOfIsolation.objects.all()
    serializer_class = BiologicalSampleOfIsolationSerializer
    filter_fields = '__all__'


class HospitalAdmissionUnitViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HospitalAdmissionUnit.objects.all()
    serializer_class = HospitalAdmissionUnitSerializer
    filter_fields = '__all__'


class IsolationLocationViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = IsolationLocation.objects.all()
    serializer_class = IsolationLocationSerializer
    filter_fields = '__all__'


class SampleViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_fields = '__all__'


class CLSIViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CLSI.objects.all()
    serializer_class = CLSISerializer
    filter_fields = '__all__'


class EUCASTViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = EUCAST.objects.all()
    serializer_class = EUCASTSerializer
    filter_fields = '__all__'


class AssemblyViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    filter_fields = ['sample','assembly','total_scaffolds','circular_scaffolds']


class DataFilesViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DataFiles.objects.all()
    serializer_class = DataFilesSerializer
    filter_fields = '__all__'


class ScaffoldViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Scaffold.objects.all()
    serializer_class = ScaffoldSerializer
    filter_fields = '__all__'


class AnnotationViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    filter_fields = '__all__'


class RgiViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Rgi.objects.all()
    serializer_class = RgiSerializer
    filter_fields = '__all__'


class MLSTViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MLST.objects.all()
    serializer_class = MLSTSerializer
    filter_fields = '__all__'


class SpeciesVerificationViewSet(BulkModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SpeciesVerification.objects.all()
    serializer_class = SpeciesVerificationSerializer
    filter_fields = '__all__'
