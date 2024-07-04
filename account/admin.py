from django.contrib import admin
from .models import User
from wallet.models import Transaction
# Register your models here.


class TransactionsInline(admin.TabularInline):
    """inline in users admin page"""
    model = Transaction
    extra = 1
    fields = ('mount', 'mode', 'date')
    readonly_fields = ('date',)
    



class UserAdmin(admin.ModelAdmin):
    """user admin page customization"""
    fields = ('username', 'financial_credit')
    # readonly_fields = ('financial_credit',)
    inlines = [TransactionsInline]



admin.site.register(User, UserAdmin)