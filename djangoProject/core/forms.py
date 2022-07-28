from django import forms

from core.models import Staff, Criteria, IntegralYear


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name']


class CriteriaForm(forms.ModelForm):
    class Meta:
        model = Criteria
        fields = ['title']


class IntegralYearForm(forms.ModelForm):
    class Meta:
        model = IntegralYear
        fields = ['title',
                  'value_product', 'fond_zp', 'average_annual_value_capital', 'average_annual_value_fond',
                  'w', 'average_zp',
                  'profit_before_tax']
