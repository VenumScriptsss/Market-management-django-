from django import forms

from adminPanel.models import productsModel

class createProductFrom(forms.ModelForm):

	class Meta:
		model= productsModel
		fields= ['productname', 'quantity', 'date_ex', 'category', 'price','suplier', ]

	
