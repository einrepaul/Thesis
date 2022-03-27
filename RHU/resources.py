from import_export import resources
from import_export.fields import Field
from RHU.models import MedicalInfo

class MedicalInfoResource(resources.ModelResource):

    class Meta:
        model = MedicalInfo
        exclude = ('id',)
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('caseNumber',)
        fields = ('caseNumber', 'patient', 'age', 'sex', 
                'civilStatus', 'barangay', 'temperature', 'pulse', 'respiration', 
                'bloodPressure', 'bloodType', 'height', 'weight', 'comments')
        