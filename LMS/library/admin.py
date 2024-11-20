from django.contrib import admin
from .models import books,mybag,Checkout

# Register your models here.
admin.site.register(books)
admin.site.register(mybag)

class CheckoutAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        # Make all fields read-only once the record is checked out
        if obj and obj.checkout_date:  # If the checkout_date is set, making it readonly
            return [field.name for field in obj._meta.fields]
        return []  # Otherwise, no fields are read-only by default
    
    def delete_model(self, request, obj):
        
        # When a checkout is deleted, set the associated book's status to 'available'
        book = obj.book  # Get the book associated with the checkout
        book.status = True  # Set the status to available (True)
        book.save()  # Save the updated book status
        
        super().delete_model(request, obj)  

admin.site.register(Checkout, CheckoutAdmin)
