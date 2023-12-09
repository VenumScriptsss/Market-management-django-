from django.db import models
from adminPanel.models import productsModel,soldModel,categoryModel
from datetime import datetime
# Create your models here.

class saleModel(models.Model):
	saleProducts = models.ManyToManyField(productsModel)
	saleDate = models.DateTimeField(verbose_name="date d'encaissement",auto_now_add=True)
	saleQuantityStr = models.CharField(verbose_name="chaine de quantites des produits vendu", max_length=80)
	salePrice = models.IntegerField(verbose_name = "prix total de vend", null=False, default = 0)



	def __str__(self):
		#return self.saleDate.strftime("%Y:%m:%d:%H:%M")
		return str(self.id)

	class Meta:
		ordering = ['saleDate']

""" class saleProducts(models.Model):
	saleProductName = models.CharField(verbose_name='nom produit vendu', max_length=50, null=False)
	saleProductId = 
	saleProdQuantity = models.IntegerField(verbose_name="quantiter vendu de produit", default=1)
	sale = models.ForeignKey(saleModel)
	
	
	def __str__(self):
		return self..productname
 """