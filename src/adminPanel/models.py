from unicodedata import name
from django.db import models
from datetime import datetime


# Create your models here.
class soldModel(models.Model):
	sold_productid			= models.IntegerField(verbose_name='produit id', unique=True)
	sold_productname		= models.CharField(verbose_name='nom produit', max_length=50, null=False)
	sold_starting_date		= models.DateField(verbose_name='date debut Sold')
	sold_ending_date		= models.DateField(verbose_name='date fin Sold')
	sold_price				= models.IntegerField(verbose_name='prix Sold', default=0)
	sold_soldProducts		= models.IntegerField(verbose_name='quantité des produits vendu on Sold',default=0)
	sold_active				= models.BooleanField(verbose_name='sold actif', default=False)
	def __str__(self):
		return self.sold_productname

	class Meta:
		ordering = ['sold_starting_date']
		verbose_name = 'sold'
		verbose_name_plural = 'solded products'



class productsModel(models.Model):
	#product_id = models.AutoField(verbose_name='id',primary_key=True)
	productname 		= models.CharField(verbose_name='nom produit', max_length=50, null=False, unique= True)
	quantity			= models.IntegerField(verbose_name='quantité', null=True)
	date_delivered		= models.DateField(verbose_name='date arrivé', auto_now_add= True)
	date_ex				= models.DateField(verbose_name='date primé')
	suplier				= models.CharField(verbose_name='livrer par', max_length=50)
	category			= models.CharField(verbose_name='categorie', max_length=50, default='autre')
	price				= models.IntegerField(verbose_name='prix',null=False, default='0')
	sold				= models.BooleanField(verbose_name='solder', default=False)
	purchasePrx			= models.IntegerField(null=False,default=-1)
	unityPerBox			= models.IntegerField(null = False,default=10)
	unitsSold_thisMonth = models.CharField(verbose_name='uniter vendue ce mois',max_length=20,null=False)

	def __str__(self):
		return self.productname

	class Meta:
		ordering = ['date_delivered']
		verbose_name = 'stock'
		verbose_name_plural = 'products'


	def monthlyReset(currMonth):
		prods = productsModel.objects.all()
		for prod in prods:
			prod.unitsSold_thisMonth = "0."+str(currMonth)


class categoryModel(models.Model):
	categoryname = models.CharField(verbose_name='nom category', max_length=50, null=False,unique=True)
	#length = models.IntegerField(verbose_name='nombre des produits dans la categorie', default=0)


	def __str__(self):
		return self.categoryname

""" 	class Meta:
		ordering = ['length']
		verbose_name = 'categorie'
		verbose_name_plural = 'les categories' """


class SchedualedSpends(models.Model):
	name		= models.CharField(verbose_name='nom de la depence programmer',max_length=50, null=False)
	amount 		= models.IntegerField(verbose_name='montant de la depence',null=False)
	dateDelv 	= models.DateField(verbose_name='date programmer pour la depence')
	
	def	__str__(self):
		return self.name
	
