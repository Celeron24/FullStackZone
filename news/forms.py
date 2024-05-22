from django import forms

class RSSFeedSearchForm(forms.Form):
    query = forms.CharField(label='Query', max_length=100, widget=forms.DateInput(attrs={
                                                                                    'class': 'form-control'}))

    start_date = forms.DateField(label='Start Date', input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={
                                                                                    'type': 'date',
                                                                                    'class': 'form-control me-5'}))

    end_date = forms.DateField(label='End Date',  input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={
                                                                                    'type': 'date',
                                                                                    'class': 'form-control'}))


class ArchiveNewsSearchForm(forms.Form):
    filter_archive_date = forms.DateField(label='Archive Date', required=False, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={
                                                                                    'type': 'date',
                                                                                    'class': 'form-control'}))