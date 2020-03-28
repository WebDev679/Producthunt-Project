from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .models import Vote
from django.utils import timezone
# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products':products})

@login_required
def create(request):
    products = Product.objects
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.FILES['image'] and request.FILES['icon'] and request.POST['url']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            product.image = request.FILES['image']
            product.icon = request.FILES['icon']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'product/create.html', {"error":'Fill up all the entries'})
    else:
        return render(request, 'products/create.html')

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        try:
            check_vote = Vote.objects.get(product=product, user=product.hunter)
            return redirect('/products/' + str(product.id))
        except Vote.DoesNotExist:
            vote = Vote()
            product.votes_total += 1
            vote.product = product
            vote.user = product.hunter
            product.save()
            vote.save()
            return redirect('/products/' + str(product.id))
    else:
        return render(request, 'products/product.html', {'product':product})

def all_products(request):
    products_start = Product.objects.all()
    products = []
    for product in products_start:
        if product.hunter.username == request.user.username:
            products.append(product)
    return render(request, 'products/all.html', {'products':products})
