from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.SelectDateWidget
    )
    end_date = forms.DateField(
        label='End Date',
        widget=forms.SelectDateWidget
    )
    channel = forms.CharField(
        label='Channel Name',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(DateRangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.helper.form_method = 'GET'
        self.helper.form_class = 'form form-horizontal'
        self.helper.label_class = 'col-sm-4 col-md-2'
        self.helper.field_class = 'col-sm-4 col-md-4'
        self.helper.add_input(Submit('Search', 'Search'))


class TelegramLoginCodeForm(forms.Form):
    login_code = forms.CharField(
        label='Enter the code sent to your phone',
        required=True
    )
