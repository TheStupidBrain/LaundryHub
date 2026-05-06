from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import User, Order, OrderItem, Service

def register_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        phone_user = User.objects.filter(phone=phone).first()
        email_user = User.objects.filter(email=email).first()

        if email_user and '@placeholder.com' not in email_user.email:
            messages.error(request, "User with this email already exists.")
            return redirect('register')
            
        if phone_user:
            if '@placeholder.com' in phone_user.email:
                # Upgrade placeholder account created at store
                phone_user.name = name
                phone_user.email = email
                phone_user.set_password(password)
                phone_user.save()
                user = phone_user
            else:
                messages.error(request, "User with this phone already exists.")
                return redirect('register')
        else:
            user = User.objects.create_user(email=email, phone=phone, password=password, name=name, user_type='Customer')
            
        login(request, user, backend='core.backends.PhoneOrEmailBackend')
        return redirect('dashboard_redirect')
    return render(request, 'core/register.html')

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        
        user = authenticate(request, username=identifier, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_redirect(request):
    if request.user.user_type == 'Admin':
        return redirect('admin_dashboard')
    elif request.user.user_type == 'Staff':
        return redirect('staff_dashboard')
    return redirect('customer_dashboard')

@login_required
def customer_dashboard(request):
    if request.user.user_type != 'Customer': return redirect('dashboard_redirect')
    orders = Order.objects.filter(customer_phone=request.user.phone).order_by('-created_at')
    return render(request, 'core/customer_dashboard.html', {'orders': orders})

@login_required
def staff_dashboard(request):
    if request.user.user_type not in ['Staff', 'Admin']: return redirect('dashboard_redirect')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order_id} status updated to {new_status}")
        return redirect('staff_dashboard')
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'core/staff_dashboard.html', {'orders': orders})

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'Admin': return redirect('dashboard_redirect')
    
    # Calculate constant totals
    all_orders = Order.objects.all()
    total_orders_count = all_orders.count()
    total_revenue = all_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    search_query = request.GET.get('search', '')
    if search_query:
        orders = all_orders.filter(customer_phone__icontains=search_query).order_by('-created_at')
    else:
        orders = all_orders.order_by('-created_at')
        
    return render(request, 'core/admin_dashboard.html', {
        'orders': orders, 
        'total_orders_count': total_orders_count,
        'total_revenue': total_revenue, 
        'search_query': search_query
    })

@login_required
def add_staff(request):
    if request.user.user_type != 'Admin': return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(phone=phone).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "A user with this phone or email already exists.")
        else:
            User.objects.create_user(
                email=email, 
                phone=phone, 
                password=password, 
                name=name, 
                user_type='Staff'
            )
            messages.success(request, f"Staff member {name} added successfully!")
            return redirect('admin_dashboard')
            
    return render(request, 'core/staff_create.html')

@login_required
def create_order(request):
    if request.user.user_type != 'Admin': return redirect('dashboard_redirect')
    services = Service.objects.all()

    if request.method == 'POST':
        phone = request.POST.get('customer_phone')
        name = request.POST.get('customer_name', 'Unknown')
        
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={'name': name, 'user_type': 'Customer', 'email': f"{phone}@placeholder.com"}
        )
        if created:
            user.set_password('defaultpassword')
            user.save()
        
        with transaction.atomic():
            is_home_delivery = request.POST.get('is_home_delivery') == 'on'
            delivery_address = request.POST.get('delivery_address', '')
            
            order = Order.objects.create(
                customer_phone=phone, 
                status='Pending', 
                total_amount=0,
                is_home_delivery=is_home_delivery,
                delivery_address=delivery_address
            )
            total = 0
            service_ids = request.POST.getlist('service_ids')
            quantities = request.POST.getlist('quantities')
            
            for index, s_id in enumerate(service_ids):
                qty = int(quantities[index] if index < len(quantities) else 1)
                if qty > 0:
                    service = get_object_or_404(Service, id=s_id)
                    line_price = service.price * qty
                    total += line_price
                    OrderItem.objects.create(
                        order=order,
                        service_type=service.name,
                        quantity=qty,
                        price=service.price
                    )
            order.total_amount = total
            order.save()
            messages.success(request, f"Order #{order.id} created successfully!")
            return redirect('admin_dashboard')
    return render(request, 'core/order_create.html', {'services': services})

@login_required
def request_delivery(request, order_id):
    if request.user.user_type != 'Customer': return redirect('dashboard_redirect')
    
    order = get_object_or_404(Order, id=order_id, customer_phone=request.user.phone)
    if request.method == 'POST':
        address = request.POST.get('delivery_address')
        if address:
            order.is_home_delivery = True
            order.delivery_address = address
            order.save()
            messages.success(request, f"Home delivery requested successfully for Order #{order.id}!")
    return redirect('customer_dashboard')

@login_required
def delete_order(request, order_id):
    if request.user.user_type != 'Admin': 
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, f"Order #{order_id} has been deleted successfully.")
        
    return redirect('admin_dashboard')
