from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class AccountAdmin(UserAdmin):
	list_display = ('username','email','phone_number','date_joined','last_login','is_active','is_admin','is_staff')
	search_fields = ('pk','email','username',)
	readonly_fields=('pk','date_joined','last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(UserAccount, AccountAdmin)
admin.site.register(UserImage)
admin.site.register(UserProfile)
admin.site.register(Customer)