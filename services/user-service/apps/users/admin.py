from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('phone', 'address', 'date_of_birth')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    # Поля для отображения в списке пользователей
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Поля для поиска
    search_fields = ('email', 'first_name', 'last_name')
    
    # Порядок сортировки
    ordering = ('email',)
    
    # Поля для редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Contact Details', {'fields': ('phone', 'address')}),
        ('Personal Information', {'fields': ('date_of_birth',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )








# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False

# class UserAdmin(BaseUserAdmin):
#     inline = (UserProfileInline,)
#     list_display = ['email', 'username', 'first_name', 'last_name', 'is_active', 'phone']
#     list_filter = ['is_active', 'is_staff', 'date_joined']
#     search_fields = ['email', 'username', 'first_name', 'last_name']
#     ordering = ['-data_joined']

# admin.site.register(User, UserAdmin)
