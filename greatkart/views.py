from django.shortcuts import render

from store.models import Product

def homePage(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, 'home.html', context=context)