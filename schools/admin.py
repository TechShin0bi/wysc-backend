from django.contrib import admin
from django.utils.html import format_html
from .models import Address, School, Campus, Role


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address_line', 'city', 'state_province', 'country')
    list_filter = ('country', 'state_province', 'city')
    search_fields = ('address_line', 'address_line2', 'city', 'state_province', 'postal_code', 'country')
    ordering = ('country', 'state_province', 'city')


class CampusInline(admin.TabularInline):
    model = Campus
    extra = 0
    show_change_link = True
    fields = ('name', 'code', 'is_main_campus', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'short_name', 'motto')
    inlines = [CampusInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'short_name', 'motto')
        }),
        ('Contact Information', {
            'fields': ('website', 'logo')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0
    show_change_link = True
    fields = ('name','school_type')
    # autocomplete_fields = ('name',)


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'code', 'is_main_campus', 'is_active')
    list_filter = ('is_active', 'is_main_campus', 'school')
    search_fields = ('name', 'code', 'school__name', 'email', 'phone')
    list_select_related = ('school', 'address')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('school', 'address')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('school', 'address')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus_display')
    list_filter = ('name',)
    search_fields = (
        'name','campus__name'
    )
    list_select_related = ('campus',)
    list_select_related = ('campus',)
    readonly_fields = ('created_at', 'updated_at')
    
    def campus_display(self, obj):
        return obj.campus.name if obj.campus else "-"
    campus_display.short_description = 'Campus'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('campus')
