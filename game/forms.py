# game/forms.py

from django import forms


class JeuForm(forms.Form):
   compte1 = forms.CharField()
   message = forms.CharField(max_length=1000)
    
class FormulaireForm(forms.Form):
    name = forms.CharField(max_length=100)


    


