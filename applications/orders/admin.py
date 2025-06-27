from django.contrib import admin
from applications.orders.models.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'status',
        'owner',
        'is_deleted',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'is_deleted', 'created_at', 'owner')
    search_fields = ('title', 'description', 'owner__username', 'owner__email')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    ordering = ('-created_at',)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return Order.all_objects.select_related('owner')
