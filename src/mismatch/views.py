from django.shortcuts import render

# Create your views here.
def mismatch_home_view(request):
	return render(request, 'mismatch/home.html',{})