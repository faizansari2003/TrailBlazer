from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Bike, Category, Color, Brand

def all_bikes_view(request):
    # Get filter parameters
    color_ids = request.GET.getlist('color')
    brand_ids = request.GET.getlist('brand')
    category_ids = request.GET.getlist('category')
    min_price = request.GET.get('min_price', 5000)
    max_price = request.GET.get('max_price', 15000)

    # Filter bikes based on parameters
    bikes = Bike.objects.all()
    if color_ids:
        bikes = bikes.filter(color__id__in=color_ids)
    if brand_ids:
        bikes = bikes.filter(brand__id__in=brand_ids)
    if category_ids:
        bikes = bikes.filter(category__id__in=category_ids)
    bikes = bikes.filter(price__gte=min_price, price__lte=max_price)

    # Pagination
    paginator = Paginator(bikes, 6)  # Show 6 bikes per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the page object

    # Fetch all brands, categories, and colors for the filter sidebar
    brands = Brand.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()

    # Return the filtered data to the template
    return render(request, 'product/show_product.html', {
        'page_obj': page_obj,  # Pass the page object to the template
        'brands': brands,
        'categories': categories,
        'colors': colors,
        'selected_colors': color_ids,  # Pass selected colors to the template
        'selected_brands': brand_ids,  # Pass selected brands to the template
        'selected_categories': category_ids,  # Pass selected categories to the template
        'min_price': min_price,  # Pass minimum price to the template
        'max_price': max_price,  # Pass maximum price to the template
    })



from django.shortcuts import render
from .models import Bike, Brand, Category, Color
from django.core.paginator import Paginator


def search_product(request):
    query = request.GET.get('q', '').strip()  # Get search query
    bikes = Bike.objects.filter(name__icontains=query) if query else Bike.objects.none()  # Filter bikes by name
    bikes = Bike.objects.filter(description__icontains=query) if query else Bike.objects.none()  # Filter bikes by name


    # Pagination for search results
    paginator = Paginator(bikes, 6)  # Show 6 bikes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all brands, categories, and colors for filters
    brands = Brand.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()

    return render(request, 'product/show_product.html', {
        'page_obj': page_obj,
        'brands': brands,
        'categories': categories,
        'colors': colors,
        'query': query,  # Pass the query to the template
    })


from django.shortcuts import render, get_object_or_404
from product.models import Bike

def product_detail(request, product_id):
    # Get the product by ID
    product = get_object_or_404(Bike, id=product_id)

    # Get similar products based on the brand
    similar_products = Bike.objects.filter(brand=product.brand).exclude(id=product.id)

    return render(request, 'product/product.html', {
        'product': product,
        'similar_products': similar_products,
    })








from django.shortcuts import render
from product.models import Bike


def index_view(request):
    featured_bikes = Bike.objects.filter(is_featured=True, is_available=True)
    print("Featured Bikes:", featured_bikes)  # Check if this matches the shell output
    return render(request, 'index.html', {'featured_bikes': featured_bikes})