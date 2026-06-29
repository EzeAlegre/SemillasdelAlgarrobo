from django.contrib import admin

from .models import Ticket, TicketComment


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'priority', 'status', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'description', 'created_by__username')
    list_editable = ('status', 'priority', 'assigned_to')
    inlines = [TicketCommentInline]
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'category', 'priority', 'status')}),
        ('Asignación', {'fields': ('created_by', 'assigned_to')}),
        ('Fechas', {'fields': ('created_at', 'updated_at', 'resolved_at')}),
    )


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'created_at')
    search_fields = ('content', 'ticket__title')
