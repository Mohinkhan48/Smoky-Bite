from django.contrib import admin
from django.utils import timezone
from django.db.models import Sum, F
from .models import Category, MenuItem, Order, OrderItem
import uuid

class SmokyBitesAdminSite(admin.AdminSite):
    site_header = "SMOKY BITES ADMIN"
    index_template = "admin/index.html"

    def index(self, request, extra_context=None):
        query_date = request.GET.get('date')
        if query_date:
            try:
                target_date = timezone.datetime.strptime(query_date, '%Y-%m-%d').date()
            except ValueError:
                target_date = timezone.now().date()
        else:
            target_date = timezone.now().date()

        orders_today = Order.objects.filter(created_at__date=target_date)
        
        total_items = OrderItem.objects.filter(
            order__created_at__date=target_date
        ).aggregate(total=Sum('quantity'))['total'] or 0

        total_revenue = orders_today.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Calculate profit for the target date
        total_profit = OrderItem.objects.filter(
            order__created_at__date=target_date
        ).aggregate(
            profit=Sum((F('price') - F('cost_price')) * F('quantity'))
        )['profit'] or 0

        # Pre-format as rounded strings for bulletproof template rendering
        extra_context = extra_context or {}
        extra_context['daily_stats'] = {
            'total_orders': total_items,
            'total_revenue': f"{total_revenue:.2f}",
            'total_profit': f"{total_profit:.2f}",
            'selected_date': target_date,
        }
        return super().index(request, extra_context)

admin_site = SmokyBitesAdminSite(name='smoky_admin')

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(MenuItem, site=admin_site)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'cost_price', 'item_cost_tool', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'cost_price', 'is_available')

    def item_cost_tool(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse(f'admin:orders_menuitem_change', args=[obj.pk])
        return format_html('<a class="button" href="{}" style="background:#3498db !important; padding:4px 8px; font-size:10px;">Item Cost</a>', url)
    item_cost_tool.short_description = "Cost Tool"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['menu_item']
    fields = ('menu_item', 'quantity', 'price', 'cost_price')
    readonly_fields = ('price', 'cost_price')
    extra = 1

@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name_bold', 'phone_link', 'time', 'pay_method', 'pay_status', 'order_status', 'amount_display')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_id', 'customer_name', 'customer_number')
    ordering = ('-created_at',)
    list_per_page = 20
    actions = ['generate_profit_report']
    
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Overview', {
            'fields': (('order_id', 'created_at'), ('status', 'payment_status'), 'fulfillment_type'),
            'classes': ('wide',)
        }),
        ('Customer Details', {
            'fields': (('customer_name', 'customer_number'),),
            'classes': ('wide',)
        }),
        ('Payment & Billing', {
            'fields': (('payment_method', 'total_amount'),),
            'classes': ('wide',)
        }),
    )
    
    readonly_fields = ('order_id', 'created_at')

    def order_number(self, obj):
        return obj.order_id[:8].upper()
    order_number.short_description = 'ID'

    def customer_name_bold(self, obj):
        from django.utils.html import format_html
        return format_html('<span class="customer-name-bold">{}</span>', obj.customer_name)
    customer_name_bold.short_description = 'Customer'
    customer_name_bold.admin_order_field = 'customer_name'

    def phone_link(self, obj):
        from django.utils.html import format_html
        if not obj.customer_number:
            return "-"
        return format_html('<a href="tel:{}" class="phone-link">📞 {}</a>', obj.customer_number, obj.customer_number)
    phone_link.short_description = 'Contact'

    def amount_display(self, obj):
        from django.utils.html import format_html
        return format_html('<span style="font-weight:bold; color:#ffd700;">₹{}</span>', obj.total_amount)
    amount_display.short_description = 'Total'
    amount_display.admin_order_field = 'total_amount'

    def pay_method(self, obj):
        return obj.payment_method
    pay_method.short_description = 'Mode'

    def pay_status(self, obj):
        from django.utils.html import format_html
        cls = f"status-badge status-{obj.payment_status.lower()}"
        return format_html('<span class="{}">{}</span>', cls, obj.payment_status)
    pay_status.short_description = 'Payment'
    pay_status.admin_order_field = 'payment_status'

    def order_status(self, obj):
        from django.utils.html import format_html
        cls = f"status-badge status-{obj.status.lower()}"
        return format_html('<span class="{}">{}</span>', cls, obj.status)
    order_status.short_description = 'Status'
    order_status.admin_order_field = 'status'

    def time(self, obj):
        return obj.created_at.strftime("%H:%M")
    time.short_description = 'Time'
    time.admin_order_field = 'created_at'

    def generate_profit_report(self, request, queryset):
        total_rev = queryset.aggregate(total=Sum('total_amount'))['total'] or 0
        total_prof = OrderItem.objects.filter(order__in=queryset).aggregate(
            profit=Sum((F('price') - F('cost_price')) * F('quantity'))
        )['profit'] or 0
        
        self.message_user(request, f"Profit Report: Total Revenue ₹{total_rev} | Total Profit ₹{total_prof} for {queryset.count()} orders.")
    generate_profit_report.short_description = "💰 Generate Profit Report for selected"

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }