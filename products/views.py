
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def index(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    return render(request,'products/index.html',{'products' : products})

def contact(request):
    return render(request,'products/contact.html')


def shop(request):
    products = Product.objects.all()
    return render(request,'products/shop.html',{'products' : products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request,'products/detail.html',{'product' : product})

def product_filter(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category = category)
    return render(request,'products/shop.html',{'category' : category, 'products' : products})


