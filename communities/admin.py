from django.contrib import admin

from .models import Community, Donation, Need


class NeedInline(admin.TabularInline):
    model = Need
    extra = 0
    fields = ('title', 'category', 'target_amount', 'is_urgent', 'status')


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'population', 'owner', 'is_active', 'active_needs_count')
    list_filter = ('province', 'is_active')
    search_fields = ('name', 'description', 'email')
    inlines = [NeedInline]

    @admin.display(description='Necesidades activas')
    def active_needs_count(self, obj):
        return obj.active_needs_count


@admin.register(Need)
class NeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'category', 'target_amount', 'raised_display', 'is_urgent', 'status')
    list_filter = ('category', 'is_urgent', 'status', 'community__province')
    search_fields = ('title', 'description', 'community__name')
    list_editable = ('status', 'is_urgent')

    @admin.display(description='Recaudado')
    def raised_display(self, obj):
        return f'${obj.raised_amount:,.0f} / ${obj.target_amount:,.0f}'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('confirmation_code', 'need', 'donor', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('confirmation_code', 'need__title', 'donor__username')
    readonly_fields = ('confirmation_code', 'created_at')
