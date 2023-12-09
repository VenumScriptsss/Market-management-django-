"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from homepage.views import homepage_view
from adminPanel.views import adminPanel_view,statistics_view,adminPanel_stats_prodAnalys_view,adminpanel_logout_view,adminPanel_stock_view,adminPanel_addProduct_view\
,adminPanel_editProduct_view,adminPanel_confEditProduct_view,adminPanel_prix_view,adminPanel_pricesEdit_view\
,adminPanel_categories_view,adminPanel_editSold_view,adminPanel_addSold_view,adminPanel_addCategory_view,adminPanel_stats_view
from caisse.views import caisse_view,saleDetails_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name= 'home'),
    path('admin-panel', adminPanel_view, name='admin-panel'),
    path('', include('django.contrib.auth.urls')),
    path('admin-panel/statistics', adminPanel_stats_view, name='statistics'),
    path('admin-panel/statistics/view-prod', adminPanel_stats_prodAnalys_view, name='statsViewprod'),
    path('admin-panel/logout', adminpanel_logout_view, name='logout'),
    path('admin-panel/stock', adminPanel_stock_view, name='stock'),
    path('admin-panel/stock/add-product', adminPanel_addProduct_view, name='add-product'),
    path('admin-panel/stock/add-categorie', adminPanel_addCategory_view, name='add-categorie'),
    path('admin-panel/stock/edit-product', adminPanel_editProduct_view, name='edit-product'),
    path('admin-panel/stock/edit-product/confirm', adminPanel_confEditProduct_view, name='conf-edit-product'),
    path('admin-panel/prix', adminPanel_prix_view, name='prix'),
    path('admin-panel/prix/prix-categories', adminPanel_categories_view, name='prix-categorie'),
    path('admin-panel/prix/prices-edit', adminPanel_pricesEdit_view, name='price-edit'),
    path('admin-panel/prix/add-sold', adminPanel_addSold_view, name='add-sold'),
    path('admin-panel/prix/edit-sold', adminPanel_editSold_view, name='edit-sold'),
    path('admin-panel/prix/delete-sold', adminPanel_editSold_view, name='delete-sold'),
    #CAISSE URLS 
    path('caisse', caisse_view, name='caisse'),
    path('sale-details', saleDetails_view, name='sale-details'),
        


]
