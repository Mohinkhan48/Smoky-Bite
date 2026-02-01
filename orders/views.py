import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.management import call_command
from .models import Category, MenuItem, Order, OrderItem

def get_safe_category(name):
    """
    Safely get or create a category. 
    If multiple exist, keep one and merge/delete others to fix MultipleObjectsReturned.
    """
    cats = Category.objects.filter(name=name)
    if cats.count() == 0:
        return Category.objects.create(name=name)
    elif cats.count() == 1:
        return cats.first()
    else:
        # Self-healing: Duplicates found
        primary = cats.first()
        for duplicate in cats[1:]:
            # Move items if any (though safe to checking)
            duplicate.items.update(category=primary)
            duplicate.delete()
        return primary

def menu_view(request):
    # --- AUTO-HEALING: Ensure database tables exist ---
    try:
        # Check if the tables actually exist by querying Category
        Category.objects.exists()
    except Exception:
        # Tables are missing (likely fresh Render deploy). Run migrations now.
        call_command('migrate', interactive=False)
        
    # Only populate if no categories exist to save database IO in production
    if not Category.objects.exists():
        menu = {
            'MOMOS MENU': [('CKN STEEM MOMOS', 60), ('CKN FRIED MOMOS', 70), ('CKN PERI PERI FRIED MOMOS', 70)],
            'BURGER': [('CKN BURGER', 79), ('CKN CHEESE BURGER', 99), ('CKN ZINGER BURGER', 110)],
            'BROASTED & FRIES': [('BROASTED CHICKEN (4 PCS)', 149), ('PERI PERI FRENCH FRIES', 70), ('SALTED FRENCH FRIES', 70)],
            'HOT & CRISPY': [('CKN CHEESE BALLS (5 PCS)', 79), ('CKN CRISPY STRIPS (5 PCS)', 79), ('CKN NUGGETS (5 PCS)', 79), ('CKN CRISPY POPCORN', 79)],
            'MOCKTAILS': [('BLUE ANGEL', 49), ('LIME MINT', 49), ('BLUEBERRY', 49), ('GINGER LIME', 49)]
        }
        
        for cat_name, items in menu.items():
            cat = get_safe_category(cat_name)
            for name, price in items:
                MenuItem.objects.get_or_create(
                    category=cat, 
                    name=name, 
                    defaults={'price': price}
                )
            
        specials_data = {
            'HOT & SPICY': [('LEG PIECE ( 1 PCS )', 70), ('LOLLIPOP ( 4 PCS )', 120), ('WINGS ( 5 PCS )', 130), ('TIKKA ( 8 PCS )', 140)],
            'PERI PERI': [('LEG PIECE ( 1 PCS )', 80), ('LOLLIPOP ( 4 PCS )', 130), ('WINGS ( 5 PCS )', 140), ('TIKKA ( 8 PCS )', 150)],
            'MALAI SPECIAL': [('LEG PIECE ( 1 PCS )', 90), ('LOLLIPOP ( 4 PCS )', 140), ('WINGS ( 5 PCS )', 150), ('TIKKA ( 8 PCS )', 160)],
            'COMBOS': [('MEDIUM COMBO', 399), ('LARGE COMBO', 599)]
        }
        
        for cat_name, items in specials_data.items():
            cat = get_safe_category(cat_name)
            for name, price in items:
                MenuItem.objects.get_or_create(
                    category=cat, 
                    name=name, 
                    defaults={'price': price}
                )

    # Fetch all active categories with their items - Optmized with prefetch_related
    categories = Category.objects.filter(is_active=True).prefetch_related('items')
    specials_names = ['HOT & SPICY', 'PERI PERI', 'MALAI SPECIAL', 'COMBOS']
    
    standard_categories = [c for c in categories if c.name not in specials_names]
    
    # Sort special_categories to match strict order
    special_categories = []
    for name in specials_names:
        cat = next((c for c in categories if c.name == name), None)
        if cat:
            special_categories.append(cat)
    
    context = {
        'standard_categories': standard_categories,
        'special_categories': special_categories
    }
    return render(request, 'menu.html', context)

def cart_view(request):
    return render(request, 'cart.html')


