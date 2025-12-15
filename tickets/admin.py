from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_by', 'assigned_to')
    list_filter = ('status',)
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
