from django.contrib import admin
from .models import EmailVerification

# expose email verification to admin panel
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'verified_by_admin')

admin.site.register(EmailVerification, EmailVerificationAdmin)