@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_items = data.get('items', [])
            
            if not cart_items:
                return JsonResponse({'error': 'Cart is empty'}, status=400)

            # Create Order (Wait for payment for UPI, Confirm immediately for CASH)
            payment_method = data.get('payment_method', 'CASH')
            initial_status = 'CONFIRMED' if payment_method == 'CASH' else 'PENDING'
            
            customer_name = data.get('customer_name', 'Guest')
            customer_number = data.get('customer_number', '')
            order = Order.objects.create(
                status=initial_status, 
                payment_method=payment_method, 
                payment_status='PENDING', 
                customer_name=customer_name,
                customer_number=customer_number
            )
            total = 0

            for item in cart_items:
                menu_item_id = item.get('id')
                quantity = item.get('quantity')
                
                try:
                    menu_item = MenuItem.objects.get(id=menu_item_id)
                except MenuItem.DoesNotExist:
                     continue # Skip invalid items

                price = menu_item.price
                
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price
                )
                total += price * quantity
            
            order.total_amount = total
            order.save()
            
            response_data = {'order_id': str(order.order_id), 'amount': float(total)}

            if payment_method == 'UPI':
                from django.conf import settings
                from urllib.parse import quote
                
                upi_conf = getattr(settings, 'UPI_CONFIG', {})
                upi_id = upi_conf.get('ID', 'smokybites@upi')
                merchant_name = upi_conf.get('MERCHANT_NAME', 'Smoky Bites')
                merchant_quoted = quote(merchant_name)
                amount = float(total)
                mc = upi_conf.get('MC', '5411')
                currency = upi_conf.get('CURRENCY', 'INR')
                
                # BUSINESS MODE: 
                # For registered merchants, adding 'mc' and a concise 'tr' 
                # is mandatory for secure and trackable transactions.
                short_tr = f"SB{str(order.order_id).replace('-', '')[:20]}"
                
                upi_uri = (
                    f"upi://pay?"
                    f"pa={upi_id}"
                    f"&pn={merchant_quoted}"
                    f"&mc={mc}"
                    f"&am={amount:.2f}"
                    f"&cu={currency}"
                    f"&tr={short_tr}"
                    f"&tn=SmokyBitesOrder"
                )
                
                
                # Encode for QR URL
                encoded_upi = quote(upi_uri)
                # Using a more reliable QR API with HTTPS
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_upi}"
                
                response_data['qr_url'] = qr_url
                response_data['upi_uri'] = upi_uri

            return JsonResponse(response_data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)


def confirm_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            order = Order.objects.get(order_id=order_id)
            
            order.payment_method = 'UPI'
            order.payment_status = 'PAID_UNVERIFIED'
            # Do NOT automatically set status to CONFIRMED. 
            # This requires Admin manual verification now to prevent "cheating".
            order.status = 'PENDING' 
            order.save()
            
            return JsonResponse({'status': 'success'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'order_success.html', {'order': order})

def dashboard_stats_api(request):
    """API to fetch financial stats for real-time dashboard updates."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    from django.utils import timezone
    from django.db.models import Sum, F
    
    target_date = timezone.now().date()
    orders_today = Order.objects.filter(created_at__date=target_date, status='CONFIRMED')
    
    total_orders = OrderItem.objects.filter(
        order__created_at__date=target_date,
        order__status='CONFIRMED'
    ).aggregate(total=Sum('quantity'))['total'] or 0

    total_revenue = orders_today.aggregate(total=Sum('total_amount'))['total'] or 0
    
    total_profit = OrderItem.objects.filter(
        order__created_at__date=target_date,
        order__status='CONFIRMED'
    ).aggregate(
        profit=Sum((F('price') - F('cost_price')) * F('quantity'))
    )['profit'] or 0

    return JsonResponse({
        'total_orders': total_orders,
        'total_revenue': f"{total_revenue:.2f}",
        'total_profit': f"{total_profit:.2f}"
    })

def get_menu_prices(request):
    """API for admin real-time total calculation"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    items = MenuItem.objects.all().values('id', 'price')
    return JsonResponse({str(item['id']): float(item['price']) for item in items})