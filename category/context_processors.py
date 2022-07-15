from os import link
from .models import Category


# To give the links based on the category slug

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
