from django.contrib import admin
from django.utils import timezone
from django.db.models import Sum, F
from .models import Category, MenuItem, Order, OrderItem
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.urls import path
from django.shortcuts import redirect
import uuid

class SmokyBitesAdminSite(admin.AdminSite):
    site_header = "SMOKY BITES ADMIN"
    site_title = "SMOKY BITES POS"
    index_template = "admin/index.html"
    app_index_template = "admin/index.html"

    def get_stats_context(self, request):
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
        
        total_profit = OrderItem.objects.filter(
            order__created_at__date=target_date
        ).aggregate(
            profit=Sum((F('price') - F('cost_price')) * F('quantity'))
        )['profit'] or 0

        return {
            'total_orders': total_items,
            'total_revenue': f"{total_revenue:.2f}",
            'total_profit': f"{total_profit:.2f}",
            'selected_date': target_date,
        }

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['daily_stats'] = self.get_stats_context(request)
        return super().index(request, extra_context)

    def app_index(self, request, app_label, extra_context=None):
        extra_context = extra_context or {}
        extra_context['daily_stats'] = self.get_stats_context(request)
        return super().app_index(request, app_label, extra_context)

admin_site = SmokyBitesAdminSite(name='smoky_admin')

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    actions = None

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
        return format_html(
            '<a class="button" href="{}" style="'
            'background: #3498db !important; '
            'padding: 5px 12px; '
            'font-size: 10px; '
            'border-radius: 50px; '
            'font-weight: 900; '
            'letter-spacing: 1px; '
            'box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3); '
            'transition: all 0.3s; '
            'display: inline-block;'
            '">ITEM COST</a>', url)
    item_cost_tool.short_description = "Cost Tool"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['menu_item']
    fields = ('menu_item', 'quantity', 'price', 'cost_price')
    readonly_fields = ('price', 'cost_price')
    extra = 1

@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name_bold', 'phone_link', 'time', 'pay_method', 'pay_status', 'order_status', 'amount_display', 'delete_order')
    list_per_page = 20
    
    class RestrictStatusFilter(admin.SimpleListFilter):
        title = 'Status'
        parameter_name = 'status'
        def lookups(self, request, model_admin):
            return [
                ('CONFIRMED', 'Confirmed'),
                ('DELIVERED', 'Delivered'),
                ('UNDELIVERED', 'Undelivered'),
            ]
        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(status=self.value())
            return queryset

    # list_filter = (RestrictStatusFilter, 'payment_status', 'payment_method', 'created_at')

    search_fields = ('order_id', 'customer_name', 'customer_number')
    ordering = ('-created_at',)
    actions = ['delete_selected'] # Explicitly enabled for bulk deletion
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'toggle-delivery/<int:order_id>/<str:new_status>/',
                self.admin_site.admin_view(self.toggle_delivery_status),
                name='toggle_delivery_status',
            ),
        ]
        return custom_urls + urls

    def toggle_delivery_status(self, request, order_id, new_status):
        order = Order.objects.get(pk=order_id)
        if new_status in ['DELIVERED', 'UNDELIVERED']:
            order.status = new_status
            order.save()
        return redirect(request.META.get('HTTP_REFERER', 'admin:orders_order_changelist'))
    
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

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            kwargs['choices'] = [
                ('CONFIRMED', 'Confirmed'),
                ('DELIVERED', 'Delivered'),
                ('UNDELIVERED', 'Undelivered'),
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)


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
        from django.urls import reverse
        
        cls = f"status-badge status-{obj.status.lower()}"
        status_html = format_html('<span class="{}">{}</span>', cls, obj.status)
        
        if obj.status in ['CONFIRMED', 'DELIVERED', 'UNDELIVERED']:
            # Minimal inline options that don't change layout
            id_prefix = f"order-{obj.pk}"
            delivered_url = reverse('admin:toggle_delivery_status', args=[obj.pk, 'DELIVERED'])
            undelivered_url = reverse('admin:toggle_delivery_status', args=[obj.pk, 'UNDELIVERED'])
            
            return format_html(
                '<div class="status-click-wrapper" onclick="toggleStrictOptions(\'{}\')">'
                '{}'
                '<div id="{}-options" class="strict-options" style="display:none;">'
                '<a href="#" onclick="confirmStatusUpdate(\'{}\', \'Delivered\'); return false;" class="opt-btn">Delivered</a>'
                '<a href="#" onclick="confirmStatusUpdate(\'{}\', \'Undelivered\'); return false;" class="opt-btn">Undelivered</a>'
                '</div>'
                '</div>',
                id_prefix,
                status_html,
                id_prefix,
                delivered_url,
                undelivered_url
            )
            
        return status_html
    order_status.short_description = 'Status'
    order_status.admin_order_field = 'status'

    def delete_order(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse(f'admin:orders_order_delete', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="'
            'background: #ff4757 !important; '
            'padding: 5px 12px; '
            'font-size: 10px; '
            'border-radius: 50px; '
            'font-weight: 900; '
            'color: #fff !important; '
            'letter-spacing: 1px; '
            'box-shadow: 0 4px 10px rgba(255, 71, 87, 0.3); '
            'transition: all 0.3s; '
            'display: inline-block;'
            'text-decoration: none;'
            '">DELETE</a>', url)
    delete_order.short_description = "Action"

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

# Allow User/Group management in the custom admin panel
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)