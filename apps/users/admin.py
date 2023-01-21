from django.contrib import admin
from .models import User, Region, District
from .role import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['permissions']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'phone', 'role', 'is_superuser', 'province']
    fields = ['name', 'surname', 'image', 'phone', 'province', 'district_or_city', 'address', 'role']
    @staticmethod
    def role(obj):
        return obj.role.name


class DistrictInline(admin.TabularInline):
    model = District
    extra = 12

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    inlines = [DistrictInline]
