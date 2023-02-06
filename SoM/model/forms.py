from django import forms

class BeamForm(forms.Form):
    unit_choices = (
        ('1', 'm'),
        ('2', 'mm'),
        ('3', 'in'),
        ('4', 'ft'),
    )
    len=forms.FloatField()
    unit_1=forms.ChoiceField(choices=unit_choices)
    f=forms.FloatField()
    ft=forms.FloatField()
    w=forms.FloatField()
    wt=forms.FloatField()
    unit_2=forms.ChoiceField(choices=unit_choices)


class SupportForm(forms.Form):
    a=forms.FloatField()
    b=forms.FloatField()