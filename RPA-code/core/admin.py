from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Application
from typing import Any, Optional, Tuple, List

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'address', 'date_joined', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add our custom fields to the existing fieldsets
        self.fieldsets = list(self.fieldsets)
        self.fieldsets.append(
            ('Additional Info', {'fields': ('phone', 'address')})
        )
        # Add our custom fields to the add form
        self.add_fieldsets = list(self.add_fieldsets)
        self.add_fieldsets.append(
            ('Additional Info', {'fields': ('phone', 'address')})
        )

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('type', 'user', 'status', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('user__username', 'user__email', 'type', 'full_name')
    date_hierarchy = 'created_at'
    
    def get_fieldsets(self, request: Any, obj: Optional[Application] = None) -> list[tuple[Optional[str], dict[str, Any]]]:
        common_fields = ['user', 'type', 'status', 'created_at', 'full_name', 'sex', 'birth_year', 'birth_month', 'birth_day']
        
        if obj and obj.type == 'citizenship':
            return [
                (None, {
                    'fields': common_fields
                }),
                ('Citizenship Details', {
                    'fields': [
                        'citizenship_certificate_number',
                        'birth_district',
                        'birth_municipality',
                        'birth_ward_no',
                        'permanent_district',
                        'permanent_municipality',
                        'permanent_ward_no',
                        'issuing_officer_name',
                        'issuing_officer_title',
                        'issuing_date_bs'
                    ]
                })
            ]
        elif obj and obj.type == 'pan':
            return [
                (None, {
                    'fields': common_fields
                }),
                ('PAN Details', {
                    'fields': ['pan_number']
                })
            ]
        elif obj and obj.type == 'contact':
            return [
                (None, {
                    'fields': common_fields
                }),
                ('Contact Details', {
                    'fields': ['message']
                })
            ]
        
        # For add form or unknown type
        return [
            (None, {
                'fields': common_fields
            })
        ]
