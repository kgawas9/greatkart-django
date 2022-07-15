from itertools import product
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from carts.models import CartItem

from .models import Product
from category.models import Category

from django.db.models import Q

from carts.views import _cart_id

# Create your views here.
def storeHomePage(request, category_slug=None, page_slicer=0):
    categories = None
    products = None

    if category_slug is not None:
        # first find out the category based on the category slug field from category table
        page_slicer = 3
        categories = get_object_or_404(Category, slug=category_slug)     
        products = Product.objects.filter(category = categories, is_available=True).order_by('id')

        product_count = products.count()
    else:
        page_slicer = 6
        products = Product.objects.all().filter(is_available=True).order_by('id')
        
        product_count = products.count()

    # -------------------------------------------------
    # for implementaton of pagination
    paginator = Paginator(products, page_slicer)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    # -------------------------------------------------

    context = {
        'products': paged_products,
        'count': product_count,
    }
    return render(request, 'store/store.html', context=context)

def product_detail(request, category_slug, product_slug):
    try:
        product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

        # product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'product': product,
        'product_exist': in_cart,
    }    
    return render(request, 'store/product-detail.html', context=context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
    
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword) | Q(description__icontains = keyword))
            product_count = products.count()
            
            context = {
                'products': products,
                'count': product_count,
            }
            
            return render(request, 'store/store.html', context=context)
    
    return render(request, 'store/store.html')