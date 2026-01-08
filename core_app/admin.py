

from django.contrib import admin
from .models import Book, Borrow, Action, Reservation
admin.site.register(Borrow)
admin.site.register(Action)
admin.site.register(Reservation)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'count', 'status') 
    readonly_fields = ('status',)