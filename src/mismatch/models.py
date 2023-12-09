from django.db import models

# Create your models here.

class products(models.Model):

	name = models.CharField(max_length=20, null=False)
	date_deliverd = models.DateField()
	date_exe = models.DateField()	
	quantity = models.IntegerField(blank=True)
	suplier = models.CharField(max_length = 30, null = False)
	
	def __str__(self):
		return self.name
	
	class Meta:
		ordering = ["date_deliverd"]
		verbose_name = 'product'
		verbose_name_plural = 'the products'