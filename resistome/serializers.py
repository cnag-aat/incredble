from rest_framework import serializers
from resistome.models import *
from rest_framework_bulk import BulkSerializerMixin


class SpeciesSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Species
        fields = '__all__'


class CarbapenemaseSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Carbapenemase
        fields = '__all__'


class BiologicalSampleOfIsolationSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BiologicalSampleOfIsolation
        fields = '__all__'


class HospitalAdmissionUnitSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HospitalAdmissionUnit
        fields = '__all__'


class IsolationLocationSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IsolationLocation
        fields = '__all__'


class SampleSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'


class CLSISerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CLSI
        fields = '__all__'


class EUCASTSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EUCAST
        fields = '__all__'


class AssemblySerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assembly
        fields = '__all__'


class DataFilesSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataFiles
        fields = '__all__'


class ScaffoldSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scaffold
        fields = '__all__'


class AnnotationSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'


class RgiSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rgi
        fields = '__all__'


class MLSTSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MLST
        fields = '__all__'


class SpeciesVerificationSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpeciesVerification
        fields = '__all__'
