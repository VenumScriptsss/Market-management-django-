from django.shortcuts import render
from adminPanel.models import productsModel,soldModel,categoryModel
from caisse.models import saleModel
from datetime import datetime

#Reseting the units that was sold this month on every product using monthlyRest 
currMonth = int(datetime.today().month)
if currMonth > int(productsModel.objects.get(id=1).unitsSold_thisMonth.split('.')[1]):
	productsModel.monthlyReset(currMonth)


def caisse_view(request):
	products = productsModel.objects.all()
	sales = saleModel.objects.all()
	lastThreesales = sales.order_by('-saleDate')[:3]
	context = {}
	context['products'] = products
	context['sales'] = sales
	context['lastsales'] = lastThreesales

	
	if 'encaissement' in request.POST:

		sale = saleModel()
		sale.save()
		
		for elem in request.POST:
			if elem  == 'encaissement' or elem == 'csrfmiddlewaretoken':
				continue
			sale.saleProducts.add(products.get(id=elem))
			sale.saleQuantityStr+=str(request.POST[elem])
			thisMonth = datetime.today().month
			thisProd = products.get(id=elem)
			prdUnitsSold,prodLastSaleMnth= thisProd.unitsSold_thisMonth.split('.') 
			if thisProd.prodLastSaleMnth == str(thisMonth):
				thisProd.unitsSold_thisMonth = str(int(prdUnitsSold)+int(request.POST[elem]))+'.'+prodLastSaleMnth
			else:
				thisProd.unitsSold_thisMonth = str(request.POST[elem])+'.'+str(datetime.today().month)

			thisProd.save()
		sale.save()		

		
	return render(request, 'caisse/caisse.html', context)

def	saleDetails_view(request):

	products = productsModel.objects.all()
	sales = saleModel.objects.all()
	context = {}
	saleId = request.POST['saleId']
	thisSale = sales.get(id=saleId)

	saleProds = thisSale.saleProducts.all()
#	print("printitng:",saleProds)
	context['saleProds'] = saleProds
	context['products'] = products
	context['sales'] = sales
	context['thisSale'] = thisSale


	if "edit" in request.POST:
		string = ""
		count = 0
		qntArr = list(thisSale.saleQuantityStr)
		for  elem in request.POST:
			if elem in ["csrfmiddlewaretoken","edit","saleId"]:
				continue
			#print(elem,request.POST[elem]+" vs ",thisSale.saleQuantityStr[count])
			if request.POST[elem] == "-1":
				thisSale.saleProducts.remove(products.get(id=elem))
				qntArr.pop(count)
				count-=1
			elif request.POST[elem] != thisSale.saleQuantityStr[count]:
				qntArr[count] = request.POST[elem]
				string+=(qntArr[count])
			else:
				string+=(qntArr[count])
			count+=1

		thisSale.saleQuantityStr = string
		thisSale.save()
	return render(request, 'caisse/sale-details.html', context)