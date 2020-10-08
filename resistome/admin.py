from django.contrib import admin
from django.contrib.admin.decorators import register
from resistome.models import *
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=samples.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    #field_names = queryset.keys()
    for obj in queryset:
        row =[]
        for name in obj._meta.fields:
            try:
                row.append(str(getattr(property, name)))
            except:
                row.append(" ")
        writer.writerow(row)
    return response
export_csv.short_description = "Export CSV"

@register(RelaxaseType)

@register(RepliconType)

@register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', )


@register(Carbapenemase)


@register(BiologicalSampleOfIsolation)
class BiologicalSampleOfIsolationAdmin(admin.ModelAdmin):
    list_display = ('name', )


@register(HospitalAdmissionUnit)
class HospitalAdmissionUnitAdmin(admin.ModelAdmin):
    list_display = ('name', )


@register(IsolationLocation)
class IsolationLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'community')


@register(Sample)
class SampleAdmin(admin.ModelAdmin):
##    actions = [export_csv]
    search_fields = ('barcode', 'name')


@register(CLSI)
class CLSIAdmin(admin.ModelAdmin):
    list_display = (
        'sample',
        'piper',
        'pt',
        'ctx',
        'caz',
        'caz_avi',
        'cef',
        'azt',
        'mem',
        'imi',
        'imi_rele',
        'ert',
        'fosfo',
        'genta',
        'tobra',
        'amk',
        'cip',
        'colis',
    )
    autocomplete_fields = ('sample', )
    search_fields = ('sample__barcode', )


@register(EUCAST)
class EUCASTAdmin(admin.ModelAdmin):
    list_display = (
        'sample',
        'piper',
        'pt',
        'ctx',
        'caz',
        'caz_avi',
        'cef',
        'azt',
        'mem',
        'imi',
        'imi_rele',
        'ert',
        'fosfo',
        'genta',
        'tobra',
        'amk',
        'cip',
        'colis',
    )
    autocomplete_fields = ('sample', )
    search_fields = ('sample__barcode', )


@register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    list_display = (
        'assembly',
        'sample',
        'total_scaffolds',
        'circular_scaffolds',
        'circularity_ratio',
        'scaffolds_2kb_or_shorter',
        'assembly_length',
        'max_scaffold_length',
        'assembler',
        'image',
        )
    autocomplete_fields = ('sample', )
    search_fields = ('sample__barcode', 'assembly', )

@register(DataFiles)
class DataFilesAdmin(admin.ModelAdmin):
    list_display = (
        'assembly',
        'assembly_fasta',
        'annotation_protein_fasta',
        'annotation_transcript_fasta',
        'annotation_gff',
        )
    autocomplete_fields = ('assembly', )
    search_fields = ('assembly', )

@register(Scaffold)
class ScaffoldAdmin(admin.ModelAdmin):
    # list_display = (
    #     'sample',
    #     'assembly',
    #     'scaffold',
    #     'jbrowse_link',
    #     'scaffold_length',
    #     'depth',
    #     'circular',
    #     'centrifuge_species',
    #     'centrifuge_seq',
    #     'relaxase_type',
    #     'replicon_type',
    #     'mash_neighbor_cluster'
    #     )
    autocomplete_fields = ('sample', 'assembly', )
    search_fields = ('scaffold', 'sample__barcode', 'assembly__assembly', 'assembly__sample__barcode')


@register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = (
        'scaffold',
        'start',
        'end',
        'orientation',
        'gene',
        'gene_name',
        'rgi',
        'ec_number',
        'product',
        'inference',
        'jbrowse_link',
        'protein_sequence',
        )
    autocomplete_fields = ('scaffold', )
    search_fields = ('scaffold__scaffold', 'gene', )


@register(Rgi)
class RgiAdmin(admin.ModelAdmin):
    list_display = (
        'annotation',
        'gene',
        'complete',
        'start_type',
        'rbs_motif',
        'rbs_spacer',
        'gc_cont',
        'cut_off',
        'pass_bitscore',
        'best_hit_bitscore',
        'best_hit_aro',
        'best_identities',
        'aro',
        'model_type',
        'snps_in_best_hit_aro',
        'other_snps',
        'drug_class',
        'rgi_resistance_mechanism',
        'resistance_mechanism',
        'amr_gene_family',
        'predicted_dna',
        'predicted_protein',
        'card_protein_sequence',
        'percentage_length_of_reference_sequence',
        )
    raw_id_fields = ('annotation', )
    search_fields = ('annotation__scaffold__assembly__sample__barcode', 'annotation__scaffold__scaffold', 'gene', )

@register(AMRF)
class AMRFAdmin(admin.ModelAdmin):
    list_display = (
        'annotation',
        'gene',
        'gene_symbol',
        'sequence_name',
        'scope',
        'amrf_element_type',
        'element_type',
        'element_subtype',
        'amrfclass',
        'amrf_class',
        'amrf_subclass',
        'method',
        'target_length',
        'reference_sequence_length',
        'pct_coverage_of_reference_sequence',
        'pct_identity_to_reference_sequence',
        'alignment_length',
        'accession_of_closest_sequence',
        'name_of_closest_sequence',
        'hmm_id',
        'hmm_description',
        )
    raw_id_fields = ('annotation', )
    search_fields = ('annotation__scaffold__assembly__sample__barcode', 'annotation__scaffold__scaffold', 'gene', )

@register(MLST)
class MLSTAdmin(admin.ModelAdmin):
    list_display = (
        'assembly',
        'pubmlst',
        'st',
        'alleles',
        )
    autocomplete_fields = ('assembly', )
    search_fields = ('assembly__sample__barcode', 'assembly__assembly', )

@register(Centrifuge)
class CentrifugeAdmin(admin.ModelAdmin):
    list_display = (
        'scaffold',
        'centrifuge_species',
        'centrifuge_seq',
        )
    autocomplete_fields = ('scaffold', )
    search_fields = ('scaffold__sample__barcode', 'scaffold__assembly', )

@register(SpeciesVerification)
class SpeciesVerificationAdmin(admin.ModelAdmin):
    list_display = (
        'sample',
        'illumina_sp',
        'ont_sp',
        'lims_sp',
        'seq_agreement',
        'verified',
        )
    autocomplete_fields = ('sample', )
    search_fields = ('sample__barcode', )

@register(AmrfClass)
class AmrfClass(admin.ModelAdmin):
    list_display = ('name', )


class MyUserAdmin(UserAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
    group.short_description = 'Groups'
    list_filter = UserAdmin.list_filter + ('groups__name',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'group')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
