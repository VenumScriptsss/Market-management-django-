from django.shortcuts import render,redirect
from adminPanel.models import productsModel, soldModel, categoryModel,SchedualedSpends
from caisse.models import saleModel
from adminPanel.forms import createProductFrom
from django.db.models import Q
import urllib.request
from datetime import datetime
counter = 1
prods = productsModel.objects.all()

currMonth = int(datetime.today().month)
if currMonth > int(prods.get(id=1).unitsSold_thisMonth.split('.')[1]):
	productsModel.monthlyReset(currMonth)

# Create your views here.
def adminPanel_view(request):
	context = {}
	context['username'] = request.user.username
	return render(request, 'adminPanel/admin-panel.html',context)

def statistics_view(request):
	return render(request, 'adminPanel/statistics.html',{})

def adminpanel_logout_view(request):
	logout(request)
	return redirect('home')

def adminPanel_stock_view(request):
	context = {}
	global counter
	products = productsModel.objects.all()
	context['products'] = products	
	solds = soldModel.objects.all()
	context['solds'] = solds	
	if 'search' in request.POST:		
		search_rqst = request.POST['searchprd']
		context['search_title'] = search_rqst
		context['products']= products.filter(Q(suplier__contains=search_rqst) | Q(productname__contains =search_rqst)\
			|Q(date_ex__contains=search_rqst) | Q(date_delivered__contains=search_rqst) | Q(price__contains=search_rqst)\
			|Q(category__contains=search_rqst))	
		
	if 'orderby-id' in request.POST:
		print(counter)
		counter*=-1
		if counter == -1:
			context['products']= products.order_by('-id')
		else:
			context['products']= products.order_by('id')	
	
	elif 'orderby-datedelv' in request.POST:
		print(counter)
		counter*=-1
		if counter == -1:
			context['products']= products.order_by('-date_delivered')
		else:
			context['products']= products.order_by('date_delivered')

	elif 'orderby-quantity' in request.POST:
		counter*=-1
		if counter == -1:
			context['products']= products.order_by('-quantity')
		else:
			context['products']= products.order_by('quantity')	
	
	elif 'orderby-price' in request.POST:
		counter*=-1
		if counter == -1:
			context['products']= products.order_by('-price')
		else:
			context['products']= products.order_by('price')	

	elif 'orderby-date-ex' in request.POST:
		counter*=-1
		if counter == -1:
			context['products']= products.order_by('-date_ex')
		else:
			context['products']= products.order_by('date_ex')	
	elif 'orderby-sold' in request.POST:
		counter*=-1
		if counter == -1:
			context['products']= products.order_by('-sold')
		else:
			context['products']= products.order_by('sold')

	
	return	render(request, 'adminPanel/stock.html',context)


def adminPanel_addProduct_view(request):
	context = {}
	if 	request.POST:
		form = createProductFrom(request.POST)
		if form.is_valid():
			form.save()
			form = createProductFrom()
			return redirect('stock')
		else:
			print("its not valid")
			context['form'] = form	

	
	return render(request, 'adminPanel/add-product.html', context)

def adminPanel_addCategory_view(request):
	context = {}
	if request.POST:
		newcategory = categoryModel(Categoryname = request.POST['categoryname'])
		newcategory.save()
		return redirect('stock')
	return render(request, 'adminPanel/add-categorie.html')


def adminPanel_editProduct_view(request):
	context = {}
	if 'edit' in request.POST:
		productid = request.POST['edit']
		products = productsModel.objects.all()
		oldform = products.get(id = productid)
		context['oldform'] = oldform

	

	return render(request, 'adminPanel/edit-product.html', context)	


def adminPanel_confEditProduct_view(request):
	context = {}
	if request.POST:
		print("\n conf view working \n")
		form = request.POST
		oldformid = form['oldformid']
		products = productsModel.objects.all()
		oldform = products.get(id = oldformid)

		#treating the sold value(-1 and 1) 
		if form['sold']=="Arrête Sold":
			sold=True
		else:
			sold=False
		#treating the price value(DA)
		price = form['price']
		price = price.replace('DA','')

		oldform.productname=form['productname']
		oldform.quantity=form['quantity']
		oldform.date_ex=form['date_ex']
		oldform.suplier=form['suplier']
		oldform.category=form['category']
		oldform.price=price
		oldform.sold=sold
		oldform.save()

		return redirect('stock')
	else:
		print("\nits not working\n")

	return render(request, 'adminPanel/conf-edit.html', context)	

def adminPanel_prix_view(request):
	context = {}
	products = productsModel.objects.all()
	context['products'] = products

	solds = soldModel.objects.all()
	context['solds'] = solds
	if 'search' in request.POST:		
		search_rqst = request.POST['searchprd']
		context['search_title'] = search_rqst
		context['products']= products.filter(Q(suplier__contains=search_rqst) | Q(productname__contains =search_rqst)\
			|Q(date_ex__contains=search_rqst) | Q(date_delivered__contains=search_rqst) | Q(price__contains=search_rqst)\
			|Q(category__contains=search_rqst))			 

	return render(request, 'adminPanel/prix.html', context)

def adminPanel_pricesEdit_view(request):
	context = {}
	products = productsModel.objects.all()
	context['products'] = products	

	if 'price-edit' in request.POST:
		productid = request.POST['price-edit']
		oldform = products.get(id = productid)
		context['oldform'] = oldform	
		context['return'] = 'prices'

	if 'confirm-edit' in request.POST:
		print("\nconf\n")
		newform = request.POST
		oldform = products.get(id = newform['oldformid'])

		if 'price' in newform:
			oldform.price = newform['price']
		if 'sold-price' in newform:
			oldform.sold_price = newform['sold-price']

		oldform.save()
		context['return'] = 'stats'
			
		return redirect('prix')
	if 'statsEditPrx' in request.POST:
		productid = request.POST['statsEditPrx']
		oldform = products.get(id=productid)
		context['oldform'] = oldform	
		context['return'] = 'stats'

	return render(request, 'adminPanel/prices-edit.html', context)	


