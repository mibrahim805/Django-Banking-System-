from django.contrib import admin

# Register your models here.


from bank.models import Bank, Branch

admin.site.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ["name", "swift_code", "institution_number", "description"]



admin.site.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["name", "transit_number", "address", "email", "capacity", "last_modified"]
