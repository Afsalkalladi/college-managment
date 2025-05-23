from django import forms
from .models import TeacherResource
from apps.academics.models import Subject, AcademicYear

class TeacherResourceForm(forms.ModelForm):
    class Meta:
        model = TeacherResource
        fields = ['subject', 'title', 'description', 'resource_type', 'file', 'external_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'external_link': forms.URLInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            # Get current academic year
            current_year = AcademicYear.objects.filter(is_current=True).first()
            if current_year:
                # Filter subjects to show only assigned subjects
                assigned_subjects = Subject.objects.filter(
                    teacherassignment__teacher=teacher,
                    teacherassignment__academic_year=current_year,
                    teacherassignment__is_active=True
                )
                self.fields['subject'].queryset = assigned_subjects
    
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        external_link = cleaned_data.get('external_link')
        
        if not file and not external_link:
            raise forms.ValidationError("Please provide either a file or an external link.")
        
        if file and external_link:
            raise forms.ValidationError("Please provide either a file or an external link, not both.")
        
        return cleaned_data