def adminPanel_categories_view(request):
	context = {}
	products = productsModel.objects.all()

	if 'cat-boissants' in request.POST:
		context['products']= products.filter(Q(category__contains='boissants'))
		context['category'] = 'Boissnats'
	if 'cat-nouriture' in request.POST:
		context['products'] = products.filter(Q(category__contains='nouriture'))
		context['category'] = 'Nouriture'
	if 'cat-produits' in request.POST:
		context['products'] = products.filter(Q(category__contains='produits'))
		context['category'] = 'Produits'
	if 'cat-autre' in request.POST:
		context['products'] = products.filter(Q(category__contains='autre'))
		context['category'] = 'Autre'

	return render(request , 'adminPanel/prix-categories.html', context)

def adminPanel_addSold_view(request):
	context = {}
	products = productsModel.objects.all()
	if 'solding-product-id' in request.POST:
		productid = request.POST['solding-product-id']
		product = products.get(id=productid)
		context['product'] = product

	if	'add-sold' in request.POST:
		form = request.POST
		productid = form['product-id']
		product = products.get(id=productid)
		
		soldingform = soldModel(sold_productid= product.id, sold_productname= product.productname,\
		sold_starting_date= form['start-sold'], sold_ending_date = form['end-sold'], sold_price = form['sold-price'])

		soldingform.save()
		product.sold = True
		product.save()
		return redirect('prix')
	return render(request, 'adminPanel/add-sold.html', context)

def adminPanel_editSold_view(request):
	context = {}
	products = productsModel.objects.all()
	soldDB = soldModel.objects.all()
	context['todayDate']= datetime.date.today()

	if 'solding-product-id' in request.POST:
		productid = request.POST['solding-product-id']
		product = products.get(id = productid)
		context['product'] = product
		if product.sold:
			sold = soldDB.get(sold_productid=productid)
			context['product_sold'] = sold
		
			if sold.sold_starting_date <= datetime.date.today():
				context['sold_active'] = True
			else: context['sold_active'] = False  
	
	if	'add-sold' in request.POST:
		form = request.POST
		productid = form['product-id']
		product = products.get(id = productid)
		
		soldingform = soldModel(sold_productid= product.id, sold_productname= product.productname,\
		sold_starting_date= form['start-sold'], sold_ending_date = form['end-sold'], sold_price = form['sold-price'])

		soldingform.save()
		product.sold = True
		product.save()
		return redirect('prix')

	if 'edit-sold' in request.POST:	
		form = request.POST
		soldingform = soldDB.get(sold_productid = form['product-id'])
		soldingform.sold_price = form['sold-price']
		soldingform.sold_starting_date = form['start-sold']
		soldingform.sold_ending_date = form['end-sold']
		soldingform.save()
		return redirect('prix')
	
	if 'delete-sold' in request.POST:
		form = request.POST
		sold = soldDB.get(sold_productid=form['product-id'])
		sold.delete()
		product = products.get(id= form['product-id'])
		product.sold = False
		product.save()

		return redirect('prix')
	return render(request, 'adminPanel/edit-sold.html', context)

def adminPanel_stats_view(request):
	context = {}
	products = productsModel.objects.all()
	sales = saleModel.objects.all()
	spends = SchedualedSpends.objects.all()
	now = datetime.today()
	#add a str date
	monthStart = datetime(now.year,now.month,1).date()
	currMonthSales = saleModel.objects.filter(saleDate__gte=monthStart,saleDate__lte=now)
	context['producst'] = products
	context['currMonthSales'] = currMonthSales

	Rev = 0
	for sale in sales:
		for saleProd in sale.saleProducts.all():
			Rev+= saleProd.price
	context['monthRev']= Rev
	yesterday = datetime(now.year,now.month,now.day-1).date()
	todaySales = saleModel.objects.filter(saleDate__gt=yesterday)
	context['todaySales'] = todaySales
	Rev = 0
	for sale in todaySales:
		for saleProd in sale.saleProducts.all():
			Rev += saleProd.price
	context['todayRev'] = Rev

	mostSold = products.order_by('-unitsSold_thisMonth')[:5]
	context['thisMonth_mostSoldPrds'] = mostSold
	expProducts = productsModel.objects.filter(date_ex__lt=now.date())
	Rev = 0
	for prd in expProducts:
		Rev += prd.price
	monthSpends = SchedualedSpends.objects.filter(dateDelv__gte=monthStart)
	for spence in monthSpends:
		Rev += spence.amount
	
	context['expProds'] = expProducts
	context['monthSpends'] = monthSpends
	context['monthLoss'] = Rev
	context['profit'] = int(context['monthRev'])-int(context['monthLoss'])

	return render(request, 'adminPanel/statistics.html',context)

def adminPanel_stats_prodAnalys_view(request):
	context = {}
	print(request.POST['anlysPrd'])
	if 'anlysPrd' in request.POST:
		prod = prods.get(id=request.POST['anlysPrd'])
		context['prod'] = prod
		context['purchasePrx'] = prod.purchasePrx
		#context['unitsPerBox'] = prod.unitPerBox
		context['soldUnites'] = prod.unitsSold_thisMonth.split('.')[0]
	return render(request, 'adminPanel/prod-view.html',context)